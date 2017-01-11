#!/usr/bin/python
# coding: utf-8

"""
    Author: YuJun
    Email: cuteuy@gmail.com
    Date created: 2017/1/11
"""

import math
from random import random


def enclidean(v1, v2):
    d = 0.0
    for i in range(len(v1)):
        d += (v1[i]-v2[i])**2
    return math.sqrt(d)


def get_distances(data, vec1):
    distance_list = []
    for i in range(len(data)):
        vec2 = data[i]['input']
        distance_list.append((enclidean(vec1, vec2), i))
    distance_list.sort()
    return distance_list


# knn估计
def knn_estimate(data, vec1, k=5):
    distance_list = get_distances(data, vec1)
    avg = 0.0
    for i in range(k):
        idx = distance_list[i][1]
        avg += data[idx]['result']
    avg /= k
    return avg


# 带权knn估计
def inverse_weight(dist, num=1.0, const=0.1):
    return num/(dist+const)


def subtract_weight(dist, const=1.0):
    if dist > const:
        return 0
    else:
        return const - dist


def gaussian(dist, sigma=10.0):
    return math.e**(-dist**2/(2*sigma**2))


def weighted_knn(data, vec1, k=5, weight_func=gaussian):
    distance_list = get_distances(data, vec1)
    avg = 0.0
    total_weight = 0.0

    for i in range(k):
        dist = distance_list[i][0]
        idx = distance_list[i][1]
        weight = weight_func(dist)
        avg += weight*data[idx]['result']
        total_weight += weight
    avg /= total_weight
    return avg


# 分割数据、交叉验证
def divide_data(data, test_rate=0.05):
    train_set = []
    test_set = []
    for row in data:
        if random() < test_rate:
            test_set.append(row)
        else:
            train_set.append(row)
    return train_set, test_set


def test_algorithm(alg_func, train_set, test_set):
    error = 0.0
    for row in test_set:
        guess = alg_func(train_set, row['input'])
        error += (row['result']-guess)**2
    return error/len(test_set)


def cross_validate(alg_func, data, trials=100, test_rate=0.05):
    error = 0.0
    for i in range(trials):
        train_set, test_set = divide_data(data, test_rate)
        error += test_algorithm(alg_func, train_set, test_set)
    return error/trials


# 判断价格落入某一区间的概率
def prob_guess(data, vec1, low, high, k=5, weight_func=gaussian):
    distance_list = get_distances(data, vec1)
    new_weight = 0.0
    total_weight = 0.0

    for i in range(k):
        distance = distance_list[i][0]
        idx = distance_list[i][1]
        weight = weight_func(distance)
        v = data[idx]['result']
        if low <= v <= high:
            new_weight += weight
        total_weight += weight
    if total_weight == 0:
        return 0
    return new_weight/total_weight


# 概率可视化
def prob_graph(data, vec1, high, k=5, weight_func=gaussian, sigma=5.0):
    t1 = arange(0.0, high, 0.1)
    probabilities = [prob_guess(data, vec1, v, v+0.1, k, weight_func) for v in t1]
    smoothed = []
    for i in range(len(probabilities)):
        sv = 0.0
        for j in range(0, len(probabilities)):
            dist = abs(i-j)*0.1
            weight = gaussian(dist, sigma=sigma)
            sv += weight*probabilities[j]
        smoothed.append(sv)
    smoothed = array(smoothed)
    plot(t1, smoothed)
    show()
