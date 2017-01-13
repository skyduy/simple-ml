#!/usr/bin/python
# coding: utf-8

"""
    Author: YuJun
    Email: cuteuy@gmail.com
    Date created: 2017/1/12
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    非负矩阵因式分解：
    (PCA/SVD亦可提取特征，二者应用场景不同)

    以文章和单词为例举例:
    articles = ['A', 'B', 'C', 'D']
    words = ['act', 'boy', 'cat', 'dog', 'eat']
    matrix = [
            cat boy cat dog eat
        A   [3  0   1   2   5]
        B   [1  2   0   3   2]
        C   [0  0   2   1   5]
        D   [3  1   0   1   3]
    ]
    表示act 在 A B C D 文章中分别出现了 3 1 0 3 次
    也表示C文章出现的这五个单词的次数分别为0 0 2 1 5

    分解之后：

    特征矩阵：
    [               单词act               单词boy           单词cat           单词dog           单词eat
    特征1    [  5.86067486e-01,    2.37269094e-15,   2.38865489e+00,   9.81993764e-01,   6.59576170e+00],
    特征2    [  1.84027199e+00,   8.55530859e-01,   3.86863356e-13,    1.49822638e+00,   1.55053582e+00]
    ]
    即由四个原本特征（四个单词），构造成两个新的特征。（降维作用）

    权重矩阵：
    [       特征1         特征2
    文章A    [ 0.48519836,  1.14573763],
    文章B    [ 0.03786622,  1.21365218],
    文章C    [ 0.76607513,  0.00279523],
    文章D    [ 0.14288861,  1.21719325]
    ]
    这里面便是两个新的特征在各文章中的权重。

    如果分解后的特征数量与文章数量刚好相等，
    那么最理想的情况就是为每篇文章都找到一个与之完美匹配的特征（即权重矩阵中，每行只有一个正数，其它均为0）


    之所以称之为非负，因为返回的特征和权重均为非负，意思是无法从某些特征中去掉其他一部分特征，形成新特征。
"""
import numpy as np


def dif_cost(m1, m2):
    """
    :type m1: np.matrix
    :type m2: np.matrix
    :return:    差的平方和
    """
    r = np.asarray(m1-m2)
    return np.sum(r**2)


def factorize(v, pc=10, max_iter=50):
    """
    :type v:    np.matrix
    :param v:   原矩阵
    :param pc:  要被拆分成的新的特征的数量
    :param max_iter:    最大迭代次数
    :returns:   权重矩阵，特征矩阵

    非负矩阵因式分解 Non-Negative Matrix Factorization 最优解

    hn  转置后的权重矩阵*数据矩阵
    hd  转置后的权重矩阵*原权重矩阵*特征矩阵
    wn  数据矩阵*转置后的特征矩阵
    wd  权重矩阵*特征矩阵*转置后的特征矩阵
    """
    (ic, fc) = np.shape(v)  # (文章数, 单词数)

    # 随机选择权重矩阵 和 特征矩阵
    w = np.matrix([[np.random.random() for _ in range(pc)] for _ in range(ic)])
    h = np.matrix([[np.random.random() for _ in range(fc)] for _ in range(pc)])

    for i in range(max_iter):
        wh = w*h
        cost = dif_cost(v, wh)
        if i % 10 == 0:
            print cost
        if cost == 0:
            break
        hn = (np.transpose(w)*v)
        hd = (np.transpose(w)*w*h)
        h = np.matrix(np.asarray(h)*np.asarray(hn)/np.asarray(hd))

        wn = (v*np.transpose(h))
        wd = (w*h*np.transpose(h))
        w = np.matrix(np.array(w)*np.array(wn)/np.array(wd))

    return w, h
