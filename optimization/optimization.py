#!/usr/bin/python
# coding: utf-8

"""
    Author: YuJun
    Email: cuteuy@gmail.com
    Date created: 2017/1/10
"""


import random
import math


def random_optimize(domain, cos_fuc):
    best = 999999999
    best_random = None
    for i in range(1000):
        r = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
        cost = cos_fuc(r)
        if cost < best:
            best = cost
            best_random = r

    return best_random, best


def hill_climb(domain, cost_func):
    sol = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]

    while 1:
        neighbors = []
        for j in range(len(domain)):
            if sol[j] > domain[j][0]:
                neighbors.append(sol[0:j] + [sol[j]-1] + sol[j+1:])
            if sol[j] < domain[j][1]:
                neighbors.append(sol[0:j] + [sol[j]+1] + sol[j+1:])
        current = cost_func(sol)
        best = current
        for j in range(len(neighbors)):
            cost = cost_func(neighbors[j])
            if cost < best:
                best = cost
                sol = neighbors[j]
        if best == current:
            break

    return sol, best


def annealing_optimize(domain, cost_fuc, t=10000.0, cool=0.95, step=1):
    vec = [float(random.randint(domain[i][0], domain[i][1])) for i in range(len(domain))]

    while t > 0.001:
        i = random.randint(0, len(domain)-1)

        direction = random.randint(-step, step)

        new_vec = vec[:]
        new_vec[i] += direction
        if new_vec[i] < domain[i][0]:
            new_vec[i] = domain[i][0]
        elif new_vec[i] > domain[i][1]:
            new_vec[i] = domain[i][1]

        cost = cost_fuc(vec)
        new_cost = cost_fuc(new_vec)

        # 这里 pow(math.e, -(new_cost-cost)/t) 为模拟火的概率
        # 若new_cost > cost 的话，如果t很高，比较能接收new_cost
        # 随着t的降低，比较能接受较小的new_cost
        # 随着t更低，逐渐不能接受高的new_cost
        if new_cost < cost or random.random() < pow(math.e, -(new_cost-cost)/t):
            vec = new_vec

        t *= cool

    return vec, cost_fuc(vec)


def genetic_optimize(domain, cost_func, pop_size=50, step=1, mut_prob=0.2, elite=0.2, max_iter=100):

    def mutate(old_vec):
        index = random.randint(0, len(domain)-1)
        direction = random.randint(-step, step)
        new_vec = old_vec[:]
        new_vec[index] += direction
        if new_vec[index] < domain[index][0]:
            new_vec[index] = domain[index][0]
        elif new_vec[index] > domain[index][1]:
            new_vec[index] = domain[index][1]
        return new_vec

    def crossover(r1, r2):
        index = random.randint(1, len(domain)-2)
        return r1[0:index] + r2[index:]

    pop = []
    for i in range(pop_size):
        vec = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
        pop.append(vec)

    top_elite = int(elite*pop_size)

    scores = [()]
    for i in range(max_iter):
        scores = [(cost_func(v), v) for v in pop]
        scores.sort()
        ranked = [v for(s, v) in scores]

        pop = ranked[0:top_elite]

        while len(pop) < pop_size:
            if random.random() < mut_prob:
                c = random.randint(0, top_elite)
                new_member = mutate(ranked[c])
                pop.append(new_member)  # 这里是从存存活下来的里面变异来的
            else:
                c1 = random.randint(0, top_elite)
                c2 = random.randint(0, top_elite)
                new_member = crossover(ranked[c1], ranked[c2])
                pop.append(new_member)

        # print scores[0][0]

    return scores[0][1], scores[0][0]

