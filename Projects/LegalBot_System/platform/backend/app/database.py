from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings

connect_args = (
    {"check_same_thread": False}
    if settings.DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Columns added after initial release — create_all only creates missing tables.
_NEW_COLUMNS: dict[str, str] = {
    "segment": "VARCHAR DEFAULT ''",
    "language": "VARCHAR DEFAULT 'en'",
    "retrieved_chunks": "JSON",
    "citations": "JSON",
    "feedback_score": "INTEGER DEFAULT 0",
}


def migrate() -> None:
    insp = inspect(engine)
    if "conversations" not in insp.get_table_names():
        return
    existing = {c["name"] for c in insp.get_columns("conversations")}
    with engine.begin() as conn:
        for name, ddl in _NEW_COLUMNS.items():
            if name not in existing:
                conn.execute(
                    text(f"ALTER TABLE conversations ADD COLUMN {name} {ddl}")
                )
