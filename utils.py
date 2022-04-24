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


def str2float(s: str) -> float:
    s = s.replace("-", "")
    s = s.replace("*", "")
    return float(s) if s else 0.0


def str2int(s: str) -> int:
    return int(str2float(s))
