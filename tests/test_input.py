import pytest
from pydantic import ValidationError
from app.schemas.input import DynamicInputSchema, TransactionInput


def test_dynamic_input_valid():
    payload = {"payload": {"key": "value"}}

    schema = DynamicInputSchema(**payload)

    assert schema.payload["key"] == "value"


def test_missing_payload_key():
    payload = {"user": {"id": "550e8400-e29b-41d4-a716-446655440000"}}

    with pytest.raises(ValidationError) as exc:
        DynamicInputSchema(**payload)

    errors = exc.value.errors()
    assert errors[0]["type"] == "missing"


def test_dynamic_input_none():
    with pytest.raises(ValidationError) as exc:
        DynamicInputSchema(payload=None)

    errors = exc.value.errors()
    assert errors[0]["type"] == "dict_type"


def test_dynamic_input_extra_field():
    with pytest.raises(ValidationError) as exc:
        DynamicInputSchema(payload={"a": 1}, extra_field="x")

    errors = exc.value.errors()
    assert errors[0]["type"] == "extra_forbidden"


def test_dynamic_input_empty_payload():
    payload = {"payload": {}}

    with pytest.raises(ValidationError) as exc:
        DynamicInputSchema(**payload)

    errors = exc.value.errors()
    assert any("Payload cannot be empty" in e["msg"] for e in errors)


def test_nested_complex_json():
    payload = {
        "payload": {
            "level1": {"level2": {"level3": {"amount": 100}}},
            "list_field": [{"id": 1}, {"id": 2}],
        }
    }

    schema = DynamicInputSchema(**payload)

    assert schema.payload["level1"]["level2"]["level3"]["amount"] == 100
    assert len(schema.payload["list_field"]) == 2


def test_invalid_type():
    payload = {"payload": "this should be a dict"}

    with pytest.raises(ValidationError) as exc:
        DynamicInputSchema(**payload)

    errors = exc.value.errors()
    assert errors[0]["type"] == "dict_type"


def test_transaction_valid():
    data = {
        "transaction_id": "tx1",
        "customer_id": "cust1",
        "amount": 100.5,
        "currency": "USD",
        "country": "br",
        "device_trusted": True,
    }

    schema = TransactionInput(**data)

    assert schema.country == "BR"
    assert schema.amount == 100.5
    assert schema.device_trusted is True


def test_transaction_default_device_trusted():
    data = {
        "transaction_id": "tx1",
        "customer_id": "cust1",
        "amount": 100.5,
        "currency": "USD",
        "country": "BR",
    }

    schema = TransactionInput(**data)

    assert schema.device_trusted is False


def test_transaction_invalid_amount():
    with pytest.raises(ValidationError) as exc:
        TransactionInput(
            transaction_id="tx1",
            customer_id="cust1",
            amount=0,
            currency="USD",
            country="BR",
        )

    errors = exc.value.errors()
    assert errors[0]["type"] == "greater_than"


def test_transaction_invalid_currency():
    with pytest.raises(ValidationError) as exc:
        TransactionInput(
            transaction_id="tx1",
            customer_id="cust1",
            amount=100,
            currency="GBP",
            country="BR",
        )

    errors = exc.value.errors()
    assert errors[0]["type"] == "literal_error"


def test_transaction_invalid_country_length():
    with pytest.raises(ValidationError) as exc:
        TransactionInput(
            transaction_id="tx1",
            customer_id="cust1",
            amount=100,
            currency="USD",
            country="BRA",
        )

    errors = exc.value.errors()
    assert errors[0]["type"] == "string_too_long"


def test_transaction_empty_transaction_id():
    with pytest.raises(ValidationError) as exc:
        TransactionInput(
            transaction_id="",
            customer_id="cust1",
            amount=100,
            currency="USD",
            country="BR",
        )

    errors = exc.value.errors()
    assert errors[0]["type"] == "string_too_short"


def test_transaction_strict_mode():
    with pytest.raises(ValidationError) as exc:
        TransactionInput(
            transaction_id="tx1",
            customer_id="cust1",
            amount="100",
            currency="USD",
            country="BR",
        )

    errors = exc.value.errors()
    assert errors[0]["type"] == "float_type"


def test_transaction_extra_field():
    with pytest.raises(ValidationError) as exc:
        TransactionInput(
            transaction_id="tx1",
            customer_id="cust1",
            amount=100,
            currency="USD",
            country="BR",
            unexpected="value",
        )

    errors = exc.value.errors()
    assert errors[0]["type"] == "extra_forbidden"
