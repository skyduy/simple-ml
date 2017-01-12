#!/usr/bin/python
# coding: utf-8

"""
    Author: YuJun
    Email: cuteuy@gmail.com
    Date created: 2017/1/12
"""

import numpy as np
from nmf import factorize
from word_data_prepare import make_matrix


def ft():
    word_matrix, word_vec, article_titles = make_matrix()
    print 'task begin'
    weight_matrix, feature_matrix = factorize(word_matrix, 30, 300)

    np.savetxt('word_data/weight_matrix.txt', weight_matrix)
    np.savetxt('word_data/feature_matrix.txt', feature_matrix)


def show_result(f_out='word_data/features.txt', a_out='word_data/articles.txt'):
    """
    :param f_out: 文件1的名字，每块第一行表示新特征权重最大的几个单词，后几行在哪几篇文章中权重最大
    :param a_out: 文件2的名字，每块第一行表示文章名，后几行表示组成该文章权重最大的几个特征
    :return:
    """
    word_matrix, wordvec, titles = make_matrix()
    w = np.asmatrix(np.loadtxt('word_data/weight_matrix.txt'))
    h = np.asmatrix(np.loadtxt('word_data/feature_matrix.txt'))
    pc, wc = np.shape(h)
    top_patterns = [[] for _ in range(len(titles))]
    pattern_names = []

    with open(f_out, 'w') as f:
        for i in range(pc):
            slist=[]
            for j in range(wc):
                slist.append((h[i, j], wordvec[j]))
            slist.sort()
            slist.reverse()

            n = [s[1] for s in slist[0:10]]
            f.write(str(n)+'\n')
            pattern_names.append(n)

            flist = []
            for j in range(len(titles)):
                flist.append((w[j, i], titles[j]))
                top_patterns[j].append((w[j, i], i, titles[j]))

            flist.sort()
            flist.reverse()

            for k in flist[0:5]:
                f.write(str(k)+'\n')
            f.write('\n')

    with open(a_out, 'w') as f:
        for j in range(len(titles)):
            f.write(titles[j].encode('utf8')+'\n')

            top_patterns[j].sort()
            top_patterns[j].reverse()

            for i in range(3):
                f.write(str(top_patterns[j][i][0]) + ' ' + str(pattern_names[top_patterns[j][i][1]]) + '\n')
            f.write('\n')


if __name__ == '__main__':
    # ft()
    show_result()




















