import pandas as pd
from surprise import SVD, Reader, Dataset
# model-based recommendation


def load_data():
    critics = {
        'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                      'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 'The Night Listener': 3.0},
        'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 'Just My Luck': 1.5,
                         'Superman Returns': 5.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 3.5},
        'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0, 'Superman Returns': 3.5,
                             'The Night Listener': 4.0},
        'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 'The Night Listener': 4.5,
                         'Superman Returns': 4.0, 'You, Me and Dupree': 2.5},
        'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'Just My Luck': 2.0,
                         'Superman Returns': 3.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 2.0},
        'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'The Night Listener': 3.0,
                          'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
        'Toby': {'Snakes on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}
    }
    uid, iid, rating = [], [], []
    for user, prefer in critics.items():
        for item, score in prefer.items():
            uid.append(user)
            iid.append(item)
            rating.append(score)
    min_rating = min(rating)
    max_rating = max(rating)
    raw_data = {'uid': uid, 'iid': iid, 'rating': rating}
    df = pd.DataFrame(raw_data)
    reader = Reader(rating_scale=(min_rating, max_rating))
    data = Dataset.load_from_df(df[['uid', 'iid', 'rating']], reader)
    return (uid, iid, rating), data


def train(data, n_components):
    algo = SVD(n_factors=n_components)
    algo.fit(data)
    return algo


if __name__ == '__main__':
    raw_data, data = load_data()
    model = train(data.build_full_trainset(), 6)
    for uid, iid, rating in zip(*raw_data):
        print(model.predict(uid, iid).est, rating)
