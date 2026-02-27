from abc import ABC, abstractmethod
from app.schemas.report import RuleResultSchema
from typing import Dict, Any

class BaseRule(ABC):
    """Abstract base class for all rules."""
    @abstractmethod
    def apply(self, payload: Dict[str, Any]) -> RuleResultSchema:
        pass