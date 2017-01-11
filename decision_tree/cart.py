#!/usr/bin/python
# coding: utf-8

"""
    Author: YuJun
    Email: cuteuy@gmail.com
    Date created: 2017/1/11
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Classification and Regression Tree
"""

from PIL import Image, ImageDraw


class DecisionTree(object):
    def __init__(self, col=-1, value=None, results=None, tb=None, fb=None):
        self.col = col  # 待检验的判断条件对应索索引值
        self.value = value
        self.results = results
        self.tb = tb
        self.fb = fb

    def get_width(self):
        if self.tb is None and self.fb is None:
            return 1
        return self.tb.get_width()+self.fb.get_width()

    def get_depth(self):
        if self.tb is None and self.fb is None:
            return 0
        return max(self.tb.get_depth(), self.fb.get_depth()) + 1

    def save_as_picture(self, pic_name='tree.jpg'):
        def draw_node(draw, tree, x, y):
            if tree.results is None:
                w1 = tree.fb.get_width() * 100
                w2 = tree.tb.get_width() * 100

                left = x - (w1 + w2) / 2
                right = x + (w1 + w2) / 2

                draw.text((x - 20, y - 10), str(tree.col) + ':' + str(tree.value), (0, 0, 0))
                draw.line((x, y, left + w1 / 2, y + 100), fill=(255, 0, 0))
                draw.line((x, y, right - w2 / 2, y + 100), fill=(255, 0, 0))

                draw_node(draw, tree.fb, left + w1 / 2, y + 100)
                draw_node(draw, tree.tb, right - w2 / 2, y + 100)
            else:
                txt = '\n'.join(['%s:%d' % v for v in tree.results.items()])
                draw.text((x - 20, y), txt, (0, 0, 0))

        w = self.get_width() * 100
        h = self.get_depth() * 100 + 120

        img = Image.new('RGB', (w, h), (255, 255, 255))
        draw_proto = ImageDraw.Draw(img)
        draw_node(draw_proto, self, w / 2, 20)
        img.save(pic_name, 'JPEG')

    def show_as_txt(self, indent=''):
        if self.results is not None:
            print str(self.results)
        else:
            print str(self.col) + ':' + str(self.value) + '? '

            print indent + 'T->',
            self.tb.show_as_txt(indent + '  ')
            print indent + 'F->',
            self.fb.show_as_txt(indent + '  ')


def unique_counts(rows):
    results = {}
    for row in rows:
        r = row[len(row)-1]
        results.setdefault(r, 0)
        results[r] += 1
    return results


def gini_impurity(rows):
    """
    基尼不纯度：如果集合中的每一项都属于同一分类，推测结果总是正确，此时误差度为0
    """
    total = len(rows)
    counts = unique_counts(rows)
    imp = 0
    for k1 in counts:
        p1 = float(counts[k1])/total
        for k2 in counts:
            if k1 == k2:
                continue
            p2 = float(counts[k2])/total
            imp += p1*p2
    return imp


def entropy(rows):
    """
    熵， 评价集合纯度，同基尼不纯度达到峰值速度更慢
    """
    from math import log
    results = unique_counts(rows)
    ent = 0.0
    for r in results.keys():
        p = float(results[r])/len(rows)
        ent -= p*(lambda x: log(x)/log(2))(p)
    return ent


def get_variance(rows):
    """
    用于判断匪类结果为数字类型时的“纯度”
    """
    if len(rows) == 0:
        return 0
    data = [float(row[len(row)-1]) for row in rows]
    mean = sum(data)/len(data)
    variance = sum([(d-mean)**2 for d in data])/len(data)
    return variance


def divide_set(rows, column, value):
    if isinstance(value, int) or isinstance(value, float):
        sf = lambda row: row[column] >= value
    else:
        sf = lambda row: row[column] == value
    set1 = [term for term in rows if sf(term)]
    set2 = [term for term in rows if not sf(term)]

    return set1, set2


# 贪婪方法建造树
def build_tree(rows, score_func=entropy):
    if len(rows) == 0:
        return DecisionTree()
    current_score = score_func(rows)

    best_gain = 0.0
    best_criteria = None
    best_sets = None

    column_count = len(rows[0])-1
    for col in range(0, column_count):
        for row in rows:
            set1, set2 = divide_set(rows, col, row[col])
            p = float(len(set1))/len(rows)
            gain = current_score - p*score_func(set1) - (1-p)*score_func(set2)
            if gain > best_gain and len(set1) > 0 and len(set2) > 0:
                best_gain = gain
                best_criteria = col, row[col]
                best_sets = set1, set2

    if best_gain > 0:
        true_branch = build_tree(best_sets[0])
        false_branch = build_tree(best_sets[1])
        return DecisionTree(col=best_criteria[0], value=best_criteria[1],
                            tb=true_branch, fb=false_branch)
    else:
        return DecisionTree(results=unique_counts(rows))


# 对建造好的树进行剪枝，防止过拟合
def prune(tree, min_gain):
    if tree.tb.results is None:
        prune(tree.tb, min_gain)
    if tree.fb.results is None:
        prune(tree.fb, min_gain)

    if tree.tb.results is not None and tree.tb is not None:
        tb, fb = [], []
        for v, c in tree.tb.results.items():
            tb += [[v]] * c
        for v, c in tree.fb.results.items():
            fb += [[v]] * c

        delta = entropy(tb + fb) - (entropy(tb) + entropy(fb)) / 2
        if delta < min_gain:
            tree.tb, tree.fb = None, None
            tree.results = unique_counts(tb + fb)


# 对新结果进行预测
def classify(observation, tree):
    if tree.results is not None:
        return tree.results
    else:
        v = observation[tree.col]
        if isinstance(v, int) or isinstance(v, float):
            if v >= tree.value:
                branch = tree.tb
            else:
                branch = tree.fb
        else:
            if v == tree.value:
                branch = tree.tb
            else:
                branch = tree.fb

    return classify(observation, branch)


# 对缺失部分数据的新结果预测
def md_classify(observation, tree):
    if tree.results is not None:
        return tree.results
    else:
        v = observation[tree.col]
        if v is None:
            tr = md_classify(observation, tree.tb)
            fr = md_classify(observation, tree.fb)
            true_count = sum(tr.values())
            false_count = sum(fr.values())
            tw = float(true_count)/(true_count+false_count)
            fw = float(false_count)/(true_count+false_count)
            result = {}
            for k, v in tr.items():
                result[k] = v*tw
            for k, v in fr.items():
                if k not in result:
                    result[k] = 0
                    result[k] += v*fw
            return result
        else:
            if isinstance(v, int) or isinstance(v, float):
                if v >= tree.value:
                    branch = tree.tb
                else:
                    branch = tree.fb
            else:
                if v == tree.value:
                    branch = tree.tb
                else:
                    branch = tree.fb

    return md_classify(observation, branch)
