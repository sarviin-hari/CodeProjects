from __future__ import annotations
from action import PaintAction
from data_structures.queue_adt import CircularQueue
from grid import Grid

class ReplayTracker:

    def __init__(self) -> None:
        """
        Initialize instance variables CircularQueue

        Args:
        - None

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(n), where n is the int argument value passed in ArrayStack (maximum capacity)
        - Best case: O(n), where n is the int argument value passed in ArrayStack (maximum capacity)
        - Reason: Best and worst case complexity for __init__ is O(n) as it assigns CircularQueue instance to variable

        """
        # O(n), where n is the max capacity which is 10000
        self.rep_lst = CircularQueue(10000)  # Initialize CircularQueue with parameter of 10000

    def start_replay(self) -> None:
        """
        Called whenever we should stop taking actions, and start playing them back.

        Useful if you have any setup to do before `play_next_action` should be called.

        Since function is not implemented there is no complexity

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

    def add_action(self, action: PaintAction, is_undo: bool = False) -> None:
        """
        Adds an action to the replay.

        `is_undo` specifies whether the action was an undo action or not.
        Special, Redo, and Draw all have this is False.

        Args:
        - action -> An instance of PaintAction
        - is_undo -> boolean value

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: Best and worst case complexity for this method is O(1) as this method only has None check and append
                  operation to CircularQueue which all has O(1) complexity

        *** All codes are assumed as O(1) unless stated otherwise

        """
        if action is not None:  # if the action is not None, add the tuple of action and undo state into rep_list
            self.rep_lst.append((action, is_undo))

    def play_next_action(self, grid: Grid) -> bool:
        """
        Plays the next replay action on the grid.
        Returns a boolean.
            - If there were no more actions to play, and so nothing happened, return True.
            - Otherwise, return False.

        Args:
        - grid -> An instance of Grid

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(undo_apply) / O(redo_apply), where undo_apply() and redo_apply() are the methods in PaintAction
                      instance
        - Best case: O(undo_apply) / O(redo_apply), where undo_apply() and redo_apply() are the methods in PaintAction
                      instance
        - Reason: Best and worst case complexity is either O(undo_apply) or O(redo_apply) , where the complexity depends
                  on the worst case complexity of either of undo_apply() or redo_apply() method

        *** All codes are assumed as O(1) unless stated otherwise

        """

        if self.rep_lst.is_empty():  # if the rep_list is empty, return True
            return True
        else:
            act_undo = self.rep_lst.serve()  # pops out the action undo tuple from the rep_list

            if not act_undo[1]:  # if the is_undo value of tuple is False, apply the redo_apply function of the PaintAction on grid
                # O(redo_apply)
                act_undo[0].redo_apply(grid)
            else:   # if the is_undo value of tuple is True, apply the undo_apply function of the PaintAction on grid
                # O(undo_apply)
                act_undo[0].undo_apply(grid)

            return False    # return False


if __name__ == "__main__":
    action1 = PaintAction([], is_special=True)
    action2 = PaintAction([])
    print(action1, action2)

    g = Grid(Grid.DRAW_STYLE_SET, 5, 5)

    r = ReplayTracker()
    r.add_action(action1)
    r.add_action(action2)
    r.add_action(action2, is_undo=True)
    # Start the replay.
    r.start_replay()
    f1 = r.play_next_action(g)  # action 1, special
    f2 = r.play_next_action(g)  # action 2, draw
    f3 = r.play_next_action(g)  # action 2, undo
    t = r.play_next_action(g)  # True, nothing to do.
    print(f1, f2, f3, t)
    assert (f1, f2, f3, t) == (False, False, False, True)
