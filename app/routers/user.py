from .. import utils, models, schemas
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter

from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user( user:schemas.UserCreate, db: Session = Depends(get_db)):

    #first hash the password

    
    hashed_pass = utils.pwd_context.hash(user.password)
    user.password = hashed_pass

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def get_user( id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user
