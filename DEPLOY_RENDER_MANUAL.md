# 🚀 Deploy Manual no Render.com

## Pré-requisitos ✅
- [x] Código no GitHub: https://github.com/techiaemp-netizen/gabarita-ai-backend
- [x] Credenciais de produção configuradas
- [x] Conta no Render.com

## Passo a Passo para Deploy

### 1. Acesse o Render.com
- Vá para: https://render.com
- Faça login ou crie uma conta
- Conecte sua conta do GitHub

### 2. Criar Novo Web Service
1. Clique em **"New +"**
2. Selecione **"Web Service"**
3. Conecte seu repositório: `techiaemp-netizen/gabarita-ai-backend`

### 3. Configurações do Serviço
```
Name: gabarita-ai-backend
Region: Oregon (US West)
Branch: master
Root Directory: (deixe vazio)
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: python src/main.py
```

### 4. Configurar Variáveis de Ambiente
Na seção **Environment Variables**, adicione:

```bash
# Python
PYTHON_VERSION=3.11.0
PORT=10000

# Flask
FLASK_ENV=production
SECRET_KEY=sua_secret_key_aqui

# OpenAI
OPENAI_API_KEY=sua_openai_key_aqui

# Perplexity
PERPLEXITY_API_KEY=sua_perplexity_key_aqui

# Firebase
FIREBASE_PROJECT_ID=seu_project_id
FIREBASE_PRIVATE_KEY_ID=sua_private_key_id
FIREBASE_PRIVATE_KEY=sua_private_key_completa
FIREBASE_CLIENT_EMAIL=seu_client_email
FIREBASE_CLIENT_ID=seu_client_id
FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
FIREBASE_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
FIREBASE_CLIENT_X509_CERT_URL=sua_cert_url

# Mercado Pago
MERCADOPAGO_ACCESS_TOKEN=seu_access_token_producao
MERCADOPAGO_PUBLIC_KEY=sua_public_key_producao

# URLs
FRONTEND_URL=https://seu-frontend.render.com
BACKEND_URL=https://gabarita-ai-backend.onrender.com
CORS_ORIGINS=https://seu-frontend.render.com,http://localhost:3000
```

### 5. Deploy
1. Clique em **"Create Web Service"**
2. Aguarde o build e deploy (5-10 minutos)
3. Sua URL será: `https://gabarita-ai-backend.onrender.com`

### 6. Verificar Deploy
Após o deploy, teste:
- `https://gabarita-ai-backend.onrender.com/health` - Status da API
- `https://gabarita-ai-backend.onrender.com/api/test` - Teste básico

## 🔧 Configurações Importantes

### Auto-Deploy
- ✅ Ativado por padrão
- Cada push no GitHub fará novo deploy

### Plano Gratuito
- ✅ 750 horas/mês grátis
- ⚠️ Sleep após 15min inativo
- 💡 Upgrade para plano pago remove sleep

### Logs e Monitoramento
- Acesse logs em tempo real no dashboard
- Configure alertas de erro
- Monitore performance

## 🚨 Troubleshooting

### Build Falha
```bash
# Verifique requirements.txt
# Certifique-se que todas as dependências estão listadas
```

### Erro de Porta
```python
# Em src/main.py, certifique-se:
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

### Variáveis de Ambiente
- Verifique se todas estão configuradas
- Não inclua aspas nos valores
- Use valores de produção, não de teste

## 📱 Próximos Passos

1. **Frontend**: Deploy do frontend no Vercel/Netlify
2. **Domínio**: Configure domínio personalizado
3. **SSL**: Certificado automático (incluído)
4. **Monitoramento**: Configure alertas
5. **Backup**: Configure backup do banco

## 💰 Monetização Ativa

✅ **Mercado Pago Produção**: Pagamentos reais ativos
✅ **OpenAI Produção**: IA com cobrança real
✅ **Firebase Produção**: Banco de dados real
✅ **Sistema Completo**: Pronto para usuários pagantes

---

**🎉 Sua plataforma Gabarita-AI está pronta para gerar receita!**

URL do Backend: `https://gabarita-ai-backend.onrender.com`

*Lembre-se de atualizar as URLs no frontend após o deploy.*