# app/schemas/article.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# Schema base que define los campos comunes de un artículo
class ArticleBase(BaseModel):
    title: str
    content: str
    section: str

# Schema para crear artículos
class ArticleCreate(BaseModel):
    title: str
    content: str
    section: str    

# Schema para mostrar artículos (salida)
class ArticleOut(BaseModel):
    id: int
    title: str
    content: str
    section: str
    author_id: int
    editor_id: int | None
    status: str
    importance: int
    created_at: datetime
    updated_at: datetime

class Config:
      from_attributes = True

      # Modelo para actualizar articulo
class ArticleUpdate(BaseModel):
        title: str = None
        content: str = None
        section: str = None
        status: Optional[str] = None # "Borrador", "Revisión", "Publicado"
      
