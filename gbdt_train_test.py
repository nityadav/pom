import json
import os
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import config
import utils

train_file_paths = [os.path.join(config.train_dir, filename) for filename in os.listdir(config.train_dir)]
test_file_paths = [os.path.join(config.test_dir, filename) for filename in os.listdir(config.test_dir)]

gbdt = GradientBoostingClassifier(n_estimators=10, learning_rate=0.1, max_depth=6, random_state=0)
gbdt_pipeline = Pipeline(steps=[('vectorizer', DictVectorizer(sparse=False)), ('estimator', gbdt)])
train_x, train_y = utils.get_raw_x_y(train_file_paths)
gbdt_pipeline.fit(train_x, train_y)
feature_names = gbdt_pipeline.named_steps['vectorizer'].get_feature_names()
feature_imp = gbdt_pipeline.named_steps['estimator'].feature_importances_
feature_importance = {name: imp for name, imp in zip(feature_names, feature_imp)}
with open('analysis/feature_importance.json', 'w') as feature_imp_f:
    json.dump(feature_importance, feature_imp_f)


test_x, test_y = utils.get_raw_x_y(test_file_paths)
pred_y = gbdt_pipeline.predict(test_x)
true_y = np.array(test_y)
report = classification_report(true_y, pred_y)
print(report)
