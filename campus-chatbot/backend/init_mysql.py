import os

from dotenv import load_dotenv

from backend.db import create_database_if_missing, create_tables


def main():
    load_dotenv()
    db_name = os.getenv("MYSQL_DB_NAME", "campusinfo")
    create_database_if_missing(db_name)
    create_tables()
    print(f"MySQL database initialized successfully: {db_name}")


if __name__ == "__main__":
    main()
