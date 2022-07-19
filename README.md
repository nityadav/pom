### Steps to get training and test data
1. Download the `scorecards.zip` datapack and unzip it. This will create a directory called `scorecards`.
2. Create directories: `train`, `dev` and `test` in `data`
3. Run `split.py`. This essentially splits the `scorecards` data into three and places the files in `train`, `dev` and `test` directories.

### Steps to train XGBoost model and test
Run `train_eval_xgb.py`
