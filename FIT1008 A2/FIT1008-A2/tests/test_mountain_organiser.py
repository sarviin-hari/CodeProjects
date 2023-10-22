# import unittest
# from ed_utils.decorators import number
#
# from mountain import Mountain
# from mountain_organiser import MountainOrganiser
#
# class TestInfiniteHash(unittest.TestCase):
#
#     @number("6.1")
#     def test_example(self):
#         m1 = Mountain("m1", 2, 2)
#         m2 = Mountain("m2", 2, 9)
#         m3 = Mountain("m3", 3, 6)
#         m4 = Mountain("m4", 3, 1)
#         m5 = Mountain("m5", 4, 6)
#         m6 = Mountain("m6", 7, 3)
#         m7 = Mountain("m7", 7, 7)
#         m8 = Mountain("m8", 7, 8)
#         m9 = Mountain("m9", 7, 6)
#         m10 = Mountain("m10", 8, 4)
#
#         mo = MountainOrganiser()
#         mo.add_mountains([m1, m2])
#         print("####22##################################################################33")
#         # print(mo.m_list[str(m1.length), m1.name])
#
#         # raise KeyError
#
#         # # raise KeyError
#         # print(mo.m_list, mo.m_l_n)
#         # print("ENDOFNAERA#########################################################################################")
#         # mo.add_mountains([m4, m3])
#         # # print(mo.mountain_list)
#         # print(mo.m_list, mo.m_l_n)
#
#         # raise KeyError
#
#         print("#########################################################################################")
#         self.assertEqual([mo.cur_position(m) for m in [m1, m2]], [0, 1])
#         # raise KeyError
#         mo.add_mountains([m4, m3])
#         # print(mo.mountain_list)
#         # raise KeyError
#
#         self.assertEqual([mo.cur_position(m) for m in [m1, m2, m3, m4]], [1, 3, 2, 0])
#         # raise KeyError
#         print("#########################################################################################")
#         mo.add_mountains([m5])
#         print(mo.mountain_list)
#         # raise KeyError
#
#         self.assertEqual([mo.cur_position(m) for m in [m1, m2, m3, m4, m5]], [1, 4, 2, 0, 3])
#         print("#########################################################################################")
#         print("Adds 4 mountains in")
#         mo.name = 1
#         mo.add_mountains([m7, m9, m6, m8])
#         print(mo.mountain_list)
#
#         self.assertEqual([mo.cur_position(m) for m in [m1, m2, m3, m4, m5, m6, m7, m8, m9]], [1, 8, 3, 0, 4, 2, 6, 7, 5])
#         print("#########################################################################################")
#         # print(mo.cur_position(m10))
#         # raise KeyError
#
#         self.assertRaises(KeyError, lambda: mo.cur_position(m10))


import unittest
from ed_utils.decorators import number

from mountain import Mountain
from mountain_organiser import MountainOrganiser

class TestInfiniteHash(unittest.TestCase):

    @number("6.1")
    def test_example(self):
        m1 = Mountain("m1", 2, 2)
        m2 = Mountain("m2", 2, 9)
        m3 = Mountain("m3", 3, 6)
        m4 = Mountain("m4", 3, 1)
        m5 = Mountain("m5", 4, 6)
        m6 = Mountain("m6", 7, 3)
        m7 = Mountain("m7", 7, 7)
        m8 = Mountain("m8", 7, 8)
        m9 = Mountain("m9", 7, 6)
        m10 = Mountain("m10", 8, 4)

        mo = MountainOrganiser()
        mo.add_mountains([m1, m2])
        # mo.add_mountains([m3, m4])

        # mo.add_mountains([m1, m2,m4,m3,m9,m6])


        self.assertEqual([mo.cur_position(m) for m in [m1, m2]], [0, 1])
        mo.add_mountains([m4, m3])

        self.assertEqual([mo.cur_position(m) for m in [m1, m2, m3, m4]], [1, 3, 2, 0])
        mo.add_mountains([m5])
        self.assertEqual([mo.cur_position(m) for m in [m1, m2, m3, m4, m5]], [1, 4, 2, 0, 3])
        mo.add_mountains([m7, m9, m6, m8])
        self.assertEqual([mo.cur_position(m) for m in [m1, m2, m3, m4, m5, m6, m7, m8, m9]], [1, 8, 3, 0, 4, 2, 6, 7, 5])
        # raise KeyError
        # mo.add_mountains([m10])
        # print(mo.cur_position(m10))
        # print(mo.initial_mountain_tuple)

        self.assertRaises(KeyError, lambda: mo.cur_position(m10))