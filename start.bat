@echo off
echo 🚗 Iniciando VendaVoa...

REM Verificar se o Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado. Instale o Python 3.8+ e tente novamente.
    pause
    exit /b 1
)

REM Verificar se está no ambiente virtual
if "%VIRTUAL_ENV%"=="" (
    echo ⚠️ Criando ambiente virtual...
    python -m venv venv
    call venv\Scripts\activate.bat
)

REM Instalar dependências
echo 📦 Instalando dependências...
pip install -r requirements.txt

REM Verificar se o arquivo .env existe
if not exist .env (
    echo ⚠️ Arquivo .env não encontrado. Copiando exemplo...
    copy .env .env.local
    echo ✏️ Configure suas variáveis de ambiente no arquivo .env.local
)

REM Criar dados de exemplo (opcional)
set /p response=Deseja criar dados de exemplo? (s/n): 
if /i "%response%"=="s" (
    echo 🌱 Criando dados de exemplo...
    python scripts/seed_data.py
)

REM Iniciar servidor
echo 🚀 Iniciando servidor...
echo 📱 Acesse: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo ⏹️ Pressione Ctrl+C para parar

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause