#!/usr/bin/python
# coding: utf-8

"""
    Author: YuJun
    Email: cuteuy@gmail.com
    Date created: 2017/1/11
"""
from random import random, randint
from pylab import arange, array, plot, show
from prediction import cross_validate, weighted_knn, knn_estimate, gaussian, prob_guess, prob_graph
from optimization.optimization import random_optimize, genetic_optimize, annealing_optimize, hill_climb


def wine_price(rating, age):
    """
    根据等级和酿酒时间生成葡萄酒的价格
    """
    peak_age = rating - 50
    price = rating / 2
    if age > peak_age:
        price *= (5 - (age - peak_age) / 2)
    else:
        price *= (5 * ((age + 1) / peak_age))
    if price < 0:
        price = 0
    return price


def wine_set1():
    rows = []
    for _ in range(300):
        rating = random() * 50 + 50
        age = random() * 50
        price = wine_price(rating, age)
        price *= (random() * 0.2 + 0.9)
        rows.append({'input': (rating, age), 'result': price})
    return rows


def wine_set2():
    rows = []
    for i in range(300):
        rating = random()*50 + 50
        age = random()*50
        aisle = float(randint(1, 20))
        bottles_size = [375.0, 750.0, 1500.0, 3000.0][randint(0, 3)]
        price = wine_price(rating, age)
        price *= (bottles_size/750)
        price *= (random()*0.2 + 0.9)
        rows.append({'input': (rating, age, aisle, bottles_size), 'result': price})
    return rows


def wine_set3():
    rows = wine_set1()
    for row in rows:
        if random() < 0.5:
            row['result'] *= 0.6
    return rows


# 特征缩放
def rescale(data, scale):
    scaled_data = []
    for row in data:
        scaled = [scale[i]*row['input'][i] for i in range(len(scale))]
        scaled_data.append({'input': scaled, 'result': row['result']})
    return scaled_data


# 针对缩放向量构造代价函数，后通过交叉验证方式训练并获取合适的缩放比例
def create_cost_func(alg_func, data):
    def cost_func(scale):
        scaled_data = rescale(data, scale)
        return cross_validate(alg_func, scaled_data, trials=10)
    return cost_func


# -----------------------------------------


# data1 = wine_set1()
# print weighted_knn(data1, (99, 5))
# print cross_validate(weighted_knn, data1)


data2 = wine_set2()
cost_f = create_cost_func(weighted_knn, data2)
weight_domain = [(0, 20)] * 4
scale_weight, cost = genetic_optimize(weight_domain, cost_f, pop_size=5, max_iter=20)
print scale_weight, cost


# data3 = wine_set3()
# prob_graph(data3, [99, 20], 120)
