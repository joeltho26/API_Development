from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
import os
import time

load_dotenv()
database_password = os.getenv("POSTGRES_PASSWORD")
database_name = os.getenv("DATABASE_NAME")
database_user = os.getenv("DATABASE_USER")
database_host = os.getenv("DATABASE_HOST")

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    
while True:
    try:
        conn = psycopg2.connect(host=database_host, database=database_name, 
                                user=database_user, password=database_password, 
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connecting to database failed!")
        print("Error: ",error)
        time.sleep(5)

@app.get("/")
async def get_message():
    return {"mesage":"API Development Demo. Welcome!"}

@app.get("/posts")
def get_posts():
    cursor.execute(query="select * from posts")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: Post):
    data = payload.model_dump()
    cursor.execute(query="insert into posts (title,content,published) values (%s,%s,%s)", 
                   vars=(data['title'], data['content'], data['published']))
    conn.commit()
    return {"data": "created post successfully!" }

@app.get("/posts/latest")
def get_latest_post():
    cursor.execute(query="select * from posts order by id desc")
    post = cursor.fetchone()
    return {"latest_post": post}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(query="select * from posts where id = %s", vars=str(id))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found!")
    return {"post": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    cursor.execute(query="delete from posts where id = %s returning *", vars=(str(id),))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found to delete!")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, payload: Post):
    data = payload.model_dump()
    cursor.execute(query="update posts set title = %s, content = %s where id = %s returning *", 
                   vars=(data['title'],data['content'],str(id)))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found to update!")
    return Response(status_code=status.HTTP_200_OK)
    
    