import arcade
import arcade.key as keys
import math

from action import PaintAction, PaintStep
from data_structures.stack_adt import ArrayStack
from grid import Grid
from layer_util import get_layers, Layer
from layers import lighten
from replay import ReplayTracker
from undo import UndoTracker


class MyWindow(arcade.Window):
    """ Painter Window """

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 700
    SIDEBAR_WIDTH = 100
    BUTTONS_HEIGHT = 100
    SCREEN_TITLE = "Paint"

    REPLAY_TIMER_DELTA = 0.05

    GRID_SIZE_X = 32
    GRID_SIZE_Y = 32

    BG = [255, 255, 255]

    # SCAFFOLD PART
    # Unless you're adding new features, you shouldn't need to touch this.

    def __init__(self) -> None:
        """Initialise visual and logic variables."""
        super().__init__(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.SCREEN_TITLE)
        arcade.set_background_color(self.BG)
        self.grid: Grid = None
        self.draw_style = Grid.DRAW_STYLE_SET
        self.z_pressed = False
        self.y_pressed = False
        self.z_timer = 0
        self.y_timer = 0
        self.enable_ui = True
        self.replay_timer = 0
        self.on_init()

    def reset(self) -> None:
        """Reset the screen."""
        self.grid = Grid(self.draw_style, self.GRID_SIZE_X, self.GRID_SIZE_Y)
        self.timestamp = 0

        self.selected_layer_index = -1
        self.dragging = None
        self.prev_drawn = None
        self.prev_pos = None
        self.draw_size = 2

        # Visual calculations
        self.DRAW_PANEL = self.SCREEN_WIDTH - self.SIDEBAR_WIDTH
        self.GRID_SQ_WIDTH = self.DRAW_PANEL / self.GRID_SIZE_X
        self.GRID_SQ_HEIGHT = self.SCREEN_HEIGHT / self.GRID_SIZE_Y
        self.LAYER_BUTTON_SIZE = self.SIDEBAR_WIDTH / 2
        # Action button sprites
        self.action_buttons = arcade.SpriteList()
        self.draw_mode_button = arcade.Sprite(
            "img/on_off.png" if self.draw_style == Grid.DRAW_STYLE_SET else (
                "img/additive.png" if self.draw_style == Grid.DRAW_STYLE_ADD else "img/sequence.png"
            ),
            scale=50/48,
        )
        self.draw_mode_button.center_x = self.DRAW_PANEL + self.LAYER_BUTTON_SIZE / 2
        self.draw_mode_button.center_y = self.LAYER_BUTTON_SIZE / 2
        self.action_buttons.append(self.draw_mode_button)
        self.replay_button = arcade.Sprite(
            "img/replay.png",
            scale=50/48,
        )
        self.replay_button.center_x = self.DRAW_PANEL + 3 * self.LAYER_BUTTON_SIZE / 2
        self.replay_button.center_y = self.LAYER_BUTTON_SIZE / 2
        self.action_buttons.append(self.replay_button)
        self.brush_big_button = arcade.Sprite(
            "img/brush_up.png",
            scale=50/48,
        )
        self.brush_big_button.center_x = self.DRAW_PANEL + self.LAYER_BUTTON_SIZE / 2
        self.brush_big_button.center_y = 3 * self.LAYER_BUTTON_SIZE / 2
        self.action_buttons.append(self.brush_big_button)
        self.brush_small_button = arcade.Sprite(
            "img/brush_down.png",
            scale=50/48,
        )
        self.brush_small_button.center_x = self.DRAW_PANEL + 3 * self.LAYER_BUTTON_SIZE / 2
        self.brush_small_button.center_y = 3 * self.LAYER_BUTTON_SIZE / 2
        self.action_buttons.append(self.brush_small_button)
        self.special_button = arcade.Sprite(
            "img/special.png",
            scale=50/48,
        )
        self.special_button.center_x = self.DRAW_PANEL + self.LAYER_BUTTON_SIZE / 2
        self.special_button.center_y = 5 * self.LAYER_BUTTON_SIZE / 2
        self.action_buttons.append(self.special_button)

        self.on_reset()

    def setup(self) -> None:
        """Set up the game and initialize the variables."""
        self.reset()

    def on_draw(self) -> None:
        """Draw everything"""
        self.clear()
        # UI - Layers
        for i, layer in enumerate(get_layers()):
            if layer is None: break
            xstart = (i % 2) * self.LAYER_BUTTON_SIZE + self.DRAW_PANEL
            xend = ((i % 2)+1) * self.LAYER_BUTTON_SIZE + self.DRAW_PANEL
            ystart = self.SCREEN_HEIGHT - (i//2) * self.LAYER_BUTTON_SIZE
            yend = self.SCREEN_HEIGHT - (i//2+1) * self.LAYER_BUTTON_SIZE
            bg = lighten.apply(layer.bg or self.BG[:], 0, 0, 0) if self.selected_layer_index == i else (layer.bg or self.BG[:])
            if not self.enable_ui:
                bg = lighten.apply(bg, 0, 0, 0)
            arcade.draw_lrtb_rectangle_filled(xstart, xend, ystart, yend, bg)
            arcade.draw_lrtb_rectangle_outline(
                xstart, xend, ystart, yend, (0, 0, 0), border_width=1,
            )
            arcade.draw_text(str(i), xstart, (ystart+yend)/2, (0, 0, 0), 18, width=xend-xstart, align="center", bold=True, anchor_y="center")
        # UI - Draw Modes / Action buttons
        self.action_buttons.draw()
        # Grid
        for x in range(self.GRID_SIZE_X):
            for y in range(self.GRID_SIZE_Y):
                arcade.draw_lrtb_rectangle_filled(
                    self.GRID_SQ_WIDTH * x,
                    self.GRID_SQ_WIDTH * (x+1),
                    self.GRID_SQ_HEIGHT * (y+1),
                    self.GRID_SQ_HEIGHT * y,
                    self.grid[x][y].get_color(self.BG[:], self.timestamp, x, y),
                )

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        """Called when the mouse buttons are pressed."""
        if x > self.DRAW_PANEL:
            if not self.enable_ui:
                return
            # Buttons
            for i, layer in enumerate(get_layers()):
                if layer is None: break
                xstart = (i % 2) * self.LAYER_BUTTON_SIZE + self.DRAW_PANEL
                xend = ((i % 2)+1) * self.LAYER_BUTTON_SIZE + self.DRAW_PANEL
                ystart = self.SCREEN_HEIGHT - (i//2) * self.LAYER_BUTTON_SIZE
                yend = self.SCREEN_HEIGHT - (i//2+1) * self.LAYER_BUTTON_SIZE
                if xstart <= x < xend and yend <= y < ystart:
                    self.selected_layer_index = i
                    break
            # Actions
            xstart = self.DRAW_PANEL
            xend = self.LAYER_BUTTON_SIZE + self.DRAW_PANEL
            ystart = self.LAYER_BUTTON_SIZE
            yend = 0
            if xstart <= x < xend and yend <= y < ystart:
                self.change_draw_mode()
            xstart = self.LAYER_BUTTON_SIZE + self.DRAW_PANEL
            xend = 2 * self.LAYER_BUTTON_SIZE + self.DRAW_PANEL
            ystart = self.LAYER_BUTTON_SIZE
            yend = 0
            if xstart <= x < xend and yend <= y < ystart:
                self.start_replay()
            xstart = self.DRAW_PANEL
            xend = self.LAYER_BUTTON_SIZE + self.DRAW_PANEL
            ystart = 2 * self.LAYER_BUTTON_SIZE
            yend = self.LAYER_BUTTON_SIZE
            if xstart <= x < xend and yend <= y < ystart:
                self.on_increase_brush_size()
            xstart = self.LAYER_BUTTON_SIZE + self.DRAW_PANEL
            xend = 2 * self.LAYER_BUTTON_SIZE + self.DRAW_PANEL
            ystart = 2 * self.LAYER_BUTTON_SIZE
            yend = self.LAYER_BUTTON_SIZE
            if xstart <= x < xend and yend <= y < ystart:
                self.on_decrease_brush_size()
            xstart = self.DRAW_PANEL
            xend = 1 * self.LAYER_BUTTON_SIZE + self.DRAW_PANEL
            ystart = 3 * self.LAYER_BUTTON_SIZE
            yend = 2 * self.LAYER_BUTTON_SIZE
            if xstart <= x < xend and yend <= y < ystart:
                self.on_special()
        else:
            self.dragging = True
            self.try_draw(x, y)

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        """Called when the mouse buttons are released."""
        self.dragging = False
        self.prev_drawn = None
        self.prev_pos = None

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        """Called when the mouse moves."""
        if not self.dragging:
            return
        if not(0 <= self.selected_layer_index < len(get_layers())):
            return
        if x > self.DRAW_PANEL:
            return
        self.try_draw(x, y)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Called when a keyboard key is pressed."""
        if not self.enable_ui:
            return
        self.z_pressed = keys.Z == symbol and (modifiers & keys.MOD_CTRL)
        self.y_pressed = keys.Y == symbol and (modifiers & keys.MOD_CTRL)
        if self.z_pressed:
            self.on_undo()
            self.z_timer = 0.5
        if self.y_pressed:
            self.on_redo()
            self.y_timer = 0.5

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        """Called when a keyboard key is released."""
        self.z_pressed = False
        self.y_pressed = False

    def try_draw(self, x, y) -> None:
        """Attempt to draw at a position, but safely fail if an invalid square."""
        if self.selected_layer_index == -1:
            return
        layer = get_layers()[self.selected_layer_index]
        if self.prev_pos is not None:
            # Try draw in increments of 0.5 to avoid skipping squares.
            mhat_dist = abs(x - self.prev_pos[0]) + abs(y - self.prev_pos[1])
            increment = 0.5
            points_to_draw = []
            for d in range(1, math.ceil(mhat_dist/increment)+1):
                distance = min(d * increment / mhat_dist, 1)
                nx = distance * (x - self.prev_pos[0]) + self.prev_pos[0]
                ny = distance * (y - self.prev_pos[1]) + self.prev_pos[1]
                nx_pos = int(nx // self.GRID_SQ_WIDTH)
                ny_pos = int(ny // self.GRID_SQ_HEIGHT)
                points_to_draw.append((nx_pos, ny_pos))
        else:
            x_pos = int(x // self.GRID_SQ_WIDTH)
            y_pos = int(y // self.GRID_SQ_HEIGHT)
            points_to_draw = [
                (x_pos, y_pos)
            ]
        for px, py in points_to_draw:
            if self.prev_drawn is None or (px, py) != self.prev_drawn:
                if 0 <= px < self.GRID_SIZE_X and 0 <= py < self.GRID_SIZE_Y:
                    self.on_paint(layer, px, py)
                    self.prev_drawn = (px, py)
        self.prev_pos = (x, y)

    def start_replay(self) -> None:
        """Begin the replay mode."""
        self.enable_ui = False
        self.grid = Grid(self.draw_style, self.GRID_SIZE_X, self.GRID_SIZE_Y)
        self.replay_timer = self.REPLAY_TIMER_DELTA
        self.on_replay_start()

    def on_update(self, delta_time) -> None:
        """Movement and game logic."""
        self.timestamp += delta_time
        if self.z_pressed:
            self.z_timer -= delta_time
            if self.z_timer <= 0:
                self.on_undo()
                self.z_timer += 0.05
        if self.y_pressed:
            self.y_timer -= delta_time
            if self.y_timer <= 0:
                self.on_redo()
                self.y_timer += 0.05
        if not self.enable_ui:
            self.replay_timer -= delta_time
            if self.replay_timer <= 0:
                self.replay_timer += self.REPLAY_TIMER_DELTA
                finished = self.on_replay_next_step()
                if finished:
                    self.enable_ui = True

    def change_draw_mode(self) -> None:
        """Changes the draw mode of the application, and resets the window."""
        if self.draw_style == Grid.DRAW_STYLE_SET:
            self.draw_style = Grid.DRAW_STYLE_ADD
        elif self.draw_style == Grid.DRAW_STYLE_ADD:
            self.draw_style = Grid.DRAW_STYLE_SEQUENCE
        elif self.draw_style == Grid.DRAW_STYLE_SEQUENCE:
            self.draw_style = Grid.DRAW_STYLE_SET
        self.reset()

    # STUDENT PART

    def on_init(self) -> None:
        """
        Initialisation that occurs after the system initialisation.
        Initialize instances of UndoTracker and ReplayTracker

        Args:
        - None

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(n), where n is the int argument value passed in ArrayStack / CircularQueueArray (10000)
        - Best case: O(n), where n is the int argument value passed in ArrayStack / CircularQueueArray (10000)
        - Reason: Best and worst case complexity of this function is O(n) as it handles initializing
                  UndoTracker and ReplayTracker which initializes ArrayStack and CircularQueueArray instance. This is
                  because when initializing ArrayStack adn CircularQueue, it calls the ArrayR functions which runs
                  a for loop that stores None value in each of the capacity. Thus, it takes O(n) complexity, where n is
                  the size of maximum capacity which is 10000

        """
        self.undo = UndoTracker()   # Initialize UndoTracker()
        self.replay = ReplayTracker()   # Initialize ReplayTracker()

    def on_reset(self):
        """
        Called when a window reset is requested.
        Resets the UndoTracker and ReplayTracker by creating a new instance for both variables

        Args:
        - None

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(n), where n is the int argument value passed in ArrayStack / CircularQueueArray (10000)
        - Best case: O(n), where n is the int argument value passed in ArrayStack / CircularQueueArray (10000)
        - Reason: Best and worst case complexity of this function is O(n) as it handles initializing
                  UndoTracker and ReplayTracker which initializes ArrayStack and CircularQueueArray instance. This is
                  because when initializing ArrayStack adn CircularQueue, it calls the ArrayR functions which runs
                  a for loop that stores None value in each of the capacity. Thus, it takes O(n) complexity, where n is
                  the size of maximum capacity which is 10000

        """
        self.undo = UndoTracker()   # resets the undo list
        self.replay = ReplayTracker()   # resets the replay list

    def on_paint(self, layer: Layer, px, py) -> None:
        """
        Called when a grid square is clicked on, which should trigger painting in the vicinity.
        Vicinity squares outside of the range [0, GRID_SIZE_X) or [0, GRID_SIZE_Y) can be safely ignored.

        Args:
        - layer (Layer class instance): The layer being applied.
        - px (int): x position of the brush.
        - py (int): y position of the brush.

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(m * (n + add)), where m is the size of self.grid.x, n is the size of
                     self.grid.y, add is the complexity of add function of the layer store instance,
                     add_step is the complexity of the add_step method in PaintAction instance
        - Best case: O(m * (n + add)), where m is the size of self.grid.x, n is the size of
                     self.grid.y, add is the complexity of add function of the layer store instance,
                     add_step is the complexity of the add_step method in PaintAction instance
        - Reason: Best and worst case complexity of this function is O(m * (n + comp= + add + add_step)) as the
                  complexity depends on the m, n, add, add_step based on their size of the input. The complexity is
                  O(m * (n + .....)) as this code runs a for loop in a for loop which has internal methods with
                  different complexities

        *** All codes are assumed as O(1) unless stated otherwise

        """
        new_act = PaintAction()  # create a new_instance for PaintAction

        # to paint the Manhattan distance, we must select all the grid coordinates that has the same distance between
        # each other from the point that is selected to paint (px, py)

        # O(m), where m is the self.grid.x value that indicates the length of x-axis
        for x_coordinate in range(self.grid.x):

            # O(n), where n is the self.grid.y value that indicates the length of y-axis
            for y_coordinate in range(self.grid.y):
                if abs(x_coordinate-px) + abs(y_coordinate-py) <= self.grid.brush_size:   # Checks if the absolute value of x difference and y difference is less than or equal to brush size

                    # O(add)
                    bool_val = self.grid[x_coordinate][y_coordinate].add(layer)   # if it is set bool_val to the result of adding the layer
                    if bool_val:    # if true (layer is added), add the PaintStep of grid coordinates and layer to PaintAction
                        new_act.add_step(PaintStep((x_coordinate, y_coordinate), layer))

        self.undo.add_action(new_act)   # adds the action in UndoTracker
        self.replay.add_action(new_act, False)  # Adds the action with new_act and is_undo=False value as its parameter

    def on_undo(self) -> None:
        """
        Called when an undo is requested.
        Undo the action and add the undo action in replay

        Args:
        - None

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(undo_apply), where undo_apply is the complexity of the method in PaintAction class which is called from undo() method from self.undo()
        - Best case: O(undo_apply), where undo_apply is the complexity of the method in PaintAction class which is called from undo() method from self.undo()
        - Reason: The complexity of all the other lines in this function is O(1) except for the undo_apply function as
                  it does a special check and calls grid.special if True or does a for loop based on the number of steps
                  in action if False. Thus, the complexity of this code depends on the best and worst case of the
                  codes in undo_apply, so we can say the best and worse case complexity of this method as
                  O(undo_apply)

        *** All codes are assumed as O(1) unless stated otherwise

        """
        # O(undo_apply), undo_apply is the complexity of a method in PaintAction class which is called from undo()
        act = self.undo.undo(self.grid)  # undo the action
        self.replay.add_action(act, True)   # adds the undo action to replay list with act and is_undo=True value as its parameter

    def on_redo(self) -> None:
        """
        Called when a redo is requested.
        """
        act = self.undo.redo(self.grid)  # Try to redo the undo action by calling the redo function in undotracker
        if act is not None:  # if PaintAction is returned in act, adds the redo action to self.action and adds the redo action to the replay_list with add and is_undo=False as parameter
            self.replay.add_action(act, False)

    def on_special(self) -> None:
        """
        Called when the special action is requested.

        Args:
        - None

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(undo_apply), where undo_apply is the complexity of the method in PaintAction class which is called from undo() method from self.undo()
        - Best case: O(undo_apply), where undo_apply is the complexity of the method in PaintAction class which is called from undo() method from self.undo()
        - Reason: The complexity of all the other lines in this function is O(1) except for the undo_apply function as
                  it does a special check and calls grid.special if True or does a for loop based on the number of steps
                  in action if False. Thus, the complexity of this code depends on the best and worst case of the
                  codes in undo_apply, so we can say the best and worse case complexity of this method as
                  O(undo_apply)

        *** All codes are assumed as O(1) unless stated otherwise

        """
        self.grid.special() # Triggers the special function in all grids
        new_act = PaintAction() # create a new PaintAction instance
        new_act.is_special = True   # set the is_special class variable to True
        self.replay.add_action(new_act, False)  # adds the special action to replay list with new_act and is_undo=False value as its parameter
        self.undo.add_action(new_act)   # adds the action into UndoTracker instance

    def on_replay_start(self) -> None:
        """
        Called when the replay starting is requested.

        Args:
        - None

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - None

        """
        pass

    def on_replay_next_step(self) -> bool:
        """
        Called when the next step of the replay is requested.
        Returns boolean to check whether the replay is finished.

        Args:
        - None

        Raises:
        - None

        Returns:
        - boolean value (True if there is action to play, False if no action to play)

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: Best and worst case complexity for this method is O(1) as this method only calls the
                  increase_brush_size() method which does integer comparison and increments variable value by 1


        *** All codes are assumed as O(1) unless stated otherwise

        """

        # O(play_next_action), where play_next_action is the complexity
        replay_bool = self.replay.play_next_action(self.grid)   # Calls the play next action function in replay of instance ReplayTracker, which returns the boolean value
        return replay_bool  # returns the boolean value

    def on_increase_brush_size(self) -> None:
        """
        Called when an increase to the brush size is requested.
        Increase the brush size by 1

        Args:
        - None

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: Best and worst case complexity for this method is O(1) as this method only calls the
                  increase_brush_size() method which does integer comparison and increments variable value by 1


        *** All codes are assumed as O(1) unless stated otherwise

        """

        self.grid.increase_brush_size()  # Calls the increase brush size function in grid to increase the brush size

    def on_decrease_brush_size(self) -> None:
        """
        Called when a decrease to the brush size is requested.
        Decrease the brush size by 1

        Args:
        - None

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: Best and worst case complexity for this method is O(1) as this method only calls the
                  decrease_brush_size() method which does integer comparison and decrements variable value by 1


        *** All codes are assumed as O(1) unless stated otherwise

        """
        self.grid.decrease_brush_size()  # Calls the decrease brush size function in grid to decrease the brush size

def main():
    """ Main function """
    window = MyWindow()
    window.setup()
    arcade.run()

def run_with_func(func, pause=False):
    from threading import Thread
    window = MyWindow()
    window.setup()
    if pause:
        _ = input("Press enter to begin test.")
    t = Thread(target=func, args=(window,))
    t.start()
    arcade.run()


if __name__ == "__main__":
    main()
