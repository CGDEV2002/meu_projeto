"""
API de Clientes
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db import get_db
from app.models.client import Client
from app.models.user import User
from app.api.auth import get_current_user

router = APIRouter(prefix="/clients", tags=["Clients"])

# Schemas
class ClientCreate(BaseModel):
    name: str
    phone: str
    cpf: Optional[str] = None
    email: Optional[str] = None
    negotiation_status: str = "interested"
    notes: Optional[str] = None
    car_id: Optional[int] = None

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    cpf: Optional[str] = None
    email: Optional[str] = None
    negotiation_status: Optional[str] = None
    notes: Optional[str] = None
    car_id: Optional[int] = None

class ClientResponse(BaseModel):
    id: int
    name: str
    phone: str
    cpf: Optional[str]
    email: Optional[str]
    negotiation_status: str
    notes: Optional[str]
    car_id: Optional[int]
    tenant_id: int
    created_at: str
    
    class Config:
        from_attributes = True

# Rotas
@router.get("/", response_model=List[ClientResponse])
async def get_clients(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    car_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listar todos os clientes do tenant"""
    query = db.query(Client).filter(Client.tenant_id == current_user.tenant_id)
    
    if status:
        query = query.filter(Client.negotiation_status == status)
    
    if car_id:
        query = query.filter(Client.car_id == car_id)
    
    clients = query.offset(skip).limit(limit).all()
    return clients

@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obter detalhes de um cliente específico"""
    client = db.query(Client).filter(
        Client.id == client_id,
        Client.tenant_id == current_user.tenant_id
    ).first()
    
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    return client

@router.post("/", response_model=ClientResponse)
async def create_client(
    client_data: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Criar um novo cliente"""
    db_client = Client(
        **client_data.dict(),
        tenant_id=current_user.tenant_id
    )
    
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    
    return db_client

@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: int,
    client_data: ClientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Atualizar um cliente existente"""
    client = db.query(Client).filter(
        Client.id == client_id,
        Client.tenant_id == current_user.tenant_id
    ).first()
    
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Atualizar apenas campos fornecidos
    for field, value in client_data.dict(exclude_unset=True).items():
        setattr(client, field, value)
    
    db.commit()
    db.refresh(client)
    
    return client

@router.delete("/{client_id}")
async def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deletar um cliente"""
    client = db.query(Client).filter(
        Client.id == client_id,
        Client.tenant_id == current_user.tenant_id
    ).first()
    
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    db.delete(client)
    db.commit()
    
    return {"message": "Client deleted successfully"}