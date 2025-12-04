# 🚗 VendaVoa - Sistema PWA para Revendedores de Carros

Sistema completo de gestão para revendedoras de carros com interface moderna e responsiva.

## 🚀 Funcionalidades

- ✅ **Gestão de Carros**: CRUD completo com fotos, preços e status
- ✅ **Gestão de Clientes**: Controle de leads e negociações
- ✅ **Integração WhatsApp**: Botão direto para conversa
- ✅ **Documentos**: Controle de documentação por carro
- ✅ **Multi-tenant**: Suporte a múltiplas lojas
- ✅ **PWA**: Funciona offline e pode ser instalado
- ✅ **Responsivo**: Interface otimizada para celular
- ✅ **Autenticação JWT**: Sistema seguro de login
- ✅ **API REST**: Documentação automática com FastAPI

## 🛠 Tecnologias

- **Backend**: Python + FastAPI + SQLAlchemy
- **Frontend**: HTML5 + CSS3 + JavaScript (Vanilla)
- **Database**: SQLite (local) / PostgreSQL (produção)
- **PWA**: Service Worker + Web App Manifest
- **Deploy**: Render/Railway (Free Tier)

## 📦 Instalação Local

### Pré-requisitos
- Python 3.8+
- Git

### Passo a Passo

1. **Clone o repositório**:
```bash
git clone <seu-repositorio>
cd VendaVoa
```

2. **Crie ambiente virtual**:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale dependências**:
```bash
pip install -r requirements.txt
```

4. **Configure variáveis de ambiente**:
```bash
# Copie o .env.example e ajuste as configurações
cp .env .env.local
```

5. **Execute a aplicação**:
```bash
# Na pasta raiz do projeto
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

6. **Acesse o sistema**:
- URL: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🚀 Deploy no Render (Gratuito)

### 1. Preparação

Crie um arquivo `render.yaml`:

```yaml
services:
  - type: web
    name: vendavoa
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        value: postgresql://user:password@host:port/database
      - key: SECRET_KEY
        generateValue: true
      - key: ENVIRONMENT
        value: production
```

### 2. Deploy

1. Faça push do código para GitHub
2. Conecte o repositório no Render
3. Configure as variáveis de ambiente:
   - `SECRET_KEY`: Gere uma chave secreta forte
   - `DATABASE_URL`: Configure PostgreSQL gratuito
4. Deploy automático!

## 🚀 Deploy no Railway (Gratuito)

### 1. Preparação

Crie um arquivo `railway.json`:

```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health"
  }
}
```

### 2. Deploy

1. Conecte o GitHub ao Railway
2. Configure variáveis de ambiente
3. Deploy automático!

## 📱 Como Usar

### Primeiro Acesso

1. Acesse a aplicação
2. Clique em "Cadastre-se"
3. Preencha os dados da sua loja
4. Faça login

### Gerenciar Carros

1. No Dashboard, clique em "Adicionar Carro"
2. Preencha as informações (marca, modelo, ano, preço)
3. Adicione uma foto (URL)
4. Defina o status (Disponível/Reservado/Vendido)

### Gerenciar Clientes

1. Acesse um carro específico
2. Clique em "Adicionar Cliente"
3. Preencha nome, telefone e status da negociação
4. Use o botão WhatsApp para contato direto

### Documentos

1. Na página do carro, clique em "Adicionar Documento"
2. Defina tipo, obrigatoriedade e status
3. Adicione link para o arquivo

## 🔧 Configurações Avançadas

### Banco de Dados

Para usar PostgreSQL em produção:

```bash
# Instale psycopg2
pip install psycopg2-binary

# Configure a URL no .env
DATABASE_URL=postgresql://user:password@host:port/database
```

### Uploads de Imagem

Para permitir upload de imagens (opcional):

1. Configure um serviço como Cloudinary ou AWS S3
2. Adicione endpoint para upload na API
3. Integre no frontend

### Notificações Push (Futuro)

O PWA já está preparado para notificações:

```javascript
// No service worker
self.addEventListener('push', function(event) {
    // Implementar notificações
});
```

## 🔒 Segurança

- ✅ Senhas hasheadas com bcrypt
- ✅ JWT com expiração configurável
- ✅ Validação de dados com Pydantic
- ✅ CORS configurado
- ✅ SQL Injection protegido (SQLAlchemy ORM)

## 📊 Performance

- ✅ Queries otimizadas
- ✅ Lazy loading de imagens
- ✅ Cache de assets estáticos
- ✅ Compressão automática
- ✅ Service Worker para offline

## 🐛 Troubleshooting

### Erro de CORS
```javascript
// Adicione seu domínio no main.py
allow_origins=["https://seuldominio.com"]
```

### Banco não cria tabelas
```bash
# Delete o banco e reinicie
rm vendavoa.db
python -c "from app.db import engine, Base; Base.metadata.create_all(engine)"
```

### PWA não instala
- Verifique se está usando HTTPS
- Confirme se o manifest.json está acessível
- Teste no Chrome DevTools > Application > Manifest

## 📈 Próximas Funcionalidades

- [ ] Relatórios de vendas
- [ ] Integração com WhatsApp Business API
- [ ] Upload de imagens
- [ ] Notificações push
- [ ] Exportação de dados
- [ ] Backup automático

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 💬 Suporte

- 📧 Email: seuemail@exemplo.com
- 💬 WhatsApp: [Link do WhatsApp]
- 🐛 Issues: [GitHub Issues]

---

**Feito com ❤️ para facilitar a vida dos revendedores de carros!**