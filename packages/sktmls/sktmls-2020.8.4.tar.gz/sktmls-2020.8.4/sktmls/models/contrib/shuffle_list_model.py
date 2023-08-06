import random
from typing import Any, Dict, List

from sktmls.models import MLSRuleModel


class ShuffleListModel(MLSRuleModel):
    def __init__(self, model_name: str, model_version: str, item_id: str, item_name: str, shuffle_list: List[str]):
        super().__init__(model_name, model_version, ["user_id"])

        self.item_id = item_id
        self.item_name = item_name
        self.shuffle_list = shuffle_list

    def predict(self, x: List[Any]) -> Dict[str, Any]:
        random.shuffle(self.shuffle_list)
        return {
            "items": {
                "id": self.item_id,
                "name": self.item_name,
                "props": {self.item_id: self.shuffle_list},
                "type": self.item_id,
            }
        }
