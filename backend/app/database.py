import os 
from sqlalchemy import create_engine # Conexión mysql 
from sqlalchemy.orm import sessionmaker # Para crear sesiones que interactúan con la DB

# Construyo la URL de conexion para Mysql 
DATABASE_URL = f"mysql+pymysql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"

# Creo el motor de conexión a la base de datos
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True, # Verifica la conexión antes de usarla
)

# Creo SessionLocal, una clase que se usará para crear sesiones de base de datos
SessionsLocal = sessionmaker(
    autocommit=False,  
    autoflush=False, # no manda cambios pendientes hasta que lo indicamos
    bind=engine # vinculala sesisesión con nuestro motor 
    
)
