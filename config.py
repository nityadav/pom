scorecards_dir = "scorecards"
data_dir = "data"
models_dir = "models"
train_dir = "{}/train".format(data_dir)
dev_dir = "{}/dev".format(data_dir)
test_dir = "{}/test".format(data_dir)
features_file = "features.txt"
train_file = "{}/train.svm".format(data_dir)
dev_file = "{}/dev.svm".format(data_dir)
test_file = "{}/test.svm".format(data_dir)

params_grid = {
    "booster": ["dart", "gbtree"],
    "eta": [0.01, 0.05, 0.1],
    "gamma": [0.0, 0.01, 0.1, 1.0, 2.0, 4.0],
    "max_depth": [3, 6, 9, 12],
    "objective": "binary:logistic",
    "min_child_weight": [1, 2, 4, 8, 16, 32],
    "subsample": [0.1, 0.3, 0.5, 0.7, 0.9],
    "colsample_bytree": [0.1, 0.3, 0.5, 0.7, 0.9],
    "lambda": [0.0, 0.01, 0.1, 1.0, 2.0, 4.0],
    "alpha": [0.0, 0.01, 0.1, 1.0, 2.0, 4.0],
}
