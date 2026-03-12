from app.rules.engine import RulesEngine
from app.contexts.generic import GenericValidationContext
from app.contexts.transaction import TransactionValidationContext
from app.contexts.internal_api import InternalAPIValidationContext


def create_engine() -> RulesEngine:
    engine = RulesEngine()

    engine.register_context(GenericValidationContext())
    engine.register_context(TransactionValidationContext())
    engine.register_context(InternalAPIValidationContext())

    print("Registered contexts:", engine.contexts.keys())

    return engine
