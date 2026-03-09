from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from app.database import get_db
from app.models.article import Article
from app.schemas.article import ArticleOut, ArticleCreate, ArticleUpdate
from typing import List

router = APIRouter()
# Rutas para artículos
@router.post("/", response_model=ArticleOut)
def crear_articulo(articulo: ArticleCreate, db: Session = Depends(get_db), author_id: int = 1):
    new_article = Article(
        title=articulo.title,
        content=articulo.content,
        section=articulo.section,
        author_id=author_id,
        status="borrador"  # por defecto
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article
# ----listar artículos (con filtros opcionales)---

@router.get("/", response_model=List[ArticleOut])
def listar_articulos(db: Session = Depends(get_db)):
    return db.query(Article).all()

# --- Filtrar por autor ---

@router.get("/by_author/{author_id}", response_model=List[ArticleOut])
def get_articles_by_author(author_id: int, db: Session = Depends(get_db)):
    return db.query(Article).filter(Article.author_id == author_id).all()

# --- Filtrar por estado ---

@router.get("/by_status/", response_model=List[ArticleOut])
def get_articles_by_status(
    status: str = Query(..., enum=["borrador", "revision", "publicado"]),
    db: Session = Depends(get_db)
):
    return db.query(Article).filter(Article.status == status).all()

# --- Publicar artículo (solo editor) ---

def check_editor_role(user_role: str):
    if user_role != "editor":
        raise HTTPException(status_code=403, detail="No autorizado")

@router.put("/publish/{article_id}", response_model=ArticleOut)
def publish_article(article_id: int, db: Session = Depends(get_db), user_role: str = "editor"):
    check_editor_role(user_role)
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    article.status = "publicado"
    db.commit()
    db.refresh(article)
    return article

@router.patch("/{article_id}", response_model=ArticleOut)
def patch_article(article_id: int, article_data: ArticleUpdate, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    update_data = article_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(article, key, value)
    db.commit()
    db.refresh(article)
    return article

# Debug opcional para ver todos los artículos

@router.get("/debug")
def debug_articles(db: Session = Depends(get_db)):
    return db.query(Article).all()

# delete article

@router.delete("/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db)):
    # Buscar el artículo
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    
    # Eliminar
    db.delete(article)
    db.commit()
    
    return {"message": f"Artículo {article_id} eliminado"}