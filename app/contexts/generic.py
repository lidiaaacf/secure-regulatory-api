from app.contexts.base import ValidationContext
from app.rules.security_rules import (
    NoSuspiciousKeysRule,
    NoScriptInjectionRule,
)
from app.rules.business_rules import (
    NoEmptyStringsRule,
    UserIdUUIDRule,
)
from app.contexts.base import ValidationContextEnum


class GenericValidationContext(ValidationContext):
    name = ValidationContextEnum.generic.value

    def get_rules(self):
        return [
            NoEmptyStringsRule(),
            UserIdUUIDRule(),
            NoSuspiciousKeysRule(),
            NoScriptInjectionRule(),
        ]
