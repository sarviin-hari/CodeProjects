from __future__ import annotations

import time
from typing import Generic, TypeVar

from data_structures.hash_table import LinearProbeTable
from data_structures.referential_array import ArrayR

K = TypeVar("K")
V = TypeVar("V")

class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self) -> None:
        """

        Args:
        - None

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(n)
        - Best case: O(n)
        - Reason: The complexity is O(n), where n is length of array from the first index of self.TABLE_SIZES
                  Best and worst case complexity for __init__ is O(n) as it handles assigning ArrayR instance to
                  a variable, which takes O(n) complexity
        """

        self.level = 0
        self.hash_array = ArrayR(self.TABLE_SIZE)
        self.count = 0

    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.

        Args:
        - None

        Raises:
        - KeyError

        Returns:
        - value - int - value stored in the key

        Complexity:
        - Worst case: O(N), where n is the number of arrays to be traversed before finding the element
                      This is because the N value depends on the Nth hash table the key-value pair is stored
        - Best case: O(1), when the key and value can be found from level 0
        """

        hash_val = self.hash(key)
        key_val_pair = self.hash_array[hash_val]

        while True:
            if key_val_pair is None:
                raise KeyError
            in_key, in_val = key_val_pair

            if not isinstance(in_val, InfiniteHashTable):
                if in_key == key:
                    return in_val
                raise KeyError
            hash_val = in_val.hash(key)
            key_val_pair = in_val.hash_array[hash_val]

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        Change count
        """
        print(self)
        aux_check = self._insert_helper(key, value, self)

        if aux_check is None:
            return

        prev_key, prev_val, instance = self._insert_helper(key, value, self)
        while instance.hash(key) == instance.hash(prev_key):
            instance.arr[instance.hash(key)] = (key[:instance.level + 1], InfiniteHashTable())
            new_instance = instance.arr[instance.hash(key)][1]
            new_instance.level = instance.level + 1

            instance = new_instance
            # increase the counter for the
            instance.count += 1

        self._insert_helper(key, value, instance)
        self._insert_helper(prev_key, prev_val, instance)
        instance.count -= 1

        print(instance.hash(key), instance.hash(prev_key))

    def _insert_helper(self, key: K, value: V, instance: InfiniteHashTable):  # best case - O(1) ; worse cose - O(l), where l is the level
        hash_index = instance.hash(key)

        if instance.hash_array[hash_index] is None:
            instance.count += 1
            instance.hash_array[hash_index] = (key, value)
            return None

        prev_key, prev_val = instance.hash_array[hash_index]

        if isinstance(prev_val, InfiniteHashTable):
            return self._insert_helper(key, value, prev_val)

        return prev_key, prev_val, instance
        # print(prev_key, prev_val, key, value, instance)
        #
        # while instance.hash(key) == instance.hash(prev_key):
        #     instance.hash_array[instance.hash(key)] = (key[:instance.level +1], InfiniteHashTable())
        #     new_instance = instance.hash_array[instance.hash(key)][1]
        #     new_instance.level = instance.level + 1
        #     instance = new_instance
        #     instance.count += 1
        #
        # self._insert_helper(key, value, instance)
        # self._insert_helper(prev_key, prev_val, instance)
        # instance.count -= 1
        #
        # print(instance.hash(key), instance.hash(prev_key))

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.

        Args:
        - None

        Raises:
        - KeyError - raised by the get_location method when there is no such key in hash array

        Returns:
        - None

        Complexity:
        - Worst case: O(n), where n is the length hash table to search for the element stored in the hash table when
                      it has only 1 element after deletion
        - Best case: O(1), when the element is in the first hash array, set the value to None and return takes O(1)
        """

        instance_list = []
        key_index = self.get_location(key)

        # if the element is in the first hash array, set it to None
        if len(key_index) == 1:
            self.hash_array[key_index[0]] = None
            self.count -= 1
            return

        # stores all the instances of hash_arrays into the instance_list
        val = self
        instance_list.append(val)
        for i in range(len(key_index)-1):
            val = val.hash_array[key_index[i]][1]
            instance_list.append(val)

        # delete the item by setting it to None
        val.hash_array[key_index[-1]] = None
        val.count -= 1

        # Reinitialize the single element
        # print(type(val), len(val), val.count)
        # raise KeyError
        if val.count == 1:
            internal_val, internal_key, instance = None, None, None

            # gets the single element in the hash table
            for i in range(self.TABLE_SIZE):
                if instance_list[-1].hash_array[i] is not None:
                    instance = instance_list.pop()
                    internal_key, internal_val = instance.hash_array[i]  # just a value
                    break

            # if the value of the element is instance of InfiniteHashTable, then no need to reinitialize
            if isinstance(internal_val, InfiniteHashTable):
                return

            # find the parent class to store
            while len(instance) == 1 and instance.level != 0:
                instance = instance_list.pop()

            # set the element in the position to the key and value
            instance.hash_array[instance.hash(internal_key)] = (internal_key, internal_val)

    def __len__(self):
        return self.aux_len(self)

    def aux_len(self, val):
        """
        Args:
        - val - instance of InfiniteHashTable or int of value of the key

        Raises:
        - None

        Returns:
        - Length of the list

        Complexity:
        - Worst case:
        - Best case:

        """
        if isinstance(val, int):
            return 1
        value = 0
        for index in range(len(val.arr)):
            if val.arr[index] is not None:
                value += self.aux_len(val.arr[index][1])
        return value

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """

        return str(self.__repr__())

    def get_location(self, key):
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.

        Args:
        - key - str - key to search for the value

        Raises:
        - KeyError - raised by the get_location method when there is no such key in hash array

        Returns:
        - A list of indexes

        Complexity:
        - Worst case: O(n), where n is the length hash table to search for the element stored in the hash table when
                      it has only 1 element after deletion
        - Best case: O(1), when the element is in the first hash array, set the value to None and return takes O(1)
        """

        loc = []
        index = self.hash(key)
        false_key, val = self.hash_array[index]
        loc.append(index)

        while isinstance(val, InfiniteHashTable):
            index = val.hash(key)
            print(loc)
            loc.append(index)
            try:
                false_key, val = val.hash_array[index]
            except TypeError:
                raise KeyError
        print(false_key, key)
        if false_key == key:
            return loc
        raise KeyError

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True
