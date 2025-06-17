from typing import Any, Dict
import datetime
from .base_valuation_model import BaseValuationModel

class SimpleValuationModel(BaseValuationModel):
    def __init__(self, model_config: Dict[str, Any]):
        self._name = model_config.get("name", "SimpleValuationModel")
        self._version = model_config.get("version", "0.1.0-mvp")
        self.base_value = model_config.get("base_value", 100)
        self.multiplier_factor = model_config.get("multiplier_factor", {"high_priority": 1.5, "low_priority": 0.5})

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> str:
        return self._version

    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        input_priority = data.get("priority", "low_priority").lower()
        
        valuation_score = self.base_value * self.multiplier_factor.get(input_priority, 1.0)
        
        if data.get("is_sensitive_data", False):
            valuation_score *= 1.2
        
        confidence_score = 0.85 

        return {
            "valuation_score": round(valuation_score, 2),
            "confidence_score": confidence_score,
            "valuation_timestamp": datetime.datetime.utcnow().isoformat(),
            "model_used": self.name,
            "model_version": self.version,
        }

if __name__ == "__main__":
    model_config = {
        "name": "DemoMLModel",
        "version": "0.1-alpha",
        "base_value": 50,
        "multiplier_factor": {"critical": 2.0, "normal": 1.0, "low": 0.5}
    }
    simple_model = SimpleValuationModel(model_config)

    data_high_priority = {"data_id": "cust_123", "priority": "Critical", "is_sensitive_data": True}
    data_low_priority = {"data_id": "cust_456", "priority": "Low", "is_sensitive_data": False}
    data_normal = {"data_id": "cust_789", "priority": "Normal"}

    print(f"Valuation for high priority data: {simple_model.predict(data_high_priority)}")
    print(f"Valuation for low priority data: {simple_model.predict(data_low_priority)}")
    print(f"Valuation for normal data: {simple_model.predict(data_normal)}")
