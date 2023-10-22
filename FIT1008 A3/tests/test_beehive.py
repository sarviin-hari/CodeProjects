import unittest
from ed_utils.decorators import number, visibility
from ed_utils.timeout import timeout

from beehive import BeehiveSelector, Beehive

class TestBeehiveSelector(unittest.TestCase):

    @timeout()
    @number("5.1")
    def test_simple(self):
        s = BeehiveSelector(5)

        b1, b2, b3, b4, b5 = (
            Beehive(15, 12, 13, capacity=40, nutrient_factor=5, volume=15),
            Beehive(25, 22, 23, capacity=15, nutrient_factor=8, volume=40),
            Beehive(35, 32, 33, capacity=40, nutrient_factor=3, volume=40),
            Beehive(45, 42, 43, capacity=1, nutrient_factor=85, volume=10),
            Beehive(55, 52, 53, capacity=400, nutrient_factor=5000, volume=0),
        )
        for hive in [b1, b2, b3, b4, b5]:
            s.add_beehive(hive)

        # l2 = [Beehive(2, 56, 12, capacity=67, nutrient_factor=5, volume=17),
        #       Beehive(45, 3, 15, capacity=69, nutrient_factor=5, volume=10),
        #       Beehive(52, 85, 1, capacity=45, nutrient_factor=3, volume=26),
        #       Beehive(45, 3, 15, capacity=400, nutrient_factor=9, volume=32),
        #       Beehive(45, 3, 15, capacity=60, nutrient_factor=2, volume=32)]
        # s.set_all_beehives(l2)
        #
        # for i in s.hive.the_array:
        #     print(i)
        # raise KeyError
        
        all_emeralds = []
        for i in range(15):
            all_emeralds.append(s.harvest_best_beehive())
            # if i == 3:
            #     raise KeyError
        # print(all_emeralds)
        # raise KeyError
        expected = [
            # Choices are:
            120, # Beehive b2 or b3
            120, # Beehive b2 or b3
            120, # Beehive b2
            # Now, b3 has volume 0 and b2 has volume 10
            85, # Pick b4 10 times
            85,
            85,
            85,
            85,
            85,
            85,
            85,
            85,
            85,
            80, # b2
            75, # b1
        ]
        self.assertEqual(len(all_emeralds), len(expected))
        for actual, ex in zip(all_emeralds, expected):
            self.assertAlmostEqual(actual, ex, 0)


        
