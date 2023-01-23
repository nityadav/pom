### Steps to get training and test data
1. Download the `scorecards.zip` datapack and unzip it. This will create a directory called `scorecards`.
2. Run `prepare_data.py`. This script splits the `scorecards` data into three and places the files in `data/train`, `data/dev` and `data/test` directories.

### Steps to train XGBoost model and test
Run `train_eval_xgb.py`

### To add new features
Change `data_models.py` by adding your feature in the ``PerformanceFeatures`` class
