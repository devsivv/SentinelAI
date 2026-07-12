"""
Shared pytest fixtures. Keep this file thin — the goal (per SYSTEM_RULES.md §6)
is demo-breakage detection, not exhaustive coverage.
"""
import pytest


@pytest.fixture
def sample_case_id():
    return "c-test-0001"


@pytest.fixture
def sample_sms_payload():
    return {
        "case_id": "c-test-0001",
        "input_type": "sms",
        "payload": {"text": "Your account will be blocked. Update KYC immediately: http://bit.ly/fake-kyc"},
    }


@pytest.fixture
def sample_transaction_payload():
    return {
        "case_id": "c-test-0001",
        "input_type": "transaction",
        "payload": {"amount": 49999, "account_age_days": 2, "is_new_payee": True},
    }
