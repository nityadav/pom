import argparse
import os

import numpy as np
import xgboost as xgb
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import classification_report

import config
import utils
from tabulate import tabulate


def load_data(x, y, vectorizer, train=False):
    if train:
        vectorizer.fit(x)
    x_mat = vectorizer.transform(x)
    y_arr = np.array(y)
    return x_mat, y_arr, xgb.DMatrix(x_mat, label=y_arr, missing=np.NaN, feature_names=vectorizer.get_feature_names_out())


def get_feature_imp(contribution_matrix, feature_names):
    feature_contribs = np.sum(np.abs(contribution_matrix), axis=0)
    return sorted(zip(feature_names, feature_contribs), key=lambda x: x[1], reverse=True)


def main(args):
    if not os.path.isdir(config.models_dir):
        os.mkdir(config.models_dir)

    train_file_paths = [os.path.join(config.train_dir, filename) for filename in os.listdir(config.train_dir)]
    dev_file_paths = [os.path.join(config.dev_dir, filename) for filename in os.listdir(config.dev_dir)]
    test_file_paths = [os.path.join(config.test_dir, filename) for filename in os.listdir(config.test_dir)]

    train_x, train_y = utils.get_raw_x_y(train_file_paths)
    dev_x, dev_y = utils.get_raw_x_y(dev_file_paths)
    test_x, test_y = utils.get_raw_x_y(test_file_paths)

    dict_vectorizer = DictVectorizer()
    train_x, train_y, dtrain = load_data(train_x, train_y, dict_vectorizer, True)
    dev_x, dev_y, ddev = load_data(dev_x, dev_y, dict_vectorizer)
    test_x, test_y, dtest = load_data(test_x, test_y, dict_vectorizer)

    num_pos = sum(train_y)
    num_neg = len(train_y) - num_pos

    if args.action == 'train':
        train_params = {
            'max_depth': 6,
            'eta': 0.1,
            'objective': 'binary:logistic',
            'scale_pos_weight': num_neg / num_pos
        }
        booster = xgb.train(train_params, dtrain, 10, evals=[(ddev, 'eval'), (dtrain, 'train')])
        booster.save_model('models/{}.json'.format(args.model))
        booster.dump_model('models/{}.txt'.format(args.model))
        contribs = booster.predict(dtest, pred_contribs=True)
        feat_imp = get_feature_imp(contribs[:, :-1], dict_vectorizer.get_feature_names_out().tolist())
        print('Features by their importance:\n{}'.format(tabulate(feat_imp)))
    else:
        booster = xgb.Booster()
        booster.load_model('models/{}.json'.format(args.model))

    pred_y = booster.predict(dtest, output_margin=True)
    threshold = 0.5
    pred_y = np.array([1 if y > threshold else 0 for y in pred_y])
    print(classification_report(test_y, pred_y))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train and evaluate xgboost model')
    parser.add_argument('--action', default='train', choices=['train', 'eval'])
    parser.add_argument('--model', default='xgb')
    main(parser.parse_args())
