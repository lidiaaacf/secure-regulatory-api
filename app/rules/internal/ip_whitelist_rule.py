from typing import Dict, Any
from app.rules.base import BaseRule
from app.schemas.report import RuleResultSchema

INTERNAL_IP_PREFIXES = ["10.", "192.168.", "172.16."]


class IPWhitelistRule(BaseRule):

    name = "internal_ip_whitelist"

    def evaluate(self, payload: Dict[str, Any]) -> RuleResultSchema:

        ip = payload.get("ip")

        allowed = ip and any(ip.startswith(p) for p in INTERNAL_IP_PREFIXES)

        return RuleResultSchema(
            rule=self.name,
            status="passed" if allowed else "failed",
            severity="low" if allowed else "high",
            message="Internal IP verified" if allowed else "External IP blocked",
        )
