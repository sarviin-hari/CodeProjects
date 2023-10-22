import unittest
from ed_utils.decorators import number

from double_key_table import DoubleKeyTable

class TestDoubleHash(unittest.TestCase):

    @number("3.1")
    def test_example(self):
        """
        See spec sheet image for clarification.
        """
        # Disable resizing / rehashing.
        dt = DoubleKeyTable(sizes=[12], internal_sizes=[5])
        # print(dt.l1, dt.l2)
        # for i in range(12):
        #     print("Out")
        #     print(dt.external_table[i])
        #     for j in range(5):
        #         print("In")
        #         print(id(dt.external_table[i]))

        dt.hash1 = lambda k: ord(k[0]) % 12
        dt.hash2 = lambda k, sub_table: ord(k[-1]) % 5

        # print(dt.l1)

        dt["Tim", "Jen"] = 1
        dt["Amy", "Ben"] = 2
        dt["May", "Ben"] = 3
        dt["Ivy", "Jen"] = 4
        dt["May", "Tom"] = 5
        dt["Tim", "Bob"] = 6

        # print(dt["Tim", "Jen"] )
        # raise KeyError

        # print(dt)
        # raise KeyError

        print("-----------------------------------------------------------------------------------------------------")

        # for i in range(12):
        #     print(dt.external_table[i], i)
        #     if dt.external_table[i] is not None:
        #         for j in range(5):
        #             print(dt.external_table[i][1], j)

        print("-----------------------------------------------------------------------------------------------------")
        self.assertRaises(KeyError, lambda: dt._linear_probe("May", "Jim", False))
        self.assertEqual(dt._linear_probe("May", "Jim", True), (6, 1))
        dt["May", "Jim"] = 7 # Linear probing on internal table
        self.assertEqual(dt._linear_probe("May", "Jim", False), (6, 1))
        self.assertRaises(KeyError, lambda: dt._linear_probe("Het", "Liz", False))
        self.assertEqual(dt._linear_probe("Het", "Liz", True), (2, 2))
        dt["Het", "Liz"] = 8 # Linear probing on external table
        self.assertEqual(dt._linear_probe("Het", "Liz", False), (2, 2))

    @number("3.2")
    def test_delete(self):
        # Disable resizing / rehashing.
        dt = DoubleKeyTable(sizes=[12], internal_sizes=[5])
        dt.hash1 = lambda k: ord(k[0]) % 12
        dt.hash2 = lambda k, sub_table: ord(k[-1]) % 5

        dt["Tim", "Jen"] = 1
        dt["Amy", "Ben"] = 2
        dt["Tim", "Kat"] = 3
        self.assertEqual(dt._linear_probe("Tim", "Kat", False), (0, 1))
        del dt["Tim", "Jen"]
        # We can't do this as it would create the table.
        # self.assertEqual(dt._linear_probe("Het", "Bob", True), (1, 3))
        del dt["Tim", "Kat"]
        print("\n", "Next Line", "\n")
        # Deleting again should make space for Het.
        # print(dt.external_table[0])
        # print(dt.external_table[1])
        dt["Het", "Bob"] = 4
        print("\n", "Next Line", "\n")
        self.assertEqual(dt._linear_probe("Het", "Bob", False), (0, 3))
        print("\n", "Next Line", "\n")
        self.assertRaises(KeyError, lambda: dt._linear_probe("Tim", "Jen", False))
        print("\n", "Next Line", "\n")
        dt["Tim", "Kat"] = 5
        self.assertEqual(dt._linear_probe("Tim", "Kat", False), (1, 1))

    @number("3.3")
    def test_resize(self):
        dt = DoubleKeyTable(sizes=[3, 5], internal_sizes=[3, 5])
        dt.hash1 = lambda k: ord(k[0]) % dt.table_size
        dt.hash2 = lambda k, sub_table: ord(k[-1]) % sub_table.table_size

        dt["Tim", "Bob"] = 1        # (0, 2)
        # No resizing yet.
        self.assertEqual(dt.table_size, 3)
        self.assertEqual(dt._linear_probe("Tim", "Bob", False), (0, 2))
        dt["Tim", "Jen"] = 2        # (0, 0)
        # Internal resize.
        self.assertEqual(dt.table_size, 3)
        self.assertEqual(dt._linear_probe("Tim", "Bob", False), (0, 3))

        # External resize
        dt["Pip", "Bob"] = 4        # (2, 2)
        self.assertEqual(dt.table_size, 5)
        self.assertEqual(dt._linear_probe("Tim", "Bob", False), (4, 3))
        self.assertEqual(dt._linear_probe("Pip", "Bob", False), (0, 2))

    @number("3.4")
    def test_keys_values(self):
        # Disable resizing / rehashing.
        dt = DoubleKeyTable(sizes=[12], internal_sizes=[5])
        dt.hash1 = lambda k: ord(k[0]) % 12
        dt.hash2 = lambda k, sub_table: ord(k[-1]) % 5

        dt["Tim", "Jen"] = 1
        dt["Amy", "Ben"] = 2
        dt["May", "Ben"] = 3
        dt["Ivy", "Jen"] = 4
        dt["May", "Tom"] = 5
        dt["Tim", "Bob"] = 6
        dt["May", "Jim"] = 7
        dt["Het", "Liz"] = 8

        print("\n", "In dt.keys")
        print(dt.external_table[6][1].count)
        print(dt.hash1("Tim"), dt.hash1("Amy"), dt.hash1("May"), dt.hash1("Ivy"), dt.hash1("Het"))
        self.assertEqual(set(dt.keys()), {"Tim", "Amy", "May", "Ivy", "Het"})
        self.assertEqual(set(dt.keys("May")), {"Ben", "Tom", "Jim"})

        self.assertEqual(set(dt.values()), {1, 2, 3, 4, 5, 6, 7, 8})
        self.assertEqual(set(dt.values("Tim")), {1, 6})

    @number("3.5")
    def test_iters(self):
        # Test that these are actually iterators,
        # and so changing the underlying data structure changes the next value.
        dt = DoubleKeyTable()
        # dt.table_size()
        dt["May", "Jim"] = 1
        dt["Kim", "Tim"] = 2


        print("Start Iterator keys")

        key_iterator = dt.iter_keys()
        # print(next(key_iterator))
        # print(next(key_iterator))
        # print(next(key_iterator))
        # for val in key_iterator:
        #     print(val)
        # raise KeyError
        # print("Start Iterator values")

        value_iterator = dt.iter_values()
        # print(next(value_iterator))
        # print(next(value_iterator))
        # print(next(value_iterator))
        # for val in value_iterator:
        #     print(val)
        # print(dt.external_table[1])
        # raise KeyError


        key = next(key_iterator)
        self.assertIn(key, ["May", "Kim"])
        # key = next(key_iterator)
        # self.assertIn(key, ["Kim", "Tim"])

        value = next(value_iterator)
        self.assertIn(value, [1, 2])

        del dt["May", "Jim"]
        del dt["Kim", "Tim"]
        # print(dt.hash1("May"), dt.hash1("Kim"))
        # raise KeyError
        # Retrieving the next value should either raise StopIteration or crash entirely.
        # Note: Deleting from an element being iterated over is bad practice
        # We just want to make sure you aren't returning a list and are doing this
        # with an iterator.
        self.assertRaises(BaseException, lambda: next(key_iterator))
        self.assertRaises(BaseException, lambda: next(value_iterator))


