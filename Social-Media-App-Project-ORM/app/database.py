from sqlmodel import create_engine, SQLModel, Session
from dotenv import load_dotenv
import os
from typing_extensions import Annotated
from fastapi import Depends

load_dotenv()
database_password = os.getenv("POSTGRES_PASSWORD")
database_name = os.getenv("DATABASE_NAME")
database_user = os.getenv("DATABASE_USER")
database_host = os.getenv("DATABASE_HOST")
database_port = os.getenv("DATABASE_PORT")

postgresql_database_url = f"postgresql://{database_user}:{database_password}@{database_host}/{database_name}"
engine = create_engine(url=postgresql_database_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_session)]

