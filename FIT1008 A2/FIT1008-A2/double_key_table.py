from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')

class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes:list|None=None, internal_sizes:list|None=None) -> None:
        """
        Args:
        - sizes - List - List of external table sizes
        - internel_sizes - List - List of internal table sizes

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
        self.size_index = 0  # Stores the index of table size
        self.count = 0  # Stores the number of elements in the DoubleHashTable
        self.sizes = sizes  # stores the list for the External Hash Table
        self.internal_sizes = internal_sizes    # stores the list for the Internal Hash Table

        if sizes is not None:   # if sizes is not None, reinitialize self.TABLE_SIZES as sizes
            self.TABLE_SIZES = self.sizes
        self.external_table: ArrayR[tuple[(K1, K2), V]] = ArrayR(self.TABLE_SIZES[self.size_index])  # creates an array of length from TABLE_SIZES

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """
        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)

        # print("Size of internal table: ", sub_table.table_size)
        return value

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.

        isinsert is to find the key
        if True -> return first available slot
        if False -> key found, return key position
                    key not found, return KeyError

        Args:
        - key1 - str - key for external table
        - key2 - str - key for internal table
        - is_insert - boolean - indicates if an element is to be added or not

        Raises:
        - KeyError

        Returns:
        - None

        Complexity:
        - Worst case: O(len(key) + 2*N*comp==), where O(len(key)) is the complexity of teh hash function, N is the
                      size of the hash table and comp== determines the complexity when comparing two keys.
                      This worst-case scenario occurs when all positions in the hash table are occupied and all
                      positions must be searched to find the empty space or key for both internal and external hash
                      table indicating O(N*comp==) * 2.
        - Best case:  O(len(key)), which is the complexity of the hash function.
                      This happens when the first position checked is empty, and the key can be inserted directly
                      without any probing in both external and internal table.
        """

        pos1 = self.hash1(key1)  # gets the hash value for the key
        pos_confirmed = False   # default is False, set to True if key already exists or if there is space to insert key

        for i in range(self.table_size):
            # print("Position to add None or not: ", pos1, self.external_table[pos1])

            # if there is no element in the position
            if self.external_table[pos1] is None:

                # if the element is to be inserted into the hash table
                if is_insert:
                    # Creates the instances for internal hash table
                    if self.internal_sizes is None:
                        internal_table = LinearProbeTable()
                    else:
                        internal_table = LinearProbeTable(self.internal_sizes)

                    # Change the hash function in internal hash table
                    internal_table.hash = lambda k: self.hash2(k, internal_table)

                    # Sets the position of external table with key and value (internal hash table instance)
                    self.external_table[pos1] = (key1, internal_table)
                    self.count += 1  # increase the length of external table by 1
                    pos_confirmed = True    # set the pos_confirmed to True
                    break   # break the loop

                # if the element is not to be inserted into the hash table, raise KeyError as it does not exist in table
                else:
                    raise KeyError(key1)

            # if the element already exist in the table, break the loop
            elif self.external_table[pos1][0] == key1:
                # pos1 = pos1
                pos_confirmed = True
                break

            # if there is element in the given position and the key does not match, increase the position by 1
            else:
                pos1 = (pos1 + 1) % self.table_size

        # if key2 not in self.external_table[pos1][1] and is_insert is False:
        #     raise KeyError
        # if key2 not in self.external_table[pos1][1] and is_insert is True:

        # if the element cannot be added or the key does not match
        if pos_confirmed is False:
            # if is_insert is True, raise FullError, else, raise KeyError
            if is_insert:
                raise FullError("Table is full!")
            else:
                raise KeyError(key1)

        # call the linear probe function for the internal hash table
        pos2 = self.external_table[pos1][1]._linear_probe(key2, is_insert)

        return pos1, pos2

    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.

        Args:
        - key - str - key for external table

        Raises:
        - KeyError

        Returns:
        - An Interator object for the keys

        Complexity:
        - Worst case: O(N), where N is the size of the external hash table. When the key parameter is None, we need to
                      iterate through all the entries in the external table to find the keys.
        - Best case: O(1), where key is not None and the if the key of the internal table is in the first index

        """
        if key is None:

            for i in range(len(self.external_table)):
                if self.external_table[i] is not None:
                    yield self.external_table[i][0]

        else:
            pos1 = self.hash1(key)

            for i in range(self.table_size):
                if self.external_table[pos1] is None:
                    yield []
                    break
                if self.external_table[pos1][0] != key:
                    pos1 = (pos1 + 1) % self.table_size
                else:
                    for keys in self.external_table[pos1][1].keys():
                        yield keys
                    break

    def keys(self, key:K1|None=None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.

        Args:
        - key - str - key for external table

        Raises:
        - None

        Returns:
        - List of keys

        Complexity:
        - Worst case: O(N), where N is the size of the external hash table. When the key parameter is None, we need to
                      iterate through all the entries in the external table to find the keys.
        - Best case: O(1), where key is not None and the if the key of the internal table is in the first index
        """
        all_key = []
        if key is None:
            for i in range(self.table_size):
                if self.external_table[i] is not None:
                    all_key.append(self.external_table[i][0])
            return all_key
        else:
            pos1 = self.hash1(key)

            for i in range(self.table_size):
                if self.external_table[pos1] is None:
                    return all_key
                if self.external_table[pos1][0] != key:
                    pos1 = (pos1 + 1) % self.table_size
                else:
                    return self.external_table[pos1][1].keys()

    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.

        Args:
        - key - str - key for external table

        Raises:
        - None

        Returns:
        - An Iterator object for the values

        Complexity:
        - Worst case: O(M*N), where N is the size of the external hash table and N is the maximum length of all the
                      value lists. When the key parameter is None, we need to iterate through all the entries in the
                      external table to find the values and in worst case, all the elements in the external table has
                      values so we have to traverse through all the internal table in the external table as well.
        - Best case: O(1), where the key value is not None and if the key of the internal table is in the first index
        """

        if key is None:
            for i in range(len(self.external_table)):
                if self.external_table[i] is not None:  # if self.external_table[i][0] is not None:
                    val_list = self.external_table[i][1].values()
                    for j in range(len(val_list)):
                        yield val_list[j]
        else:

            pos1 = self.hash1(key)
            for i in range(self.table_size):
                # If no elem in the given index, return empty list
                if self.external_table[pos1] is None:
                    yield []
                    break
                if self.external_table[pos1][0] != key:
                    pos1 = (pos1 + 1) % self.table_size

                else:
                    for val in self.external_table[pos1][1].values():
                        yield val
                    break

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.

        Args:
        - key - str - key for external table

        Raises:
        - None

        Returns:
        - List of values

        Complexity:
        - Worst case: O(M*N), where N is the size of the external hash table and N is the maximum length of all the
                      value lists. When the key parameter is None, we need to iterate through all the entries in the
                      external table to find the values and in worst case, all the elements in the external table has
                      values so we have to traverse through all the internal table in the external table as well.
        - Best case: O(1), where the key value is not None and if the key of the internal table is in the first index
        """

        all_values = []
        if key is None:
            for i in range(len(self.external_table)):
                if self.external_table[i] is not None:  # if self.external_table[i][0] is not None:
                    val_list = self.external_table[i][1].values()
                    for j in range(len(val_list)):
                        all_values.append(val_list[j])
            return all_values
        else:
            pos1 = self.hash1(key)
            for i in range(len(self.external_table)):
                # If no elem in the given index, return empty list
                if self.external_table[pos1] is None:
                    return all_values
                if self.external_table[pos1][0] != key:
                    pos1 = (pos1 + 1) % self.table_size
                else:
                    val_list = self.external_table[pos1][1].values()
                    return val_list

    def __contains__(self, key: tuple[K1, K2]) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.

        Args:
        - key - tuple - key1, key2 of class str in a tuple

        Raises:
        - None

        Returns:
        - boolean - True/False

        Complexity:
        - Worst case: The complexity is the same as the worst case complexity of get_item() of this class.
                      O(len(key) + 2*N*comp==), where O(len(key)) is the complexity of teh hash function, N is the
                      size of the hash table and comp== determines the complexity when comparing two keys.
                      This worst-case scenario occurs when all positions in the hash table are occupied and all
                      positions must be searched to find the empty space or key for both internal and external hash
                      table indicating O(N*comp==) * 2.
        - Best case:  The complexity is the same as the base case complexity of get_item() of this class.
                      O(len(key)), which is the complexity of the hash function.
                      This happens when the first position checked is empty, and the key can be inserted directly
                      without any probing in both external and internal table.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.

        Args:
        - key - tuple - key1, key2 of class str in a tuple

        Raises:
        - None

        Returns:
        - boolean - True/False

        Complexity:
        - Worst case: O(len(key) + 2*N*comp==), where O(len(key)) is the complexity of teh hash function, N is the
                      size of the hash table and comp== determines the complexity when comparing two keys.
                      This worst-case scenario occurs when all positions in the hash table are occupied and all
                      positions must be searched to find the empty space or key for both internal and external hash
                      table indicating O(N*comp==) * 2.
        - Best case:  O(len(key)), which is the complexity of the hash function.
                      This happens when the first position checked is empty, and the key can be inserted directly
                      without any probing in both external and internal table.
        """
        pos = self._linear_probe(key[0], key[1], False)
        return self.external_table[pos[0]][1][key[1]]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        Args:
        - key - tuple - key1, key2 of class str in a tuple
        - data - str/int/tuple or etc, depending on the storage requirement

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(len(key) + 2*N*comp==), where O(len(key)) is the complexity of teh hash function, N is the
                      size of the hash table and comp== determines the complexity when comparing two keys.
                      This worst-case scenario occurs when all positions in the hash table are occupied and all
                      positions must be searched to find the empty space or key for both internal and external hash
                      table indicating O(N*comp==) * 2.
        - Best case:  O(len(key)), which is the complexity of the hash function.
                      This happens when the first position checked is empty, and the key can be inserted directly
                      without any probing in both external and internal table.
        """
        print("in")
        pos = self._linear_probe(key[0], key[1], True)

        self.external_table[pos[0]][1][key[1]] = data

        if len(self) > self.table_size / 2:
            self._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:      # Need to add while loop to reshuffle to correct position
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.

        Args:
        - key - tuple - key1, key2 of class str in a tuple
        - data - str/int/tuple or etc, depending on the storage requirement

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(delete), where delete is the worst case complexity of the delete special method in
                      the hash table
        - Best case: O(delete), where delete is the best case complexity of the delete special method in
                      the hash table
        """

        position = self._linear_probe(key[0], key[1], False)

        del self.external_table[position[0]][1][key[1]]

        if len(self.external_table[position[0]][1]) == 0:
            # Remove the element
            self.external_table[position[0]] = None
            self.count -= 1

            pos = (position[0] + 1) % self.table_size
            while self.external_table[pos] is not None:
                key1, value = self.external_table[pos]
                self.external_table[pos] = None
                # Reinsert.
                newpos = self.hash1(key1)
                # probe to find the next available free slot (linear probing)
                while self.external_table[newpos] is not None:
                    newpos = (newpos + 1) % self.table_size
                self.external_table[newpos] = (key1, value)
                pos = (pos + 1) % self.table_size

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        Args:
        - None

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(N*linear_probe), where N is the length of the new hash array and linear_probe is the
                      complexity of the _linear_probe function in internal hash table of LinearProbeTable class.
                      This happens when the whole list has large number of elements and multiple linear probing is
                      required

        - Best case:  O(N), where N is the length of the new hash array
                      This happens when no linear probing is required to resize
        """

        old_array = self.external_table
        self.size_index += 1
        if self.size_index == len(self.TABLE_SIZES):
            return
        self.external_table = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0
        for item in old_array:
            if item is not None:
                key, value = item
                key_list = value.keys()
                value_list = value.values()
                for j in range(len(key_list)):
                    self[key, key_list[j]] = value_list[j]


    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return len(self.external_table)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table

        Args:
        - None

        Raises:
        - None

        Returns:
        - Integer

        Complexity:
        - Worst case: O(1), the function just returns the self.count value
        - Best case:  O(1), the function just returns the self.count value
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.

        Args:
        - None

        Raises:
        - None

        Returns:
        - Integer

        Complexity:
        - Worst case: O(N), where N is the length of the external table
        - Best case:  O(N), where N is the length of the external table
        """
        res = "\nString Representation: \n"
        for i in range(len(self.external_table)):
            if self.external_table[i] is not None:
                string_val = self.external_table[i][1].__str__()
                res += "Index: " + str(i) + " --> " + str(self.external_table[i][0]) + string_val + "\n"
        return res


