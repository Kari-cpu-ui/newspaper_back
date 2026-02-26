from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

# -------------------- USUARIOS --------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum('redactor', 'editor'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now()) # Fecha automatica al crear el usuario

    # Relaciones
    articles_authored = relationship("Article", back_populates="author", foreign_keys='Article.author_id')
    articles_edited = relationship("Article", back_populates="editor", foreign_keys='Article.editor_id')


# -------------------- ARTÍCULOS --------------------
class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    section = Column(String(50))
    status = Column(Enum('borrador', 'revision', 'publicado'), default='borrador')
    importance = Column(Integer, default=0)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    editor_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(TIMESTAMP, server_default=func.now()) # Fecha automatica al crear el artículo
    updated_at = Column(TIMESTAMP,server_default=func.now(), onupdate=func.now()) # Fecha automatica al actualizar el artículo

    # Relaciones entre tablas
    author = relationship("User", back_populates="articles_authored", foreign_keys=[author_id])
    editor = relationship("User", back_populates="articles_edited", foreign_keys=[editor_id])


# -------------------- SUSCRIPCIONES --------------------
class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())