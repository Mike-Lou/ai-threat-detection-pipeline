from pydantic import BaseModel
from typing import List, Dict, Any


class LogEntry(BaseModel):
    bytes_in: float
    bytes_out: float
    packets: float
    errors: float


class ScoreRequest(BaseModel):
    logs: List[LogEntry]
    

class ScoreResponse(BaseModel):
    scores: List[float]
    anomalies: List[bool]
    alerts: List[Dict[str, Any]]
