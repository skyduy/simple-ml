#!/usr/bin/python
# coding: utf-8

"""
    Author: YuJun
    Email: cuteuy@gmail.com
    Date created: 2017/1/10
"""


from math import sqrt
import random


# Tanimoto系数 交集与并集的比率
# 当数据只有0 1而不是单词组成时，欧几里德距离或者皮尔逊相关度便不再适用与相似度测量了
def tanimoto(v1, v2):
    c1, c2, shr = 0, 0, 0
    for i in range(len(v1)):
        if v1[i] != 0:
            c1 += 1
        if v2[i] != 0:
            c2 += 1
        if v1[i] != 0 and v2[i] != 0:
            shr += 1
    return 1.0 - (float(shr)/(c1+c2-shr))


# 皮尔逊相关度
def pearson(v1, v2):
    """
    皮尔逊相关度在数组上的实现
    :param v1: 向量1
    :param v2: 向量2
    :return: 两向量相似度
    """

    # 偏好求和
    sum1 = sum(v1)
    sum2 = sum(v2)

    # 求平方和
    sum1_sq = sum([pow(v, 2) for v in v1])
    sum2_sq = sum([pow(v, 2) for v in v2])

    # 求乘积之和
    sum_p = sum(v1[i]*v2[i] for i in range(len(v1)))

    # 计算皮尔逊评价值
    num = sum_p - (sum1*sum2/len(v1))
    den = sqrt((sum1_sq - pow(sum1, 2)/len(v1))*(sum2_sq - pow(sum2, 2)/len(v1)))
    if den == 0:
        return 0

    return 1 - num/den


# k-means算法
def k_means_cluster(rows, distance=pearson, k=4):
    # 每个维度上可出现的最大最小值
    ranges = [(min(row[i] for row in rows), max(row[i] for row in rows)) for i in range(len(rows[0]))]
    clusters = [[random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0] for i in range(len(rows[0]))]
                for _ in range(k)]

    last_matches = None
    for t in range(100):
        print 'Iteration %d' % t
        best_matches = [[] for _ in range(k)]

        # 进行k-means聚类
        for j in range(len(rows)):
            row = rows[j]
            best_match = 0
            for i in range(k):
                d = distance(clusters[i], row)
                if d < distance(clusters[best_match], row):
                    best_match = i
            best_matches[best_match].append(j)

        if best_matches == last_matches:
            break
        last_matches = best_matches

        # 寻找中心点
        for i in range(k):
            avgs = [0.0]*len(rows[0])
            if len(best_matches[i]) > 0:
                for row_id in best_matches[i]:
                    for m in range(len(rows[row_id])):
                        avgs[m] += rows[row_id][m]
                for j in range(len(avgs)):
                    avgs[j] /= len(best_matches[i])
                clusters[i] = avgs

    return last_matches


# 根据“真实距离”映射到二维空间上，以待可视化
def scale_down(data, distance=pearson, rate=0.01, max_iter=1000):
    """
    :param data:  待映射数据
    :param distance:  “真实距离”计算法方法
    :param rate:  移动步伐
    :param max_iter:  最大移动次数
    :return:  二维空间下的data坐标
    """
    n = len(data)
    # 每一对数据之间的的皮尔逊相关系数，即“真实聚类”
    real_dist = [[distance(data[i], data[j]) for j in range(n)] for i in range(n)]

    # 随机初始化节点在二维空间中的启示距离
    loc = [[random.random(), random.random()] for _ in range(n)]
    fake_dist = [[0.0 for _ in range(n)] for _ in range(n)]

    last_error = None
    for m in range(max_iter):
        # 计算当前情形下二维空间中的“虚假距离”
        for i in range(n):
            for j in range(n):
                fake_dist[i][j] = sqrt(
                    sum([pow(loc[i][x]-loc[j][x], 2) for x in range(len(loc[i]))])  # 这里的len(loc[i])就是2
                )
        # 待移动距离，借鉴梯度下降思想
        grad = [[0.0, 0.0] for _ in range(n)]

        total_error = 0
        for k in range(n):
            for j in range(n):
                if k == j:
                    continue
                # 误差值为目标距离与当前距离之间差值的百分比
                error_term = (fake_dist[j][k]-real_dist[j][k])/real_dist[j][k]

                # 根据误差的多少，按比例进行移动
                grad[k][0] += ((loc[k][0]-loc[j][0])/fake_dist[j][k])*error_term
                grad[k][1] += ((loc[k][1]-loc[j][1])/fake_dist[j][k])*error_term

                total_error += abs(error_term)
        print total_error

        if last_error and last_error < total_error:
            break
        last_error = total_error

        # 开始移动
        for k in range(n):
            loc[k][0] -= rate*grad[k][0]
            loc[k][1] -= rate*grad[k][1]

    return loc
