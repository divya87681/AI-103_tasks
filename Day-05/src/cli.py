import argparse
import json
import sys

from knowledge_repository import RepositoryError
from postgres_adapter import PostgresKnowledgeRepository


def main():
    parser = argparse.ArgumentParser(
        description="Look up an FAQ with PostgreSQL role-based access."
    )
    parser.add_argument("--user-id", required=True, help="User identifier")
    parser.add_argument("--faq-id", required=True, type=int, help="FAQ ID")
    args = parser.parse_args()

    repository = PostgresKnowledgeRepository()

    try:
        response = repository.lookup(args.user_id, args.faq_id)
        print(json.dumps(response, indent=2))
        return 0
    except RepositoryError as exc:
        print(
            json.dumps({"status": "ERROR", "message": str(exc)}, indent=2)
        )
        return 1
    except Exception as exc:
        print(
            json.dumps({"status": "ERROR", "message": str(exc)}, indent=2)
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
