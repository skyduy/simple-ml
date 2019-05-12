import random
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import svm, preprocessing


def svm_classifier(X, y, kernel='linear'):
    """  可发现目标全局最小值
    Relying on basic knowledge of reader about kernels.
    算法导论 P167
    线性支持向量机分类器，适用于可线性分类的数据，通过参数可调整 soft margin
        Linear Kernel: K(X,Y)=XTY

    非线性支持向量机：使用非线性变化Φ，将原特征空间映射到新的特征空间
    在使用SVM过程中，对偶拉格朗日函数中会出现 Φ(Xi) * Φ(Xj)，可使用核技术简化
        Polynomial kernel: K(X,Y)=(γ⋅XTY+r)d,γ>0
        Radial basis function (RBF) Kernel: K(X,Y)=exp(∥X−Y∥2/2σ2) which in simple form can be written as exp(−γ⋅∥X−Y∥2),γ>0
        Sigmoid Kernel: K(X,Y)=tanh(γ⋅XTY+r) which is similar to the sigmoid function in logistic regression.

    Here r, d, and γ are kernel parameters
    """
    clf = svm.SVC(C=1.0, kernel=kernel)  # C: 松弛变量的代价权重
    clf.fit(X, y)
    return clf


def plot_age_matches(data):
    success = data[data[10] == 1]
    fail = data[data[10] == 0]

    plt.plot(success[0], success[5], 'bo')
    plt.plot(fail[0], fail[5], 'b+')
    plt.show()


def process(df):
    def extract(row):
        def yesno(x):
            return 1 if x == 'yes' else -1 if x == 'no' else x

        common = 0
        if isinstance(row[3], str) and isinstance(row[8], str):
            i = set(row[3].split(':'))
            j = set(row[8].split(':'))
            common = len(i & j)
        data = [row[0], yesno(row[1]), yesno(row[2]),
                row[5], yesno(row[6]), yesno(row[7]), common]
        return pd.Series(data)

    data = df.apply(extract, axis=1).astype(float)
    scaler = preprocessing.MinMaxScaler()
    scaler.fit(data)
    return scaler.transform(data)


if __name__ == '__main__':
    data = pd.read_csv('data/matchmaker.csv', header=None).sample(frac=1)
    train_data = data[:400]
    train_y = train_data[10]
    valid_data = data[100:]
    valid_y = valid_data[10]

    def train_with_age():  # 只使用年龄数据
        # plot_age_matches(data)
        X = np.array(list(zip(train_data[0], train_data[5])))
        clf = svm_classifier(X, train_y, kernel='rbf')

        valid_X = np.array(list(zip(valid_data[0], valid_data[5])))
        print('Age only acc: {0:.2f}%'.format(
            100 * sum(clf.predict(valid_X) == valid_y) / len(valid_y)))

    def train_with_all():
        clf = svm_classifier(process(train_data), train_y, kernel='rbf')
        valid_X = process(valid_data)
        print('Using all acc: {0:.2f}%'.format(
            100 * sum(clf.predict(valid_X) == valid_y) / len(valid_y)))

    train_with_age()
    train_with_all()
