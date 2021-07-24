from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer
import json

with open('test.json') as test_f:
    f = json.load(test_f)
    v = DictVectorizer(sparse=False)
    X_y = v.fit_transform(f)
    print(v.get_feature_names())
