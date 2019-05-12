# 目的是以更少的空间去存储原数据，即从原数据中提取主要成分，舍弃占据大量空间的次要成分

import numpy as np
import matplotlib.pyplot as plt
from sklearn import decomposition
from PIL import Image
from utils import show_images
from sklearn.datasets import fetch_olivetti_faces


def plot(x):
    plt.scatter(x[0], x[1])
    plt.xlim([-1, 1])
    plt.ylim([-1, 1])
    plt.show()


def pca_manual(x, component=1):
    # x shape: [n_features, n_samples]
    mean = x.mean(axis=1).reshape(-1, 1)
    x -= mean
    plot(x)

    sigma = np.cov(x)  # 特征协方差矩阵
    # lambda_, U = np.linalg.eig(sigma)  # 主成分特征向量和对应基（列为基）
    U, lambda_, _ = np.linalg.svd(sigma)  # 同上，但是排好序了

    z = np.dot(U.transpose(), x)  # 新基下的坐标
    # plot(z)
    # 如果是白化，这个Z各维度除以sqrt lambda_，使得方差一致，然后再rebuild即可

    x_rebuild = np.dot(U[:, 0:component], z[0:component, :])
    plot(x_rebuild)


def pca_sklearn(x, component=1, feature_first=True):
    pca = decomposition.PCA(n_components=component)
    plot(x)
    if feature_first:
        x = x.transpose()  # 接收shape (n_samples, n_features)
    z_reduced = pca.fit_transform(x)
    x_rebuild = pca.inverse_transform(z_reduced)
    if feature_first:
        x_rebuild = x_rebuild.transpose()
    plot(x_rebuild)


def svd(X, component=2):
    """
    https://www.cnblogs.com/pinard/p/6251584.html
    可应用与 LSI：https://zhuanlan.zhihu.com/p/28777266
    """
    svd = decomposition.TruncatedSVD(n_components=component)
    svd.fit(X)
    return svd


def nmf(X, component):
    # X [n_samples, n_features]
    nmf = decomposition.NMF(component)
    W = nmf.fit_transform(X)
    # W [n_samples, n_components]
    H = nmf.components_
    # H [n_components, n_features]
    return W, H


def compress_pic_using_svd(n=50):
    im = Image.open('data/dsw.png')
    x = np.array(im)
    r = svd(x, n)
    compressed = r.transform(x)
    rebuilt = r.inverse_transform(compressed)
    img = Image.fromarray(rebuilt)
    img.show()


def compress_features_using_nmf(component=4):
    faces = fetch_olivetti_faces().data  # shape [400, 4096]
    W, H = nmf(faces, component)
    images = []
    for i in range(component):
        component = H[i].reshape(64, 64) * 255
        images.append(component)
    show_images(images)


if __name__ == '__main__':
    # x = np.loadtxt('data/pcaData.txt', dtype=np.float64)
    # pca_sklearn(x)
    # pca_manual(x)
    compress_features_using_nmf(6)
