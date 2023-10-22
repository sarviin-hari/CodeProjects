from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Mountain:
    name: str
    difficulty_level: int
    length: int

    def __le__(self, other):
        """
        Args:
        - other - mountain class instance - for comparison

        Raises:
        - KeyError

        Returns:
        - boolean - True / False

        Complexity:
        - Worst case: O(comp==), due to the comparison of string when length of self is the same as length of other
        - Best case: O(1), when the only comparison is integer comparison of length
        """
        if self.length < other.length:
            return True
        elif self.length == other.length:
            if self.name < other.name:
                return True
        return False

    def __lt__(self, other):
        """
        Args:
        - other - mountain class instance - for comparison

        Raises:
        - KeyError

        Returns:
        - boolean - True / False

        Complexity:
        - Worst case: O(comp==), due to the comparison of string when length of self is the same as length of other
        - Best case: O(1), when the only comparison is integer comparison of length
        """
        if self.length < other.length:
            return True
        elif self.length == other.length:
            if self.name < other.name:
                return True
        return False
