from typing import List
from app.contexts.base import ValidationContext, ValidationContextEnum
from app.rules.base import BaseRule

from app.rules.internal.ip_whitelist_rule import IPWhitelistRule
from app.rules.internal.payload_size_rule import PayloadSizeRule
from app.rules.internal.unsafe_pattern_rule import UnsafePatternRule


class InternalAPIValidationContext(ValidationContext):

    name = ValidationContextEnum.internal_api.value

    def get_rules(self) -> List[BaseRule]:
        return [
            IPWhitelistRule(),
            PayloadSizeRule(),
            UnsafePatternRule(),
        ]
