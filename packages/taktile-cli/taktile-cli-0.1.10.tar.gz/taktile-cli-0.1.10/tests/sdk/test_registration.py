import numpy as np
import pandas as pd
import pytest
from typing import List, Dict, Callable

from tktl import Tktl
from tktl.core.exceptions.exceptions import ValidationException


@pytest.mark.parametrize(
    "X,y",
    [
        (pd.DataFrame({"a": [1, 2, 3]}), pd.Series([4, 5, 5])),  # pandas
        (np.array([[1], [2], [3]]), np.array([4, 5, 5])),  # numpy
        ({"a": [1, 2, 3]}, [4, 5, 5]),  # base
    ],
)
def test_creation(X, y):
    tktl = Tktl()

    @tktl.endpoint(X=X, y=y, kind="tabular")
    def predict(X):
        return [0] * len(X)

    endpoint = tktl.endpoints[0]
    assert type(endpoint.X) == pd.DataFrame
    assert type(endpoint.y) == pd.Series
    assert endpoint.y.name == "Outcome"
    assert endpoint.func(pd.DataFrame(X)) == [0, 0, 0]


@pytest.mark.parametrize("kind", ["tabular", "regression", "binary"])
def test_tabular_kinds(kind):
    tktl = Tktl()
    X = pd.DataFrame({"a": [1, 2, 3]})
    y = pd.Series([4, 5, 5])

    @tktl.endpoint(X=X, y=y, kind=kind)
    def predict(X):
        return [0] * len(X)

    endpoint = tktl.endpoints[0]
    assert isinstance(endpoint.X, pd.DataFrame)
    assert isinstance(endpoint.y, pd.Series)
    assert endpoint.y.name == "Outcome"
    assert endpoint.func(pd.DataFrame(X)) == [0, 0, 0]


def test_auxiliary_kind():
    tktl = Tktl()

    @tktl.endpoint(kind="auxiliary")
    def predict_untyped(x):
        return x

    @tktl.endpoint(kind="auxiliary", payload_model=List[str], response_model=Dict)
    def predict_typed(x):
        return x

    for endpoint in tktl.endpoints:
        assert isinstance(endpoint.func, Callable)
        assert endpoint.func(["foo"]) == ["foo"]


def test_func_shape():
    with pytest.raises(ValidationException):
        tktl = Tktl()
        X = {"a": [1, 2, 3]}
        y = [4, 5, 5]

        @tktl.endpoint(X=X, y=y)
        def predict(X):
            return [0] * (len(X) - 1)


def test_input_shape():
    with pytest.raises(ValidationException):
        tktl = Tktl()
        X = {"a": [1, 2, 3]}
        y = [4, 5]

        @tktl.endpoint(X=X, y=y)
        def predict(X):
            return [0] * len(X)


def test_validate_func():
    tktl = Tktl()

    with pytest.raises(ValidationException):
        X = {"a": [1, 2, 3]}
        y = [4, 5, 5]

        @tktl.endpoint(X=X, y=y, kind="regression")
        def predict_regression(X):
            return ["a", "b", "c"]  # must be numeric

    with pytest.raises(ValidationException):
        tktl = Tktl()
        X = {"a": [1, 2, 3]}
        y = [4, 5, 5]

        @tktl.endpoint(X=X, y=y, kind="binary")
        def predict_binary(X):
            return [-2, 0, 1.5]  # must be in [0, 1]


def test_unknown_kind():
    with pytest.raises(ValidationException):
        tktl = Tktl()
        X = {"a": [1, 2, 3]}
        y = [4, 5, 5]

        @tktl.endpoint(X=X, y=y, kind="unknown kind")
        def predict(X):
            return [0] * len(X)


def test_missing():
    tktl = Tktl()
    X = {"a": [1, 2, 3]}
    y = pd.Series([0.1, 0.2, None])

    with pytest.warns(UserWarning):

        @tktl.endpoint(X=X, y=y, kind="regression")
        def predict(X):
            return [0] * len(X)


def test_large():
    tktl = Tktl()
    n = int(1e6) + 1
    X = pd.DataFrame({"a": np.random.uniform(size=n)})
    y = pd.Series(np.random.uniform(size=n))

    with pytest.warns(UserWarning):

        @tktl.endpoint(X=X, y=y, kind="regression")
        def predict(X):
            return [0] * len(X)


def test_auxiliary():
    tktl = Tktl()

    @tktl.endpoint(kind="auxiliary", payload_model=List[str], response_model=List[str])
    def string_endpoint(x):
        return x
