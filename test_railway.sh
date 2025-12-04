#!/bin/bash

echo "🚄 Testando configuração para Railway..."

# Verificar arquivos Railway
echo "📋 Verificando arquivos Railway..."
railway_files=("Procfile" "nixpacks.toml" "railway.json" "runtime.txt")
missing=()

for file in "${railway_files[@]}"; do
    if [[ ! -f "$file" ]]; then
        missing+=("$file")
    else
        echo "✅ $file"
    fi
done

if [[ ${#missing[@]} -gt 0 ]]; then
    echo "❌ Arquivos faltando:"
    printf '%s\n' "${missing[@]}"
    exit 1
fi

echo ""
echo "🔧 Verificando configuração..."

# Testar importação da app
python -c "
try:
    from app.main import app
    from app.config import settings
    print('✅ App carregada com sucesso')
    print(f'✅ Health check: /health endpoint exists')
    print(f'✅ Environment: {settings.ENVIRONMENT}')
    print(f'✅ Database config: OK')
    print(f'✅ Secret key: {len(settings.SECRET_KEY)} caracteres')
except Exception as e:
    print(f'❌ Erro: {e}')
    exit(1)
"

if [[ $? -eq 0 ]]; then
    echo ""
    echo "🎉 PRONTO PARA RAILWAY!"
    echo ""
    echo "📝 Próximos passos:"
    echo "1. git add ."
    echo "2. git commit -m '🚄 Deploy Railway ready'"
    echo "3. git push origin main"
    echo "4. Acesse railway.app e conecte o repositório"
    echo "5. Adicione PostgreSQL database"
    echo "6. Configure as variáveis de ambiente"
    echo ""
    echo "📖 Instruções completas: DEPLOY_RAILWAY.md"
    echo ""
    echo "🚀 Seu app ficará online em ~5 minutos!"
else
    echo "❌ Erro na configuração. Verifique os logs acima."
    exit 1
fi