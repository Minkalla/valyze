from pydantic import BaseModel
from typing import Any, Dict, Optional

class ValyzeInputSchema(BaseModel):
    data_id: str
    category: str
    value_points: Dict[str, Any]
    is_sensitive: Optional[bool] = False
    source: Optional[str] = None
