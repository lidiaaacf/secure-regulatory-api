from app.rules.engine import RulesEngine
from app.contexts.generic import GenericValidationContext
from app.contexts.transaction import TransactionValidationContext


def create_engine() -> RulesEngine:
    engine = RulesEngine()
    engine.register_context(GenericValidationContext())
    engine.register_context(TransactionValidationContext())
    return engine
