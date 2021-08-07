import os
from pipeline import PomPipeline
import json
import config

train_file_paths = [os.path.join(config.train_dir, filename) for filename in os.listdir(config.train_dir)]
pipeline = PomPipeline()
feature_imp = pipeline.train(train_file_paths)
with open('analysis/feature_importance.json', 'w') as feature_imp_f:
    json.dump(feature_imp, feature_imp_f)
pipeline.predict(['test/64156.json'])
