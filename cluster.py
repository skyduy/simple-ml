from sklearn.cluster import KMeans, DBSCAN
from distance import tanimoto_distance, prepare_data


# k means算法，基于欧几里得距离 （此时均值意义最为明显）
def k_means_euclidean(x, k=4):  # 基于欧几里得距离的K-means算法
    k_means = KMeans(n_clusters=k, max_iter=100, verbose=True)
    k_means.fit(x)
    return k_means


# DBSCAN 聚类方法
def dbscan(x, eps, min_samples, distance=tanimoto_distance):
    clustering = DBSCAN(eps, min_samples, metric='precomputed')
    x_dis = [[distance(a, b) for b in x] for a in x]
    clustering.fit(x_dis)
    return clustering


def run_dbscan():
    title, words, data = prepare_data('data/blogdata.txt')
    res = dbscan(data, eps=0.14, min_samples=4)
    print(res.labels_)


if __name__ == '__main__':
    run_dbscan()
