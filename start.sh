#!/bin/bash

# Script para executar o projeto localmente
echo "🚗 Iniciando VendaVoa..."

# Verificar se o Python está instalado
if ! command -v python &> /dev/null; then
    echo "❌ Python não encontrado. Instale o Python 3.8+ e tente novamente."
    exit 1
fi

# Verificar se está no ambiente virtual
if [[ "$VIRTUAL_ENV" = "" ]]; then
    echo "⚠️  Criando ambiente virtual..."
    python -m venv venv
    
    # Ativar ambiente virtual
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        # Windows
        source venv/Scripts/activate
    else
        # Linux/Mac
        source venv/bin/activate
    fi
fi

# Instalar dependências
echo "📦 Instalando dependências..."
pip install -r requirements.txt

# Verificar se o arquivo .env existe
if [ ! -f .env ]; then
    echo "⚠️  Arquivo .env não encontrado. Copiando exemplo..."
    cp .env .env.local
    echo "✏️  Configure suas variáveis de ambiente no arquivo .env.local"
fi

# Criar dados de exemplo (opcional)
read -p "Deseja criar dados de exemplo? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "🌱 Criando dados de exemplo..."
    python scripts/seed_data.py
fi

# Iniciar servidor
echo "🚀 Iniciando servidor..."
echo "📱 Acesse: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "⏹️  Pressione Ctrl+C para parar"

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000