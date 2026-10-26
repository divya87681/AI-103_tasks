import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from knowledge_repository import (
    AccessDeniedError,
    FAQ,
    FAQNotFoundError,
    KnowledgeRepository,
    User,
    UserNotFoundError,
)


@pytest.fixture
def repository():
    users = {
        "employee_001": User("employee_001", "Employee"),
        "manager_001": User("manager_001", "Manager"),
        "admin_001": User("admin_001", "Admin"),
        "inactive_001": User("inactive_001", "Employee", False),
    }

    faqs = {
        1: FAQ(1, "Office timings?", "9 AM to 6 PM.", "Employee"),
        2: FAQ(2, "Leave approval?", "Ask your manager.", "Manager"),
        3: FAQ(3, "Database access?", "Follow admin procedures.", "Admin"),
    }

    return KnowledgeRepository(users, faqs)


def test_employee_can_read_employee_faq(repository):
    result = repository.lookup("employee_001", 1)
    assert result["status"] == "SUCCESS"
    assert result["access"] == "GRANTED"


def test_manager_can_read_manager_faq(repository):
    result = repository.lookup("manager_001", 2)
    assert result["status"] == "SUCCESS"


def test_admin_can_read_admin_faq(repository):
    result = repository.lookup("admin_001", 3)
    assert result["status"] == "SUCCESS"


def test_employee_cannot_read_manager_faq(repository):
    with pytest.raises(AccessDeniedError):
        repository.lookup("employee_001", 2)


def test_employee_cannot_read_admin_faq(repository):
    with pytest.raises(AccessDeniedError):
        repository.lookup("employee_001", 3)


def test_unknown_user_is_rejected(repository):
    with pytest.raises(UserNotFoundError):
        repository.lookup("unknown_user", 1)


def test_inactive_user_is_rejected(repository):
    with pytest.raises(UserNotFoundError):
        repository.lookup("inactive_001", 1)


def test_missing_faq_is_rejected(repository):
    with pytest.raises(FAQNotFoundError):
        repository.lookup("employee_001", 999)


def test_denied_lookup_is_audited(repository):
    with pytest.raises(AccessDeniedError):
        repository.lookup("employee_001", 2)

    assert repository.audit_logs[-1]["status"] == "DENIED"
