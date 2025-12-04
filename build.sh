#!/bin/bash

# Script de build para o Render
echo "🚀 Iniciando build do VendaVoa..."

# Instalar dependências
echo "📦 Instalando dependências..."
pip install -r requirements.txt

# Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p uploads/photos
mkdir -p uploads/documents

# Inicializar banco de dados
echo "🗄️ Inicializando banco de dados..."
python init_db.py

echo "✅ Build concluído com sucesso!"

echo "Build completed successfully!"