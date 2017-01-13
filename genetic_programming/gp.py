#!/usr/bin/python
# coding: utf-8

"""
    Author: YuJun
    Email: cuteuy@gmail.com
    Date created: 2017/1/13
"""

from random import random, randint, choice
from copy import deepcopy
from math import log


class FuncWrapper(object):
    def __init__(self, function, child_count, name):
        self.function = function
        self.child_count = child_count
        self.name = name


class Node(object):
    def __init__(self, fw, children):
        self.function = fw.function
        self.name = fw.name
        self.children = children

    def evaluate(self, inp):
        results = [n.evaluate(inp) for n in self.children]
        return self.function(results)

    def display(self, indent=0):
        print (' '*indent) + self.name
        for c in self.children:
            c.display(indent+1)


class ParamNode(object):
    def __init__(self, idx):
        self.idx = idx

    def evaluate(self, inp):
        return inp[self.idx]

    def display(self, indent=0):
        print '%sp%d' % (' '*indent, self.idx)


class ConstNode:
    def __init__(self, v):
        self.v = v

    def evaluate(self, _):
        return self.v

    def display(self, indent=0):
        print '%s%d' % (' '*indent, self.v)

add_wrapper = FuncWrapper(lambda l: l[0]+l[1], 2, 'add')
sub_wrapper = FuncWrapper(lambda l: l[0]-l[1], 2, 'subtract')
mul_wrapper = FuncWrapper(lambda l: l[0]*l[1], 2, 'multiply')
if_wrapper = FuncWrapper(lambda l: l[1] if l[0] > 0 else l[2], 3, 'if')
gt_wrapper = FuncWrapper(lambda l: 1 if l[0] > l[1] else 0, 2, 'is_greater')
# 还有其他运算。 三角函数，其他数学函数，统计分布，距离度量，三参函数
func_list = [add_wrapper, sub_wrapper, mul_wrapper, if_wrapper, gt_wrapper]


def example_tree():
    return Node(if_wrapper, [
        Node(gt_wrapper, [ParamNode(0), ConstNode(3)]),
        Node(add_wrapper, [ParamNode(1), ConstNode(5)]),
        Node(sub_wrapper, [ParamNode(1), ConstNode(2)]),
    ])


def make_random_tree(pc, max_depth=4, fpr=0.5, ppr=0.6):
    if random() < fpr and max_depth > 0:
        f = choice(func_list)
        children = [make_random_tree(pc, max_depth-1, fpr, ppr) for _ in range(f.child_count)]
        return Node(f, children)
    elif random() < ppr:
        return ParamNode(randint(0, pc-1))
    else:
        return ConstNode(randint(0, 10))


# 实际函数体
def hidden_function(x, y):
    return x**2 + 2*y + 3*x + 5


# 引入数据
def build_hidden_set():
    rows = []
    for i in range(200):
        x = randint(0, 40)
        y = randint(0, 40)
        rows.append([x, y, hidden_function(x, y)])
    return rows


# 代价函数
def score_func(tree, s):
    dif = 0
    for data in s:
        v = tree.evaluate([data[0], data[1]])
        dif += abs(v-data[2])
    return dif


# 变异
def mutate(t, pc, prob_change=0.1):
    if random() < prob_change:
        return make_random_tree(pc)
    else:
        result = deepcopy(t)
        if isinstance(t, Node):
            result.children = [mutate(c, pc, prob_change) for c in t.children]
        return result


# 交叉
def crossover(t1, t2, prob_swap=0.7, top=1):
    if random < prob_swap and not top:
        return deepcopy(t2)
    else:
        result = deepcopy(t1)
        if isinstance(t1, Node) and isinstance(t2, Node):
            result.child = [crossover(c, choice(t2.children), prob_swap, 0) for c in t1.children]
        return result


def get_rank_func(data_set):
    def rank_func(population):
        scores = [(score_func(t, data_set), t) for t in population]
        scores.sort()
        return scores
    return rank_func


def evolve(pc, pop_size, rank_func, max_gen=500,
           mutation_rate=0.1, breeding_rate=0.4, prob_exp=0.7, prob_new=0.05):
    def select_index():
        return int(log(random())/log(prob_exp))

    population = [make_random_tree(pc) for _ in range(pop_size)]
    scores = [()]
    for i in range(max_gen):
        scores = rank_func(population)
        print scores[0][0]
        if scores[0][0] == 0:
            break
        new_pop = [scores[0][1], scores[1][1]]

        while len(new_pop) < pop_size:
            if random() > prob_new:
                new_pop.append(mutate(
                    crossover(
                        scores[select_index()][1],
                        scores[select_index()][1],
                        prob_swap=breeding_rate
                    ),
                    pc,
                    prob_change=mutation_rate
                ))
            else:
                new_pop.append(make_random_tree(pc))
        population = new_pop
    scores[0][1].display()
    return scores[0][1]


# ----------------------------------------


def grid_game(p):
    # 游戏区域大小
    max_area = (3, 3)

    # 每位玩家的上一步移动方向， 0 1 2 3四种方向
    last_move = [-1, -1]

    # 初始化玩家位置
    location = list([[randint(0, max_area[0]), randint(0, max_area[1])]])
    location.append([(location[0][0]+2) % 4, (location[0][1]+2) % 4])

    # 平局前至少需要50步
    for o in range(50):

        # 针对每位玩家
        for i in range(2):
            locations = location[i][:] + location[1-i][:]  # 自身
            locations.append(last_move[i])  # 记录该移动时，二者的位置以及上一次的位移

            # location 最少情况下记忆五个参数，因此调用时参数传递为5
            move = p[i].evaluate(locations) % 4  # 通过上述记录获取下一次的位移

            # 同一方向移动两次，则另一个玩家获胜
            if last_move[i] == move:
                return 1-i
            last_move[i] = move
            if move == 0:
                location[i][0] -= 1
                if location[i][0] < 0:  # 被挤到边上可以弃权
                    location[i][0] = 0
            if move == 1:
                location[i][0] += 1
                if location[i][0] > max_area[0]:
                    location[i][0] = max_area[0]
            if move == 2:
                location[i][1] -= 1
                if location[i][1] < 0:
                    location[i][1] = 0
            if move == 3:
                location[i][1] += 1
                if location[i][1] > max_area[1]:
                    location[i][1] = max_area[1]

            if location[i] == location[1-i]:
                return i

    return -1


def tournament(p1):
    """
    作用是获取get rank function
    """
    losses = [0] * len(p1)
    for i in range(len(p1)):
        for j in range(len(p1)):
            if i == j:
                continue
            winner = grid_game([p1[i], p1[j]])

            if winner == 0:
                losses[j] += 2
            elif winner == 1:
                losses[i] += 2
            else:
                losses[i] += 1
                losses[j] += 1
    z = zip(losses, p1)
    z.sort()
    return z


class HumanPlayer(object):
    def evaluate(self, board):
        me = tuple(board[0:2])
        others = [tuple(board[x:x+2]) for x in range(2, len(board)-1, 2)]

        for i in range(4):
            for j in range(4):
                if (i, j) == me:
                    print 'O',
                elif (i, j) in others:
                    print 'X',
                else:
                    print '.',
            print
        lm = board[len(board) - 1]
        if lm == 0:
            r = 'W'
        elif lm == 1:
            r= 'S'
        elif lm == 2:
            r = 'A'
        elif lm == 3:
            r = 'D'
        else:
            r = '*'
        print 'Your last move was %s' % r
        print '  W'
        print 'A S D'
        print 'Enter move: ',
        move = str(raw_input())
        while move.lower() not in ['w', 'a', 's', 'd']:
            move = str(raw_input('Input wrong, again:'))
        if move == 'w':
            move = 0
        elif move == 'a':
            move = 2
        elif move == 'd':
            move = 3
        else:
            move = 1
        return move
