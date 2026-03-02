from typing import Any, Dict
from app.rules.base import BaseRule
from app.schemas.report import RuleResultSchema

class NoEmptyStringsRule(BaseRule):
    name = "no_empty_strings"

    def evaluate(self, payload: Dict[str, Any]) -> RuleResultSchema:
        empty_found = False

        def scan(obj):
            nonlocal empty_found
            if isinstance(obj, dict):
                for value in obj.values():
                    scan(value)
            elif isinstance(obj, list):
                for item in obj:
                    scan(item)
            elif isinstance(obj, str) and obj.strip() == "":
                empty_found = True

        scan(payload)

        if empty_found:
            return RuleResultSchema(
                rule=self.name,
                status="failed",
                severity="medium",
                details="Empty string detected"
            )

        return RuleResultSchema(
            rule=self.name,
            status="passed",
            severity="low"
        )


class NoSuspiciousKeysRule(BaseRule):
    name = "no_suspicious_keys"
    SUSPICIOUS = {"password", "secret", "token"}

    def evaluate(self, payload: Dict[str, Any]) -> RuleResultSchema:
        found = []

        def scan(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key.lower() in self.SUSPICIOUS:
                        found.append(key)
                    scan(value)
            elif isinstance(obj, list):
                for item in obj:
                    scan(item)

        scan(payload)

        if found:
            return RuleResultSchema(
                rule=self.name,
                status="failed",
                severity="high",
                details=f"Suspicious keys detected: {found}"
            )

        return RuleResultSchema(
            rule=self.name,
            status="passed",
            severity="low"
        )