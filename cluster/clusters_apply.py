#!/usr/bin/python
# coding: utf-8

"""
    Author: YuJun
    Email: cuteuy@gmail.com
    Date created: 2017/1/10
"""
from PIL import Image, ImageDraw
from clusters import pearson, k_means_cluster, scale_down


# 聚类节点单位
class ClusterNode(object):
    def __init__(self, vec, left=None, right=None, distance=0.0, node_id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = node_id
        self.distance = distance


# 进行聚类
def generate_cluster(rows, distance=pearson):
    distances = {}
    current_node_id = -1

    nodes = [ClusterNode(rows[i], node_id=i) for i in range(len(rows))]

    while len(nodes) > 1:
        lowest_pair = (0, 1)
        closest = distance(nodes[0].vec, nodes[1].vec)

        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                if (nodes[i].id, nodes[j].id) not in distances:
                    distances[(nodes[i].id, nodes[j].id)] = distance(nodes[i].vec, nodes[j].vec)
                d = distances[(nodes[i].id, nodes[j].id)]
                if d < closest:
                    closest = d
                    lowest_pair = (i, j)
        merge_vec = [(nodes[lowest_pair[0]].vec[i] + nodes[lowest_pair[1]].vec[i])/2.0
                     for i in range(len(nodes[0].vec))]

        new_node = ClusterNode(merge_vec, left=nodes[lowest_pair[0]],
                               right=nodes[lowest_pair[1]], distance=closest, node_id=current_node_id)

        current_node_id -= 1
        del nodes[lowest_pair[1]]
        del nodes[lowest_pair[0]]
        nodes.append(new_node)

    return nodes[0]


# 打印出聚类结果
def print_clusters(node, labels=None, n=0):
    for i in range(n):
        print ' ',
    if node.id < 0:
        print '-'
    else:
        if labels is None:
            print node.id
        else:
            print labels[node.id]

    if node.left is not None:
        print_clusters(node.left, labels=labels, n=n + 1)
    if node.right is not None:
        print_clusters(node.right, labels=labels, n=n + 1)


# 工具：二维数据反转，目的实现基于单词的聚类
def rotate_matrix(data):
    new_data = []
    for i in range(len(data[0])):
        new_row = [data[j][i] for j in range(len(data))]
        new_data.append(new_row)
    return new_data


# 工具：绘制二维图片
def draw_2d(data, labels, jpeg='distance.jpg'):
    img = Image.new('RGB', (400, 400), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    for i in range(len(data)):
        x = (data[i][0]+0.5)*100
        y = (data[i][1]+0.5)*100
        draw.text((x, y), labels[i], (0, 0, 0))
    img.save(jpeg, 'JPEG')


# 工具：准备数据
def prepare_data(filename):
    lines = [line for line in file(filename)]

    # First line is the column titles
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        # First column in each row is the rowname
        rownames.append(p[0])
        # The data for this row is the remainder of the row
        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data

if __name__ == "__main__":
    blog_names, words, data = prepare_data('blogdata.txt')
    # # 行为单位聚类，即针对文章聚类
    # cluster = generate_cluster(data)
    # print_clusters(cluster, blog_names)

    # # 列为单位聚类，即针对单词聚类
    # rev_data = rotate_matrix(data)
    # cluster = generate_cluster(rev_data)
    # print_clusters(cluster, words)

    # # k-means聚类
    # k_clust = k_means_cluster(data, k=4)
    # print k_clust

    loc = scale_down(data, rate=0.01)
    draw_2d(loc, blog_names)
