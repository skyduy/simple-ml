#!/usr/bin/python
# coding: utf-8

"""
    Author: YuJun
    Email: cuteuy@gmail.com
    Date created: 2017/1/13
"""

from gp import example_tree, build_hidden_set, get_rank_func, evolve
from gp import tournament, grid_game, HumanPlayer
# node = example_tree()
# print node.evaluate([1, 3])
#
# rank_fun = get_rank_func(build_hidden_set())
# evolve(2, 500, rank_fun, mutation_rate=0.2, breeding_rate=0.1, prob_exp=0.7, prob_new=0.1)

winner = evolve(5, 100, tournament, 50)
grid_game([winner, HumanPlayer()])
