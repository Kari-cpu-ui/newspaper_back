from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

# Crear usuario
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password_hash: str = Field(max_length=72)  # Limite 72 caracteres
    role: str = "redactor"

    # Esquema para mostrar el usuario creado sin la contraseña

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        from_attributes = True 

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        from_attributes = True  