"""
API de Documentos
"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict

from app.db import get_db
from app.models.document import Document
from app.models.car import Car
from app.models.user import User
from app.api.auth import get_current_user
from app.utils.upload import save_uploaded_file, delete_file

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
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    document_type: str
    file_url: Optional[str]
    notes: Optional[str]
    is_required: bool
    is_completed: bool
    car_id: int

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

@router.post("/upload/{document_id}")
async def upload_document_file(
    document_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload de arquivo para um documento"""
    # Verificar se o documento pertence ao tenant do usuário
    document = db.query(Document).join(Car).filter(
        Document.id == document_id,
        Car.tenant_id == current_user.tenant_id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    try:
        # Remover arquivo antigo se existir
        if document.file_url:
            delete_file(document.file_url)
        
        # Salvar novo arquivo
        file_url = await save_uploaded_file(file, "documents")
        
        # Atualizar documento
        document.file_url = file_url
        document.is_completed = True
        db.commit()
        
        return {
            "message": "File uploaded successfully",
            "file_url": file_url,
            "document_id": document_id
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/create-with-file/{car_id}")
async def create_document_with_file(
    car_id: int,
    name: str = Form(...),
    document_type: str = Form(...),
    file: UploadFile = File(...),
    notes: str = Form(""),
    is_required: str = Form("false"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Criar documento e fazer upload do arquivo em uma só operação"""
    # Verificar se o carro pertence ao tenant do usuário
    car = db.query(Car).filter(
        Car.id == car_id,
        Car.tenant_id == current_user.tenant_id
    ).first()
    
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )
    
    try:
        # Salvar arquivo
        file_url = await save_uploaded_file(file, "documents")
        
        # Criar documento
        db_document = Document(
            name=name,
            document_type=document_type,
            file_url=file_url,
            notes=notes,
            is_required=is_required.lower() == 'true',
            is_completed=True,
            car_id=car_id
        )
        
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        
        return db_document
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

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