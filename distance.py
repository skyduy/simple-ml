import random
import numpy as np
from PIL import Image, ImageDraw
from scipy.stats import pearsonr
from scipy.spatial.distance import euclidean
from sklearn.metrics import jaccard_similarity_score


# 距离：越小越相似
# 集合交 / 集合并
def tanimoto_distance(v1, v2):
    return 1 - jaccard_similarity_score(v1, v2)


# affinity 皮尔逊相关度： 概率论中的 ρ = 变量之间的协方差 / 变量标准差之积
def pearsonr_distance(v1, v2):
    return 1 - pearsonr(v1, v2)[0]


def euclidean_distance(v1, v2):
    return euclidean(v1, v2)


def scale_down(data, dist=tanimoto_distance, rate=0.01, max_iter=1000):
    """
    将高维数据的距离映射到二维平面下，高维数据距离越大，二维下距离越远
    :param data:  待映射数据
    :param dist:  “真实距离”计算法方法
    :param rate:  梯度下降速度
    :param max_iter:  迭代次数
    :return:  二维空间下的data坐标
    """
    n = len(data)
    dist_high = [[dist(data[i], data[j]) for j in range(n)] for i in range(n)]

    # 随机初始化节点在二维空间中的位置
    loc = [[random.random(), random.random()] for _ in range(n)]

    last_error = None
    for _ in range(max_iter):
        # 计算当前情形下二维空间中的“欧几里得”距离
        dist_2d = [[euclidean_distance(loc[i], loc[j]) for j in range(n)]
                   for i in range(n)]

        # 待移动距离，借鉴梯度下降思想
        grad = [[0.0, 0.0] for _ in range(n)]

        total_error = 0
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                # 误差值为目标距离与当前距离之间差值的百分比
                error_term = (dist_2d[j][i] - dist_high[j]
                              [i]) / dist_high[j][i]

                # 根据误差的多少，按比例进行移动
                grad[i][0] += ((loc[i][0] - loc[j][0]) /
                               dist_2d[j][i]) * error_term
                grad[i][1] += ((loc[i][1] - loc[j][1]) /
                               dist_2d[j][i]) * error_term

                total_error += abs(error_term)
        print(total_error)
        if last_error and last_error < total_error:
            break
        last_error = total_error

        # 开始移动
        for i in range(n):
            loc[i][0] -= rate * grad[i][0]
            loc[i][1] -= rate * grad[i][1]

    return loc


# 工具：绘制二维图片
def draw_2d(data, labels, jpeg='out/distance.jpg'):
    img = Image.new('RGB', (2400, 2400), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    for i in range(len(data)):
        x = (data[i][0] + 0.5) * 1200
        y = (data[i][1] + 0.5) * 1200
        draw.text((x, y), labels[i], (0, 0, 0))
    img.save(jpeg, 'JPEG')


# 工具：准备数据
def prepare_data(fn):
    with open(fn) as f:
        first_row = next(f)
        words = first_row.strip().split('\t')[1:]
        data = list()
        titles = list()
        for line in f:
            p = line.strip().split('\t')
            titles.append(p[0])
            data.append(np.array([float(x) for x in p[1:]]))
    data = np.array(data)
    return titles, words, data


if __name__ == "__main__":
    titles, words, data = prepare_data('data/blogdata.txt')
    loc = scale_down(data, rate=0.005)
    draw_2d(loc, titles)
