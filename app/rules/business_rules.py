from app.rules.base import BaseRule
from app.schemas.report import RuleResultSchema
from typing import Dict, Any
from uuid import UUID

class AmountMaxLimitRule(BaseRule):
    name = "amount_max_limit"
    max_limit = 10000

    def evaluate(self, payload: Dict[str, Any]) -> RuleResultSchema:
        amount = payload.get("amount")

        if amount is None:
            return RuleResultSchema(
                rule=self.name,
                status="passed",
                severity="low",
                details="No amount field present"
            )

        if amount <= self.max_limit:
            return RuleResultSchema(
                rule=self.name,
                status="passed",
                severity="high"
            )

        return RuleResultSchema(
            rule=self.name,
            status="failed",
            severity="high",
            details=f"Amount {amount} exceeds maximum {self.max_limit}"
        )


class EmailDomainRule(BaseRule):
    name = "email_domain_check"
    allowed_domains = ["example.com", "company.com"]

    def evaluate(self, payload: Dict[str, Any]) -> RuleResultSchema:
        email = payload.get("email")

        if not email:
            return RuleResultSchema(
                rule=self.name,
                status="passed",
                severity="low",
                details="No email field present"
            )

        domain = email.split("@")[-1] if "@" in email else ""

        if domain in self.allowed_domains:
            return RuleResultSchema(
                rule=self.name,
                status="passed",
                severity="medium"
            )

        return RuleResultSchema(
            rule=self.name,
            status="failed",
            severity="medium",
            details=f"Email domain '{domain}' not allowed"
        )


class UserIdUUIDRule(BaseRule):
    name = "user_id_uuid_check"

    def evaluate(self, payload: Dict[str, Any]) -> RuleResultSchema:
        user_id = payload.get("user_id")

        if not user_id:
            return RuleResultSchema(
                rule=self.name,
                status="passed",
                severity="low",
                details="No user_id field present"
            )

        try:
            UUID(str(user_id))
            return RuleResultSchema(
                rule=self.name,
                status="passed",
                severity="high"
            )
        except ValueError:
            return RuleResultSchema(
                rule=self.name,
                status="failed",
                severity="high",
                details="user_id is not a valid UUID"
            )