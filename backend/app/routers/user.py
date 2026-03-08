from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal

class ArticleUpdate(BaseModel):
    title: str
    content: str


# Función que en entrega la sesion  a FastAPI y la cierra automaticamente 
def get_db():
    db = SessionLocal() # Creo una sesión de base de datos
    try:
        yield db # Entrego la sesión a FastAPI para que la use en las rutas
    finally:
        db.close() # Cierro la sesión después de que se haya usado


   