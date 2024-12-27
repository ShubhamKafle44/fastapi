from .. import models, schemas
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter()
@router.get('/posts', response_model=List[schemas.Post])
def get_posts(db: Session =  Depends(get_db)):
    # cursor.execute("""SELECT * FROM social_media""")
    # posts = cursor.fetchall()
    # print(posts)
    posts = db.query(models.Post)
    print(type(posts))
    posts = db.query(models.Post).all()


    return posts


@router.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO social_media(title, content, published) VALUES(%s, %s, %s) RETURNING*""",(post.title,post.content, post.published))
    # new_post =  cursor.fetchone()
    # conn.commit()
    # return{f"new_post created": new_post}
    
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post




@router.get('/posts/{id}')
def get_posts(id: int,db: Session = Depends(get_db)):
    print(id)
    # cursor.execute("""SELECT * from social_media WHERE id = %s""",(str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        # response.status_code =status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} was not found. "}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"the id {id} was not found.")
    return post


@router.delete('/posts/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)


    # cursor.execute("""DELETE FROM social_media WHERE id = %s RETURNING* """, (str(id),))
    # delete_post= cursor.fetchone()
    # print(delete_post)
    # conn.commit()

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id {id} doesnot exist")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put('/posts/{id}')
def update_posts(id: int, post:schemas.PostCreate, db: Session = Depends(get_db)):

    # cursor.execute("""UPDATE social_media SET title = %s, content = %s, published =%s WHERE id = %s RETURNING* """, (post.title, post.content,post.published, id))
    # updated_post =  cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    update_post = post_query.first()

    if update_post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id {id} doesnot exist")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


