from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from .config import settings

postgresql_database_url = f"postgresql://{settings.database_user}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"
engine = create_engine(url=postgresql_database_url)
Session_Local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# dependency
def get_db():
    db = Session_Local()
    try:
        yield db
    finally:
        db.close()

