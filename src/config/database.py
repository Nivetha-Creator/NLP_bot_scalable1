from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.settings import settings
from src.nlp_bot_scalable.database.models import Base


# Find project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Database file path
DATABASE_FILE = BASE_DIR / "chatbot.db"

# Create database URL
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create database tables
Base.metadata.create_all(bind=engine)
