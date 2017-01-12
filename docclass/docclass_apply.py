#!/usr/bin/python
# coding: utf-8

"""
    Author: YuJun
    Email: cuteuy@gmail.com
    Date created: 2017/1/11
"""

import re
from docclass import FisherClassifier, NaiveBayer


def getwords(doc):
    splitter = re.compile('\\W*')
    words = [s.lower() for s in splitter.split(doc) if 2 < len(s) < 20]
    # 保证重复单词不会多次出现。
    return dict([(w, 1) for w in words])


def sample_data_prepare(obj):
    obj.prepare_data('Nobody owns the water.', 'good')
    obj.prepare_data('the quick rabbit jumps feces', 'good')
    obj.prepare_data('buy pharmaceuticals now', 'bad')
    obj.prepare_data('make quick money at the online casino', 'bad')
    obj.prepare_data('the quick brown fox jumps', 'good')

cl1 = NaiveBayer(getwords)
sample_data_prepare(cl1)
print cl1.classify('the water')


cl2 = FisherClassifier(getwords)
sample_data_prepare(cl2)
cl2.set_minimum('bad', 0.6)
cl2.set_minimum('good', 0.2)
print cl2.classify('quick money', 'unknown')
print cl2.classify('the water', 'unknown')
