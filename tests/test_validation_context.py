from app.contexts.base import ValidationContext
from types import SimpleNamespace


class FakeRule:
    def evaluate(self, payload):
        return SimpleNamespace(status="passed")


class FakeContext(ValidationContext):
    name = "fake"

    def get_rules(self):
        return [FakeRule(), FakeRule()]


def test_context_initializes_rules():
    context = FakeContext()

    assert len(context.rules) == 2


def test_context_evaluate_runs_all_rules():
    called = 0

    class FakeRule:
        def evaluate(self, payload):
            nonlocal called
            called += 1
            return SimpleNamespace(status="passed")

    class FakeContext(ValidationContext):
        name = "fake"

        def get_rules(self):
            return [FakeRule(), FakeRule(), FakeRule()]

    context = FakeContext()

    results = context.evaluate({"a": 1})

    assert called == 3
    assert len(results) == 3


def test_context_passes_payload_to_rules():
    received_payload = None

    class FakeRule:
        def evaluate(self, payload):
            nonlocal received_payload
            received_payload = payload
            return SimpleNamespace(status="passed")

    class FakeContext(ValidationContext):
        name = "fake"

        def get_rules(self):
            return [FakeRule()]

    context = FakeContext()
    payload = {"amount": 100}

    context.evaluate(payload)

    assert received_payload == payload


def test_context_with_no_rules():
    class EmptyContext(ValidationContext):
        name = "empty"

        def get_rules(self):
            return []

    context = EmptyContext()

    results = context.evaluate({"a": 1})

    assert results == []
