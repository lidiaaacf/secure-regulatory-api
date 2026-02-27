from typing import List, Dict, Any
from app.schemas.report import RuleResultSchema
from app.rules.business_rules import AmountMaxLimitRule, EmailDomainRule, UserIdUUIDRule
from app.rules.base import BaseRule

class RulesEngine:
    def __init__(self, rules: List[BaseRule] = None):
        self.rules = rules or [AmountMaxLimitRule(), EmailDomainRule(), UserIdUUIDRule()]

    def run(self, payload: Dict[str, Any]) -> List[RuleResultSchema]:
        results = []
        for rule in self.rules:
            results.append(rule.apply(payload))
        return results