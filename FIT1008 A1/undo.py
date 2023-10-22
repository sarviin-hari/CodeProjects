from __future__ import annotations
from action import PaintAction
from data_structures.stack_adt import ArrayStack
from grid import Grid

class UndoTracker:

    def __init__(self) -> None:
        """
        Initialize instance variables array_stack and last_action

        Args:
        - None

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(n), where n is the int argument value passed in ArrayStack
        - Best case: O(n), where n is the int argument value passed in ArrayStack
        - Reason: Best and worst case complexity for __init__ is O(n) as it handles assigning CircularQueue instance to
                  a variable, where n is the size of maximum capacity 10000

        """

        # O(n), where n is the maximum capacity -> Initialize ArrayStack with parameter 10000
        self.undo_stack = ArrayStack(10000)    # Initialize ArrayStack() with parameter 10000
        self.redo_stack = ArrayStack(10000)    # Initialize ArrayStack() with parameter 10000

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker
        How: if the array to store undo is not full, add the action in the array

        If your collection is already full,
        feel free to exit early and not add the action.

        Args:
        - action -> An instance of PaintAction

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: Best and worst case complexity for this method is O(1) as this method only has None check, integer
                  comparison and adding an action to teh stack which all takes O(1) complexity

        *** All codes are assumed as O(1) unless stated otherwise

        """

        if action is not None:  # Checks if the action is None
            if not self.undo_stack.is_full():  # if the action is not None, check if the array is full
                self.undo_stack.push(action)   # if not full add the action to the array_stack

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.
        How: removes the last element from the undo_stack, adds it into redo_stack array and undo_apply the action

        Args:
        - grid -> An instance of Grid

        Raises:
        - None

        Returns:
        - The action that was undone, or None.

        Complexity:
        - Worst case: O(undo_apply), where undo_apply is a method in PaintAction class
        - Best case: O(undo_apply), where undo_apply is a method in PaintAction class
        - Reason: The complexity of all the other lines in this function is O(1) except for the undo_apply function as
                  it does a special check and calls grid.special if True or does a for loop based on the number of steps
                  in action if False. Thus, the complexity of this code depends on the best and worst case of the
                  codes in undo_apply, so we can say the best and worse case complexity of this method as
                  O(undo_apply)

        *** All codes are assumed as O(1) unless stated otherwise

        """

        if self.undo_stack.is_empty():  # if the array_stack is empty, return None
            return None
        else:
            last = self.undo_stack.pop()   # gets the last most added action
            self.redo_stack.push(last)  # store the last most added action in last action

            # The best and worse case complexity is O(undo_apply)
            last.undo_apply(grid)   # Call the undo_apply function of PaintAction on grid, to undo the action

            return last  # Return the PaintAction that was undone

    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.
        How: removes the last element from the redo_stack array, adds it into undo_stack array and redo_apply the action

        Args:
        - grid -> An instance of Grid

        Raises:
        - None

        Returns:
        - The action that was redone, or None.

        Complexity:
        - Worst case: O(redo_apply), where redo_apply is a method in PaintAction class
        - Best case: O(redo_apply), where redo_apply is a method in PaintAction class
        - Reason: The complexity of all the other lines in this function is O(1) except for the redo_apply function as
                  it does a special check and calls grid.special if True or does a for loop based on the number of steps
                  in action if False. Thus, the complexity of this code depends on the best and worst case of the
                  codes in redo_apply, so we can say the best and worse case complexity of this method as
                  O(redo_apply)

        *** All codes are assumed as O(1) unless stated otherwise

        """
        if self.redo_stack.is_empty():  # if the array_stack is empty, return None
            return None
        else:
            last = self.redo_stack.pop()   # gets the most recent undone action
            self.undo_stack.push(last)  # store the action that will be redone in array_stack

            # The best and worse case complexity is O(redo_apply)
            last.redo_apply(grid)   # Call the redo_apply function of PaintAction on grid, to redo the action

            return last  # Return the PaintAction that was redone
