import argparse

import numpy as np
import xgboost as xgb
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from sklearn.metrics import f1_score

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

    param_hyperopt = {
        'learning_rate': hp.loguniform('learning_rate', np.log(0.01), np.log(1)),
        # 'max_depth': scope.int(hp.quniform('max_depth', 5, 15, 1)),
        'max_depth': hp.choice('max_depth', [6, 8, 10]),
        'booster': hp.choice('booster', ['gbtree', 'dart']),
        'colsample_bytree': hp.uniform('colsample_by_tree', 0.6, 1.0),
        'reg_lambda': hp.uniform('reg_lambda', 0.0, 1.0),
        'reg_alpha': hp.quniform('reg_alpha', 10, 50, 5),
        'gamma': hp.uniform('gamma', 0, 9),
        'scale_pos_weight': num_neg / num_pos,
        'objective': 'binary:logistic',
    }

    def objective_function(params):
        booster = xgb.train(params, dtrain, 50)
        scores = booster.predict(ddev)
        pred_y = np.array([1 if s > args.threshold else 0 for s in scores])
        true_y = ddev.get_label()
        pom_f1 = f1_score(true_y, pred_y)
        return {'loss': -pom_f1, 'status': STATUS_OK}

    trials = Trials()
    best_param = fmin(objective_function,
                      param_hyperopt,
                      algo=tpe.suggest,
                      max_evals=5,
                      trials=trials,
                      rstate=np.random.default_rng(1))
    loss = [x['result']['loss'] for x in trials.trials]
    print(best_param)

    # booster = xgb.train(train_params, dtrain, 50, evals=[(ddev, 'eval'), (dtrain, 'train')])
    # booster.save_model('models/{}.json'.format(args.model))
    # booster.dump_model('models/{}.txt'.format(args.model))
    # contribs = booster.predict(dtest, pred_contribs=True)
    # feat_imp = get_feature_imp(contribs[:, :-1], feature_names)
    # print('Features by their importance:\n{}'.format(tabulate(feat_imp)))
    #
    # pred_y = booster.predict(dtest, output_margin=True)
    # threshold = 0.5
    # pred_y = np.array([1 if y > threshold else 0 for y in pred_y])
    # print(classification_report(dtest.get_label(), pred_y))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Description of the script.')
    parser.add_argument('--action', default='train', choices=['train', 'eval'])
    parser.add_argument('--train_file', default='data/train.svm')
    parser.add_argument('--dev_file', default='data/dev.svm')
    parser.add_argument('--test_file', default='data/test.svm')
    parser.add_argument('--threshold', default=0.5)
    parser.add_argument('--model', default='svm_model')
    main(parser.parse_args())
