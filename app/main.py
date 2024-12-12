from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool=True
    rating: Optional[int] = None
while(True):
    try: 
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password = 'Sh9846702835@' , cursor_factory = RealDictCursor)
        cursor  = conn.cursor()
        print("Database connection succesful")
        break
    except Exception as err:
        print("failed")
        print(err)
        time.sleep(2)

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
    cursor.execute("""SELECT * FROM social_media""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO social_media(title, content, published) VALUES(%s, %s, %s) RETURNING*""",(post.title,post.content, post.published))
    new_post =  cursor.fetchone()
    conn.commit()
    return{f"new_post created": new_post}

@app.get('/posts/{id}')
def get_posts(id: int, response: Response):
    print(id)
    cursor.execute("""SELECT * from social_media WHERE id = %s""",(str(id),))
    post = cursor.fetchone()
    if not post:
        # response.status_code =status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} was not found. "}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"the id {id} was not found.")
    return {"data":post }


@app.delete('/posts/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):

    cursor.execute("""DELETE FROM social_media WHERE id = %s RETURNING* """, (str(id),))
    delete_post= cursor.fetchone()
    print(delete_post)
    conn.commit()
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id {id} doesnot exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put('/posts/{id}')
def update_posts(id: int, post:Post):

    cursor.execute("""UPDATE social_media SET title = %s, content = %s, published =%s WHERE id = %s RETURNING* """, (post.title, post.content,post.published, id))
    updated_post =  cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id {id} doesnot exist")
 
    return  {"data": updated_post}