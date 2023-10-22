from __future__ import annotations

from data_structures.referential_array import ArrayR
from layer_store import SetLayerStore, AdditiveLayerStore, SequenceLayerStore, LayerStore


class Grid:
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0

    def __init__(self, draw_style, x, y) -> None:

        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.

        Args:
        - draw_style: string value, x: int value, y: int value

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(mn), where m is the value of self.x, while n is the value of self.y.
        - Best case: O(mn), where m is the value of self.x, while n is the value of self.y.
        - Reason: O(mn) + O(1) -> O(mn), since the nested for loop has no restriction to not happen
        """

        # O(1)
        if draw_style in self.DRAW_STYLE_OPTIONS:   # Checks if the draw_style parameter is one of the given choices in self.DRAW_STYLE_OPTIONS
            self.draw_style = draw_style    # if draw_style is part of the option, set self.draw_style as the given draw_style

        # O(1)
        self.x = x  # Set x to instance variable self.x

        # O(1)
        self.y = y  # Set y to instance variable self.y

        # O(1)
        self.brush_size = self.DEFAULT_BRUSH_SIZE   # Set the class variable DEFAULT_BRUSH_SIZE to instance variable self.brush_size

        # O(1)
        self.grid = ArrayR(self.x)  # Initialize an ArrayR with self.x as its parameter (no. of elements) and store in self.grid

        # O(mn), where m is the value of self.x, while n is the value of self.y.
        # If m=n, the Big(O) complexity of the code below can be identified as O(n**2), where n is self.x / self.y
        for index_x in range(self.x):   # O(m), where m is the value of self.x
            array_y = ArrayR(self.y)    # Initialize an ArrayR with self.y as its parameter (no. of elements) and store in a variable array_y

            for index_y in range(self.y):   # O(n), where n is the value of self.y
                array_y[index_y] = self.layer_check()   # For each index of array_y, call the self.layer_check() function of time complexity O(1) which returns an instance of LayerStore and store the insatnce on that specific index
            self.grid[index_x] = array_y    # store the array_y of layer_store instances in each index of self.grid x indexes

    def layer_check(self):
        """
        Checks what the draw_style parameter is and call the specific class instance for that particular class

        Args:
        - None

        Raises:
        - None

        Returns:
        - layer instance

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: The code returns an instance of LayerStore class based on draw_style attribute. Since initialization
                  of LayerStore instance is just O(1), the complexity is O(1) as well
        """

        if self.draw_style == "SET":
            layer = SetLayerStore()  # If draw_style is "SET", layer_check() returns an instance of the SetLayerStore class
        elif self.draw_style == "ADD":
            layer = AdditiveLayerStore()    # If draw_style is "ADD", layer_check() returns an instance of the AdditiveLayerStore class
        elif self.draw_style == "SEQUENCE":
            layer = SequenceLayerStore()    # If draw_style is "SEQUENCE", layer_check() returns an instance of the SequenceLayerStore class
        else:
            layer = None    # if the draw_style other than "SET", "ADD" or "SEQUENCE" return None
        return layer

    # O(1)
    def __getitem__(self, index: int) -> ArrayR|LayerStore:
        """
        Gets the instance of the index of the grid

        Args:
        - index: int value

        Raises:
        - None

        Returns:
        - the instance from the index of the grid

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: The best and worse case complexity for accessing an index is O(1)

        """
        # O(1)
        return self.grid[index] # when get_item magic method is called, return the element / value stored at that specific index

    def increase_brush_size(self) -> None:
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.

        Args:
        - None

        Raises:
        - None

        Returns:
        - the instance from the index of the grid

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: Best and Worst case ecomplexity for integer comparison and incrementation is O(1)

        """
        # O(1)
        if not self.brush_size == Grid.MAX_BRUSH:
            self.brush_size += 1    # if the current self.brush_size is not equal to the MAXIMUM_BRUSH size, increase the brush size by 1

    def decrease_brush_size(self) -> None:
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.

        Args:
        - None

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: Best and Worst case ecomplexity for integer comparison and decremental is O(1)

        """
        # O(1) as the operation is just a comparison operation and decrementing an instance variable
        if not self.brush_size == Grid.MIN_BRUSH:
            self.brush_size -= 1     # if the current self.brush_size is not equal to the MINIMUM_BRUSH size, decrease the brush size by 1

    def special(self) -> None:
        """
        Activate the special affect on all grid squares.

        Args:
        - None

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(mn), where m is the value of self.x, while n is the value of self.y.
        - Best case: O(mn), where m is the value of self.x, while n is the value of self.y.
        - Reason: Best and Worst case is O(mn), since the nested for loop has no restriction to not happen

        """

        # O(mn), where m is the value of self.x, while n is the value of self.y.
        # If m=n, the Big(O) complexity of the code below can be identified as O(n**2), where n is self.x / self.y
        for i in range(self.x):  # for every x and y index on the grid, the special effect is triggered
            for j in range(self.y):
                self.grid[i][j].special()
