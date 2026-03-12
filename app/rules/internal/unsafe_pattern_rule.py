import re
from app.rules.base import BaseRule
from app.schemas.report import RuleResultSchema

BLOCK_PATTERNS = [r"(select\s)", r"(drop\s)", r"<script>", r"\.\./"]


class UnsafePatternRule(BaseRule):

    name = "unsafe_pattern"

    def evaluate(self, payload):

        text = str(payload.get("body", {}))

        for pattern in BLOCK_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return RuleResultSchema(
                    rule=self.name,
                    status="failed",
                    severity="critical",
                    message=f"Unsafe pattern detected: {pattern}",
                )

        return RuleResultSchema(
            rule=self.name,
            status="passed",
            severity="low",
            message="No unsafe patterns detected",
        )
