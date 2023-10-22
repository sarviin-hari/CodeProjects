from __future__ import annotations

from ratio import Percentiles
from threedeebeetree import Point

def make_ordering(my_coordinate_list: list[Point]) -> list[Point]:
    """One possible implementation. There are many."""

    result = []

    if len(my_coordinate_list) <= 17:
        return my_coordinate_list

    a = 1 / 8 * 100

    lst = my_coordinate_list[:]

    def test(check_list, result_list):
        if len(check_list) <= 17:
            return check_list

        hell_x = Percentiles()
        hell_y = Percentiles()
        hell_z = Percentiles()

        # O(n log n)
        for i in check_list:
            hell_x.add_point(i[0])
            hell_y.add_point(i[1])
            hell_z.add_point(i[2])

        # O(log n)
        x_list = hell_x.ratio(a, a)
        y_list = hell_y.ratio(a, a)
        z_list = hell_z.ratio(a, a)

        n_list = []

        # O(n), where n is the number of elem in list
        for i in range(len(check_list)):
            if check_list[i][0] in x_list and check_list[i][1] in y_list and check_list[i][2] in z_list:
                n_list.append(check_list[i])

        # O(1)
        check = n_list.pop()
        result_list.append(check)

        new_l = [[], [], [], [], [], [], [], []]

        # O(n), where n is the number of elements in the current list of possible coordinates
        for i in check_list:
            if i != check:
                x, y, z = check  # Extracts x, y, and z coordinates from the node's key
                x_cmp, y_cmp, z_cmp = i  # Extracts x, y, and z coordinates from the given key
                octant = (x_cmp >= x, y_cmp >= y, z_cmp >= z)  # Determines the octant based on the comparison of coordinates
                octant_index = 4 * octant[0] + 2 * octant[1] + octant[
                    2]  # converts the binary representation of the octant into a decimal value used as the index.
                new_l[octant_index].append(i)

        # O(n), where n is the length of the new_l
        for i in new_l:
            l = test(i, [])
            result_list = result_list + l

        return result_list

    r = test(lst, result)

    return r
