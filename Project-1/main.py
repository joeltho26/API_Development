from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    
my_posts = [{
    "title" : "Food",
    "content" : "Italy metropolitan pizza",
    "id" : 1    
    },
    {
    "title" : "Travel",
    "content" : "India Taj Mahal",
    "id" : 2  
    }     
]

@app.get("/")
async def get_message():
    return {"mesage":"Adam & Eve"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

# @app.post("/createposts")
# def create_post(payload: dict = Body(...)):
#     return {"new_post": {f"title: {payload['title']}, content: {payload['content']}"}}

# @app.post("/createposts")
# def create_post(payload: Post):
#     return {"new_post": {f"title: {payload.title}, content: {payload.content}, published: {payload.published}, rating: {payload.rating}"}}

# @app.post("/posts")
# def create_post(payload: Post):
#     my_posts.append(payload)
#     return {"data": payload.model_dump()}

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post

@app.post("/posts")
def create_post(payload: Post):
    data = payload.model_dump()
    data['id'] = randrange(1,10000000)
    my_posts.append(data)
    return {"data": my_posts}

@app.get("/posts/latest")
def get_latest_post():
    return {"latest_post": my_posts[len(my_posts)-1]}

@app.get("/posts/{id}")
def get_post(id: int):
    return {"post": find_post(id)}
    