from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseValuationModel(ABC):
    @abstractmethod
    def __init__(self, model_config: Dict[str, Any]):
        pass

    @abstractmethod
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        pass
