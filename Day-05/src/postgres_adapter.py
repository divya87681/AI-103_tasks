import os

import psycopg
from psycopg.rows import dict_row

from knowledge_repository import (
    ROLE_LEVELS,
    AccessDeniedError,
    FAQNotFoundError,
    RepositoryError,
    UserNotFoundError,
)


class PostgresKnowledgeRepository:
    """PostgreSQL-backed FAQ repository with role checks and audit logging."""

    def __init__(self, database_url=None):
        self.database_url = database_url or os.getenv("DATABASE_URL")

    def lookup(self, user_id: str, faq_id: int) -> dict:
        if not self.database_url:
            raise RepositoryError(
                "DATABASE_URL is not configured. "
                "Set the database connection string before using PostgreSQL."
            )

        error_type = None
        error_message = None
        result = None
        audit_status = "ERROR"

        try:
            with psycopg.connect(self.database_url) as conn:
                with conn.cursor(row_factory=dict_row) as cur:
                    cur.execute(
                        """
                        SELECT role_name, is_active
                        FROM user_roles
                        WHERE user_id = %s
                        """,
                        (user_id,),
                    )
                    user = cur.fetchone()

                    if user is None or not user["is_active"]:
                        audit_status = "DENIED"
                        error_type = UserNotFoundError
                        error_message = "User not found or inactive."

                    else:
                        cur.execute(
                            """
                            SELECT faq_id, question, answer, required_role
                            FROM faqs
                            WHERE faq_id = %s AND is_active = TRUE
                            """,
                            (faq_id,),
                        )
                        faq = cur.fetchone()

                        if faq is None:
                            audit_status = "NOT_FOUND"
                            error_type = FAQNotFoundError
                            error_message = "FAQ not found."

                        else:
                            user_level = ROLE_LEVELS.get(user["role_name"])
                            required_level = ROLE_LEVELS.get(
                                faq["required_role"]
                            )

                            if (
                                user_level is None
                                or required_level is None
                                or user_level < required_level
                            ):
                                audit_status = "DENIED"
                                error_type = AccessDeniedError
                                error_message = (
                                    "You are not authorized to access this FAQ."
                                )
                            else:
                                audit_status = "SUCCESS"
                                result = {
                                    "status": "SUCCESS",
                                    "faq_id": faq["faq_id"],
                                    "question": faq["question"],
                                    "answer": faq["answer"],
                                    "access": "GRANTED",
                                }

                    cur.execute(
                        """
                        INSERT INTO audit_logs
                            (user_id, faq_id, action, status)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (user_id, faq_id, "LOOKUP", audit_status),
                    )

        except psycopg.Error as exc:
            raise RepositoryError(
                "PostgreSQL operation failed. Check the connection, "
                "database availability, schema, and permissions."
            ) from exc

        # Raise after the transaction commits so denied/not-found
        # lookup audit records are retained.
        if error_type is not None:
            raise error_type(error_message)

        return result
