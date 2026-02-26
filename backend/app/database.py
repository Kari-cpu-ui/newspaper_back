import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


load_dotenv()

# Construyo la URL de conexion para MySQL usando variables de entorno
DATABASE_URL = f"mysql+pymysql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}?ssl_mode=REQUIRED"

# Creo el motor de conexión a la base de datos
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verifica la conexión antes de usarla
)

# Creo SessionLocal, clase para instanciar sesiones con la DB
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base declarativa para los modelos
Base = declarative_base()

# Función para inyectar sesión en FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()