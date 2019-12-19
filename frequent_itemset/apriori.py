# coding: utf-8
"""
先验算法
"""
import collections


def load_data():
    data_set = [
        [1, 2, 3, 4],
        [1, 2, 4, 5],
        [1, 3, 4, 5],
    ]
    return {frozenset(i) for i in data_set}


class Apriori:
    def __init__(self, data=None):
        if data is None:
            self.data = load_data()
        else:
            self.data = data
        self.num_items = len(self.data)
        self.one_itemset = {frozenset({i}) for transaction in self.data for i in transaction}

    def filter_supported(self, candidates, min_support):
        candidate_cnt = collections.Counter()
        for each in self.data:
            for item in candidates:
                if item.issubset(each):
                    candidate_cnt[item] += 1

        pivot = min_support * self.num_items
        prompted, kicked = [], []
        for itemset, count in candidate_cnt.items():
            if count >= pivot:
                prompted.append(itemset)
            else:
                kicked.append(itemset)

        return prompted, kicked

    def generate_next(self, prompted, kicked):
        res = set()
        next_k = len(prompted[0]) + 1
        for i, a in enumerate(prompted):
            for b in prompted[i + 1:]:
                merged = a | b
                if len(merged) == next_k:
                    ok = True
                    for each in kicked:
                        if each.issubset(merged):
                            ok = False
                            break
                    if ok:
                        res.add(merged)
        return res

    def apriori(self, min_support=0.5):
        res = list()
        candidate = self.one_itemset
        while candidate:
            prompted, kicked = self.filter_supported(candidate, min_support)
            print('{}\n{}\n{}\n\n'.format(candidate, prompted, kicked))
            if not prompted:
                break
            res.append(prompted)
            candidate = self.generate_next(prompted, kicked)

        return res


if __name__ == '__main__':
    aaa = Apriori()
    for iii in aaa.apriori():
        print(iii)
