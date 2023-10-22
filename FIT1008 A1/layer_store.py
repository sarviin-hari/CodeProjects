from __future__ import annotations
from abc import ABC, abstractmethod

import layer_util
from data_structures.array_sorted_list import ArraySortedList
from data_structures.queue_adt import CircularQueue
from data_structures.sorted_list_adt import ListItem
from data_structures.stack_adt import ArrayStack
from layer_util import Layer
from layers import invert


class LayerStore(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass


class SetLayerStore(LayerStore):
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """

    def __init__(self) -> None:
        """
        Calls the parent super class
        Initialize instance variables layer, special_check and special_layer

        Args:
        - None

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: Best and worst case complexity for __init__ is O(1) as it only handles calling the parent class
          and assigning variables
        """

        super().__init__()  # O(1) -> Calls the LayerStore abstract class
        self.layer = None  # O(1) -> set the instance variable layer to None
        self.special_check = False  # O(1) -> set the instance variable special_check to False
        self.special_layer = invert  # O(1) -> set the instance variable special_layer to invert layer

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        How: Set the new layer if it is not in the self.layer variable

        Args:
        - layer: one of the layers from the layer class instances

        Raises:
        - None

        Returns:
        - boolean (True if layer is assigned, else False)

        Complexity:
        - Worst case: O(comp)
        - Best case: O(comp)
        - Reason: The best and worst case complexity of the below add function is O(comp) which occurs due to the
                  comparison of two layer instances. Since all thw other code has O(1) complexity, this code has
                  O(comp) for both best and worst case

        *** All codes are assumed as O(1) unless stated otherwise
        """

        # O(1)
        if layer is not None:  # Checks if the layer is not None

            # O(comp), because the comparison is between 2 references
            if self.layer == layer:  # Check if the current stored layer is the same as the layer in parameter
                return False  # If the layers are the same return False
            self.layer = layer  # If the layers are not the same, store the layer in the parameter in self.layer, return True
            return True
        return False  # if layer is None return False

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        How: If special check is false, apply the current layer only, else, apply the current layer and invert layer

        Args:
        - start (tuple[int, int, int]): initial color
        - timestamp (int): delta-time value for continuous display
        - x (int): x-coordinate to get_color
        - y (int): y-coordinate to get_color

        Raises:
        - None

        Returns:
        - tuple[int, int, int] -> Current color after layer applied

        Complexity:
        - Worst case: O(apply)
          - Reason: O(apply), At the worst case, the apply function of layer is called where its complexity depends on
                    the type of layer. Thus, the complexity is O(apply)
        - Best case: O(1)
          - Reason: Worst case complexity is O(1) when the layer is None and special_check is False where the code
                    block's conditional statements and return statement execute in a fixed amount of time

        *** All codes are assumed as O(1) unless stated otherwise

        """

        if self.layer is None:  # Check if the self.layer is None
            if self.special_check:  # If the special_check is True, apply the invert layer on the color given and return the color
                # O(apply)
                return self.special_layer.apply(start, timestamp, x, y)
            return start  # if special_check is False, return the start color without applying layers

        # O(1) -> boolean comparison
        if self.special_check:  # Checks if special_check is True

            # O(apply), where the complexity of apply depends on the layer
            current_color = self.layer.apply(start, timestamp, x, y)  # if it is True, apply the layer on the color
            current_color = self.special_layer.apply(current_color, timestamp, x, y)  # apply invert on the color that the layer was applied and return the color
            return current_color
        current_color = self.layer.apply(start, timestamp, x, y)  # if special_check is False, apply the layer and return the color
        return current_color

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        How: Sets self.layer to None regardless of layer in parameter

        Args:
        - layer: one of the layers from the layer class instances

        Raises:
        - None

        Returns:
        - boolean (True if layer erased, else False)

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: Best and worst case complexity is O(1) as the whole code is based on checking if the variable is None
                  and setting the variable to None

        *** All codes are assumed as O(1) unless stated otherwise

        """

        # O(1)
        if self.layer is not None:  # Checks if the variable is not None
            self.layer = None  # if the variable is not None, set the self.layer variable to None, return True
            return True
        return False

    def special(self) -> None:
        """
        Special mode: Apply invert on color
        The logic of this code is based on the fact that the invert of an invert is the original color. So, if the
        special method is called once the special check is True, we can assume that when we apply invert twice
        which returns the original color
        How: Sets the special check to true if it is false and vice versa

        Args:
        - None

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: The best and worst case complexity is O(1) as the code is based on checking the boolean value of
                  the variable. If variable is True, set to False. If variable is False, set to True.

        *** All codes are assumed as O(1) unless stated otherwise

        """

        if not self.special_check:  # Checks if instance variable special check is False
            self.special_check = True  # if it is False set it to True
        else:
            self.special_check = False  # If it is True set it to False


class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """

    def __init__(self) -> None:
        """
        Calls the super class LayerStore __init__ method
        Initialize instance variable layer_array with CircularQueue instances

        Args:
        - None

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(n), where n is the number of layers from [getlayers() * 100] passed in CircularQueue
        - Best case: O(n), where n is the number of layers from [getlayers() * 100] passed in CircularQueue
        - Reason: Best and worst case complexity for __init__ is O(n) as it assigns CircularQueue instance to a
                  variable which calls ArrayR which does a loop n times to create an array instance with None as the
                  value

        """

        super().__init__()  # O(1) -> Calls the LayerStore abstract class

        # O(n), where n is the number of layers from getlayers() * 100
        self.layer_array = CircularQueue(len(layer_util.get_layers()) * 100)  # Initialize CircularQueue with parameter from the number of layers from the get_layers method * 100.

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        How: Append the layer to the end of the array if it is not None

        Args:
        - layer: one of the layers from the layer class instances

        Raises:
        - raise Exception("Queue is full") when the number of elements in the queue is equal to the max capacity

        Returns:
        - boolean (True if layer is added in array, else False)

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: Best and worst case is O(1) as The operation of appending a new item to the end of the list takes
                  constant time, O(1) and returning False when there is no layer also has O(1) complexity

        *** All codes are assumed as O(1) unless stated otherwise

        """

        if layer is not None:  # Checks if the layer is not None

            # O(1) as the append method in CircularQueue is of Big O complexity O(1)
            self.layer_array.append(layer)  # append the layer in the CircularQueue Instance, then return True
            return True

        return False

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        How: Apply each layer in order of the first layer stored in array to the last

        Args:
        - start (tuple[int, int, int]): initial color
        - timestamp (int): delta-time value for continuous display
        - x (int): x-coordinate to get_color
        - y (int): y-coordinate to get_color

        Raises:
        - None

        Returns:
        - tuple[int, int, int] -> Current color after layer applied

        Complexity:
        - Worst case: O(n*apply), where n is the length of self.later_array
          - Reason: O(n) * O(apply) -> O(n*apply), At the worst case, the for loop runs maximum time and the apply
                    function of layers also runs as many times as the for loop. So, the complexity is calculated by
                    multiplying both complexities
        - Best case: O(1), when there is no layer in the layer array
          - Reason: At the best case, when the layer_array is empty, the start color is returned keeping the
                    complexity at O(1)

        *** All codes are assumed as O(1) unless stated otherwise

        """

        # O(1), as the start color is returned only
        if self.layer_array.is_empty():  # if there are no layers in the layer_array, return the starting color back
            return start

        color = start  # set the variable color to start

        # The worst case complexity code below is O(n), where n is the length of layer_array
        for _ in range(len(self.layer_array)):  # For every element of layer in the layer_array list, the layer is applied to the color
            layer = self.layer_array.serve()  # remove the first layer that was added in the array and store it in layer

            # O(apply), where the complexity of apply depends on the layer
            color = layer.apply(color, timestamp, x, y)  # The layer applied color is returned and stored in variable color
            self.layer_array.append(layer)  # store the layer back to the original CircularQueue array

        return color  # return the color after layer was applied

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        How: Removes the first added layer regardless of layer in parameter

        Args:
        - layer: one of the layers from the layer class instances

        Raises:
        - raise Exception("Queue is empty") when there is no elements in the queue

        Returns:
        - boolean (True if layer erased, else False)

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: Best and worst case is O(1) as the operation of erasing (serve) an item from the end of the list takes
                  constant time, O(1) and returning False when layer array is empty has O(1) complexity

        *** All codes are assumed as O(1) unless stated otherwise

        """

        if not self.layer_array.is_empty():  # if the layer_array is not empty, the last layer is removed and return True

            # O(1) as the serve method in CircularQueue is of Big O complexity O(1)
            self.layer_array.serve()
            return True
        return False

    def special(self) -> None:
        """
        Special mode: Reverses teh order of the array
        How: ArrayStack is used to store in reverse order of layer and restore the order into CircularQueue

        Args:
        - None

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(n), where n is the length of layer_array
        - Best case: O(n), where n is the length of layer_array
        - Reason: The best case and worst case time complexity of the special method is O(n), where n is the length of
                  self.layer_array. This is because the time complexity is dominated by the two loops that both run n
                  times and n is the only input size that affects the running time.

        *** All codes are assumed as O(1) unless stated otherwise

        """

        new_lifo_array = ArrayStack(len(self.layer_array))  # Creates a new array of ArraySTack with the length of layer_array

        # O(n), where n is the length of layer_array
        for i in range(len(self.layer_array)):  # for loop runs n times, where each element in the layer array of CircularQueue is removed and pushed into the new_lifo_array of ArrayStack Object
            new_lifo_array.push((self.layer_array.serve()))  # This reorders the elements where the last elem becomes the first and vice versa

        # O(n), where n is the length of new_lifo_array which is the same as the original layer_array
        for i in range(len(new_lifo_array)):
            layer = new_lifo_array.pop()  # for loop runs n times, where each element in the new_lifo_array of ArrayStack is popped and appended into the layer_array of CircularQueue Object
            self.layer_array.append(layer)  # Since Circular Queue removes from the first element to the last element, the reversed order is stored back in self.layer_array


class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """

    def __init__(self) -> None:
        """
        Calls the super class Layer Store __init__method
        Initialize instance variable layer_array with ArraySortedList instances

        Args:
        - None

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(n), where n is the number of layers from getlayers()
        - Best case: O(n), where n is the number of layers from getlayers()
        - Reason: Best and worst case complexity for __init__ is O(n) as it assigns ArraySortedList instance to a
                  variable which calls ArrayR which does a loop n times to create an array instance with None as the
                  value

        """
        super().__init__()  # O(1) -> Calls the LayerStore abstract class

        # O(n), where n is the number of layers from getlayers()
        self.layer_array = ArraySortedList(len(layer_util.get_layers()))    # Initialize ArraySortedList with parameter of number of layers from getlayers()

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        How: Checks if the layer is in the layer_array, if not add the layer to the array

        Args:
        - layer: one of the layers from the layer class instances

        Raises:
        - None

        Returns:
        - boolean (True if layer is added in array, else False)

        Complexity:
        - Worst case: O(n), where n is the length of layer_array
          - Reason: For the worst case, it is O(n) + O(n) which is the addition of loop check if List item exists and
                    addition of layer in array sorted position where the addition of both complexity results in O(n),
                    where n is the length of the array
        - Best case: O(log n), when layer is None (return False)

        *** All codes are assumed as O(1) unless stated otherwise

        """

        if layer is not None:   # checks if the layer is not None
            layer_tuple = ListItem(layer, layer.index)  # create a new instance of ListItem with the key as layer.index and value as layer

            # Worst case is O(n), where n is the length of layer_array at which the loop must run through all elements
            # Best case is O(1), where the layer_tuple can be found in 1 iteration
            if layer_tuple in self.layer_array:  # checks if the ListItem is already in the array list or not, if it is return False
                return False

            # Worst case is O(n), where the layer_array has to be rearranged completely to add an element + O(log(n)),
            # where _index_to_add(item) function is a binary search at which n is the length of the array. But, since
            # for worst case we take the dominant complexity O(n) + O(log(n)) -> O(n), where n is length of layer_array
            # Best case is O(log n), where the element to add is at the end of the list which takes O(log n) complexity
            # to find and when the element is added in the last index no rearrange is required
            self.layer_array.add(layer_tuple)   # adds the ListItem in a sorted position by layer.index in ArraySortedList and return True
            return True

        return False

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        How: Loops through the whole layer_array and apply each layer in order of layer.index

        Args:
        - start (tuple[int, int, int]): initial color
        - timestamp (int): delta-time value for continuous display
        - x (int): x-coordinate to get_color
        - y (int): y-coordinate to get_color

        Raises:
        - None

        Returns:
        - tuple[int, int, int] -> Current color after layer applied

        Complexity:
        - Worst case: O(n*apply), where n is length of layer_array, and apply depends on complexity of layer.apply
          - Reason: O(n) * O(apply) -> O(n*apply), At the worst case, the for loop runs maximum time and the apply
                    function of layers also runs as many times as the for loop. So, the complexity is calculated by
                    multiplying both complexities
        - Best case: O(1), when there is no layer in the layer array
          - Reason: The best case is O(1) when the array is empty where we just return the initial color

        *** All codes are assumed as O(1) unless stated otherwise

        """

        # O(1) -> Integer comparison
        if self.layer_array.is_empty():  # if there are no layers in the layer_array, return the starting color back
            return start

        color = start  # set the variable color to start
        # Worst case is O(n*apply), where n is the length of layer_array and the complexity of apply depends on layer
        # Since the complexity of for loop is O(n) and apply is O(apply), O(n) * O(apply) = O(n*apply)
        # Best case is O(n), where n is the length of self.layer_array
        for i in range(self.layer_array.length):  # For every element of layer in the layer_array list, the layer is applied to the color
            # O(apply), where the complexity of apply depends on the layer
            color = self.layer_array[i].value.apply(color, timestamp, x, y)  # The layer applied color is returned and stored in variable color

        return color  # return color

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        How: Checks if the layer is in array, and delete if it is in array

        Args:
        - layer: one of the layers from the layer class instances

        Raises:
        - None

        Returns:
        - boolean (True if layer erased, else False)

        Complexity:
        - Worst case: O(n), where n is teh length of the array
          - Reason: O(n) + O(log n) -> O(n), at the worst case, the binary search in index() method will run O(log n)
                    complexity and delete at index takes O(n) to shuffle all the elements when first index removed.
                    Addition of 2 complexity we will select the most dominant which is O(n)
        - Best case: O(log n)
          - Reason: Although index() and delete_at_index() in remove() have O(1) complexities for best case, they do not
                    correlate as for index() best case is middle index, while delete_at_index() best case is at
                    the last index. So for the best case we can assume that the index is the last element, where the
                    index() runs for O(log n) complexity and delete_at_index() runs at O(1) complexity. Thus,
                    the complexity is O(log n) where n is the length of the array

        *** All codes are assumed as O(1) unless stated otherwise

        """

        if layer is not None:  # Checks if the layer is None

            if ListItem(layer, layer.index) not in self.layer_array:    # Checks if ListItem is already added in the ArraySortedList, if it is not, return False
                return False

            layer_item = ListItem(layer, layer.index)   # gets the ListItem instance for the layer

            # Worst case of item() is O(log n), where _index_to_add(item) function is a binary search at which n is the
            # length of the array.
            # Best case of item() is O(1), where when the index of the element is at middle

            # remove method calls item() and delete_at_index() function in ArraySortedList()
            # Worst case of remove function is O(n), where n is the length of the array
            # Best case of remove function is O(log n ), where n is the length of the array
            self.layer_array.remove(layer_item)  # calls the remove function in ArraySortedList()

            return True # return True

        return False  # if not it does not delete anything and return False

    def special(self) -> None:
        """
        Special mode: Sort the names of the layers lexicographically and erase the middle index
        How: Since the sorting algorithm will sort based on the key values,
             the elements in layer_array stored in a new list with layer name as key so it will be sorted automatically

        Args:
        - None

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(n * add), where n is the length of the array and add is the complexity of add function in ArraySortedlist
        - Best case: O(n * add), where n is the length of the array and add is the complexity of add function in ArraySortedlist
        - Reason: The best case and worst case time complexity of the special method is O(n * add), where n is the
                  length of self.layer_array and add is the complexity of add function of ArraySortedList. This is
                  because the time complexity is based off the for loop which runs n times and for every iteration,
                  the add function is called which has the complexity of O(add). So, the best and worse case depends on
                  add function as n time iteration occurs as n is just the length of the array. Thus, it is O(n * add)

        *** All codes are assumed as O(1) unless stated otherwise

        """

        # O(n), where n is the length of self.layer_array
        name_list = ArraySortedList(len(self.layer_array))  # Initialize a new SortedArrayList of length self.layer_array

        if not self.layer_array.is_empty():  # Checks if the layer_array is empty

            length = len(self.layer_array)  # gets the length of the layer_array

            # Worse case: Big O Complexity is O(n * add), where n is the length of the array and add is the complexity of add function in ArraySortedlist
            # Best case: Big O Complexity is O(n * add), where n is the length of the array and add is the complexity of add function in ArraySortedlist
            for i in range(length):  # The for loop runs the length of layer_array times
                layer_ref = self.layer_array[i]  # For each iteration it gets the value of an element in the array (ListItem)
                name_list.add(ListItem(layer_ref.value, layer_ref.value.name))  # adds the layer instance and the name of the layer as Listitem into the name_list

            # Below if function finds the middle index from the rearranged array
            if self.layer_array.length % 2 != 0:  # Checks if the length of array is odd
                index_to_remove = (length // 2)  # the index is the middle value (odd)
            else:
                index_to_remove = (length // 2) - 1  # the index to remove is the smaller of the middle value (even)

            # Worse case: Big O Complexity of self.erase function is O(n), where n is the length of the layer_array
            # Best case: Big O Complexity of self.erase function is O(log n), where n is the length of the layer_array
            self.erase(name_list[index_to_remove].value)  # erase the middle value layer from layer_array
