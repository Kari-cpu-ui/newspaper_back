from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserOut
from typing import List

router = APIRouter()

@router.get("/usuarios", response_model=List[UserOut])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(User).all()