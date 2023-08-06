from abc import ABC, abstractmethod
import functools
import warnings
from typing import Callable

import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype

from tktl.core.exceptions import exceptions


class Endpoint(ABC):
    def __init__(self, func):
        self.func = func
        self._validate()

    @abstractmethod
    def _validate():
        raise NotImplementedError

    @property
    @abstractmethod
    def kind():
        raise NotImplementedError


class TabularEndpoint(Endpoint):
    kind = "tabular"

    def __init__(self, func, X, y):
        self.func = func
        self.X = self._convert_x(X)
        self.y = self._convert_y(y)
        self._drop_missing_values()
        self._validate()

    @staticmethod
    def _convert_x(X):
        try:
            X = pd.DataFrame(X)
        except ValueError:
            raise exceptions.ConversionException("Could not convert X to pd.DataFrame")

        if len(X) > 1e6:
            warnings.warn(
                f"X is very large (N={len(X)}). "
                f"Please consider using a smaller reference dataset."
            )
        return X

    @staticmethod
    def _convert_y(y):
        try:
            y = pd.Series(y)
            y.name = y.name or "Outcome"

        except ValueError:
            raise exceptions.ConversionException("Could not convert y to pandas series")

        return y

    def _drop_missing_values(self):
        id_missing = self.y.isna()
        n_missing = id_missing.sum()
        if id_missing.sum() > 0:
            warnings.warn(f"y contains {n_missing} missing values that will be dropped")
            self.X = self.X.loc[~id_missing]
            self.y = self.y.loc[~id_missing]

    def _validate(self):
        self._validate_func()
        self._validate_shapes()

    def _validate_func(self):
        pred = self.func(self.X)
        pred = pd.Series(pred)

        if not is_numeric_dtype(pred):
            raise exceptions.ValidationException("Function output is not numeric")

    def _validate_shapes(self):
        pred = self.func(self.X)

        if not len(pred) == len(self.X):
            raise exceptions.ValidationException("Predictions inconsistent with X")
        if not len(self.y) == len(self.X):
            raise exceptions.ValidationException("y is inconsistent with input data X")


class BinaryEndpoint(TabularEndpoint):
    kind = "binary"

    @staticmethod
    def _convert_y(y):
        try:
            y = pd.Series(y).astype(bool)
            y.name = y.name or "Outcome"

        except ValueError:
            raise exceptions.ConversionException(
                "Could not convert y to pd.Series of type bool"
            )

        return y

    def _validate_func(self):
        pred = self.func(self.X)
        pred = pd.Series(pred)

        if not is_numeric_dtype(pred):
            raise exceptions.ValidationException("Function output is not numeric")

        if not 0 <= pred.min():
            raise exceptions.ValidationException(
                "Function output cannot be negative for endpoint kind binary"
            )

        if not pred.max() <= 1:
            raise exceptions.ValidationException(
                "Function output cannot exceed 1 for endpoint kind binary"
            )


class RegressionEndpoint(TabularEndpoint):
    kind = "regression"

    @staticmethod
    def _convert_y(y):
        try:
            y = pd.Series(y).astype(float)
            y.name = y.name or "Outcome"

        except ValueError:
            raise exceptions.ConversionException(
                "Could not convert y to pd.Series of type float"
            )

        return y

    def _validate_func(self):
        pred = self.func(self.X)
        pred = pd.Series(pred)

        if not is_numeric_dtype(pred):
            raise exceptions.ValidationException("Function output is not numeric")


class AuxiliaryEndpoint(Endpoint):
    kind = "auxiliary"

    def __init__(self, func, payload_model=None, response_model=None):
        self.func = func
        self.payload_model = payload_model
        self.response_model = response_model
        self._validate()

    def _validate(self):
        assert isinstance(self.func, Callable)


class Tktl:
    def __init__(self):
        self.endpoints = []

    # This is the user-facing decorator for function registration
    def endpoint(
        self,
        func: Callable = None,
        kind: str = "regression",
        X: pd.DataFrame = None,
        y: pd.Series = None,
        payload_model=None,
        response_model=None,
    ):
        """Register function as a Taktile endpoint

        Parameters
        ----------
        func : Callable, optional
            Function that describes the desired operation, by default None
        kind : str, optional
            Specification of endpoint type ("regression", "binary", "auxiliary"),
            by default "regression"
        X : pd.DataFrame, optional
            Reference input dataset for testing func. Used when argument "kind"
            is set to "regression" or "binary", by default None.
        y : pd.Series, optional
            Reference output for evaluating func. Used when argument "kind"
            is set to "regression" or "binary", by default None.
        payload_model:
            Type hint used for documenting and validating payload. Used in
            auxiliary endpoints only.
        response_model:
            Type hint used for documenting and validating response. Used in
            auxiliary endpoints only.

        Returns
        -------
        Callable
            Wrapped function
        """
        if func is None:
            return functools.partial(
                self.endpoint,
                kind=kind,
                X=X,
                y=y,
                payload_model=payload_model,
                response_model=response_model,
            )

        if kind == "tabular":
            endpoint = TabularEndpoint(func=func, X=X, y=y)
        elif kind == "regression":
            endpoint = RegressionEndpoint(func=func, X=X, y=y)
        elif kind == "binary":
            endpoint = BinaryEndpoint(func=func, X=X, y=y)
        elif kind == "auxiliary":
            endpoint = AuxiliaryEndpoint(
                func=func, payload_model=payload_model, response_model=response_model
            )
        else:
            raise exceptions.ValidationException(f"Unknown endpoint kind: '{kind}'")

        self.endpoints.append(endpoint)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            pred = func(*args, **kwargs)
            return pred

        return wrapper
