from typing import Dict, Any
from app.rules.base import BaseRule
from app.schemas.report import RuleResultSchema


class PayloadSizeRule(BaseRule):

    name = "payload_size_check"

    MAX_SIZE = 50000

    def evaluate(self, payload):

        size = payload.get("payload_size", 0)

        passed = size < self.MAX_SIZE

        return RuleResultSchema(
            rule=self.name,
            passed=passed,
            message="Payload size ok" if passed else "Payload too large",
        )
