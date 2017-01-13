#!/usr/bin/python
# coding: utf-8

"""
    Author: YuJun
    Email: cuteuy@gmail.com
    Date created: 2017/1/12
"""

import json
import jieba
import feedparser

feed_list = [
    'http://weishu.me/atom.xml',
    'http://www.race604.com/rss/',
    'http://andrewliu.in/atom.xml',
    'http://waylenw.github.io/atom.xml',
    'http://blog.bihe0832.com/pages/atom.xml',
    'http://yanghui.name/atom.xml',
    'http://www.vmatianyu.cn/feed',
    'http://veaer.com/atom.xml',
    'https://drakeet.me/feed',
    'http://antonioleiva.com/feed/',
    'http://www.androidcentral.com/feed',
    'http://www.kymjs.com/feed.xml',
    'http://droidyue.com/atom.xml',
    'http://hukai.me/atom.xml',
    'https://www.liaohuqiu.net/atom.xml',
    'http://dbanotes.net/feed',
    'http://www.laruence.com/feed',
    'http://trickyandroid.com/rss/',
    'http://androidweekly.cn/rss/',
    'http://www.wklken.me/feed.xml',
    'https://android-arsenal.com/rss.xml',
    'http://blog.jobbole.com/category/android/feed/',
    'http://blog.daimajia.com/rss/',
    'http://beyondvincent.com/atom.xml',
    'http://www.trinea.cn/feed/',
    'http://www.importnew.com/feed',
    'http://blog.codingnow.com/atom.xml',
    'http://www.raychase.net/feed',
    'http://www.ruanyifeng.com/blog/atom.xml',
    'http://coolshell.cn/feed',
]


def strip_html(h):
    p = ''
    s = 0
    for c in h:
        if c == '<':
            s = 1
        elif c == '>':
            s = 0
            p += ' '
        elif s == 0:
            p += c
    return p


def separate_words(text):
    return jieba.cut(text)


def save_article_words():
    unique_all_words = {}
    all_words = {}
    article_words = []
    article_titles = []
    ec = 0
    print len(feed_list)
    for i, feed in enumerate(feed_list):
        f = feedparser.parse(feed)
        # 遍历每篇文章
        for e in f.entries:
            # 跳过标题相同的文章
            if e.title in article_titles:
                continue

            # 提取单词
            txt = e.title.encode('utf8') + strip_html(e.description.encode('utf8'))
            words = separate_words(txt)
            article_words.append({})
            article_titles.append(e.title)
            unique = {}
            # 增加所有文章中的单词统计和每个文章中的单词统计
            for word in words:
                unique.setdefault(word, 1)
                all_words.setdefault(word, 0)
                all_words[word] += 1
                article_words[ec].setdefault(word, 0)
                article_words[ec][word] += 1
            for key in unique:
                unique_all_words.setdefault(key, 0)
                unique_all_words[key] += 1
            ec += 1
        print i,
    with open('data/unique_all_words.json', 'w') as fp:
        json.dump(unique_all_words, fp)
    with open('data/all_words.json', 'w') as fp:
        json.dump(all_words, fp)
    with open('data/article_words.json', 'w') as fp:
        json.dump(article_words, fp)
    with open('data/article_titles.json', 'w') as fp:
        json.dump(article_titles, fp)


def make_matrix():
    with open('data/unique_all_words.json', 'r') as fp:
        allw = json.load(fp)
    with open('data/article_words.json', 'r') as fp:
        articlew = json.load(fp)
    with open('data/article_titles.json', 'r') as fp:
        article_titles = json.load(fp)

    wordvec = []
    # 单词过滤
    for w, c in allw.items():
        if 5 < c < len(articlew)*0.6:
            wordvec.append(w)

    l1 = [[(word in f and f[word] or 0) for word in wordvec] for f in articlew]
    # print len(l1), len(l1[0]), len(wordvec)
    return l1, wordvec, article_titles


if __name__ == '__main__':
    # save_article_words()
    pass
