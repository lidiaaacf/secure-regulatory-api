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
            status="passed" if passed else "failed",
            severity="low" if passed else "high",
            message="Payload size ok" if passed else "Payload too large",
        )
