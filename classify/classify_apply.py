#!/usr/bin/python
# coding: utf-8

"""
    Author: YuJun
    Email: cuteuy@gmail.com
    Date created: 2017/1/12
"""
from pylab import plot, show
from classify import linear_classify, nl_classify, get_offset


class MatchRow(object):
    def __init__(self, row, age_only=False):
        if age_only:
            self.data = [row[0], row[5]]
        else:
            self.data = row[0: len(row)-1]
        self.match = int(row[len(row)-1])


def load_match(fn, age_only=False):
    rows = []
    with open(fn, 'r') as f:
        for line in f:
            rows.append(MatchRow(line.split(','), age_only))
    return rows


def plot_age_matches(rows):
    xdm, ydm = [r.data[0] for r in rows if r.match == 1], [r.data[1] for r in rows if r.match == 1]
    xdn, ydn = [r.data[0] for r in rows if r.match == 0], [r.data[1] for r in rows if r.match == 0]

    plot(xdm, ydm, 'bo')
    plot(xdn, ydn, 'b+')
    show()


def process_data(old_rows):
    # yes no 转换为-1, 1, 0
    def yesno(v):
        if v == 'yes':
            return 1
        elif v == 'no':
            return -1
        else:
            return 0

    # 兴趣匹配
    def match_count(interest1, interest2):
        l1 = interest1.split(':')
        l2 = interest2.split(':')
        x = 0
        for v in l1:
            if v in l2:
                x += 1
        return x

    # 根据所在地获取实际距离
    def miles_distance(location1, location2):
        return 0
        # latitude_dif = 69.1 * (location1[0]-location2[0])   # 纬度距离差
        # longitude_dif = 53.0 * (location1[1]-location2[1])  # 经度距离差
        # return (latitude_dif**2+longitude_dif**2)**.5

    def normalize(rows):
        low = [999999999.0] * len(rows[0].data)
        high = [-9999999999.0] * len(rows[0].data)
        for r in rows:
            d_ = r.data
            for i in range(len(d_)):
                if d_[i] < low[i]:
                    low[i] = d_[i]
                if d_[i] > high[i]:
                    high[i] = d_[i]

        def scale_input(row_item):
            return [(row_item[j] - low[j]) * 1.0 / (high[j] - low[j]) if high[j] != low[j]
                    else 0 for j in range(len(row_item))]
        normalized = [MatchRow(scale_input(r.data) + [r.match]) for r in rows]

        return normalized

    new_rows = []
    for row in old_rows:
        d = row.data
        data = [float(d[0]), yesno(d[1]), yesno(d[2]), float(d[5]), yesno(d[6]), yesno(d[7]),
                match_count(d[3], d[8]), miles_distance(d[4], d[9]), row.match]
        new_rows.append(MatchRow(data))
    # return new_rows
    return normalize(new_rows)


if __name__ == '__main__':
    # # ----------------------
    # age_only_data = load_match('matchmaker.csv', age_only=True)
    # print age_only_data[0].data
    # print linear_classify([31, 33], age_only_data)
    # print linear_classify([48, 20], age_only_data)
    # plot_age_matches(age_only_data)

    # # ----------------------
    # raw_data = load_match('matchmaker.csv')
    # scale_set = process_data(raw_data)
    # print linear_classify(scale_set[11].data, scale_set)
    # print scale_set[11].match
    # print
    # print linear_classify([48, 20], scale_set)

    # ----------------------
    raw_data = load_match('matchmaker.csv')
    scale_set = process_data(raw_data)
    offset = get_offset(scale_set)
    print nl_classify(scale_set[11].data, scale_set, offset)
    print scale_set[11].match
    print
    print nl_classify([48, 20], scale_set, offset)
