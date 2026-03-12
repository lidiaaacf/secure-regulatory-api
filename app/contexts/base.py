from abc import ABC, abstractmethod
from typing import List, Dict, Any
from enum import Enum
from app.rules.base import BaseRule
from app.schemas.report import RuleResultSchema


class ValidationContextEnum(str, Enum):
    generic = "generic"
    transaction = "transaction"
    internal_api = "internal_api"
    kyc = "kyc"


class ValidationContext(ABC):
    name: ValidationContextEnum

    def __init__(self):
        self.rules: List[BaseRule] = self.get_rules()

    @abstractmethod
    def get_rules(self) -> List[BaseRule]:
        pass

    def evaluate(self, payload: Dict[str, Any]) -> List[RuleResultSchema]:
        results: List[RuleResultSchema] = []

        for rule in self.rules:
            result = rule.evaluate(payload)
            results.append(result)

        return results
