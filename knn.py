from sklearn import neighbors


def regressor(X, y, k=5):
    neigh = neighbors.KNeighborsRegressor(n_neighbors=k)
    neigh.fit(X, y)
    return neigh


def classifier(X, y, k=5):
    neigh = neighbors.KNeighborsClassifier(n_neighbors=k)
    neigh.fit(X, y)
    return neigh


if __name__ == '__main__':
    X = [[0], [1], [2], [3]]
    y = [0, 0, 1, 1]
    reg = regressor(X, y, 2)
    print(reg.predict([[1.5]]))

    clf = classifier(X, y, 3)
    print(clf.predict([[1.6]]))
    print(clf.predict_proba([[1.6]]))
