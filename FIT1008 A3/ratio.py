from __future__ import annotations

import math
from typing import Generic, TypeVar
from math import ceil
from bst import BinarySearchTree
from node import TreeNode

T = TypeVar("T")
I = TypeVar("I")

class Percentiles(Generic[T]):

    def __init__(self) -> None:
        self.lst = BinarySearchTree()
        self.counter = 0
    
    def add_point(self, item: T):
        self.lst[item] = item

    def remove_point(self, item: T):
        del self.lst[item]

    def ratio(self, x, y):
        lst = []
        improv_x = ceil((x/100)*len(self.lst))
        improv_y = math.floor(((100-y)/100)*len(self.lst))
        # print(x, y, improv_x, improv_y)

        val = self.inorder_aux(self.lst.root, improv_y, lst)
        # print(val)
        self.counter = 0
        # print(val)
        # print(self.counter, "nh")
        # print(val[improv_x:], self.lst.length, improv_x, improv_y)

        return val[improv_x:]

    def inorder_aux(self, current: T, ini_k, lst):
        """
        Actual in-order traversal of the tree
        """
        if current is not None:  # if not a base case
            # print("up")
            val = self.inorder_aux(current.left, ini_k, lst)

            if val is None:
                self.counter += 1
                if self.counter <= ini_k:
                    # print("counter")
                    lst.append(current.item)
                    # print(lst)
                if self.counter == ini_k:
                    # print("in")
                    return lst
            else:
                return val

            val = self.inorder_aux(current.right, ini_k, lst)

            if val is not None:
                return val


if __name__ == "__main__":
    points = list(range(50))
    import random
    random.shuffle(points)
    p = Percentiles()
    for point in points:
        p.add_point(point)
    # Numbers from 8 to 16.
    print(sorted(points), len(points))
    print(p.ratio(15, 66))
