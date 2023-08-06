import random
from typing import Any, Dict, List

from sktmls.models import MLSRuleModel, MLSModelError


class RandomPickModel(MLSRuleModel):
    def __init__(self, model_name: str, model_version: str, candidates: List[Dict[str, Any]], num_pick: int = 1):
        super().__init__(model_name, model_version, ["user_id"])

        if len(candidates) < num_pick:
            raise MLSModelError("The length of num_pick cannot be greater than that of candidates")

        self.candidates = candidates
        self.num_pick = num_pick

    def predict(self, x: List[Any]) -> Dict[str, Any]:
        return {"items": random.sample(self.candidates, self.num_pick)}
