from fastapi import APIRouter, Depends, HTTPException  # FastAPI y dependencias
from sqlalchemy.orm import Session                        # ORM
from app.database import get_db                                               # Obtener sesión de DB
from app.schemas.user import UserCreate, UserOut, UserLogin, Token, UserResponse
from typing import List
from passlib.context import CryptContext                  # Para encriptar contraseñas
from app.utils.security import create_access_token
from app.utils.security import get_current_user  # Import get_current_user
from app.models.user import User  # Import the User model
from app.models.user import User  # Para obtener el usuario actual y su rol
router = APIRouter()  # Router para usuarios

# 🔹 Contexto para encriptación de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔹 Función para hashear la contraseña
def hash_password(password: str):
    return pwd_context.hash(password)

# --- Crear usuario ---
@router.post("/", response_model=UserOut)  # POST /users/
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # 🔹 Revisar si el email o el name ya existe
    existing_user = db.query(User).filter(
        (User.email == user.email) | (User.name == user.name)  # <-- cambiamos username a name
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    
    # 🔹 Crear usuario
    new_user = User(
        name=user.name,               
        email=user.email,
        password_hash=hash_password(user.password_hash),  # Encriptar contraseña
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# --- Listar todos los usuarios ---
@router.get("/", response_model=List[UserOut])  # GET /users/
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# --- Listar usuarios alternativa ---
@router.get("/usuarios", response_model=List[UserOut])  # GET /users/usuarios
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):

    # buscar usuario por email
    db_user = db.query(User).filter(User.email == user.email).first()

    # si no existe el usuario o la contraseña es incorrecta, lanzar error

    if not db_user:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    # verificar contraseña
    if not pwd_context.verify(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    # crear token
    token = create_access_token({
        "user_id": db_user.id,
        "role": db_user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user