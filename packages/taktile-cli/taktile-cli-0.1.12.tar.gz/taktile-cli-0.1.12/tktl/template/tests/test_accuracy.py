import numpy as np
from sklearn.metrics import roc_auc_score
from src.endpoints import binary, X_test, y_test


def test_accuracy(json_metadata):
    lower_bound = 0.85
    pred = binary(X_test)
    auc = roc_auc_score(y_test, pred)
    assert auc > lower_bound

    # add metadata
    json_metadata["section"] = "Accuracy"
    json_metadata["pass_message"] = f"AUC exceeds lower bound of {lower_bound}"
    json_metadata["fail_message"] = f"AUC is below lower bound of {lower_bound}"


def test_mean(json_metadata):
    pred = binary(X_test)
    mean_pred = np.mean(pred)
    assert 0.3 < mean_pred < 0.4

    # add metadata
    json_metadata["section"] = "Plausibility"
    json_metadata["pass_message"] = f"Mean prediction is plausible ({mean_pred:.2f})"
    json_metadata["fail_message"] = f"Mean prediction is implausible ({mean_pred:.2f})"
