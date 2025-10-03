from sqlmodel import Field, SQLModel, text, Column, DateTime
from datetime import datetime

class Posts(SQLModel, table=True):   
    id: int | None = Field(default=None, index=True, primary_key=True, nullable=False)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(sa_column_kwargs={"server_default": "True"}, nullable=False)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False, server_default=text("now()")))
    