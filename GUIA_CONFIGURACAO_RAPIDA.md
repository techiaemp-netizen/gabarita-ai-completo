# 🚀 GUIA RÁPIDO - CONFIGURE E GANHE DINHEIRO HOJE!

## 🔥 FIREBASE - CONFIGURAÇÃO EM 10 MINUTOS

### Passo 1: Criar Projeto Firebase (GRATUITO)
1. Acesse: https://console.firebase.google.com/
2. Clique em "Adicionar projeto" ou "Create a project"
3. Nome do projeto: `gabarita-ai-producao`
4. Desabilite Google Analytics (não precisamos agora)
5. Clique em "Criar projeto"

### Passo 2: Configurar Autenticação
1. No menu lateral, clique em "Authentication"
2. Clique em "Começar" ou "Get started"
3. Vá na aba "Sign-in method"
4. Ative "Email/Password"
5. Salve

### Passo 3: Configurar Firestore Database
1. No menu lateral, clique em "Firestore Database"
2. Clique em "Criar banco de dados"
3. Escolha "Iniciar no modo de teste" (por enquanto)
4. Escolha a localização mais próxima (ex: southamerica-east1)
5. Clique em "Concluído"

### Passo 4: Gerar Chave de Serviço (IMPORTANTE!)
1. Clique no ícone de engrenagem ⚙️ > "Configurações do projeto"
2. Vá na aba "Contas de serviço"
3. Clique em "Gerar nova chave privada"
4. Escolha "JSON" e clique em "Gerar chave"
5. **BAIXE O ARQUIVO JSON** - você vai precisar dele!

### Passo 5: Copiar Informações para o .env
Abra o arquivo JSON baixado e copie as informações:

```env
# FIREBASE - COPIE DO ARQUIVO JSON
FIREBASE_PROJECT_ID=seu-project-id-aqui
FIREBASE_PRIVATE_KEY_ID=sua-private-key-id-aqui
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nSUA_CHAVE_PRIVADA_AQUI\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxxx@seu-projeto.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=seu-client-id-aqui
FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
```

---

## 💳 MERCADO PAGO - CONFIGURAÇÃO EM 5 MINUTOS

### Passo 1: Criar Conta (GRATUITO)
1. Acesse: https://www.mercadopago.com.br/
2. Clique em "Criar conta" se não tiver
3. Complete seu cadastro

### Passo 2: Acessar Área de Desenvolvedores
1. Acesse: https://www.mercadopago.com.br/developers/
2. Faça login com sua conta
3. Clique em "Suas integrações"

### Passo 3: Criar Aplicação
1. Clique em "Criar aplicação"
2. Nome: `Gabarita AI`
3. Selecione "Pagamentos online e presenciais"
4. Clique em "Criar aplicação"

### Passo 4: Obter Credenciais
1. Na sua aplicação criada, vá em "Credenciais"
2. **PARA TESTE (comece aqui):**
   - Copie o "Access Token" de TESTE
   - Adicione no .env: `MERCADO_PAGO_ACCESS_TOKEN=TEST-xxxxxxx`

3. **PARA PRODUÇÃO (depois dos testes):**
   - Ative sua conta (precisa de documentos)
   - Copie o "Access Token" de PRODUÇÃO
   - Substitua no .env: `MERCADO_PAGO_ACCESS_TOKEN=APP-xxxxxxx`

### Passo 5: Configurar Webhook (Opcional)
1. Em "Webhooks", adicione: `https://seu-dominio.com/webhook/mercadopago`
2. Copie o "Webhook Secret" para o .env

---

## ⚡ CONFIGURAÇÃO FINAL DO .env

Abra o arquivo `.env` na raiz do projeto e preencha:

```env
# ===== FIREBASE =====
FIREBASE_PROJECT_ID=seu-project-id
FIREBASE_PRIVATE_KEY_ID=sua-private-key-id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nSUA_CHAVE\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxxx@projeto.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=seu-client-id
FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token

# ===== MERCADO PAGO =====
MERCADO_PAGO_ACCESS_TOKEN=TEST-xxxxxxx-ou-APP-xxxxxxx
MERCADO_PAGO_WEBHOOK_SECRET=sua-webhook-secret

# ===== OUTRAS CONFIGURAÇÕES =====
OPENAI_API_KEY=sua-chave-openai
PERPLEXITY_API_KEY=sua-chave-perplexity
SECRET_KEY=uma-chave-secreta-qualquer-123456
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:5000
```

---

## 🧪 TESTAR CONFIGURAÇÃO

Execute o teste:
```bash
python test_configuracao.py
```

Se tudo estiver ✅ verde, você está pronto!

---

## 🚀 COLOCAR NO AR

### Opção 1: Render (Recomendado)
1. Crie conta no Render.com
2. Conecte seu repositório GitHub
3. Configure as variáveis de ambiente
4. Deploy automático!

### Opção 2: Vercel
1. Crie conta no Vercel.com
2. Importe o projeto
3. Configure as variáveis
4. Deploy!

---

## 💰 PLANOS DE PREÇOS SUGERIDOS

- **Básico:** R$ 29,90/mês - 100 questões
- **Premium:** R$ 49,90/mês - Questões ilimitadas + IA
- **Pro:** R$ 99,90/mês - Tudo + Mentoria
- **Intensivo:** R$ 199,90/mês - Preparação completa

---

## 🆘 PROBLEMAS?

### Firebase não conecta?
- Verifique se copiou EXATAMENTE as informações do JSON
- A chave privada deve ter as quebras de linha `\n`
- Certifique-se que o Firestore está criado

### Mercado Pago não funciona?
- Use primeiro o token de TESTE
- Verifique se a aplicação foi criada corretamente
- Para produção, precisa ativar a conta

### Ainda com problemas?
- Execute: `python test_configuracao.py`
- Verifique os logs do servidor
- Consulte a documentação oficial

---

## 🎉 PRONTO PARA FATURAR!

Com essas configurações, sua plataforma estará 100% funcional e pronta para receber pagamentos reais!

**Boa sorte e muito sucesso! 💰🚀**