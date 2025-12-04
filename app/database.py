import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Verificar se estamos em produção ou desenvolvimento
if os.getenv("DATABASE_URL"):
    # Produção (Render com PostgreSQL)
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    # Fix para Render PostgreSQL URL (se necessário)
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        
    engine = create_engine(DATABASE_URL)
else:
    # Desenvolvimento (SQLite local)
    DATABASE_URL = "sqlite:///./vendavoa.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()