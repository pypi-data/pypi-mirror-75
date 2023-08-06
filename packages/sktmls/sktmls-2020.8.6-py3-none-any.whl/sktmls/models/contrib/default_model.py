from typing import Any, Dict, List

from sktmls.models import MLSLightGBMModel, MLSXGBoostModel


class DefaultLightGBMModel(MLSLightGBMModel):
    def predict(self, x: List[Any]) -> Dict[str, Any]:
        return {"items": []}


class DefaultXGBoostModel(MLSXGBoostModel):
    def predict(self, x: List[Any]) -> Dict[str, Any]:
        return {"items": []}
