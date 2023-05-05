from typing import Optional
from transformers import Scorecard
import os


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


def str2float(s: str) -> Optional[float]:
    if s is not None:
        s = s.replace("-", "")
        s = s.replace("*", "")
        return float(s) if s else 0.0
    else:
        return None


def str2int(s: str) -> Optional[int]:
    return None if s is None else int(str2float(s))


def get_feat_to_idx_map(features_name_file):
    with open(features_name_file) as f:
        return {feature.strip(): idx for idx, feature in enumerate(f)}


def dict2svm(features_dict, label_feature, qid, feat_to_idx_map):
    label_val = features_dict.pop(label_feature)
    f = ['{}:{}'.format(feat_to_idx_map[k], v) for k, v in features_dict.items() if v is not None and k in feat_to_idx_map]
    return ' '.join([str(label_val)] + ['qid:{}'.format(qid)] + f)


def json_to_svm(json_dir, features_name_file, svm_out_file):
    feat_to_idx_map = get_feat_to_idx_map(features_name_file)
    match_files = [os.path.join(json_dir, filename) for filename in os.listdir(json_dir) if filename.endswith('json')]
    with open(svm_out_file, 'w') as out_f:
        svm_lines = []
        for match_file in match_files:
            match_id = os.path.basename(match_file).split('.')[0]
            scorecard = Scorecard(match_file)
            features_dict_list = scorecard.get_features_with_label()
            svm_lines += [dict2svm(features_dict, 'pom', match_id, feat_to_idx_map) for features_dict in features_dict_list]
        out_f.write('\n'.join(svm_lines))
