from fastapi import FastAPI, Response, status, HTTPException
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
    index = get_post_index(id)
    if index is not None:
        return my_posts[index]
    
def get_post_index(id) -> int:
    for idx,post in enumerate(my_posts):
        if post['id'] == id:
            return idx

def remove_post(id):
    index = get_post_index(id)
    if index is not None:
        my_posts.pop(index)
    return

def update(id, data):
    index = get_post_index(id)
    data['id'] = id
    my_posts[index] = data

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: Post):
    data = payload.model_dump()
    data['id'] = randrange(1,10000000)
    my_posts.append(data)
    return {"data": my_posts}

@app.get("/posts/latest")
def get_latest_post():
    return {"latest_post": my_posts[len(my_posts)-1]}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : f"post with id {id} not found!"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found!")
    return {"post": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found to delete!")
    remove_post(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, payload: Post):
    data = payload.model_dump()
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found to update!")
    update(id, data)
    return Response(status_code=status.HTTP_200_OK)
    
    