#!/usr/bin/python
# coding: utf-8

"""
    Author: YuJun
    Email: cuteuy@gmail.com
    Date created: 2017/1/12
"""
import math


# 基于点乘，体现哪个离均值点进
def linear_classify(point, rows):
    def get_avg(all_rows):
        averages = {}
        counts = {}
        for row in all_rows:
            cl = row.match
            averages.setdefault(cl, [0.0]*len(row.data))
            counts.setdefault(cl, 0)

            for i in range(len(row.data)):
                averages[cl][i] += float(row.data[i])
            counts[cl] += 1
        for cl, average in averages.items():
            for i in range(len(average)):
                average[i] /= counts[cl]
        return averages

    def dot_product(v1, v2):
        return sum([v1[i]*v2[i] for i in range(len(v1))])

    # 这里先求所有点的平均位置，之后再点积一次比较距离，实际效果是求该点与两类别的所有点的点积平均，进而得知该点与哪个类别更近。
    # ★ 这样做的目的是简化运算，仅需一次点积计算。  与使用核函数分类时引入核技法达到的效果类似（均简化运算）。
    avg = get_avg(rows)
    b = (dot_product(avg[1], avg[1])-dot_product(avg[0], avg[0]))/2
    y = dot_product(point, avg[0])-dot_product(point, avg[1]) + b
    if y > 0:
        return 0
    else:
        return 1


# -------------------------------------------
# 直观求“距离”，并完成分类。引入核技法后，会简化运算。核技法是数学中巧合的黑魔法。

# 核函数：径向基函数radial-basis function, 其值随距离减小，并介于0（极限）和1（当v1 = v2的时候）之间
def rbf(v1, v2, gamma=20):
    dv = [v1[i]-v2[i] for i in range(len(v1))]
    the_sum = sum([term**2 for term in dv])
    return math.e**(-gamma*the_sum)


# dot(X, M0)-dot(X, M1) + (dot(M1, M1)-dot(M0, M0))/2)
# 提取出后一项，目的重用数据，因为该部分与位置点无关。
def get_offset(rows, gamma=10):
    l0 = []
    l1 = []
    for row in rows:
        if row.match == 0:
            l0.append(row.data)
        else:
            l1.append(row.data)
    sum0 = sum(sum([rbf(v1, v2, gamma) for v1 in l0]) for v2 in l0)
    sum1 = sum(sum([rbf(v1, v2, gamma) for v1 in l1]) for v2 in l1)

    return (1.0/(len(l1)**2))*sum1 - (1.0/(len(l0)**2))*sum0


def nl_classify(point, rows, offset, gamma=10):
    sum0 = 0.0
    sum1 = 0.0
    count0 = 0
    count1 = 0

    for row in rows:
        if row.match == 0:
            sum0 += rbf(point, row.data, gamma)
            count0 += 1
        else:
            sum1 += rbf(point, row.data, gamma)
            count1 += 1
    y = (1.0/count0)*sum0 - (1.0/count1)*sum1 + offset
    if y > 0:
        return 0
    else:
        return 1
