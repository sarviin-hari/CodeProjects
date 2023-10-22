from dataclasses import dataclass
from heap import MaxHeap
from queue_adt import CircularQueue
from referential_array import ArrayR


@dataclass
class Beehive:
    """A beehive has a position in 3d space, and some stats."""

    x: int
    y: int
    z: int

    capacity: int
    nutrient_factor: int
    volume: int = 0

    def __gt__(self, other):
        if min(self.volume, self.capacity)*self.nutrient_factor > min(other.volume, other.capacity)*other.nutrient_factor:
            return True
        return False

    def __ge__(self, other):
        if min(self.volume, self.capacity)*self.nutrient_factor > min(other.volume, other.capacity)*other.nutrient_factor:
            return True
        return False


class BeehiveSelector:

    def __init__(self, max_beehives: int):
        """
        Args:
        - max_beehives: int of the maximum number of Beehive instances that can be stored

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case:
        - Best case:
        - Reason:
        """

        self.hive = MaxHeap(max_beehives)

    def set_all_beehives(self, hive_list: list[Beehive]):
        """
        Apply bottom-up heap construction in O(n) time

        Args:
        - max_beehives: List of Beehive instance

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(n), where n is the length of the max_beehives
        - Best case: O(n), where n is the length of the max_beehives
        - Reason: The first loop takes O(n) complexity to restore all the previous
                  elements to new elements from the max_beehives, and has the complexity
                  of O(n//2) which is also of O(n) complexity
        """

        self.hive.heapify(hive_list)

    def add_beehive(self, hive: Beehive): #####3333#######
        """
        Args:
        - hive: an instance of Beehive class

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(log n), where n is the number of elements in the heap
            - Reason: This is because when an element is added, its parent is compared throughout the insertion process,
                  and if necessary, the element is swapped out, which adds time proportional to the height of the heap.
                  A binary heap's height is logarithmic in the number of elements because it is a balanced tree.
        - Best case: O(1*comp)
            - Reason: This happens when element is greater or equal to one of its children (cannot be smaller)
        """
        self.hive.add(hive)
    
    def harvest_best_beehive(self):

        """
        Args:
        - None

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O((log n)*comp), where n is the number of elements in the heap
            - Reason: When deleting the root node element, the leaf node element will become the new root and sink
                      operation occurs all the way to the bottom
        - Best case: O(1*comp)
            - Reason: This happens when element is greater or equal to one of its children (cannot be smaller)
        """

        val = self.hive.get_max()
        cap = min(val.capacity, val.volume)*val.nutrient_factor

        if not ((val.volume - val.capacity) <= 0):
            val.volume = val.volume - val.capacity
            self.add_beehive(val)

        return cap
