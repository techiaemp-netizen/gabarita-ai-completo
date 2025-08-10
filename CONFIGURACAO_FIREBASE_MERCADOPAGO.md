# 🔥 Configuração Firebase e Mercado Pago - Gabarita-AI

## 🚀 Firebase Configuration

### 1. Criar Projeto Firebase
1. Acesse [Firebase Console](https://console.firebase.google.com/)
2. Clique em "Adicionar projeto"
3. Nome do projeto: `gabarita-ai-project` (ou outro nome de sua escolha)
4. Ative Google Analytics (opcional)

### 2. Configurar Authentication
1. No painel do Firebase, vá em **Authentication**
2. Clique em "Começar"
3. Na aba **Sign-in method**, ative:
   - **Email/Password**
   - **Google** (opcional)

### 3. Configurar Firestore Database
1. No painel do Firebase, vá em **Firestore Database**
2. Clique em "Criar banco de dados"
3. Escolha **Modo de produção** ou **Modo de teste**
4. Selecione a localização (recomendado: `southamerica-east1`)

### 4. Gerar Chave de Serviço
1. Vá em **Configurações do projeto** (ícone de engrenagem)
2. Aba **Contas de serviço**
3. Clique em **Gerar nova chave privada**
4. Baixe o arquivo JSON

### 5. Configurar Variáveis de Ambiente
Abra o arquivo `.env` e substitua as seguintes variáveis com os dados do arquivo JSON baixado:

```env
# Firebase Configuration
FIREBASE_PROJECT_ID=seu-project-id-aqui
FIREBASE_PRIVATE_KEY_ID=sua-private-key-id-aqui
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nSUA-PRIVATE-KEY-AQUI\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxxx@seu-project.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=seu-client-id-aqui
```

**⚠️ IMPORTANTE:** 
- A `FIREBASE_PRIVATE_KEY` deve estar entre aspas duplas
- Substitua `\n` por quebras de linha reais na chave privada
- Mantenha o formato exato da chave privada

---

## 💳 Mercado Pago Configuration

### 1. Criar Conta Mercado Pago
1. Acesse [Mercado Pago Developers](https://www.mercadopago.com.br/developers)
2. Faça login ou crie uma conta
3. Vá em **Suas integrações**

### 2. Criar Aplicação
1. Clique em **Criar aplicação**
2. Nome: `Gabarita-AI`
3. Selecione **Pagamentos online**
4. Clique em **Criar aplicação**

### 3. Obter Credenciais
1. Na sua aplicação, vá em **Credenciais**
2. **Para TESTE:**
   - Copie o **Access Token de teste**
   - Copie a **Public Key de teste**

3. **Para PRODUÇÃO:**
   - Copie o **Access Token de produção**
   - Copie a **Public Key de produção**

### 4. Configurar Webhook
1. Na aplicação, vá em **Webhooks**
2. URL do webhook: `https://seu-backend-url.com/api/pagamentos/webhook`
3. Eventos selecionados:
   - `payment`
   - `merchant_order`

### 5. Configurar Variáveis de Ambiente
No arquivo `.env`, configure:

```env
# MercadoPago Configuration
# Para TESTE (use TEST- no início)
MERCADO_PAGO_ACCESS_TOKEN=TEST-1234567890-abcdef-ghijklmnop
MERCADO_PAGO_WEBHOOK_SECRET=sua-webhook-secret-aqui

# Para PRODUÇÃO (remova TEST-)
# MERCADO_PAGO_ACCESS_TOKEN=APP_USR-1234567890-abcdef-ghijklmnop
```

---

## 🔧 Testando a Configuração

### 1. Reiniciar o Servidor
```bash
# Pare o servidor atual (Ctrl+C)
# Inicie novamente
python src/main.py
```

### 2. Verificar Logs
Se configurado corretamente, você verá:
```
[FIREBASE] Conectado ao projeto: seu-project-id
[PAYMENTS] Mercado Pago configurado com sucesso
```

### 3. Testar Firebase
- Tente fazer cadastro/login
- Verifique se os dados aparecem no Firestore

### 4. Testar Mercado Pago
- Acesse a rota de pagamentos
- Tente criar uma preferência de pagamento

---

## 🚨 Troubleshooting

### Firebase não conecta
- Verifique se todas as variáveis estão preenchidas
- Confirme se a chave privada está no formato correto
- Verifique se o projeto existe no Firebase Console

### Mercado Pago não funciona
- Confirme se o Access Token está correto
- Para teste, use tokens que começam com `TEST-`
- Verifique se a aplicação está ativa no painel

### Erro de CORS
- Configure as URLs corretas em `FRONTEND_URL` e `BACKEND_URL`
- Adicione as URLs em `CORS_ORIGINS`

---

## 📝 Próximos Passos

1. **Configurar Firebase** seguindo os passos acima
2. **Configurar Mercado Pago** seguindo os passos acima
3. **Testar em ambiente de desenvolvimento**
4. **Configurar para produção** quando estiver tudo funcionando

**🎯 Resultado esperado:** Firebase e Mercado Pago funcionando 100% em produção!