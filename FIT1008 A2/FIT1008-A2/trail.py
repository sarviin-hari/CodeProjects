from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass

from data_structures.linked_stack import LinkedStack
from mountain import Mountain

from typing import TYPE_CHECKING, Union

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality

@dataclass
class TrailSplit:
    """
    A split in the trail.
       ___path_top____
      /               \
    -<                 >-path_follow-
      \__path_bottom__/
    """

    path_top: Trail
    path_bottom: Trail
    path_follow: Trail

    def remove_branch(self) -> TrailStore:
        """
        Removes the branch, should just leave the remaining following trail.

        Args:
        - None

        Raises:
        - None

        Returns:
        - Next TrailStore instance

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: The method only returns a value which has a constant complexity
        """

        # returns the following TrailStore instance excluding the top and bottom
        return self.path_follow.store


@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail

    def __init__(self, mountain, following):
        self.mountain = mountain
        self.following = following

    def remove_mountain(self) -> TrailStore:
        """
        Removes the mountain at the beginning of this series.

        Args:
        - None

        Raises:
        - None

        Returns:
        - Next TrailStore instance

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: The method only returns a value which has a constant complexity

        """
        # returns the following store which has the TrailStore of the next instance
        return self.following.store

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """
        Adds a mountain in series before the current one.

        Args:
        - mountain -> Instance of a Mountain class

        Raises:
        - None

        Returns:
        - A TrailStore instance with new mountain added before the next TrailStore instance

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: The method only returns a value which has a constant complexity
        """
        # returns a TrailSeries instance with a mountain added followed by the previous TrailSeries instance
        return TrailSeries(mountain, Trail(TrailSeries(self.mountain, self.following)))

    def add_empty_branch_before(self) -> TrailStore:
        """
        Adds an empty branch, where the current trailstore is now the following path.

        Args:
        - None

        Raises:
        - None

        Returns:
        - TrailSplit Instance

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: The method only returns a value which has a constant complexity
        """
        # returns a TrailSplit instance with top and bottom branch as None, while the path_follow branch is the previous
        # TrailSeries instance
        return TrailSplit(Trail(None), Trail(None), Trail(TrailSeries(self.mountain, self.following)))

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """
        Adds a mountain after the current mountain, but before the following trail.

        Args:
        - mountain -> Instance of a Mountain class

        Raises:
        - None

        Returns:
        - TrailSeries Instance

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: The method only returns a value which has a constant complexity
        """
        # returns a TrailSeries instance with the previous mountain added, followed by the next mountain, followed by
        # the next following Trail instance
        return TrailSeries(self.mountain, Trail(TrailSeries(mountain, self.following)))

    def add_empty_branch_after(self) -> TrailStore:
        """
        Adds an empty branch after the current mountain, but before the following trail.

        Args:
        - None

        Raises:
        - None

        Returns:
        - TrailSeries Instance

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: The method only returns a value which has a constant complexity
        """
        # returns a TrailSeries instance where the mountain is added, followed by a branch with top and bottom as None
        # and the following as the path_follow
        return TrailSeries(self.mountain, Trail(TrailSplit(Trail(None), Trail(None), self.following)))


TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None


    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """
        Adds a mountain before everything currently in the trail.

        Args:
        - mountain -> Instance of a Mountain class

        Raises:
        - None

        Returns:
        - Trail Instance

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: The method only returns a value which has a constant complexity
        """
        # returns a Trail instance by adding a mountain followed by the following of TrailSeries
        return Trail(TrailSeries(mountain, Trail(self.store)))

    def add_empty_branch_before(self) -> Trail:
        """
        Adds an empty branch before everything currently in the trail.

        Args:
        - None

        Raises:
        - None

        Returns:
        - Trail Instance

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        - Reason: The method only returns a value which has a constant complexity
        """

        # return a Trail instance with a TrailSplit instance as its store which has
        # None as its top and bottom and self.store as its follow path
        return Trail(TrailSplit(Trail(None), Trail(None), Trail(self.store)))

    def follow_path(self, personality: WalkerPersonality) -> None:
        """
        Follow a path and add mountains according to a personality.

        Args:
        - personality -> Instance of a WalkerPersonality class

        Raises:
        - None

        Returns:
        - TrailSplit Instance
        """

        path = self.store
        following = LinkedStack()

        # loops as long as there is a path and the following list has elements
        while not (path is None and len(following) == 0):

            # Checks if path is the instance of TrailSeries
            if isinstance(path, TrailSeries):
                # if there is a mountain on the TrailStore, add in the personality
                if path.mountain is not None:
                    personality.add_mountain(path.mountain)
                # set the path as the next TrailStore
                path = path.following.store

            # Checks if path is the instance of TrailSplit
            elif isinstance(path, TrailSplit):
                # if the following path is not None, add following TrailStore in following list
                if path.path_follow != Trail(None):
                    following.push(path.path_follow)

                # gets the branch the path should follow
                isTop = personality.select_branch(path.path_top, path.path_bottom)

                # if True, select the top path and set the path as the next TrailStore
                if isTop:
                    path = path.path_top.store
                # if False, select the bottom path and set the path as the next TrailStore
                else:
                    path = path.path_bottom.store

            # Checks condition if path is None
            if path is None:
                # if there is a path in following, pop it and set it as path
                if len(following) != 0:
                    path = following.pop().store

    def collect_all_mountains(self) -> list[Mountain]:
        """
        Returns a list of all mountains on the trail.

        Args:
        - None

        Raises:
        - None

        Returns:
        - A list of mountains obtained from the whole trail
        """

        mountain_list = []
        following = []
        path = self.store
        num = 0
        while not (path is None and len(following) == 0):
            print(num, path, "\n", type(path), "\n", mountain_list, "\n")
            if isinstance(path, TrailSeries):
                print("TrailSeries, following: \n", path.following, "\n")
            else:
                print("TrailSplit, path top: \n", path.path_top, "\n")
                print("TrailSplit, path bottom: \n", path.path_bottom, "\n")
                print("TrailSplit, path follow: \n", path.path_follow, "\n")

            # Checks if path is the instance of TrailSeries
            if isinstance(path, TrailSeries):
                # if there is a mountain on the TrailStore, add in the personality
                if path.mountain is not None:
                    mountain_list.append(path.mountain)
                # set the path as the next TrailStore
                path = path.following.store

            # Checks if path is the instance of TrailSplit
            elif isinstance(path, TrailSplit):
                # if the following path is not None, add following TrailStore in following list
                if not path.path_top == Trail(None):
                    following.append(path.path_top)

                if not path.path_bottom == Trail(None):
                    following.append(path.path_bottom)

                path = path.path_follow.store

            if path is None:
                # if there is a path in following, pop it and set it as path
                if len(following) != 0:
                    print("in\n")
                    path = following.pop(len(following) - 1).store

            num += 1

        return mountain_list

    def length_k_paths(self, k) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 8 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.

        Args:
        - k - Integer that indicates the number of mountains

        Raises:
        - None

        Returns:
        - A list of a list of mountains of the length k
        """
        paths = self.rec_length_k_paths(self.store, [])

        return_list = []
        for i in range(len(paths)):
            if len(paths[i]) == k:
                return_list.append(paths[i])
            elif len(paths[i]) > k:
                return_list.append(paths[i][:k])
        return return_list

    def rec_length_k_paths(self, current_path, m_add_list):
        """
        Args:
        - current - int - Indicates the current number of mountains added
        - target - int - Indicates the target number of mountains needed
        - current_path - TrailStore - Current tree path being checked
        - m_add_list - List -  A list of mountains until the path currently in

        Raises:
        - None

        Returns:
        - A list of a list of mountains from the whole path
        """

        if current_path is None:
            return m_add_list

        # if current != target:
        if isinstance(current_path, TrailSeries):
            print("Mountain list Before: \n", m_add_list)

            if len(m_add_list) == 0:
                mount = current_path.mountain
                if current_path.mountain is not None:
                    m_add_list.append(mount)
            elif isinstance(m_add_list[0], list):
                for i in range(len(m_add_list)):
                    mount = current_path.mountain
                    if current_path.mountain is not None:
                        m_add_list[i].append(mount)
            else:
                mount = current_path.mountain
                if current_path.mountain is not None:
                    m_add_list.append(mount)

            return self.rec_length_k_paths(current_path.following.store, deepcopy(m_add_list))

        if isinstance(current_path, TrailSplit):
            print("Mountain list Before Split: \n", m_add_list)

            bot_mountain = self.rec_length_k_paths(current_path.path_bottom.store, deepcopy(m_add_list))
            print("Bottom Split: \n", bot_mountain)

            top_mountain = self.rec_length_k_paths(current_path.path_top.store, deepcopy(m_add_list))
            print("Top Split: \n", top_mountain)

            fol_bot_mountain = self.rec_length_k_paths(current_path.path_follow.store, deepcopy(bot_mountain))
            # print("kjbdfbvbsdhjbkjds")
            fol_top_mountain = self.rec_length_k_paths(current_path.path_follow.store, deepcopy(top_mountain))
            # print("ihbbhbjkfbjnjfndj")
            print("Following Bottom Split: \n", fol_bot_mountain)
            print("Following Top Split: \n", fol_top_mountain)
            # print(self.num)


            if isinstance(fol_top_mountain[0], list) and isinstance(fol_bot_mountain[0], list):
                print("in 1")
                return fol_top_mountain + fol_bot_mountain
            elif isinstance(fol_top_mountain[0], list):
                print("in 2")
                fol_top_mountain.append(fol_bot_mountain)
                return fol_top_mountain
            elif isinstance(fol_bot_mountain[0], list):
                print("in 3")
                fol_bot_mountain.append(fol_top_mountain)
                return fol_bot_mountain
            print("in 4")
            return [fol_top_mountain, fol_bot_mountain]

    # check if the list length all is supposed to be one