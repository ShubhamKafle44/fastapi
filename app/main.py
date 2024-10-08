from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool=True
    rating: Optional[int] = None

my_posts = [{"title": "title of post 1","content" :"content of the post","id":1},{"title": "title of post 2","content" :"content of the post 2","id":2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i




@app.get('/')
def root():
    return {"message": "Welcome to my api"}


@app.get('/posts')
def get_posts():
    return {"data": my_posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0,1000000)
    my_posts.append(post_dict)
    return{f"new_post created: {post_dict}"}
    
@app.get('/posts/{id}')
def get_posts(id: int, response: Response):
    print(id)
    post = find_post(id)
    if not post:
        # response.status_code =status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} was not found. "}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"the id {id} was not found.")
    return {"data":post }


@app.delete('/posts/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id {id} doesnot exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_posts(id: int, post:Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id {id} doesnot exist")
    
    post_dict =post.dict()
    my_posts[index] = post_dict
    
    return  {"data": my_posts}