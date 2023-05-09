import argparse

import numpy as np
import xgboost as xgb
from sklearn.metrics import classification_report, f1_score
from tabulate import tabulate

import config
from utils import get_feat_to_idx_map


def get_feature_imp(contribution_matrix, feature_names):
    feature_contribs = np.mean(np.abs(contribution_matrix), axis=0)
    return sorted(zip(feature_names, feature_contribs), key=lambda x: x[1], reverse=True)


def main(args):
    _, feature_names = get_feat_to_idx_map(config.features_file)
    dtrain = xgb.DMatrix(args.train_file, feature_names=feature_names)
    ddev = xgb.DMatrix(args.dev_file, feature_names=feature_names)
    dtest = xgb.DMatrix(args.test_file, feature_names=feature_names)

    train_labels = dtrain.get_label()
    num_pos = sum(train_labels)
    num_neg = len(train_labels) - num_pos

    train_params = {
        'booster': 'dart',
        'max_depth': 10,
        'eta': 0.01,
        'objective': 'binary:logistic',
        'scale_pos_weight': num_neg / num_pos
    }
    booster = xgb.train(train_params, dtrain, 50, evals=[(ddev, 'eval'), (dtrain, 'train')])
    booster.save_model('models/{}.json'.format(args.model))
    booster.dump_model('models/{}.txt'.format(args.model))
    contribs = booster.predict(dtest, pred_contribs=True)
    feat_imp = get_feature_imp(contribs[:, :-1], feature_names)
    print('Features by their importance:\n{}'.format(tabulate(feat_imp)))

    pred_y = booster.predict(dtest, output_margin=True)
    threshold = 0.5
    pred_y = np.array([1 if y > threshold else 0 for y in pred_y])
    true_y = dtest.get_label()
    print(classification_report(true_y, pred_y))
    print(f1_score(true_y, pred_y))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Description of the script.')
    parser.add_argument('--action', default='train', choices=['train', 'eval'])
    parser.add_argument('--train_file', default='data/train.svm')
    parser.add_argument('--dev_file', default='data/dev.svm')
    parser.add_argument('--test_file', default='data/test.svm')
    parser.add_argument('--model', default='svm_model')
    main(parser.parse_args())
