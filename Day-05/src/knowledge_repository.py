from dataclasses import dataclass
from typing import Optional


ROLE_LEVELS = {
    "Employee": 1,
    "Manager": 2,
    "Admin": 3,
}


@dataclass(frozen=True)
class User:
    user_id: str
    role_name: str
    is_active: bool = True


@dataclass(frozen=True)
class FAQ:
    faq_id: int
    question: str
    answer: str
    required_role: str
    is_active: bool = True


class RepositoryError(Exception):
    """Base exception for knowledge repository errors."""


class UserNotFoundError(RepositoryError):
    """Raised when the user does not exist."""


class AccessDeniedError(RepositoryError):
    """Raised when the user cannot access an FAQ."""


class FAQNotFoundError(RepositoryError):
    """Raised when the FAQ does not exist."""


class KnowledgeRepository:
    def __init__(self, users: dict, faqs: dict):
        self.users = users
        self.faqs = faqs
        self.audit_logs = []

    def lookup(self, user_id: str, faq_id: int) -> dict:
        user = self.users.get(user_id)

        if user is None or not user.is_active:
            self.audit_logs.append({
                "user_id": user_id,
                "faq_id": faq_id,
                "action": "LOOKUP",
                "status": "DENIED",
            })
            raise UserNotFoundError("User not found or inactive.")

        faq = self.faqs.get(faq_id)

        if faq is None or not faq.is_active:
            self.audit_logs.append({
                "user_id": user_id,
                "faq_id": faq_id,
                "action": "LOOKUP",
                "status": "NOT_FOUND",
            })
            raise FAQNotFoundError("FAQ not found.")

        user_level = ROLE_LEVELS.get(user.role_name)
        required_level = ROLE_LEVELS.get(faq.required_role)

        if user_level is None or required_level is None:
            self.audit_logs.append({
                "user_id": user_id,
                "faq_id": faq_id,
                "action": "LOOKUP",
                "status": "DENIED",
            })
            raise AccessDeniedError("Access denied.")

        if user_level < required_level:
            self.audit_logs.append({
                "user_id": user_id,
                "faq_id": faq_id,
                "action": "LOOKUP",
                "status": "DENIED",
            })
            raise AccessDeniedError(
                "You are not authorized to access this FAQ."
            )

        self.audit_logs.append({
            "user_id": user_id,
            "faq_id": faq_id,
            "action": "LOOKUP",
            "status": "SUCCESS",
        })

        return {
            "status": "SUCCESS",
            "faq_id": faq.faq_id,
            "question": faq.question,
            "answer": faq.answer,
            "access": "GRANTED",
        }
