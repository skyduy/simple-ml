#!/usr/bin/python
# coding: utf-8

"""
    Author: YuJun
    Email: cuteuy@gmail.com
    Date created: 2017/1/10
"""
from similarity import sim_distance, sim_pearson


# 为评论者打相似度分
def get_top_matches(preferences, person, n=5, similarity=sim_pearson):
    scores = [(similarity(preferences, person, other), other) for other in preferences if other != person]

    scores.sort()
    scores.reverse()
    return scores[0:n]
 

# 基于用户相似集，向用户推荐物品
def get_recommendations(preferences, person, similarity=sim_pearson):
    """
    若person为人，则得出该人最可能喜欢的物品
    若person为物，则得出最可能喜欢该物品的人
    """
    totals = {}
    sim_sums = {}
    for other in preferences:
        if other == person:
            continue
        sim = similarity(preferences, person, other)
        if sim <= 0:
            continue
        for item in preferences[other]:
            if item not in preferences[person] or preferences[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += preferences[other][item]*sim
                sim_sums.setdefault(item, 0)
                sim_sums[item] += sim
    rankings = [(total/sim_sums[item], item) for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings


# 工具：反转字典：评价者，被评价物交换
def transform_preferences(pres):
    result = {}
    for person in pres:
        for item in pres[person]:
            result.setdefault(item, {})
            result[item][person] = pres[person][item]
    return result


# 寻找相似物品
def calculate_similar_items(preferences, n=10):
    result = {}

    item_preferences = transform_preferences(preferences)
    c = 0
    for item in item_preferences:
        # 进度统计
        c += 1
        if c % 100 == 0:
            print "%d / %d" % (c, len(item_preferences))
        # 汇总所有
        scores = get_top_matches(item_preferences, item, n=n, similarity=sim_distance)
        result[item] = scores
    return result


# 基于物品相似集，向用户推荐物品
def get_recommend_items(preferences, matched_items, user):
    """
    :param preferences: 用户为key的偏好集
    :param matched_items: 已经构建好的物品相似集
    :param user: 要被推荐的用户 
    """
    user_rating = preferences[user]
    scores = {}
    total_sim = {}

    for (item, rating) in user_rating.items():
        for (similarity, item2) in matched_items[item]:
            if item2 in user_rating:
                continue
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating

            total_sim.setdefault(item2, 0)
            total_sim[item2] += similarity
    rankings = [(scores/total_sim[item], item) for item, scores in scores.items()]

    rankings.sort()
    rankings.reverse()
    return rankings


if __name__ == '__main__':
    # 嵌套字典。用户偏好，用户为key，偏好为value
    # value中，被评价物品为key,评价分数为value
    critics = {
        'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                      'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 'The Night Listener': 3.0},
        'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 'Just My Luck': 1.5,
                         'Superman Returns': 5.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 3.5},
        'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0, 'Superman Returns': 3.5,
                             'The Night Listener': 4.0},
        'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 'The Night Listener': 4.5,
                         'Superman Returns': 4.0, 'You, Me and Dupree': 2.5},
        'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'Just My Luck': 2.0,
                         'Superman Returns': 3.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 2.0},
        'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'The Night Listener': 3.0,
                          'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
        'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}
    }
    print get_top_matches(critics, 'Lisa Rose')

    print get_recommendations(critics, 'Toby')
    print get_recommendations(critics, 'Toby', similarity=sim_distance)

    items = calculate_similar_items(critics)

    print get_recommend_items(critics, items, 'Toby')
