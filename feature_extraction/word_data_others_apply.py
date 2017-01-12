#!/usr/bin/python
# coding: utf-8

"""
    Author: YuJun
    Email: cuteuy@gmail.com
    Date created: 2017/1/12
"""
from __future__ import unicode_literals
import math
import MySQLdb
from word_data_prepare import make_matrix
from cluster.clusters_apply import generate_cluster, print_clusters


class Classifier(object):
    """
    为了持久性保存，引入数据库
    详情见目录docclass
    """
    def __init__(self, get_features):
        self.fc = {}
        self.cc = {}
        self.con = None
        self.db = None
        self.get_features = get_features

    def connect_db(self):
        self.db = MySQLdb.connect('localhost', 'skyduy', 'skyduy', 'words',  charset='utf8')
        self.con = self.db.cursor()
        self.con.execute(
            'create table if not exists fc(feature VARCHAR(500), category VARCHAR(100),count INT) character set = utf8')
        self.con.execute(
            'create table if not exists cc(category VARCHAR(200), count BIGINT) character set = utf8')

    def increase_features(self, feature, cat):
        count = self.feature_count(feature, cat)
        if count == 0:
            self.con.execute('insert into fc values (%s, %s, 1)', (feature, cat))
        else:
            self.con.execute('update fc set count=%s where feature=%s and category=%s', (count+1, feature, cat))

    def increase_cat(self, cat):
        count = self.cat_count(cat)
        if count == 0:
            self.con.execute('insert into cc values (%s, 1)', (cat,))
        else:
            self.con.execute('update cc set count=%s where category=%s', (count+1, cat))

    def feature_count(self, feature, cat):
        self.con.execute('select count from fc where feature=%s and category=%s', (feature, cat))
        res = self.con.fetchone()
        return 0 if res is None else float(res[0])

    def cat_count(self, cat):
        self.con.execute('select count from cc where category=%s', (cat,))
        res = self.con.fetchone()
        return 0 if res is None else float(res[0])

    def total_count(self):
        self.con.execute('select sum(count) from cc')
        res = self.con.fetchone()
        return 0 if res is None else float(res[0])

    def categories(self):
        self.con.execute('select category from cc')
        res = self.con.fetchall()
        return [d[0] for d in res]

    def prepare_data(self, item, cat):
        features = self.get_features(item)
        for feature in features:
            self.increase_features(feature, cat)
        self.increase_cat(cat)
        self.db.commit()

    def feature_prob(self, feature, cat):
        if self.cat_count(cat) == 0:
            return 0
        return self.feature_count(feature, cat) / self.cat_count(cat)

    def weighted_prob(self, feature, cat, feature_prob, weight=1.0, ap=0.5):
        basic_prob = feature_prob(feature, cat)
        totals = sum([self.feature_count(feature, cat) for cat in self.categories()])
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
        cat_prob = self.cat_count(cat) / self.total_count()
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
            if possibility[cat] >= max_prob:
                max_prob = possibility[cat]
                best = cat

        for cat in possibility:
            if cat == best:
                continue
            # 只有最合适的分类概率高于其它的threshold倍，才可行。
            if possibility[cat]*self.get_threshold(best) > possibility[best]:
                return default
        return best


# 费舍尔分类器
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


def apply_bayesian_classify():
    word_matrix, word_vec, article_titles = make_matrix()

    # 某个单词多次出现，仅算作一次
    def get_word(x):
        return [word_vec[w] for w in range(len(x)) if x[w] > 0]

    cls = NaiveBayer(get_word)
    cls.connect_db()
    py_list = []
    android_list = []
    for i in range(len(article_titles)):
        if 'python' in article_titles[i].lower():
            py_list.append(i)
        elif 'android' in article_titles[i].lower():
            android_list.append(i)
    print 'Should be python:'
    for i in py_list:
        if i % 5 == 0:
            print cls.classify(word_matrix[i])
        else:
            cls.prepare_data(word_matrix[i], 'Python')
            pass
    print 'Should be android:'
    for i in android_list:
        if i % 5 == 0:
            print cls.classify(word_matrix[i])
            pass
        else:
            cls.prepare_data(word_matrix[i], 'Android')
            pass


def apply_cluster():
    word_matrix, word_vec, article_titles = make_matrix()
    c = generate_cluster(word_matrix)
    print_clusters(c, article_titles)


if __name__ == '__main__':
    # apply_bayesian_classify()
    apply_cluster()  # very slow
