from pydantic import ( 
 BaseModel,
 EmailStr
 )
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str # se envia desde fronend, luego se convierte en hash 
    role: str  # 'redactor' o 'editor'

class UserOut(UserBase):
    id: int
    role: str
    created_at: datetime

    class Config:
        orm_mode = True # Permite convertir objetos SQLAlchemy a Pydantic

# ARTICULOS

class ArticleBase(BaseModel):
    title: str
    content: str
    section: Optional[str] = None

class ArticleCreate(ArticleBase):
    author_id: int  # ID del redactor que crea el artículo

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    section: Optional[str] = None
    status: Optional[str] = None  # 'borrador', 'revision', 'publicado'
    importance: Optional[int] = None
    editor_id: Optional[int] = None  # ID del editor que revisa el artículo

class ArticleOut(ArticleBase):
    id: int
    status: str
    importance: int
    author_id: int
    editor_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

    # SUSCRIPCIONESç

class SubscriptionBase(BaseModel):
    email: EmailStr

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionRead(SubscriptionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True 
