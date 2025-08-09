# Gabarit-AI Backend

Backend da aplicação Gabarit-AI - Sistema de questões para concursos públicos.

## Tecnologias

- Python 3.11
- Flask
- Firebase Admin SDK
- OpenAI API
- Perplexity API
- MercadoPago API

## Estrutura do Projeto

```
src/
├── config/          # Configurações do Firebase
├── database/        # Banco de dados SQLite
├── models/          # Modelos de dados
├── routes/          # Rotas da API
├── services/        # Serviços externos (OpenAI, Perplexity)
├── static/          # Arquivos estáticos
└── utils/           # Utilitários
```

## Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e configure as seguintes variáveis:

- `OPENAI_API_KEY`: Chave da API OpenAI
- `PERPLEXITY_API_KEY`: Chave da API Perplexity
- `MERCADO_PAGO_ACCESS_TOKEN`: Token do MercadoPago
- `FIREBASE_*`: Configurações do Firebase
- `SECRET_KEY`: Chave secreta da aplicação
- `FRONTEND_URL`: URL do frontend
- `BACKEND_URL`: URL do backend

## Deploy no Render

Este projeto está configurado para deploy automático no Render usando o arquivo `render.yaml`.

### Configuração Manual

1. Conecte este repositório ao Render
2. Configure as variáveis de ambiente no painel do Render
3. O deploy será feito automaticamente

## Endpoints Principais

- `GET /health` - Health check
- `POST /api/auth/login` - Login de usuário
- `POST /api/questoes/gerar` - Gerar questões
- `POST /api/payments/*` - Endpoints de pagamento

## Desenvolvimento Local

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
python src/main.py
```

A aplicação estará disponível em `http://localhost:5000`