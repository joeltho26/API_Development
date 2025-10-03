from fastapi import FastAPI, Response, status, HTTPException
from .database import create_db_and_tables, SessionDep
from .model import Posts
from sqlmodel import select
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def get_message():
    return {"mesage":"API Development Demo. Welcome!"}

@app.get("/posts")
def get_posts(session: SessionDep):
    posts = session.exec(select(Posts)).all()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Posts, session: SessionDep):
    session.add(post)
    session.commit()
    session.refresh(post)
    return {"result": "created post successfully!",
            "data": post}

@app.get("/posts/latest")
def get_latest_post(session: SessionDep):
    posts = session.exec(select(Posts)).all()
    for post in posts:
        pass
    return {"data": post}

@app.get("/posts/{id}")
def get_post(id: int, session: SessionDep):
    post = session.get(Posts, id)
    # post = session.exec(select(Posts).filter(Posts.id == id)).first()
    # post = session.exec(select(Posts).where(Posts.id == id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found!")
    return {"post": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, session: SessionDep):
    post = session.exec(select(Posts).filter(Posts.id == id), execution_options={'synchronize_session': False})
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found to delete!")
    session.delete(post.first())
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Posts, session: SessionDep):
    # update_post = session.exec(select(Post).where(Post.id == id)).one()
    # update_post = session.get(Posts, id)
    updated_post = session.exec(select(Posts).where(Posts.id == id), execution_options={'synchronize_session': False}).one()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                           detail=f"post with id {id} not found to update!")
    # val = post.model_dump()
    # val['id'] = id
    updated_post.content = post.content
    updated_post.title = post.title
    # session.add(updated_post.sqlmodel_update(val))
    session.add(updated_post)
    session.commit()
    session.refresh(updated_post)
    return Response(status_code=status.HTTP_200_OK)
    
    