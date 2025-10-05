from fastapi import FastAPI
from .database import engine, Base
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# Base.metadata.create_all(bind=engine) => used to create tables, columns, etc in actual postgres/sql server, we ignore it since, we have alembic setup to do the same.

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
    "https://www.google.com"
] 

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"]
                   )

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def get_message():
    return {"mesage":"API Development Demo. Welcome!"}


