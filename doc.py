import pandas as pd
from sklearn import naive_bayes
from sklearn.feature_extraction import text
# feature_extraction 中的svd可用于LSI文本模型

def doc_classifier(X, y):
    clf = naive_bayes.MultinomialNB()
    clf.fit(X, y)
    return clf


def lda():
    # Beta分布是二项分布的共轭分布，Dirichlet 分布是多项式分布的共轭分布
    # 共轭分布是指，以此作为前验分布，在观察额外数据后的分布（后验分布）仍然满足该形式。
    #  TODO 主题模型LDA
    pass


def load_data(tf_idf=True):
    df = pd.read_csv('data/doc.csv')
    X, y = df.doc, df.label
    if tf_idf:
        vectorizer = text.TfidfVectorizer()
    else:
        vectorizer = text.CountVectorizer()
    X = vectorizer.fit_transform(X).toarray()
    return X, y


if __name__ == '__main__':
    X, y = load_data(tf_idf=False)
    clf = doc_classifier(X, y)
    print(clf.predict(X) == y)
