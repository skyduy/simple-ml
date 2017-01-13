# coding: utf-8
"""
先验算法
"""


def load_data():
    return [
        [1, 3, 4],
        [2, 3, 5],
        [1, 2, 3, 5],
        [2, 5],
    ]


def create_items(data):
    items = []
    for transaction in data:
        for item in transaction:
            if [item] not in items:
                items.append([item])
    items.sort()
    return map(frozenset, items)


def get_strong_data(data, candidates, min_support):
    candidate_cnt = {}
    for one in data:
        for item in candidates:
            if item.issubset(one):
                candidate_cnt.setdefault(item, 0)
                candidate_cnt[item] += 1
    num_items = float(len(data))
    rest_list = []
    support_data = {}
    for key in candidate_cnt:
        support = candidate_cnt[key]/num_items
        if support >= min_support:
            rest_list.insert(0, key)
        support_data[key] = support
    return rest_list, support_data


def generate_posterity(strong_data, size):
    rest_list = []
    length = len(strong_data)
    for i in range(length):
        for j in range(i+1, length):
            list1 = list(strong_data[i])[:size-2]
            list2 = list(strong_data[j])[:size-2]
            list1.sort()
            list2.sort()
            if list1 == list2:
                rest_list.append(strong_data[i] | strong_data[j])
    return rest_list


def apriori(data_set, min_support=0.5):
    items = create_items(data_set)
    data = map(set, data_set)
    strong_data, support_data = get_strong_data(data, items, min_support)
    all_data = [strong_data]
    size = 2
    while len(all_data[size-2]) > 0:
        posterity = generate_posterity(all_data[size-2], size)
        new_strong_data, new_support_data = get_strong_data(data, posterity, min_support)
        support_data.update(new_support_data)
        all_data.append(new_strong_data)
        size += 1
    return all_data, support_data


def generate_rules(all_data, support_data, min_conf):
    big_rule_list = []
    for i in range(1, len(all_data)):
        for freq_set in all_data[i]:
            h1 = [frozenset([item]) for item in freq_set]
            if i > 1:
                rules_from_set_item(freq_set, h1, support_data, big_rule_list, min_conf)
            else:
                calc_conf(freq_set, h1, support_data, big_rule_list, min_conf)
    return big_rule_list


def calc_conf(freq_set, h, support_data, br1, min_conf=0.7):
    pruned_h = []
    for set_item in h:
        conf = support_data[freq_set]/support_data[freq_set-set_item]
        if conf >= min_conf:
            print freq_set-set_item, '-->', set_item, 'conf:', conf
            br1.append((freq_set-set_item, set_item, conf))
            pruned_h.append(set_item)
    return pruned_h


def rules_from_set_item(freq_set, h, support_data, br1, min_conf=0.7):
    m = len(h[0])   # m = 1
    if len(freq_set) > m+1:  # > 2
        hmp1 = generate_posterity(h, m+1)
        hmp1 = calc_conf(freq_set, hmp1, support_data, br1, min_conf)
        if len(hmp1) > 1:
            rules_from_set_item(freq_set, hmp1, support_data, br1, min_conf)


if __name__ == '__main__':
    a, b = apriori(load_data())
    generate_rules(a, b, 0.1)
