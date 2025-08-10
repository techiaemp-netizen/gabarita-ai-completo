# 📋 Manual de Instalação - Gabarita.AI

## 🎯 Visão Geral

Este manual fornece instruções detalhadas para instalar e configurar o Gabarita.AI em diferentes ambientes.

## 🔧 Pré-requisitos

### Sistema Operacional
- **Linux:** Ubuntu 20.04+ (recomendado)
- **macOS:** 10.15+
- **Windows:** 10+ com WSL2

### Software Necessário
- **Node.js:** 20.0.0 ou superior
- **Python:** 3.11 ou superior
- **Git:** Para clonagem do repositório
- **pnpm:** Gerenciador de pacotes (recomendado)

### Contas e APIs
- **OpenAI API Key:** Para geração de questões
- **Perplexity API Key:** Para pesquisas inteligentes
- **Firebase Project:** Para autenticação e banco de dados

## 📦 Instalação Local

### 1. Clonagem do Repositório

```bash
git clone https://github.com/seu-usuario/gabarita-ai.git
cd gabarita-ai
```

### 2. Configuração do Backend

#### 2.1. Navegue para o diretório do backend
```bash
cd gabarita-ai-backend
```

#### 2.2. Crie um ambiente virtual Python
```bash
python3.11 -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows
```

#### 2.3. Instale as dependências
```bash
pip install -r requirements.txt
```

#### 2.4. Configure as variáveis de ambiente
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:
```env
# APIs de IA
OPENAI_API_KEY=sk-proj-sua_chave_openai_aqui
PERPLEXITY_API_KEY=pplx-sua_chave_perplexity_aqui

# Firebase
FIREBASE_PROJECT_ID=seu-projeto-firebase
FIREBASE_PRIVATE_KEY_ID=sua_key_id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nsua_private_key_aqui\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=firebase-adminsdk@seu-projeto.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=sua_client_id

# Configurações do Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=sua_chave_secreta_super_segura_aqui
```

#### 2.5. Configure o Firebase
1. Acesse o [Console do Firebase](https://console.firebase.google.com)
2. Crie um novo projeto ou use um existente
3. Vá em "Configurações do Projeto" > "Contas de Serviço"
4. Gere uma nova chave privada
5. Salve o arquivo JSON como `firebase-key.json` no diretório raiz do backend

#### 2.6. Inicie o servidor backend
```bash
python src/main.py
```

O servidor estará disponível em `http://localhost:5000`

### 3. Configuração do Frontend

#### 3.1. Navegue para o diretório do frontend
```bash
cd ../gabarita-ai-frontend
```

#### 3.2. Instale as dependências
```bash
pnpm install
# ou
npm install
```

#### 3.3. Configure as variáveis de ambiente
```bash
cp .env.example .env.local
```

Edite o arquivo `.env.local`:
```env
VITE_API_BASE_URL=http://localhost:5000
VITE_FIREBASE_API_KEY=sua_firebase_api_key
VITE_FIREBASE_AUTH_DOMAIN=seu-projeto.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=seu-projeto-firebase
```

#### 3.4. Inicie o servidor de desenvolvimento
```bash
pnpm dev
# ou
npm run dev
```

O frontend estará disponível em `http://localhost:5173`

## 🚀 Deploy em Produção

### 1. Build do Frontend

```bash
cd gabarita-ai-frontend
pnpm build
```

Os arquivos de produção estarão em `dist/`

### 2. Configuração do Servidor

#### 2.1. Nginx (recomendado)

Crie o arquivo `/etc/nginx/sites-available/gabarita-ai`:

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    # Frontend
    location / {
        root /var/www/gabarita-ai/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 2.2. SSL com Certbot

```bash
sudo certbot --nginx -d seu-dominio.com
```

### 3. Processo de Deploy Automatizado

#### 3.1. Usando PM2 para o Backend

```bash
# Instale o PM2 globalmente
npm install -g pm2

# Configure o arquivo ecosystem.config.js
cd gabarita-ai-backend
```

Crie `ecosystem.config.js`:
```javascript
module.exports = {
  apps: [{
    name: 'gabarita-ai-backend',
    script: 'src/main.py',
    interpreter: 'python3.11',
    env: {
      FLASK_ENV: 'production',
      PORT: 5000
    }
  }]
}
```

```bash
# Inicie a aplicação
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

## 🔧 Configurações Avançadas

### 1. Banco de Dados

#### 1.1. Firebase Firestore
- Configure as regras de segurança no Console Firebase
- Crie as coleções necessárias: `users`, `questions`, `simulations`

#### 1.2. Estrutura de Dados
```javascript
// Coleção: users
{
  uid: "string",
  email: "string",
  profile: {
    name: "string",
    cargo: "string",
    bloco: "string"
  },
  stats: {
    questionsAnswered: "number",
    correctAnswers: "number",
    level: "number",
    xp: "number"
  }
}
```

### 2. Monitoramento

#### 2.1. Logs
```bash
# Backend logs
tail -f gabarita-ai-backend/logs/app.log

# PM2 logs
pm2 logs gabarita-ai-backend
```

#### 2.2. Métricas
- Configure Google Analytics no frontend
- Use Firebase Analytics para métricas de usuário
- Monitore APIs com ferramentas como New Relic

### 3. Backup

#### 3.1. Backup do Firebase
```bash
# Instale a CLI do Firebase
npm install -g firebase-tools

# Configure backup automático
firebase firestore:export gs://seu-bucket/backup-$(date +%Y%m%d)
```

#### 3.2. Backup do Código
```bash
# Script de backup automático
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf "backup_gabarita_ai_$DATE.tar.gz" gabarita-ai/
```

## 🐛 Solução de Problemas

### Problemas Comuns

#### 1. Erro de CORS
**Problema:** Frontend não consegue acessar o backend
**Solução:** Verifique se o Flask-CORS está configurado corretamente

```python
from flask_cors import CORS
CORS(app, origins=['http://localhost:5173', 'https://seu-dominio.com'])
```

#### 2. Erro de Firebase
**Problema:** "Firebase app not initialized"
**Solução:** Verifique se o arquivo `firebase-key.json` está no local correto

#### 3. Erro de API Keys
**Problema:** APIs de IA não funcionam
**Solução:** Verifique se as chaves estão corretas no arquivo `.env`

#### 4. Erro de Build
**Problema:** Build do frontend falha
**Solução:** Limpe o cache e reinstale dependências

```bash
rm -rf node_modules package-lock.json
pnpm install
```

### Logs de Debug

#### Backend
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Frontend
```javascript
// Adicione no vite.config.js
export default {
  define: {
    __DEV__: JSON.stringify(process.env.NODE_ENV === 'development')
  }
}
```

## 📞 Suporte

### Documentação Adicional
- [Documentação do React](https://react.dev)
- [Documentação do Flask](https://flask.palletsprojects.com)
- [Documentação do Firebase](https://firebase.google.com/docs)

### Contato
Para suporte técnico, abra uma issue no repositório ou entre em contato com a equipe de desenvolvimento.

---

**Última atualização:** Janeiro 2025
**Versão:** 1.0.0

