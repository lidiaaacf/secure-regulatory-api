from pydantic import BaseModel
from typing import Literal, List


class TransactionDecision(BaseModel):
    request_id: str
    decision: Literal["APPROVED", "REVIEW", "REJECTED"]
    risk_score: int
    triggered_rules: List[str]
