from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline

from transformers import Scorecard


def get_raw_x_y(file_paths: list, label_key='pom'):
    """
    :return: [{f: v}], [l] where f is predictor name, v is the value, l is label value
    """
    all_labels = []
    all_predictors = []
    for f in file_paths:
        s = Scorecard(f)
        l = s.get_features_with_label()
        labels = [i[label_key] for i in l]
        predictors = [{k: v for k, v in i.items() if k != label_key} for i in l]
        all_labels += labels
        all_predictors += predictors
    return all_predictors, all_labels


class PomPipeline(object):
    def __init__(self, estimator):
        vectorizer = DictVectorizer(sparse=False)
        self.pipeline = Pipeline(steps=[('vectorizer', vectorizer), ('estimator', estimator)])
        self.feature_importance = None

    def train(self, file_paths: list):
        X, y = get_raw_x_y(file_paths)
        self.pipeline.fit(X, y)
        feature_names = self.pipeline.named_steps['vectorizer'].get_feature_names()
        feature_imp = self.pipeline.named_steps['estimator'].feature_importances_
        self.feature_importance = {name: imp for name, imp in zip(feature_names, feature_imp)}
        return self.feature_importance

    def predict(self, file_paths: list):
        for f in file_paths:
            X, y = get_raw_x_y([f])
            p = self.pipeline.predict_proba(X)
            print(p)
            break
