from enum import Enum
from typing import List


class MLSENV(Enum):
    DEV = "dev"
    STG = "stg"
    PRD = "prd"
    LOCAL = "local"

    @classmethod
    def list_items(cls) -> List["MLSENV"]:
        """
        List all supported environments
        """
        return [t for t in cls]

    @classmethod
    def list_values(cls) -> List[str]:
        """
        List all supported environment names
        """
        return [t.value for t in cls]
