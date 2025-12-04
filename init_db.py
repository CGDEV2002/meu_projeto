"""
Script de inicialização do banco de dados para produção
"""
from app.db import engine
from app.models import user, tenant, car, client, document

def init_db():
    """Cria todas as tabelas no banco de dados"""
    # Importar todos os modelos para garantir que sejam criados
    from app.models.user import Base
    from app.models.tenant import Base
    from app.models.car import Base
    from app.models.client import Base
    from app.models.document import Base
    
    # Criar todas as tabelas
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")

if __name__ == "__main__":
    init_db()