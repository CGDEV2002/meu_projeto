"""
Aplicação principal FastAPI
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from app.db import engine, Base
from app.api import auth, cars, clients
from app.api import docs as docs_api

# Criar tabelas
Base.metadata.create_all(bind=engine)

# Inicializar aplicação
app = FastAPI(
    title="VendaVoa - Sistema para Revendedores",
    description="Sistema completo para gestão de carros e clientes",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas da API
app.include_router(auth.router)
app.include_router(cars.router)
app.include_router(clients.router)
app.include_router(docs_api.router)

# Servir arquivos estáticos
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Rotas para as páginas
@app.get("/")
async def root():
    return FileResponse("frontend/templates/login.html")

@app.get("/login")
async def login_page():
    return FileResponse("frontend/templates/login.html")

@app.get("/dashboard")
async def dashboard_page():
    return FileResponse("frontend/templates/dashboard.html")

@app.get("/car/{car_id}")
async def car_page(car_id: int):
    return FileResponse("frontend/templates/car.html")

@app.get("/client/{client_id}")
async def client_page(client_id: int):
    return FileResponse("frontend/templates/client.html")

# Health check
@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)