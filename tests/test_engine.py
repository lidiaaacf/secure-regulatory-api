from app.rules.engine import RulesEngine
from types import SimpleNamespace
import pytest


def test_engine_register_context():
    engine = RulesEngine()

    class FakeContext:
        name = "credit"

        def evaluate(self, payload):
            return []

    engine.register_context(FakeContext())

    assert "credit" in engine.contexts


def test_engine_all_pass():
    engine = RulesEngine()

    class FakeContext:
        name = "credit"

        def evaluate(self, payload):
            return [SimpleNamespace(status="passed")]

    engine.register_context(FakeContext())

    fake_enum = SimpleNamespace(value="credit")

    results = engine.run({"amount": 5000}, context=fake_enum)

    assert all(r.status == "passed" for r in results)


def test_engine_unknown_context():
    engine = RulesEngine()

    fake_enum = SimpleNamespace(value="unknown")

    with pytest.raises(ValueError):
        engine.run({}, context=fake_enum)


def test_engine_calls_evaluate():
    engine = RulesEngine()
    called = False

    class FakeContext:
        name = "credit"

        def evaluate(self, payload):
            nonlocal called
            called = True
            return []

    engine.register_context(FakeContext())

    fake_enum = SimpleNamespace(value="credit")

    engine.run({"a": 1}, context=fake_enum)

    assert called is True
