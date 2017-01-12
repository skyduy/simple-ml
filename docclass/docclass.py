#!/usr/bin/python
# coding: utf-8

"""
    Author: YuJun
    Email: cuteuy@gmail.com
    Date created: 2017/1/11
"""

import math


# 分类器总特征
class Classifier(object):
    # 以文章分类为例进行解释。
    def __init__(self, get_features):
        self.features_count = {}    # {'python': {'bad': 0, 'good': 6}, 'the':{'bad': 3, 'good': 3}} 统计每个单词的特征
        self.cat_count = {}         # {'bad': 1, 'good': 1} 这个统计的是分类中的文章数量
        self.get_features = get_features  # 接收从给定item中获取特征，即从句子中获取各单词

    # 将某个特征添加到某个分类中
    def increase_features(self, feature, cat):
        self.features_count.setdefault(feature, {})
        self.features_count[feature].setdefault(cat, 0)
        self.features_count[feature][cat] += 1

    # 增加对某一分类的计数值
    def increase_cat(self, cat):
        self.cat_count.setdefault(cat, 0)
        self.cat_count[cat] += 1

    # 获取某个特性中，某个分类所占个数。即某个特性出现在某个分类中的次数
    def get_feature_count(self, feature, cat):
        if feature in self.features_count and cat in self.features_count[feature]:
            return float(self.features_count[feature][cat])
        return 0

    # 获取某个分类的总数
    def get_cat_count(self, cat):
        if cat in self.cat_count:
            return float(self.cat_count[cat])
        return 0

    # 所有内容项的数量（及所有单词的总数）
    def total_count(self):
        return sum(self.cat_count.values())

    # 所有分类的列表（即所有单词组成的列表）
    def categories(self):
        return self.cat_count.keys()

    # 数据准备
    def prepare_data(self, item, cat):
        features = self.get_features(item)  # 这里不会重复添加单词
        for feature in features:  # features为字典时，遍历的时key
            self.increase_features(feature, cat)
        self.increase_cat(cat)

    # 特征在分类中出项的总次数 / 分类中包含内容项的总数  （数量的概率）
    def feature_prob(self, feature, cat):
        if self.get_cat_count(cat) == 0:
            return 0
        return self.get_feature_count(feature, cat)/self.get_cat_count(cat)

    # 优化并得到最终结果：指定分类中，某单词占据比重
    def weighted_prob(self, feature, cat, feature_prob, weight=1.0, ap=0.5):
        basic_prob = feature_prob(feature, cat)
        # 计算特征在所有分类中出现的次数
        totals = sum([self.get_feature_count(feature, cat) for cat in self.categories()])
        bp = (weight*ap + totals*basic_prob)/(weight + totals)
        return bp


# 朴素贝叶斯分类器
class NaiveBayer(Classifier):
    def __init__(self, get_features):
        Classifier.__init__(self, get_features)
        self.thresholds = {}

    # 利用全概率公式，得到句子出现在某分类中的比重
    def doc_prob(self, item, cat):
        features = self.get_features(item)
        p = 1
        for feature in features:
            p *= self.weighted_prob(feature, cat, self.feature_prob)
        return p

    # 贝叶斯定理此处应用：
    # 知 a.在各指定类别中，各个文章出现的概率（条件概率1）b.所有分类的概率 c.文章的概率。求 指定文章下某分类的概率
    def prob(self, item, cat):
        cat_prob = self.get_cat_count(cat)/self.total_count()
        doc_prob = self.doc_prob(item, cat)
        return cat_prob*doc_prob

    def set_threshold(self, cat, t):
        self.thresholds[cat] = t

    def get_threshold(self, cat):
        if cat not in self.thresholds:
            return 1.0
        return self.thresholds[cat]

    def classify(self, item, default=None):
        possibility = {}
        max_prob = 0.0
        best = default
        for cat in self.categories():
            possibility[cat] = self.prob(item, cat)
            if possibility[cat] > max_prob:
                max_prob = possibility[cat]
                best = cat

        for cat in possibility:
            if cat == best:
                continue
            # 只有最合适的分类概率高于其它的三倍，才可行。
            if possibility[cat]*self.get_threshold(best) > possibility[best]:
                return default
        return best


class FisherClassifier(Classifier):

    def __init__(self, get_features):
        Classifier.__init__(self, get_features)
        self.minimums = {}

    def set_minimum(self, cat, minimum):
        self.minimums[cat] = minimum

    def get_minimum(self, cat):
        if cat not in self.minimums:
            return 0
        return self.minimums[cat]

    # feature_prob的进化版本 （概率的概率）
    def feature_in_cat_prob(self, feature, cat):
        # 特征在该分类中出现的概率
        feature_prob = self.feature_prob(feature, cat)
        if feature_prob == 0:
            return 0
        # 特征在所有分类中出现的概率
        freq_sum = sum([self.feature_prob(feature, cat) for cat in self.categories()])
        # 给定某特征，属于某分类的概率
        p = feature_prob/freq_sum
        return p

    def fisher_prob(self, item, cat):
        p = 1
        features = self.get_features(item)
        for feature in features:
            p *= (self.weighted_prob(feature, cat, self.feature_in_cat_prob))

    # --------下面的没搞懂-------------
        fscore = -2*math.log(p)
        return self.invchi2(fscore, len(features)*2)

    # 倒置对数卡方函数
    def invchi2(selfself, chi, df):
        m = chi / 2.0
        the_sum = term = math.exp(-m)
        for i in range(1, df//2):
            term *= m / i
            the_sum += term
        return min(the_sum, 1.0)
    # --------------------------------

    def classify(self, item, default=None):
        best = default
        max_prob = 0.0
        for cat in self.categories():
            p = self.fisher_prob(item, cat)
            if p > self.get_minimum(cat) and p > max_prob:
                best = cat
                max_prob = p
        return best, max_prob
