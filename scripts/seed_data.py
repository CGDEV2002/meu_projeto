"""
Script para inicializar dados de exemplo
Execute: python scripts/seed_data.py
"""
import sys
import os

# Adicionar o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import SessionLocal, engine, Base
from app.models import *
from app.api.auth import get_password_hash

# Criar todas as tabelas
Base.metadata.create_all(bind=engine)

def create_sample_data():
    db = SessionLocal()
    
    try:
        # Criar tenant de exemplo
        tenant = Tenant(
            name="AutoMax Seminovos",
            slug="automax-seminovos"
        )
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        
        # Criar usuário de exemplo
        user = User(
            email="admin@automax.com",
            hashed_password=get_password_hash("123456"),
            full_name="João Silva",
            tenant_id=tenant.id,
            is_admin=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Criar carros de exemplo
        cars_data = [
            {
                "title": "Honda Civic EX 2020",
                "brand": "Honda",
                "model": "Civic",
                "year": 2020,
                "price": 89000.00,
                "photo_url": "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=500",
                "observations": "Carro em excelente estado, único dono, revisões em dia.",
                "status": "available",
                "tenant_id": tenant.id
            },
            {
                "title": "Toyota Corolla XEI 2019",
                "brand": "Toyota", 
                "model": "Corolla",
                "year": 2019,
                "price": 82000.00,
                "photo_url": "https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=500",
                "observations": "Automatico, couro, central multimidia.",
                "status": "available",
                "tenant_id": tenant.id
            },
            {
                "title": "Hyundai HB20 Comfort 2021",
                "brand": "Hyundai",
                "model": "HB20",
                "year": 2021,
                "price": 65000.00,
                "photo_url": "https://images.unsplash.com/photo-1494905998402-395d579af36f?w=500",
                "observations": "Econômico, ideal para cidade.",
                "status": "reserved",
                "tenant_id": tenant.id
            },
            {
                "title": "Volkswagen Polo TSI 2018",
                "brand": "Volkswagen",
                "model": "Polo",
                "year": 2018,
                "price": 58000.00,
                "observations": "Motor turbo, muito potente.",
                "status": "sold",
                "tenant_id": tenant.id
            }
        ]
        
        cars = []
        for car_data in cars_data:
            car = Car(**car_data)
            db.add(car)
            cars.append(car)
        
        db.commit()
        
        # Refresh cars to get IDs
        for car in cars:
            db.refresh(car)
        
        # Criar clientes de exemplo
        clients_data = [
            {
                "name": "Maria Santos",
                "phone": "(11) 99999-1234",
                "cpf": "123.456.789-00",
                "email": "maria@email.com",
                "negotiation_status": "interested",
                "notes": "Interessada no Honda Civic, quer financiar.",
                "car_id": cars[0].id,
                "tenant_id": tenant.id
            },
            {
                "name": "Pedro Oliveira",
                "phone": "(11) 98888-5678",
                "email": "pedro@email.com",
                "negotiation_status": "negotiating",
                "notes": "Negociando o Corolla, aguardando aprovação do financiamento.",
                "car_id": cars[1].id,
                "tenant_id": tenant.id
            },
            {
                "name": "Ana Costa",
                "phone": "(11) 97777-9012",
                "negotiation_status": "closed",
                "notes": "Comprou o HB20, pagamento à vista.",
                "car_id": cars[2].id,
                "tenant_id": tenant.id
            }
        ]
        
        for client_data in clients_data:
            client = Client(**client_data)
            db.add(client)
        
        db.commit()
        
        # Criar documentos de exemplo
        documents_data = [
            {
                "name": "Documento do Veículo",
                "document_type": "transfer",
                "notes": "CRLV em nome do proprietário",
                "is_required": True,
                "is_completed": True,
                "car_id": cars[0].id
            },
            {
                "name": "Laudo de Vistoria",
                "document_type": "inspection", 
                "notes": "Vistoria aprovada, sem avarias",
                "is_required": False,
                "is_completed": True,
                "car_id": cars[0].id
            },
            {
                "name": "Contrato de Compra e Venda",
                "document_type": "contract",
                "notes": "Aguardando assinatura do comprador",
                "is_required": True,
                "is_completed": False,
                "car_id": cars[1].id
            }
        ]
        
        for doc_data in documents_data:
            document = Document(**doc_data)
            db.add(document)
        
        db.commit()
        
        print("✅ Dados de exemplo criados com sucesso!")
        print(f"🏢 Tenant: {tenant.name}")
        print(f"👤 Usuário: {user.email} / Senha: 123456")
        print(f"🚗 Carros: {len(cars_data)} cadastrados")
        print(f"👥 Clientes: {len(clients_data)} cadastrados")
        print(f"📄 Documentos: {len(documents_data)} cadastrados")
        
    except Exception as e:
        print(f"❌ Erro ao criar dados: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()