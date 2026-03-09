# scripts/seed_users.py

import random
from datetime import datetime
from app.database import SessionLocal, engine, Base
from app.models.user import User

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# Lista de nombres simulados
names = [
    "Karina Medero", "Carolina", "Luis Pérez", "Ana Gómez", "Jorge Díaz",
    "María López", "Pedro Sánchez", "Lucía Torres", "Andrés Ruiz", "Sofía Castro"
]

roles = ["redactor", "editor"]

# Crear 50 usuarios
usuarios = []
for i in range(50):
    name = random.choice(names) + f"_{i+1}"  # para evitar repetidos
    email = f"user{i+1}@example.com"
    role = random.choice(roles)
    created_at = datetime.now()

    user = User(
        name=name,
        email=email,
        password_hash="hashed_password_aqui",  #  hash de prueba
        role=role,
        created_at=created_at
    )
    usuarios.append(user)

# Insertar en la DB
db = SessionLocal()
try:
    db.add_all(usuarios)
    db.commit()
    print("Se insertaron 50 usuarios correctamente")
except Exception as e:
    db.rollback()
    print(" Error al insertar usuarios:", e)
finally:
    db.close()