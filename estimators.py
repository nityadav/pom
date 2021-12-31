from sklearn.ensemble import GradientBoostingClassifier


def get_GBDT():
    return GradientBoostingClassifier(n_estimators=10, learning_rate=0.1, max_depth=6, random_state=0)
