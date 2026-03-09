from fastapi import FastAPI
from app.database import Base, engine

# 🔹 Importa los modelos antes de crear tablas
from app.models.user import User

# Routers
from app.routes.user import router as users_router
from app.routes.article import router as articles_router

app = FastAPI(title="CMS Periódico")

# 🔹 Crear tablas (ya que los modelos están importados)
Base.metadata.create_all(bind=engine)

## Incluir routers
app.include_router(users_router, prefix="/users", tags=["Usuarios"])
app.include_router(articles_router, prefix="/articles", tags=["Artículos"])  
@app.get("/")
def root():
    return {"message": "CMS funcionando"}
