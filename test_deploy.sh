#!/bin/bash

echo "🧪 Testando aplicação antes do deploy..."

# Verificar se todos os arquivos necessários existem
echo "📋 Verificando arquivos..."
files=("requirements.txt" "render.yaml" "build.sh" "init_db.py" ".env.example" "DEPLOY_INSTRUCTIONS.md")
missing_files=()

for file in "${files[@]}"; do
    if [[ ! -f "$file" ]]; then
        missing_files+=("$file")
    fi
done

if [[ ${#missing_files[@]} -gt 0 ]]; then
    echo "❌ Arquivos faltando:"
    printf '%s\n' "${missing_files[@]}"
    exit 1
fi

echo "✅ Todos os arquivos necessários estão presentes"

# Testar se a aplicação inicia
echo "🚀 Testando inicialização da aplicação..."
python -c "
try:
    from app.main import app
    from app.config import settings
    print(f'✅ App carregada com sucesso')
    print(f'🔧 Ambiente: {settings.ENVIRONMENT}')
    print(f'💾 Database: {settings.DATABASE_URL[:50]}...')
    print(f'🔑 Secret key configurada: {len(settings.SECRET_KEY)} chars')
except Exception as e:
    print(f'❌ Erro ao carregar app: {e}')
    exit(1)
"

if [[ $? -eq 0 ]]; then
    echo "✅ Aplicação pronta para deploy!"
    echo ""
    echo "📝 Próximos passos:"
    echo "1. git add ."
    echo "2. git commit -m 'Preparação para deploy'"
    echo "3. git push origin main"
    echo "4. Seguir instruções em DEPLOY_INSTRUCTIONS.md"
else
    echo "❌ Falha no teste. Verifique os erros acima."
    exit 1
fi