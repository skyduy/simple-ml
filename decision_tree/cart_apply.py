#!/usr/bin/python
# coding: utf-8

"""
    Author: YuJun
    Email: cuteuy@gmail.com
    Date created: 2017/1/11
"""
from cart import build_tree
from cart import gini_impurity, entropy

my_data = [
    ['slashdot', 'USA', 'yes', 18, 'None'],
    ['google', 'France', 'yes', 23, 'Premium'],
    ['digg', 'USA', 'yes', 24, 'Basic'],
    ['kiwitobes', 'France', 'yes', 23, 'Basic'],
    ['google', 'UK', 'no', 21, 'Premium'],
    ['(direct)', 'New Zealand', 'no', 12, 'None'],
    ['(direct)', 'UK', 'no', 21, 'Basic'],
    ['google', 'USA', 'no', 24, 'Premium'],
    ['slashdot', 'France', 'yes', 19, 'None'],
    ['digg', 'USA', 'no', 18, 'None'],
    ['google', 'UK', 'no', 18, 'None'],
    ['kiwitobes', 'UK', 'no', 19, 'None'],
    ['digg', 'New Zealand', 'yes', 12, 'Basic'],
    ['slashdot', 'UK', 'no', 21, 'None'],
    ['google', 'UK', 'yes', 18, 'Basic'],
    ['kiwitobes', 'France', 'yes', 19, 'Basic']
]

r = build_tree(my_data)
r.show_as_txt()
r.save_as_picture()
