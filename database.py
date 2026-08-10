from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# SQLite database stored as a local file in the project directory.
DATABASE_URL = "sqlite:///./tasks.db"


# SQLite requires this setting when used with FastAPI's request handling.

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Creates a new database session for each request.
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


# Base class used by SQLAlchemy models to define database tables.
Base = declarative_base()

