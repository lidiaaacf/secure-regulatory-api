from typing import Dict, Any
from app.contexts.base import ValidationContext, ValidationContextEnum


class RulesEngine:
    def __init__(self):
        self.contexts: Dict[str, ValidationContext] = {}

    def register_context(self, context: ValidationContext):
        self.contexts[context.name] = context

    def run(self, payload: dict, context: ValidationContextEnum):
        context_name = context.value
        if context_name not in self.contexts:
            raise ValueError(f"Unknown context: {context_name}")
        return self.contexts[context_name].evaluate(payload)
