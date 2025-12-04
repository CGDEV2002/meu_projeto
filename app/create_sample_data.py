"""
Script para criar dados de exemplo no sistema
Execute: python create_sample_data.py
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import sessionmaker
from app.db import engine
from app.models.tenant import Tenant
from app.models.user import User
from app.models.car import Car
from app.models.client import Client
from app.models.document import Document
from passlib.context import CryptContext

# Configurar hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
Session = sessionmaker(bind=engine)

def create_sample_data():
    db = Session()
    
    try:
        # Verificar se tenant já existe
        sample_tenant = db.query(Tenant).filter(Tenant.slug == "carros-premium").first()
        if not sample_tenant:
            # Criar tenant de exemplo
            sample_tenant = Tenant(
                name="Carros Premium Ltda",
                slug="carros-premium"
            )
            db.add(sample_tenant)
            db.commit()
            db.refresh(sample_tenant)
            print("✅ Tenant criado")
        else:
            print("ℹ️ Tenant já existe")
        
        # Verificar se usuário já existe
        sample_user = db.query(User).filter(User.email == "admin@carrospremium.com").first()
        if not sample_user:
            # Criar usuário de exemplo
            password = "123456"
            if len(password.encode('utf-8')) > 72:
                password = password[:72]
            hashed_password = pwd_context.hash(password)
            sample_user = User(
                email="admin@carrospremium.com",
                hashed_password=hashed_password,
                full_name="João Silva",
                tenant_id=sample_tenant.id,
                is_admin=True
            )
            db.add(sample_user)
            db.commit()
            db.refresh(sample_user)
            print("✅ Usuário criado")
        else:
            print("ℹ️ Usuário já existe")
        
        # Criar carros de exemplo
        cars_data = [
            {
                "title": "Civic 2020 Completo",
                "brand": "Honda",
                "model": "Civic",
                "year": 2020,
                "price": 85000.00,
                "status": "available",
                "observations": "Carro em excelente estado, único dono, todas as revisões em dia.",
                "tenant_id": sample_tenant.id
            },
            {
                "title": "Corolla Cross 2022",
                "brand": "Toyota", 
                "model": "Corolla Cross",
                "year": 2022,
                "price": 125000.00,
                "status": "available",
                "observations": "SUV híbrido, baixa quilometragem, garantia de fábrica.",
                "tenant_id": sample_tenant.id
            },
            {
                "title": "Golf TSI 2019",
                "brand": "Volkswagen",
                "model": "Golf",
                "year": 2019,
                "price": 75000.00,
                "status": "reserved",
                "observations": "Motor 1.4 TSI, câmbio automático, multimídia.",
                "tenant_id": sample_tenant.id
            },
            {
                "title": "Onix Premier 2021",
                "brand": "Chevrolet",
                "model": "Onix",
                "year": 2021,
                "price": 65000.00,
                "status": "sold",
                "observations": "Versão Premier, completo, segunda parcela paga.",
                "tenant_id": sample_tenant.id
            }
        ]
        
        sample_cars = []
        for car_data in cars_data:
            car = Car(**car_data)
            db.add(car)
            sample_cars.append(car)
        
        db.commit()
        for car in sample_cars:
            db.refresh(car)
        
        # Criar clientes de exemplo
        clients_data = [
            {
                "name": "Maria Santos",
                "phone": "11987654321",
                "email": "maria@email.com",
                "cpf": "123.456.789-10",
                "negotiation_status": "interested",
                "notes": "Interessada no Civic, quer financiar em 48x.",
                "car_id": sample_cars[0].id,
                "tenant_id": sample_tenant.id
            },
            {
                "name": "Carlos Oliveira",
                "phone": "11976543210", 
                "email": "carlos@email.com",
                "negotiation_status": "negotiating",
                "notes": "Negociando entrada do Corolla Cross, aguardando aprovação do financiamento.",
                "car_id": sample_cars[1].id,
                "tenant_id": sample_tenant.id
            },
            {
                "name": "Ana Costa",
                "phone": "11965432109",
                "negotiation_status": "closed",
                "notes": "Comprou o Golf TSI à vista, entrega na próxima semana.",
                "car_id": sample_cars[2].id,
                "tenant_id": sample_tenant.id
            }
        ]
        
        sample_clients = []
        for client_data in clients_data:
            client = Client(**client_data)
            db.add(client)
            sample_clients.append(client)
        
        db.commit()
        for client in sample_clients:
            db.refresh(client)
        
        # Criar documentos de exemplo
        documents_data = [
            {
                "name": "Contrato de Venda - Civic",
                "document_type": "contract",
                "is_required": True,
                "is_completed": False,
                "notes": "Contrato aguardando assinatura da compradora.",
                "car_id": sample_cars[0].id
            },
            {
                "name": "Vistoria Técnica - Corolla Cross",
                "document_type": "inspection",
                "is_required": True,
                "is_completed": True,
                "notes": "Vistoria aprovada sem ressalvas.",
                "car_id": sample_cars[1].id
            },
            {
                "name": "Seguro Auto - Golf",
                "document_type": "insurance",
                "is_required": False,
                "is_completed": True,
                "notes": "Seguro contratado pela compradora.",
                "car_id": sample_cars[2].id
            },
            {
                "name": "Transferência de Propriedade - Onix",
                "document_type": "transfer",
                "is_required": True,
                "is_completed": True,
                "notes": "Transferência concluída no Detran.",
                "car_id": sample_cars[3].id
            }
        ]
        
        for doc_data in documents_data:
            document = Document(**doc_data)
            db.add(document)
        
        db.commit()
        
        print("✅ Dados de exemplo criados com sucesso!")
        print("\n📊 Resumo:")
        print(f"• 1 Tenant: {sample_tenant.name}")
        print(f"• 1 Usuário: {sample_user.email} (senha: 123456)")
        print(f"• {len(sample_cars)} Carros cadastrados")
        print(f"• {len(sample_clients)} Clientes interessados") 
        print(f"• {len(documents_data)} Documentos criados")
        print("\n🚀 Faça login com:")
        print("Email: admin@carrospremium.com")
        print("Senha: 123456")
        
    except Exception as e:
        print(f"❌ Erro ao criar dados: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()