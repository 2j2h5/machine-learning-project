"""Local verification only; excluded from the submission archive."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "lab01_eda" / "src"))
import lab01


def test_missing_ties_preserve_column_order():
    df = pd.DataFrame({"z": [None, 2], "a": [1, None], "complete": [1, 2]})
    result = lab01.summarize_missing(df)
    assert result.index.tolist() == ["z", "a"]
    assert result.tolist() == [1, 1]
    assert pd.api.types.is_integer_dtype(result.dtype)
    assert lab01.summarize_missing(df.fillna(0)).empty


def test_dedup_precedes_imputation_and_only_fill_value_is_rounded():
    df = pd.DataFrame({
        "order_id": [1, 2, 3, 2],
        "unit_price": ["1,000", 200.0, "300", 200.0],
        "quantity": [1.0, 2.0, np.nan, 2.0],
        "total_price": [999.0, 400.0, np.nan, 400.0],
        "customer_rating": [1.111, 4.444, np.nan, 4.444],
    }, index=[10, 20, 30, 40])
    original = df.copy(deep=True)
    result = lab01.clean_data(df)
    assert result.index.tolist() == [0, 1, 2]
    assert result.quantity.tolist() == [1, 2, 1]  # median 1.5, then truncation
    assert result.customer_rating.tolist() == [1.111, 4.444, 2.78]
    assert result.total_price.tolist() == [999.0, 400.0, 300.0]
    assert result.unit_price.tolist() == [1000.0, 200.0, 300.0]
    assert result.isna().sum().sum() == 0
    pd.testing.assert_frame_equal(df, original)


def test_invalid_price_is_not_silently_coerced():
    df = pd.DataFrame({"unit_price": ["4,500 Won"], "quantity": [1],
                       "total_price": [4500], "customer_rating": [4.0]})
    with pytest.raises(ValueError):
        lab01.clean_data(df)


def test_iqr_strict_fences_sorted_labels_and_nan_exclusion():
    df = pd.DataFrame({"x": [0, 1, 1, 1, 2, 3, 3, 3, 4, np.nan]},
                      index=[90, 80, 70, 60, 50, 40, 30, 20, 10, 0])
    result = lab01.detect_outliers_iqr(df, "x", k=0)
    assert result == [10, 90]
    assert all(type(value) is int for value in result)
    assert lab01.detect_outliers_iqr(df, "x", k=1000) == []


def test_iqr_zero_spread_and_empty_inputs():
    assert lab01.detect_outliers_iqr(pd.DataFrame({"x": [2] * 8 + [9]}), "x") == [8]
    assert lab01.detect_outliers_iqr(pd.DataFrame({"x": [np.nan]}), "x") == []
    assert lab01.detect_outliers_iqr(pd.DataFrame({"x": pd.Series(dtype=float)}), "x") == []


def test_group_count_excludes_nan_and_only_mean_is_rounded():
    df = pd.DataFrame({"group": ["b", "a", "a", "b"],
                       "value": [np.nan, 1.111, 2.222, 10.555]})
    original = df.copy(deep=True)
    result = lab01.compute_group_stats(df, "group", "value")
    assert result.index.tolist() == ["b", "a"]
    assert result.columns.tolist() == ["count", "mean", "sum"]
    assert result["count"].tolist() == [1, 2]
    assert result["mean"].tolist() == [10.56, 1.67]
    assert result["sum"].tolist() == pytest.approx([10.555, 3.333])
    pd.testing.assert_frame_equal(df, original)
