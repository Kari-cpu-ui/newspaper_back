from fastapi import APIRouter, Depends, HTTPException  # FastAPI y dependencias
from fastapi.params import Query  # Para filtros opcionales
from sqlalchemy.orm import Session  # Para manejar la sesión de la base de datos
from typing import List

from app.database import get_db  # Sesión DB
from app.models.article import Article  # Modelo Article
from app.models.user import User       # Modelo User para roles
from app.schemas.article import ArticleOut, ArticleCreate, ArticleUpdate  # Schemas
from app.utils.security import get_current_user  # Usuario autenticado desde JWT

router = APIRouter()  # Crear router de FastAPI


# CREAR ARTÍCULO (solo redactores)

@router.post("/", response_model=ArticleOut)
def crear_articulo(
    articulo: ArticleCreate,                      # datos del body
    db: Session = Depends(get_db),               # sesión DB
    current_user: User = Depends(get_current_user)  # usuario logueado
):
    # verificar rol
    if current_user.role != "redactor":
        raise HTTPException(status_code=403, detail="Solo redactores pueden crear artículos")

    # crear artículo usando ID del usuario logueado
    new_article = Article(
        title=articulo.title,
        content=articulo.content,
        section=articulo.section,
        author_id=current_user.id,
        status="borrador"
    )

    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


# LISTAR TODOS LOS ARTÍCULOS

@router.get("/", response_model=List[ArticleOut])
def listar_articulos(db: Session = Depends(get_db)):
    return db.query(Article).all()


# FILTRAR POR AUTOR

@router.get("/by_author/{author_id}", response_model=List[ArticleOut])
def get_articles_by_author(author_id: int, db: Session = Depends(get_db)):
    return db.query(Article).filter(Article.author_id == author_id).all()

# FILTRAR POR ESTADO

@router.get("/by_status/", response_model=List[ArticleOut])
def get_articles_by_status(
    status: str = Query(..., enum=["borrador", "revision", "publicado"]),
    db: Session = Depends(get_db)
):
    return db.query(Article).filter(Article.status == status).all()


# FILTRAR POR SECCIÓN

@router.get("/by_section/{section}", response_model=List[ArticleOut])
def get_articles_by_section(section: str, db: Session = Depends(get_db)):
    return db.query(Article).filter(Article.section == section).all()

# FILTRAR POR IMPORTANCIA

@router.get("/by_importance/", response_model=List[ArticleOut])
def get_articles_by_importance(
    min: int = 0,
    max: int = 10,
    db: Session = Depends(get_db)
):
    return db.query(Article).filter(Article.importance >= min, Article.importance <= max).all()


# PUBLICAR ARTÍCULO (solo editor)

@router.put("/publish/{article_id}", response_model=ArticleOut)
def publish_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "editor":
        raise HTTPException(status_code=403, detail="Solo editores pueden publicar artículos")

    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")

    article.status = "publicado"
    db.commit()
    db.refresh(article)
    return article


# PONER ARTÍCULO EN REVISIÓN (solo editor)

@router.put("/review/{article_id}", response_model=ArticleOut)
def review_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "editor":
        raise HTTPException(status_code=403, detail="Solo editores pueden poner artículos en revisión")

    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")

    article.status = "revision"
    db.commit()
    db.refresh(article)
    return article


# ACTUALIZAR ARTÍCULO (PATCH)
# redactores → solo sus artículos
# editores → cualquier artículo

@router.patch("/{article_id}", response_model=ArticleOut)
def patch_article(
    article_id: int,
    article_data: ArticleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")

    # solo redactores pueden actualizar sus propios artículos
    if current_user.role == "redactor" and article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado para editar este artículo")

    # 🔹 Pydantic v2 moderno: model_dump en lugar de dict
    update_data = article_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(article, key, value)

    db.commit()
    db.refresh(article)
    return article

# BORRAR ARTÍCULO (solo editor)

@router.delete("/{article_id}")
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "editor":
        raise HTTPException(status_code=403, detail="Solo editores pueden eliminar artículos")

    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")

    db.delete(article)
    db.commit()
    return {"message": f"Artículo {article_id} eliminado"}


# DEBUG: ver todos los artículos (sin filtro)

@router.get("/debug")
def debug_articles(db: Session = Depends(get_db)):
    return db.query(Article).all()

# OBTENER ARTÍCULO POR ID
@router.get("/{article_id}", response_model=ArticleOut)
def get_article_by_id(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    return article