"""
Modelo de Documento
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    document_type = Column(String, nullable=False)  # contract, inspection, insurance, etc
    file_url = Column(String)
    notes = Column(Text)
    is_required = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    car_id = Column(Integer, ForeignKey("cars.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    car = relationship("Car", back_populates="documents")