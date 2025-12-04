"""
API de Carros
"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict

from app.db import get_db
from app.models.car import Car
from app.models.user import User
from app.api.auth import get_current_user

router = APIRouter(prefix="/cars", tags=["Cars"])

# Schemas
class CarCreate(BaseModel):
    title: str
    brand: str
    model: str
    year: int
    price: Optional[float] = None
    photo_url: Optional[str] = None
    observations: Optional[str] = None
    status: str = "available"

class CarUpdate(BaseModel):
    title: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    price: Optional[float] = None
    photo_url: Optional[str] = None
    observations: Optional[str] = None
    status: Optional[str] = None

class CarResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    brand: str
    model: str
    year: int
    price: Optional[float]
    photo_url: Optional[str]
    observations: Optional[str]
    status: str
    tenant_id: int

# Rotas
@router.get("/", response_model=List[CarResponse])
async def get_cars(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listar todos os carros do tenant"""
    query = db.query(Car).filter(Car.tenant_id == current_user.tenant_id)
    
    if status:
        query = query.filter(Car.status == status)
    
    cars = query.offset(skip).limit(limit).all()
    return cars

@router.get("/{car_id}", response_model=CarResponse)
async def get_car(
    car_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obter detalhes de um carro específico"""
    car = db.query(Car).filter(
        Car.id == car_id,
        Car.tenant_id == current_user.tenant_id
    ).first()
    
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    
    return car

@router.post("/", response_model=CarResponse)
async def create_car(
    car_data: CarCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Criar um novo carro"""
    db_car = Car(
        **car_data.dict(),
        tenant_id=current_user.tenant_id
    )
    
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    
    return db_car

@router.put("/{car_id}", response_model=CarResponse)
async def update_car(
    car_id: int,
    car_data: CarUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Atualizar um carro existente"""
    car = db.query(Car).filter(
        Car.id == car_id,
        Car.tenant_id == current_user.tenant_id
    ).first()
    
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    
    # Atualizar apenas campos fornecidos
    for field, value in car_data.dict(exclude_unset=True).items():
        setattr(car, field, value)
    
    db.commit()
    db.refresh(car)
    
    return car

@router.delete("/{car_id}")
async def delete_car(
    car_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deletar um carro"""
    car = db.query(Car).filter(
        Car.id == car_id,
        Car.tenant_id == current_user.tenant_id
    ).first()
    
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    
    db.delete(car)
    db.commit()
    
    return {"message": "Car deleted successfully"}