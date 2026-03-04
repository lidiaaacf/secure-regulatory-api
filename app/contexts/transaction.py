from app.contexts.base import ValidationContext
from app.rules.business_rules import (
    AmountMaxLimitRule,
    EmailDomainRule,
)
from app.rules.security_rules import (
    NoSuspiciousKeysRule,
    NoScriptInjectionRule,
)
from app.contexts.base import ValidationContextEnum


class TransactionValidationContext(ValidationContext):
    name = ValidationContextEnum.transaction.value

    def get_rules(self):
        return [
            AmountMaxLimitRule(),
            EmailDomainRule(),
            NoSuspiciousKeysRule(),
            NoScriptInjectionRule(),
        ]
