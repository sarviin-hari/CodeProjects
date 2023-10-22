from __future__ import annotations

from algorithms.binary_search import binary_search
from algorithms.mergesort import merge, mergesort
from data_structures.hash_table import LinearProbeTable
from double_key_table import DoubleKeyTable
from infinite_hash_table import InfiniteHashTable
from mountain import Mountain


class MountainOrganiser:

    def __init__(self) -> None:
        self.m_organiser = []

    def cur_position(self, mountain: Mountain) -> int:
        """
        cur_position: should have complexity at most O(log(N)), where N is the total number of mountains included so far

        Args:
        - mountain - mountain class instance

        Raises:
        - KeyError

        Returns:
        - boolean - True / False

        Complexity:
        - Worst case: O(log N), where N is the length of m_organiser list.
                      The worse case happens due to the binary search operation which has a complexity of O(Nlog N)
        - Best case: O(log N), where N is the length of m_organiser list.
                     The best case happens due to the binary search operation which has a complexity of O(Nlog N)
        """

        index = binary_search(self.m_organiser, mountain)
        if index >= len(self.m_organiser) or self.m_organiser[index] != mountain:
            raise KeyError
        return index

    def add_mountains(self, mountains: list[Mountain]) -> None:
        """
        add_mountains: should have complexity at most O(Mlog(M)+N), where M is the length of the input list,
        and N is the total number of mountains included so far.

        Args:
        - mountains - a list of mountain class instance

        Raises:
        - KeyError

        Returns:
        - None

        Complexity:
        - Worst case: O(Mlog(M)+N), where M is the length of the input list, and N is the total number of mountains
                      included so far. The worse case happens due to the mountain list input having to sort itself
                      then merged with the self.m_organizer list
                      For the worst case the complexity is O(Mlog M + (M+N)) = O(M(log M + 1) +N) = O(Mlog(M)+N)
        - Best case: O(Mlog(M)+N), where M is the length of the input list, and N is the total number of mountains
                      included so far. The worse case happens due to the mountain list input having to sort itself
                      then merged with the self.m_organizer list
        """

        sort_val = mergesort(mountains)
        self.m_organiser = merge(self.m_organiser, sort_val)
