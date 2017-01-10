#!/usr/bin/python
# coding: utf-8

"""
    Author: YuJun
    Email: cuteuy@gmail.com
    Date created: 2017/1/10
"""
from __future__ import unicode_literals
import time
import math
from PIL import Image, ImageDraw
from optimization import annealing_optimize, genetic_optimize, random_optimize, hill_climb


def task_flight():
    """
    优化算法应用于航班选择。
    """

    # 名字和出发地
    people = [
        ('Seymour', 'BOS'),
        ('Franny', 'DAL'),
        ('Zooey', 'CAK'),
        ('Walt', 'MIA'),
        ('Buddy', 'ORD'),
        ('Les', 'OMA')
    ]

    # 目的地
    destination = 'LGA'

    # 航班
    flights = {}
    for line in file('schedule.txt'):
        # 起点，终点，起飞时间，到达时间，价格
        origin, dest, depart, arrive, price = line.strip().split(',')
        flights.setdefault((origin, dest), [])

        flights[(origin, dest)].append((depart, arrive, int(price)))


    def get_minutes(t):
        x = time.strptime(t, '%H:%M')
        # [year, month, day, hour, min, sec, ...]
        return x[3] * 60 + x[4]


    def print_schedule(r):
        for d in range(len(r)/2):
            name = people[d][0]
            origin = people[d][1]
            out = flights[(origin, destination)][int(r[2*d])]
            ret = flights[(destination, origin)][int(r[2*d+1])]
            print '%10s%10s %5s-%5s $%3s %5s-%5s $%3s' % (
                name, origin, out[0], out[1], out[2], ret[0], ret[1], ret[2]
            )


    def schedule_cost(sol):
        total_price = 0
        latest_arrival = 0
        earliest_dep = 24 * 60

        for d in range(len(sol)/2):
            origin = people[d][1]
            outbound = flights[(origin, destination)][int(sol[2*d])]
            return_flight = flights[(destination, origin)][int(sol[2*d+1])]

            # 计算总金额
            total_price += outbound[2]
            total_price += return_flight[2]

            # 记录最晚到达时间和最早离开时间
            if latest_arrival < get_minutes(outbound[1]):
                latest_arrival = get_minutes(outbound[1])
            if earliest_dep > get_minutes(return_flight[0]):
                earliest_dep = get_minutes(return_flight[0])

        # 从某人到达 至 所有人到齐前 均为等待时间
        # 从第一个人离开 至 某人离开前 均为等待时间
        total_wait = 0
        for d in range(len(sol)/2):
            origin = people[d][1]
            outbound = flights[(origin, destination)][int(sol[2*d])]
            return_flight = flights[(destination, origin)][int(sol[2*d+1])]
            total_wait += latest_arrival - get_minutes(outbound[1])
            total_wait += get_minutes(return_flight[0]) - earliest_dep

        # 若最早离开时间比最迟到达时间小（早），则说明过了一天，那么汽车租费需要增加
        if latest_arrival > earliest_dep:
            total_price += 50

        return total_price + total_wait

    domain = [(0, 9) for _ in range(len(people)*2)]

    s, c = random_optimize(domain, schedule_cost)
    print '随机搜索优化算法 总花费: %d，行程如下' % c
    print_schedule(s)

    s, c = hill_climb(domain, schedule_cost)
    print '\n爬山法优化算法 总花费: %d，行程如下' % c
    print_schedule(s)

    s, c = annealing_optimize(domain, schedule_cost)
    print '\n模拟退火优化算法 总花费: %d，行程如下' % c
    print_schedule(s)

    s, c = genetic_optimize(domain, schedule_cost)
    print '\n遗传算法优化 总花费: %d，行程如下' % c
    print_schedule(s)


def task_draw_social_network():
    people = ['Charlie', 'Augustus', 'Veruca', 'Violet', 'Mike', 'Joe', 'Willy', 'Miranda']
    links = [
        ('Augustus', 'Willy'), ('Mike', 'Joe'), ('Miranda', 'Mike'), ('Violet', 'Augustus'), ('Miranda', 'Willy'),
        ('Charlie', 'Mike'), ('Veruca', 'Joe'), ('Miranda', 'Augustus'), ('Willy', 'Augustus'), ('Joe', 'Charlie'),
        ('Veruca', 'Augustus'), ('Miranda', 'Joe')
    ]

    def cross_cost(v):
        loc = dict([(people[i], (v[i*2], v[i*2 + 1])) for i in range(0, len(people))])
        total = 0

        # 交叉判罚
        for i in range(len(links)):
            for j in range(i+1, len(links)):
                (x1, y1), (x2, y2) = loc[links[i][0]], loc[links[i][1]]
                (x3, y3), (x4, y4) = loc[links[j][0]], loc[links[j][1]]

                # 下面判断是否两条线 交叉
                den = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
                if den == 0:
                    continue
                ua = float((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / den
                ub = float((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / den
                if 0 < ua < 1 and 0 < ub < 1:
                    total += 1

        # 距离判罚
        for i in range(len(people)):
            for j in range(i+1, len(people)):
                (x1, y1), (x2, y2) = loc[people[i]], loc[people[j]]
                distance = math.sqrt(math.pow(x1-x2, 2) + math.pow(y1-y2, 2))
                if distance < 50:
                    total += (1.0 - (distance/50.0))

        return total

    def draw_network(sol, img_name):
        img = Image.new('RGB', (400, 400), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        pos = dict([(people[i], (sol[i * 2], sol[i * 2 + 1])) for i in range(0, len(people))])
        for a, b in links:
            draw.line((pos[a], pos[b]), fill=(255, 0, 0))

        for n, p in pos.items():
            draw.text(p, n, (0, 0, 0))

        img.save(img_name, 'JPEG')

    domain = [(10, 390)] * len(people) * 2

    pos1, cost1 = random_optimize(domain, cross_cost)
    pos2, cost2 = genetic_optimize(domain, cross_cost)
    pos3, cost3 = hill_climb(domain, cross_cost)
    pos4, cost4 = annealing_optimize(domain, cross_cost)

    print cost4
    draw_network(pos4, 'social_network/annealing.jpg')

    print cost2
    draw_network(pos2, 'social_network/genetic.jpg')

    print cost3
    draw_network(pos3, 'social_network/hill.jpg')

    print cost1
    draw_network(pos1, 'social_network/random.jpg')


if __name__ == '__main__':
    # task_flight()
    task_draw_social_network()
