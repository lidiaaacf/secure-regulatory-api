import pytest
from app.rules.business_rules import (
    AmountMaxLimitRule,
    EmailDomainRule,
    UserIdUUIDRule,
    NoEmptyStringsRule,
)
from app.rules.security_rules import (
    NoScriptInjectionRule,
    NoSuspiciousKeysRule,
)


@pytest.mark.parametrize(
    "amount,expected_status",
    [
        (5000, "passed"),
        (10000, "passed"),
        (20000, "failed"),
    ],
)
def test_amount_max_limit(amount, expected_status):
    rule = AmountMaxLimitRule()
    result = rule.evaluate({"amount": amount})

    assert result.status == expected_status
    assert result.rule == "amount_max_limit"

    if expected_status == "failed":
        assert result.severity == "high"
    else:
        assert result.severity == "low"


def test_amount_missing_field():
    rule = AmountMaxLimitRule()
    result = rule.evaluate({})

    assert result.status == "passed"


def test_email_domain_allowed():
    rule = EmailDomainRule()
    result = rule.evaluate({"email": "user@company.com"})

    assert result.status == "passed"
    assert result.rule == "email_domain_allowed"
    assert result.severity == "low"


def test_email_domain_blocked():
    rule = EmailDomainRule()
    result = rule.evaluate({"email": "user@gmail.com"})

    assert result.status == "failed"
    assert result.severity == "medium"


def test_email_missing():
    rule = EmailDomainRule()
    result = rule.evaluate({})

    assert result.status == "passed"


def test_valid_uuid():
    rule = UserIdUUIDRule()
    result = rule.evaluate({"user_id": "550e8400-e29b-41d4-a716-446655440000"})

    assert result.status == "passed"
    assert result.rule == "user_id_must_be_uuid"


def test_invalid_uuid():
    rule = UserIdUUIDRule()
    result = rule.evaluate({"user_id": "invalid-uuid"})

    assert result.status == "failed"
    assert result.severity == "high"


def test_uuid_missing():
    rule = UserIdUUIDRule()
    result = rule.evaluate({})

    assert result.status == "passed"


def test_empty_string_detected():
    rule = NoEmptyStringsRule()
    result = rule.evaluate({"name": ""})

    assert result.status == "failed"
    assert result.severity == "medium"


def test_empty_string_nested():
    rule = NoEmptyStringsRule()
    result = rule.evaluate({"user": {"name": ""}})

    assert result.status == "failed"


def test_empty_string_not_present():
    rule = NoEmptyStringsRule()
    result = rule.evaluate({"name": "John"})

    assert result.status == "passed"


def test_script_injection_detected():
    rule = NoScriptInjectionRule()
    result = rule.evaluate({"comment": "<script>alert('xss')</script>"})

    assert result.status == "failed"
    assert result.severity == "critical"
    assert result.rule == "no_script_injection"


def test_script_injection_nested():
    rule = NoScriptInjectionRule()
    result = rule.evaluate({"user": {"bio": "Hello <script>malicious()</script>"}})

    assert result.status == "failed"


def test_script_injection_not_present():
    rule = NoScriptInjectionRule()
    result = rule.evaluate({"comment": "Hello world"})

    assert result.status == "passed"


def test_suspicious_key_detected():
    rule = NoSuspiciousKeysRule()
    result = rule.evaluate({"password": "123"})

    assert result.status == "failed"
    assert result.severity == "high"


def test_suspicious_key_nested():
    rule = NoSuspiciousKeysRule()
    result = rule.evaluate({"user": {"secret": "123"}})

    assert result.status == "failed"


def test_suspicious_key_not_present():
    rule = NoSuspiciousKeysRule()
    result = rule.evaluate({"username": "john"})

    assert result.status == "passed"
