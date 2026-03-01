import os
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Float,
    text,
    select,
    delete,
)
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load .env automatically for backend commands and app startup.
load_dotenv()


def _build_database_url():
    # Preferred: explicit URL if user wants full control.
    explicit_url = os.getenv("DATABASE_URL")
    if explicit_url:
        return explicit_url

    # Safe fallback: build URL from plain env fields (handles special chars in password).
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "root")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = int(os.getenv("DB_PORT", "3306"))
    db_name = os.getenv("MYSQL_DB_NAME", "campusinfo")

    return URL.create(
        drivername="mysql+pymysql",
        username=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        database=db_name,
    )


DATABASE_URL = _build_database_url()
metadata = MetaData()

events = Table(
    "events",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(255)),
    Column("description", Text),
    Column("start_date", DateTime),
    Column("end_date", DateTime),
    Column("location", String(255)),
    Column("organizer", String(255)),
    Column("category", String(100))  # cultural, technical, sports, etc.
)

contacts = Table(
    "contacts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(255)),
    Column("department", String(255)),
    Column("designation", String(255)),
    Column("email", String(255)),
    Column("phone", String(50)),
    Column("office_location", String(255))
)

buildings = Table(
    "buildings",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(255)),
    Column("code", String(50)),
    Column("latitude", Float),
    Column("longitude", Float),
    Column("departments", Text),  # comma-separated
    Column("facilities", Text)
)

procedures = Table(
    "procedures",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(255)),
    Column("category", String(100)),  # admission, fee payment, etc.
    Column("steps", Text),  # JSON array of steps
    Column("documents_required", Text),
    Column("timeline", String(255))
)
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)

documents = Table(
    "documents",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("source", String(255)),
    Column("title", String(512)),
    Column("content", Text),
)

othersites = Table(
    "othersites",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False),
    Column("link", String(1024), nullable=False),
)

otherwebsites = Table(
    "otherwebsites",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False),
    Column("site_url", String(1024), nullable=False),
)


def create_tables():
    metadata.create_all(engine)


def create_database_if_missing(db_name: str = "campusinfo"):
    # Connect to MySQL server without selecting app DB to create it if missing.
    admin_url = os.getenv("MYSQL_ADMIN_URL")
    if not admin_url:
        admin_url = URL.create(
            drivername="mysql+pymysql",
            username=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "root"),
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            database="mysql",
        )
    admin_engine = create_engine(admin_url, echo=False, pool_pre_ping=True)
    with admin_engine.begin() as conn:
        conn.execute(
            text(
                f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        )


def insert_document(source: str, title: str, content: str):
    with engine.begin() as conn:
        conn.execute(documents.insert().values(source=source, title=title, content=content))


def list_otherwebsites():
    with engine.connect() as conn:
        rows = conn.execute(
            select(otherwebsites.c.id, otherwebsites.c.name, otherwebsites.c.site_url).order_by(otherwebsites.c.id)
        ).mappings().all()
        return [dict(row) for row in rows]


def replace_otherwebsites(rows):
    # rows: list[{"name": str, "site_url": str}]
    with engine.begin() as conn:
        conn.execute(delete(otherwebsites))
        if rows:
            conn.execute(otherwebsites.insert(), rows)
