from typing import Any, Dict
from app.rules.base import BaseRule
from app.schemas.report import RuleResultSchema
from bs4 import BeautifulSoup


class NoScriptInjectionRule(BaseRule):
    name = "no_script_injection"

    def evaluate(self, payload: Dict[str, Any]) -> RuleResultSchema:
        found = False

        def scan(obj: Any):
            nonlocal found
            if isinstance(obj, dict):
                for value in obj.values():
                    scan(value)
            elif isinstance(obj, list):
                for item in obj:
                    scan(item)
            elif isinstance(obj, str):
                # Parse HTML safely
                soup = BeautifulSoup(obj, "html.parser")
                if soup.find("script"):
                    found = True

        scan(payload)

        if found:
            return RuleResultSchema(
                rule=self.name,
                status="failed",
                severity="critical",
                details="Script injection pattern detected",
            )

        return RuleResultSchema(rule=self.name, status="passed", severity="low")


class NoSuspiciousKeysRule(BaseRule):
    name = "no_suspicious_keys"
    SUSPICIOUS = {"password", "secret", "token"}

    def evaluate(self, payload: Dict[str, Any]) -> RuleResultSchema:
        found = []

        def scan(obj: Any):
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
                details=f"Suspicious keys detected: {list(set(found))}",
            )

        return RuleResultSchema(rule=self.name, status="passed", severity="low")
