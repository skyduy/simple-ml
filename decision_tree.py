import pandas as pd
from scipy.sparse import hstack
from sklearn import tree, preprocessing


def decision_tree(X, y, min_gain=0.1):
    # criterion: 判断信息的混乱程度
    # splitter: 节点划分时，采取的划分策略
    # min_impurity_decrease: 至少增益min_impurity_decrease时，才形成分支
    # 决策树节点划分使得混乱度越来越低
    clf = tree.DecisionTreeClassifier(
        criterion='gini', splitter='best', min_impurity_decrease=min_gain)
    clf.fit(X, y)
    return clf


def load_data():
    df = pd.read_csv('data/buy.csv')
    y = df['target']

    # 适当情况下可缩减类别的可取值，如用区间表示，以防止过拟合和过量数据
    X = df[['source', 'location', 'read_FAQ']]

    # 若handle_unknown=ignore，则要考虑决策树预测过程中该特征缺失带来的影响
    # 因为假设是性别，决策树中会出现两条分支，而对于未知性别，无论走向哪条分支
    # 都会误判为该分支下的取值，正确做法是，两条分支都计算，再以最终值乘以其权重
    # 这里的权重与左右分支的总数目成正比：未知情况下，更倾向于分配多数者使用的标签
    one_hot = preprocessing.OneHotEncoder(handle_unknown='error')
    one_hot.fit(X)
    X = one_hot.transform(X)
    X = hstack([X, df.view_times.to_frame()])
    return X, y


def load_data2():
    df = pd.read_csv('data/buy.csv')
    y = df['target']

    # 适当情况下可缩减类别的可取值，如用区间表示，以防止过拟合和过量数据
    X1 = df[['source', 'location', 'read_FAQ']]
    X2 = df.view_times.to_frame()

    X1 = pd.get_dummies(X1)
    return pd.concat([X1, X2], axis=1), y


if __name__ == '__main__':
    X, y = load_data()
    clf = decision_tree(X, y)
    print(clf.predict_proba(X))
    print(clf.predict(X) == y)
    tree.export_graphviz(clf, 'out/tree.dot')
    # shell: dot -Tpng tree.dot -o tree.png
