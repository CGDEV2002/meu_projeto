"""
Modelo de Cliente
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    cpf = Column(String)
    email = Column(String)
    negotiation_status = Column(String, default="interested")  # interested, negotiating, closed, lost
    notes = Column(Text)
    car_id = Column(Integer, ForeignKey("cars.id"))
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamentos
    car = relationship("Car", back_populates="clients")
    tenant = relationship("Tenant", back_populates="clients")