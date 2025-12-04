"""
Utilitários para upload de arquivos
"""
import os
import uuid
from pathlib import Path
from typing import Optional
from fastapi import UploadFile, HTTPException
import shutil

# Configurações
UPLOAD_DIR = Path("uploads")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".webp"},
    "documents": {".pdf", ".doc", ".docx", ".txt", ".jpg", ".jpeg", ".png"}
}

# Criar diretórios se não existirem
UPLOAD_DIR.mkdir(exist_ok=True)
(UPLOAD_DIR / "photos").mkdir(exist_ok=True)
(UPLOAD_DIR / "documents").mkdir(exist_ok=True)

def validate_file(file: UploadFile, file_type: str = "documents") -> bool:
    """Valida se o arquivo é permitido"""
    if not file.filename:
        return False
    
    file_ext = Path(file.filename).suffix.lower()
    return file_ext in ALLOWED_EXTENSIONS.get(file_type, set())

async def save_uploaded_file(file: UploadFile, file_type: str = "documents") -> str:
    """Salva arquivo enviado e retorna o caminho"""
    if not validate_file(file, file_type):
        raise HTTPException(
            status_code=400, 
            detail=f"Tipo de arquivo não permitido. Extensões aceitas: {', '.join(ALLOWED_EXTENSIONS[file_type])}"
        )
    
    # Verificar tamanho do arquivo
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Arquivo muito grande. Máximo: {MAX_FILE_SIZE // 1024 // 1024}MB"
        )
    
    # Gerar nome único
    file_ext = Path(file.filename).suffix.lower()
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    
    # Determinar diretório
    if file_type == "images":
        file_path = UPLOAD_DIR / "photos" / unique_filename
    else:
        file_path = UPLOAD_DIR / "documents" / unique_filename
    
    # Salvar arquivo
    with open(file_path, "wb") as buffer:
        buffer.write(content)
    
    # Retornar URL relativa
    return f"/uploads/{file_type if file_type != 'images' else 'photos'}/{unique_filename}"

def delete_file(file_path: str) -> bool:
    """Remove arquivo do sistema"""
    try:
        # Remover "/uploads/" do início se existir
        if file_path.startswith("/uploads/"):
            file_path = file_path[9:]
        
        full_path = UPLOAD_DIR / file_path
        if full_path.exists():
            full_path.unlink()
            return True
        return False
    except:
        return False