"""
API de Documentos
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db import get_db
from app.models.document import Document
from app.models.car import Car
from app.models.user import User
from app.api.auth import get_current_user

router = APIRouter(prefix="/docs", tags=["Documents"])

# Schemas
class DocumentCreate(BaseModel):
    name: str
    document_type: str
    file_url: Optional[str] = None
    notes: Optional[str] = None
    is_required: bool = False
    is_completed: bool = False
    car_id: int

class DocumentUpdate(BaseModel):
    name: Optional[str] = None
    document_type: Optional[str] = None
    file_url: Optional[str] = None
    notes: Optional[str] = None
    is_required: Optional[bool] = None
    is_completed: Optional[bool] = None

class DocumentResponse(BaseModel):
    id: int
    name: str
    document_type: str
    file_url: Optional[str]
    notes: Optional[str]
    is_required: bool
    is_completed: bool
    car_id: int
    created_at: str
    
    class Config:
        from_attributes = True

# Rotas
@router.get("/", response_model=List[DocumentResponse])
async def get_documents(
    car_id: Optional[int] = None,
    document_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listar documentos"""
    query = db.query(Document).join(Car).filter(Car.tenant_id == current_user.tenant_id)
    
    if car_id:
        query = query.filter(Document.car_id == car_id)
    
    if document_type:
        query = query.filter(Document.document_type == document_type)
    
    documents = query.offset(skip).limit(limit).all()
    return documents

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obter detalhes de um documento específico"""
    document = db.query(Document).join(Car).filter(
        Document.id == document_id,
        Car.tenant_id == current_user.tenant_id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return document

@router.post("/", response_model=DocumentResponse)
async def create_document(
    document_data: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Criar um novo documento"""
    # Verificar se o carro pertence ao tenant do usuário
    car = db.query(Car).filter(
        Car.id == document_data.car_id,
        Car.tenant_id == current_user.tenant_id
    ).first()
    
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    
    db_document = Document(**document_data.dict())
    
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    return db_document

@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: int,
    document_data: DocumentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Atualizar um documento existente"""
    document = db.query(Document).join(Car).filter(
        Document.id == document_id,
        Car.tenant_id == current_user.tenant_id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Atualizar apenas campos fornecidos
    for field, value in document_data.dict(exclude_unset=True).items():
        setattr(document, field, value)
    
    db.commit()
    db.refresh(document)
    
    return document

@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deletar um documento"""
    document = db.query(Document).join(Car).filter(
        Document.id == document_id,
        Car.tenant_id == current_user.tenant_id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}