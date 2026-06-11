from pydantic import BaseModel

from typing import Dict
from typing import Any


class HITLTask(BaseModel):
    task_id: str
    query: str
    response: str
    confidence_score: float
    status: str
    metadata: Dict[str, Any]