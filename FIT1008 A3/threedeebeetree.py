from __future__ import annotations
from typing import Generic, TypeVar, Tuple
from dataclasses import dataclass, field

I = TypeVar('I')
Point = Tuple[int, int, int]

@dataclass
class BeeNode:

    key: Point
    item: I
    subtree_size: int = 1

    def __init__(self, key, item):
        self.key = key
        self.item = item
        self.lst = [None]*8

    def get_child_for_key(self, point: Point) -> BeeNode | None:
        return self.get_child_for_key_aux(self, point)

    def get_child_for_key_aux(self, current, point):
        if current is None:
            return None
        if current.key == point:
            return current

        elif point[0] < current.key[0]:
            if point[1] < current.key[1]:
                if point[2] < current.key[2]:
                    return current.lst[0]
                else:
                    return current.lst[1]
            else:
                if point[2] < current.key[2]:
                    return current.lst[2]
                else:
                    return current.lst[3]
        elif point[0] > current.key[0]:
            if point[1] < current.key[1]:
                if point[2] < current.key[2]:
                    return current.lst[4]
                else:
                    return current.lst[5]
            else:
                if point[2] < current.key[2]:
                    return current.lst[6]
                else:
                    return current.lst[7]

    # def __str__(self):



class ThreeDeeBeeTree(Generic[I]):
    """ 3️⃣🇩🐝🌳 tree. """

    def __init__(self) -> None:
        """
            Initialises an empty 3DBT
        """
        self.root = None
        self.length = 0

    def is_empty(self) -> bool:
        """
            Checks to see if the 3DBT is empty
        """
        return len(self) == 0

    def __len__(self) -> int:
        """ Returns the number of nodes in the tree. """

        return self.length

    def __contains__(self, key: Point) -> bool:
        """
            Checks to see if the key is in the 3DBT
        """
        try:
            self.get_tree_node_by_key(key)
            return True
        except KeyError:
            return False

    def __getitem__(self, key: Point) -> I:
        """
            Attempts to get an item in the tree, it uses the Key to attempt to find it
        """
        node = self.get_tree_node_by_key(key)
        return node.item

    def get_tree_node_by_key(self, key: Point) -> BeeNode:
        return self.get_tree_node_by_key_aux(self.root, key)

    def get_tree_node_by_key_aux(self, current, point):
        if current is None:
            return None
        if current.key == point:
            return current
        child = current.get_child_for_key(point)
        return self.get_tree_node_by_key_aux(child, point)

    def __setitem__(self, key: Point, item: I) -> None:
        self.root = self.insert_aux(self.root, key, item)

    def insert_aux(self, current: BeeNode | None, key: Point, item: I) -> BeeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert it
            Index -   1  2   3   4   5   6   7   8
            LIST - [sss,ssb,sbs,sbb,bss,bsb,bbs,bbb]
        """

        if current is None:  # base case: at the leaf
            current = BeeNode(key, item)
            self.length += 1
        elif key[0] < current.key[0]:
            current.subtree_size += 1
            if key[1] < current.key[1]:
                if key[2] < current.key[2]:
                    current.lst[0] = self.insert_aux(current.lst[0], key, item)
                else:
                    current.lst[1] = self.insert_aux(current.lst[1], key, item)
            else:
                if key[2] < current.key[2]:
                    current.lst[2] = self.insert_aux(current.lst[2], key, item)
                else:
                    current.lst[3] = self.insert_aux(current.lst[3], key, item)

        elif key[0] > current.key[0]:
            current.subtree_size += 1
            if key[1] < current.key[1]:
                if key[2] < current.key[2]:
                    current.lst[4] = self.insert_aux(current.lst[4], key, item)
                else:
                    current.lst[5] = self.insert_aux(current.lst[5], key, item)
            else:
                if key[2] < current.key[2]:
                    current.lst[6] = self.insert_aux(current.lst[6], key, item)
                else:

                    current.lst[7] = self.insert_aux(current.lst[7], key, item)

        else:  # key == current.key
            raise ValueError('Inserting duplicate item')
        return current





    def is_leaf(self, current: BeeNode) -> bool:
        """ Simple check whether or not the node is a leaf. """
        for i in current.lst:
            if i is not None:
                return False
        return True

if __name__ == "__main__":
    tdbt = ThreeDeeBeeTree()
    tdbt[(3, 3, 3)] = "A"
    tdbt[(1, 5, 2)] = "B"
    tdbt[(4, 3, 1)] = "C"
    tdbt[(5, 4, 0)] = "D"
    print(tdbt.root.get_child_for_key((4, 3, 1)).subtree_size) # 2
