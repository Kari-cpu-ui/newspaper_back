from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionCreate, SubscriptionOut
from app.database import get_db
from typing import List     

router = APIRouter()

# Crear suscripción
@router.post("/", response_model=SubscriptionOut)
def create_subscription(sub: SubscriptionCreate, db: Session = Depends(get_db)):
    existing = db.query(Subscription).filter(Subscription.email == sub.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    new_sub = Subscription(email=sub.email)
    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)
    return new_sub

# Listar suscripciones
@router.get("/", response_model=List[SubscriptionOut])
def list_subscriptions(db: Session = Depends(get_db)):
    return db.query(Subscription).all()

# Borrar suscripción
@router.delete("/{sub_id}")
def delete_subscription(sub_id: int, db: Session = Depends(get_db)):
    sub = db.query(Subscription).filter(Subscription.id == sub_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Suscripción no encontrada")
    db.delete(sub)
    db.commit()
    return {"message": f"Suscripción {sub_id} eliminada"}