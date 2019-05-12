import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules


def load_data():
    data = [['Milk', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
            ['Dill', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
            ['Milk', 'Apple', 'Kidney Beans', 'Eggs'],
            ['Milk', 'Unicorn', 'Corn', 'Kidney Beans', 'Yogurt'],
            ['Corn', 'Onion', 'Onion', 'Kidney Beans', 'Ice cream', 'Eggs']]

    te = TransactionEncoder()
    te_ary = te.fit(data).transform(data)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    return df


def analyze(df, min_sup=0.6, metric="confidence", min_threshold=0.8):
    frequent_itemsets = apriori(df, min_sup)
    res = association_rules(frequent_itemsets, metric, min_threshold)
    return frequent_itemsets, res


if __name__ == '__main__':
    data = load_data()
    itemsets, result = analyze(data)
    print(itemsets)
    print(result)
