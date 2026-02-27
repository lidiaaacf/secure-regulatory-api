from app.rules.base import BaseRule
from app.schemas.report import RuleResultSchema
from typing import Dict, Any
from uuid import UUID
import re

class AmountMaxLimitRule(BaseRule):
    def apply(self, payload: Dict[str, Any]) -> RuleResultSchema:
        amount = payload.get("amount", 0)
        if amount <= 10000:
            return RuleResultSchema(rule="amount_max_limit", status="passed", severity="high")
        return RuleResultSchema(rule="amount_max_limit", status="failed", severity="high",
                                details=f"Amount {amount} exceeds maximum 10000")

class EmailDomainRule(BaseRule):
    allowed_domains = ["example.com", "company.com"]
    def apply(self, payload: Dict[str, Any]) -> RuleResultSchema:
        email = payload.get("email", "")
        domain = email.split("@")[-1] if "@" in email else ""
        if domain in self.allowed_domains:
            return RuleResultSchema(rule="email_domain_check", status="passed", severity="medium")
        return RuleResultSchema(rule="email_domain_check", status="failed", severity="medium",
                                details=f"Email domain '{domain}' not allowed")

class UserIdUUIDRule(BaseRule):
    def apply(self, payload: Dict[str, Any]) -> RuleResultSchema:
        user_id = payload.get("user_id", "")
        try:
            UUID(str(user_id))
            return RuleResultSchema(rule="user_id_uuid_check", status="passed", severity="high")
        except ValueError:
            return RuleResultSchema(rule="user_id_uuid_check", status="failed", severity="high",
                                    details="user_id is not a valid UUID")