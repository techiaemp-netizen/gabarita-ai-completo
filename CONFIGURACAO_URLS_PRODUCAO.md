# 🔗 Configuração de URLs de Produção

## 📋 URLs Atuais

### **Produção**
```
LANDING_PAGE_URL = "https://gabaritai.app.br"
FRONTEND_URL = "https://gabarita-ai-frontend-pied.vercel.app"
BACKEND_URL = "https://gabarita-ai-api.onrender.com"
```

### **Desenvolvimento**
```
LANDING_PAGE_URL = "http://localhost:3000"
FRONTEND_URL = "http://localhost:3001"
BACKEND_URL = "http://localhost:5000"
```

## 🔧 Como Atualizar URLs

### **1. Landing Page (gabarita-ai-landing)**

**Arquivo:** `src/app/page.tsx`

**Buscar e substituir:**
```javascript
// ATUAL
window.location.href = 'https://gabarita-ai-frontend-pied.vercel.app/login'

// NOVO (exemplo)
window.location.href = 'https://app.gabaritai.com.br/login'
```

**Links a atualizar:**
- Linha ~83: Botão "Entrar" → `/login`
- Linha ~84: Botão "Começar Grátis" → `/signup`
- Linha ~131: Botão "Começar Agora" → `/signup`
- Linha ~135: Botão "Ver Demonstração" → `/simulado`
- Linha ~278: Botão "Começar Gratuitamente" → `/signup`
- Linha ~403: Botões dos Planos → `/signup`

### **2. Frontend (gabarita-ai-frontend)**

**Arquivo:** `src/config/api.js` (se existir)
```javascript
// Atualizar URL da API
const API_BASE_URL = 'https://gabarita-ai-api.onrender.com';
```

**Arquivos de configuração:**
- `.env.production`
- `next.config.js`
- `vercel.json`

### **3. Backend (gabarita-ai-backend)**

**Variáveis de ambiente no Render:**
```
FRONTEND_URL=https://app.gabaritai.com.br
CORS_ORIGINS=https://gabaritai.app.br,https://app.gabaritai.com.br
```

## 🚀 Processo de Deploy

### **1. Atualizar URLs**
1. Alterar URLs na landing page
2. Alterar URLs no frontend (se necessário)
3. Atualizar CORS no backend

### **2. Deploy Sequencial**
1. **Backend** (Render) - Deploy automático
2. **Frontend** (Vercel) - `vercel --prod`
3. **Landing** (Vercel) - `vercel --prod`

### **3. Testar Integração**
1. Acessar landing page
2. Clicar em "Entrar" → Deve ir para frontend/login
3. Clicar em "Começar Grátis" → Deve ir para frontend/signup
4. Testar todos os botões

## 🔍 Checklist de Verificação

### **Landing Page → Frontend**
- [ ] Botão "Entrar" redireciona para `/login`
- [ ] Botão "Começar Grátis" redireciona para `/signup`
- [ ] Botão "Começar Agora" redireciona para `/signup`
- [ ] Botão "Ver Demonstração" redireciona para `/simulado`
- [ ] Botão "Começar Gratuitamente" redireciona para `/signup`
- [ ] Botões dos planos redirecionam para `/signup`

### **Frontend → Backend**
- [ ] Login funciona
- [ ] Cadastro funciona
- [ ] Geração de questões funciona
- [ ] Pagamentos funcionam

### **Geral**
- [ ] Não há erros 404
- [ ] Não há erros de CORS
- [ ] SSL funcionando em todos os domínios
- [ ] Performance adequada

## 🛠️ Comandos Úteis

### **Deploy Landing Page**
```bash
cd gabarita-ai-landing
npm run build
vercel --prod
```

### **Deploy Frontend**
```bash
cd gabarita-ai-frontend
npm run build
vercel --prod
```

### **Verificar URLs**
```bash
# Testar landing page
curl -I https://gabaritai.app.br

# Testar frontend
curl -I https://gabarita-ai-frontend-pied.vercel.app

# Testar backend
curl -I https://gabarita-ai-api.onrender.com/health
```

## 📝 Notas Importantes

1. **Sempre testar em ambiente de desenvolvimento primeiro**
2. **Fazer backup das configurações antes de alterar**
3. **Verificar CORS após mudanças de domínio**
4. **Monitorar logs após deploy**
5. **Testar todos os fluxos de usuário**

## 🔄 Histórico de Mudanças

### **2025-01-23**
- ✅ Corrigido erro 404 nos links da landing page
- ✅ Alterados links relativos para URLs absolutas
- ✅ Todos os botões funcionando corretamente

---

**Status Atual: ✅ FUNCIONANDO PERFEITAMENTE**