from sqlalchemy import create_engine

from nlp_bot_scalable.config.settings import settings
from nlp_bot_scalable.database.models import Base


engine = create_engine(
    settings.database_url,
    echo=settings.debug,
)


def create_tables():
    Base.metadata.create_all(engine)