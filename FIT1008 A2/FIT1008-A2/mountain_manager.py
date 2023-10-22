from algorithms.mergesort import mergesort
from double_key_table import DoubleKeyTable
from mountain import Mountain


class MountainManager:

    def __init__(self) -> None:
        """

        Args:
        - None

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: It only involves the initialization of DoubleKeyTable
        """
        self.double = DoubleKeyTable()

    def add_mountain(self, mountain: Mountain):
        """

        Args:
        - mountain - Mountain class instance

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: It only involves storing a mountain in a DoubleKeyTable which has a complexity of O(1)
        """

        self.double[str(mountain.difficulty_level), mountain.name] = mountain

    def remove_mountain(self, mountain: Mountain):
        """
        Args:
        - mountain - Mountain class instance

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: It only involves deleting a mountain in a DoubleKeyTable which has a complexity of O(1)
        """

        del self.double[str(mountain.difficulty_level), mountain.name]

    def edit_mountain(self, old: Mountain, new: Mountain):
        """
        Args:
        - old - Mountain class instance
        - new - Mountain class instance

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: It only involves deleting the old mountain and adding new mountain in a DoubleKeyTable which has a
                  complexity of O(1)
        """
        self.remove_mountain(old)
        self.add_mountain(new)

    def mountains_with_difficulty(self, diff: int):
        """
        Args:
        - diff - int - mountain difficulty to access

        Raises:
        - None

        Returns:
        - A list of mountains

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: It only involves calling the values method of a DoubleKeyTable which has a complexity of O(1)
        """

        return self.double.values(str(diff))

    def group_by_difficulty(self) -> list[list[Mountain]]:
        """

        Args:
        - None

        Raises:
        - None

        Returns:
        - A list of a list of mountains

        Complexity:
        - Worst case: O(Nlog N), where N is the length of the key list (all keys in the hash table)
        - Best case: O(Nlog N), where N is the length of the key list (all keys in the hash table)
        - Reason: This is because the mergesort operation will happen at all cases which has a O(Nlog N) complexity
        """
        key = self.double.keys()

        key = mergesort(key)
        print(key)
        lst = []
        for i in range(len(key)):
            lst.append(self.double.values(key[i]))
        print(lst)
        return lst
