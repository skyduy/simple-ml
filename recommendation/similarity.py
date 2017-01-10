#!/usr/bin/python
# coding: utf-8

"""
    Author: YuJun
    Email: cuteuy@gmail.com
    Date created: 2017/1/10
"""
from math import sqrt


def sim_distance(preferences, p1, p2):
    """
    欧几里得距离：计算整体相似度
    :param preferences: 兴趣字典 {'user_1': {'hobby_1': 'score_1'}}
    :param p1: 用户1名 user_1
    :param p2: 用户2名 user_2
    :return: 用户兴趣相似度，越相似值越趋向于1
    """
    # 先判断是否有共同兴趣，若无，直接返回0
    si = {}
    for item in preferences[p1]:
        if item in preferences[p2]:
            si[item] = 1
    if len(si) == 0:
        return 0

    # 计算欧几里得距离
    sum_of_squares = sum([pow(preferences[p1][item] - preferences[p2][item], 2)
                          for item in preferences[p1] if item in preferences[p2]])

    # 规范化
    return 1/(1+sum_of_squares)


def sim_pearson(preferences, p1, p2):
    """
    皮尔逊相关度：计算二者对物品喜爱的相关度 （亦即概率论中的相关系数：协方差/标准差 ）
    :param preferences: 兴趣字典 {'user_1': {'hobby_1': 'score_1'}}
    :param p1: 用户1名 user_1
    :param p2: 用户2名 user_2
    :return: 返回值介于-1到1之间，兴趣越相似，越接近于1 兴趣恰好相反，则为-1.
    """
    si = {}
    for item in preferences[p1]:
        if item in preferences[p2]:
            si[item] = 1
    n = len(si)
    # 二者没有相同处时，默认相同处全部相同
    if n == 0:
        return 1

    # 偏好求和
    sum1 = sum([preferences[p1][it] for it in si])
    sum2 = sum([preferences[p2][it] for it in si])

    # 求平方和
    sum1_sq = sum([pow(preferences[p1][it], 2) for it in si])
    sum2_sq = sum([pow(preferences[p2][it], 2) for it in si])

    # 求乘积之和
    sum_p = sum([preferences[p1][it]*preferences[p2][it] for it in si])

    # 计算皮尔逊评价值
    num = sum_p - (sum1*sum2/n)
    den = sqrt((sum1_sq - pow(sum1, 2)/n)*(sum2_sq - pow(sum2, 2)/n))
    if den == 0:
        return 0

    r = num/den
    return r
