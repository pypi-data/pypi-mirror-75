import re
from abc import ABCMeta, abstractmethod
from typing import Any, Dict, List

import lightgbm
import xgboost

from sktmls import ModelRegistry, MLSENV


class MLSModelError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class MLSModel(metaclass=ABCMeta):
    def __init__(self, model_name: str, model_version: str):
        assert type(model_name) == str
        assert type(model_version) == str

        if not bool(re.search("^[A-Za-z0-9_]+_model$", model_name)):
            raise MLSModelError(
                "model_name should follow naming rule. MUST be in alphabet, number, underscore and endwiths '_model'"
            )

        if not bool(re.search("^[A-Za-z0-9_]+$", model_version)):
            raise MLSModelError("model_name should follow naming rule. MUST be in alphabet, number, underscore")

        self.model = None
        self.model_name = model_name
        self.model_version = model_version
        self.model_lib = None
        self.model_lib_version = None
        self.features = None

    def save(self, env: MLSENV = None, force: bool = False,) -> None:
        """
        Upload model_binary (model.joblib) and model_meta (model.json) to MLS model registry.

        Args:
            env: (MLSENV) AWS ENV.
            force: (bool) Force to overwrite model files on S3 if exists.
        """
        model_registry = ModelRegistry(env=env)
        model_registry.save(self, force)

    @abstractmethod
    def predict(self, x: List[Any]) -> Dict[str, Any]:
        pass


class MLSLightGBMModel(MLSModel):
    def __init__(self, model, model_name: str, model_version: str, features: List[str] = None):
        super().__init__(model_name, model_version)
        self.model = model
        self.model_lib = "lightgbm"
        self.model_lib_version = lightgbm.__version__

        if not features:
            self.features = self.model.feature_name()
        else:
            if len(features) < len(self.model.feature_name()):
                raise MLSModelError(
                    "The number of input features should be greater or equal to the number of features used on ML Model"
                )
            else:
                self.features = features


class MLSXGBoostModel(MLSModel):
    def __init__(self, model, model_name: str, model_version: str, features: List[str]):
        super().__init__(model_name, model_version)
        self.model = model
        self.model_lib = "xgboost"
        self.model_lib_version = xgboost.__version__

        if (
            all(isinstance(s, str) for s in features)
            and len(features) >= len(self.model.feature_importances_)
            and type(features) == list
        ):
            self.features = features
        else:
            raise MLSModelError(
                "Input feature list shold have more(or equal) to the number of model input feature or list STRING type"
            )


class MLSRuleModel(MLSModel):
    def __init__(self, model_name: str, model_version: str, features: List[str]):
        super().__init__(model_name, model_version)
        self.model_lib = "rule"
        self.model_lib_version = "N/A"

        if features:
            self.features = features
        else:
            raise MLSModelError("No feature provided")
