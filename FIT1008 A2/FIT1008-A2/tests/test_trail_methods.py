import unittest
from ed_utils.decorators import number

from mountain import Mountain
from trail import Trail, TrailSeries, TrailSplit, TrailStore

class TestTrailMethods(unittest.TestCase):

    def load_example(self):
        self.top_top = Mountain("top-top", 5, 3)
        self.top_bot = Mountain("top-bot", 3, 5)
        self.top_mid = Mountain("top-mid", 4, 7)
        self.bot_one = Mountain("bot-one", 2, 5)
        self.bot_two = Mountain("bot-two", 0, 0)
        self.final   = Mountain("final", 4, 4)
        self.trail = Trail(TrailSplit(
            Trail(TrailSplit(
                Trail(TrailSeries(self.top_top, Trail(None))),
                Trail(TrailSeries(self.top_bot, Trail(None))),
                Trail(TrailSeries(self.top_mid, Trail(None))),
            )),
            Trail(TrailSeries(self.bot_one, Trail(TrailSplit(
                Trail(TrailSeries(self.bot_two, Trail(None))),
                Trail(None),
                Trail(None),
            )))),
            Trail(TrailSeries(self.final, Trail(None)))
        ))

    @number("7.1")
    def test_example(self):
        self.load_example()

        # print(self.trail.collect_all_mountains())

        res = self.trail.length_k_paths(3)

        print("")
        print(res)
        print(len(res))
        # raise KeyError

        make_path_string = lambda mountain_list: ", ".join(map(lambda x: x.name, mountain_list))
        # This makes the result a list of strings, like so:
        # [
        #   "top-top, top-middle, final",
        #   "top-bot, top-middle, final",
        #   "bot-one, bot-two, final"
        # ]

        res = list(map(make_path_string, res))

        self.assertSetEqual(set(res), {
            "top-top, top-mid, final",
            "top-bot, top-mid, final",
            "bot-one, bot-two, final"
        })
        self.assertEqual(len(res), 3)


        res = self.trail.collect_all_mountains()

        hash_mountain = lambda m: m.name

        self.assertEqual(len(res), 6)
        self.assertSetEqual(set(map(hash_mountain, res)), set(map(hash_mountain, [
            self.top_bot, self.top_top, self.top_mid,
            self.bot_one, self.bot_two, self.final
        ])))






# import unittest
# from ed_utils.decorators import number
#
# from mountain import Mountain
# from trail import Trail, TrailSeries, TrailSplit, TrailStore
#
# class TestTrailMethods(unittest.TestCase):
#
#     def load_example2(self):
#         self.top_top = Mountain("top-top", 5, 3)
#         self.top_bot = Mountain("top-bot", 3, 5)
#         self.top_mid = Mountain("top-mid", 4, 7)
#         self.bot_one = Mountain("bot-one", 2, 5)
#         self.bot_two = Mountain("bot-two", 0, 0)
#         self.final   = Mountain("final", 4, 4)
#         self.top_top_top = Mountain("top_top_top", 2, 5)
#         self.top_top_bot = Mountain("top_top_bot", 2, 5)
#         self.top_top_mid = Mountain("top_top_mid", 2, 5)
#
#         self.final_top = Mountain("final_top", 2, 5)
#         self.final_bot = Mountain("final_bot", 2, 5)
#         self.final_mid = Mountain("final_mid", 2, 5)
#
#         self.trail = Trail(TrailSplit(
#             Trail(TrailSplit(
#                 Trail(TrailSplit(
#                 Trail(TrailSeries(self.top_top_top, Trail(None))),
#                 Trail(TrailSeries(self.top_top_bot, Trail(None))),
#                 Trail(TrailSeries(self.top_top_mid, Trail(None))),
#             )),
#                 Trail(TrailSeries(self.top_bot, Trail(None))),
#                 Trail(TrailSeries(self.top_mid, Trail(None))),
#             )),
#             Trail(TrailSeries(self.bot_one, Trail(TrailSplit(
#                 Trail(TrailSeries(self.bot_two, Trail(None))),
#                 Trail(None),
#                 Trail(None),
#             )))),
#             Trail(TrailSeries(self.final, Trail(TrailSplit(
#                 Trail(TrailSeries(self.final_top, Trail(None))),
#                 Trail(TrailSeries(self.final_bot, Trail(None))),
#                 Trail(TrailSeries(self.final_mid, Trail(None))),
#             ))))
#         ))
#
#     @number("7.2")
#     def test_example2(self):
#         self.load_example2()
#
#         # print(self.trail.collect_all_mountains())
#
#         res = self.trail.length_k_paths(3)
#         print("")
#         print(res)
#         print(len(res))
#         raise KeyError

