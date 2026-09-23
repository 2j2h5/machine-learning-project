"""Extra edge-case checks beyond the public tests; local tool, not submitted.

Run from the repository root: python submissions/lab02/tools/test_edge_cases.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import (accuracy_score, f1_score, mean_absolute_error,
                             mean_squared_error, precision_score, r2_score,
                             recall_score)

LAB = Path(__file__).resolve().parents[3] / "lab02_classification"
sys.path.insert(0, str(LAB / "src"))
import lab02  # noqa: E402


def check_classification_metrics():
    rng = np.random.default_rng(7)
    for _ in range(200):
        n = int(rng.integers(1, 60))
        y_true, y_pred = rng.integers(0, 2, n), rng.integers(0, 2, n)
        m = lab02.compute_metrics(pd.Series(y_true, index=rng.permutation(n) + 100),
                                  pd.Series(y_pred, index=np.arange(n)))
        ref = {"accuracy": accuracy_score(y_true, y_pred),
               "precision": precision_score(y_true, y_pred, zero_division=0),
               "recall": recall_score(y_true, y_pred, zero_division=0),
               "f1": f1_score(y_true, y_pred, zero_division=0)}
        for k, v in ref.items():
            assert abs(m[k] - round(v, 4)) < 1e-9, (k, m[k], v)
            assert type(m[k]) is float
    # all-negative truth, all-positive predictions
    assert lab02.compute_metrics([0, 0, 0], [0, 0, 0])["accuracy"] == 1.0
    m = lab02.compute_metrics([1, 1, 0, 0], [1, 1, 1, 1])
    assert m["recall"] == 1.0 and m["precision"] == 0.5
    # the concept note's worked example
    m = lab02.compute_metrics([1, 0, 1, 1, 0, 0, 0, 0], [1, 0, 0, 1, 0, 1, 1, 0])
    assert m == {"accuracy": 0.625, "precision": 0.5, "recall": 0.6667, "f1": 0.5714}


def check_regression_metrics():
    rng = np.random.default_rng(3)
    for _ in range(200):
        n = int(rng.integers(2, 60))
        y_true = rng.normal(40, 15, n)
        y_pred = rng.normal(40, 15, n)
        m = lab02.compute_regression_metrics(pd.Series(y_true, index=rng.permutation(n)),
                                             y_pred.tolist())
        assert abs(m["mae"] - round(mean_absolute_error(y_true, y_pred), 4)) < 1e-9
        assert abs(m["rmse"] - round(mean_squared_error(y_true, y_pred) ** 0.5, 4)) < 1e-9
        assert abs(m["r2"] - round(r2_score(y_true, y_pred), 4)) < 1e-9
    assert lab02.compute_regression_metrics([30, 50, 60, 20], [35, 45, 55, 25]) == \
        {"mae": 5.0, "rmse": 5.0, "r2": 0.9}
    assert lab02.compute_regression_metrics([1, 2, 3], [3, 3, 3])["r2"] < 0  # can go negative


def check_split():
    X, y = lab02.load_data(LAB / "data" / "clinic_noshow.csv")
    a = lab02.split_data(X, y, seed=42)[0].index
    b = lab02.split_data(X, y, seed=7)[0].index
    assert not (a == b).all(), "different seeds must give different splits"
    X_tr, X_val, y_tr, y_val = lab02.split_data(X, y, test_size=0.3)
    assert len(X_val) == 360 and abs(y_tr.mean() - y_val.mean()) < 0.02
    # scaler is fitted on train only: its mean equals the train mean, not the full mean
    p = lab02.build_model("logreg").fit(X_tr, y_tr)
    assert np.allclose(p.named_steps["scaler"].mean_, X_tr.mean().values)
    assert p.named_steps["scaler"].mean_.tolist() != X.mean().tolist()


def check_builders_unfitted():
    from sklearn.utils.validation import check_is_fitted
    from sklearn.exceptions import NotFittedError
    for obj in (lab02.build_baseline(), lab02.build_model("knn"),
                lab02.build_regression_model("baseline"), lab02.build_regression_model("knn")):
        try:
            check_is_fitted(obj)
        except NotFittedError:
            continue
        raise AssertionError(f"{obj} should be unfitted")
    assert lab02.build_model("knn").named_steps["clf"].n_neighbors == 15
    assert lab02.build_regression_model("knn").named_steps["reg"].n_neighbors == 15


def check_determinism():
    X, y = lab02.load_data(LAB / "data" / "clinic_noshow.csv")
    assert lab02.run_experiment(X, y) == lab02.run_experiment(X, y)
    Xr, yr = lab02.load_regression_data(LAB / "data" / "clinic_wait.csv")
    assert lab02.run_regression_experiment(Xr, yr) == lab02.run_regression_experiment(Xr, yr)
    assert lab02.run_regression_experiment(Xr, yr, seed=1) != lab02.run_regression_experiment(Xr, yr)


if __name__ == "__main__":
    for check in (check_classification_metrics, check_regression_metrics, check_split,
                  check_builders_unfitted, check_determinism):
        check()
        print(f"ok  {check.__name__}")
