# 🎮 Deploy dos Jogos - Gabarita AI

## 📋 Visão Geral

Este documento contém as instruções completas para o deploy do sistema de jogos do Gabarita AI, incluindo configurações para diferentes planos de usuário e todas as integrações necessárias.

## 🎯 Planos e Disponibilidade dos Jogos

### Plano Trial (Gratuito)
- ✅ **Jogo da Forca** - Disponível
- ❌ Quiz Rápido - Bloqueado
- ❌ Jogo da Memória - Bloqueado  
- ❌ Palavras Cruzadas - Bloqueado
- ❌ Roleta da Sorte - Bloqueado

### Plano Premium
- ✅ **Todos os jogos disponíveis**
- ✅ **Roleta da Sorte** - 3x por dia
- ✅ **Ranking completo**
- ✅ **Estatísticas avançadas**

### Plano "Até o Final do Concurso"
- ✅ **Todos os jogos disponíveis**
- ✅ **Roleta da Sorte** - 5x por dia
- ✅ **Prêmios especiais na roleta**
- ✅ **Acesso prioritário a novos jogos**

## 🚀 Checklist de Deploy

### 1. Backend (Render)

#### 1.1 Configuração do Ambiente
```bash
# Variáveis de ambiente necessárias no Render
OPENAI_API_KEY=sk-...
FIREBASE_CREDENTIALS='{"type":"service_account",...}'
FLASK_ENV=production
CORS_ORIGINS=https://gabarita-ai-frontend.vercel.app
API_BASE_URL=https://gabarita-ai-backend.onrender.com
```

#### 1.2 Deploy do Backend
```bash
# 1. Fazer push das alterações para o repositório
git add .
git commit -m "feat: implementação completa do sistema de jogos"
git push origin main

# 2. No Render Dashboard:
# - Conectar ao repositório GitHub
# - Configurar build command: pip install -r requirements.txt
# - Configurar start command: gunicorn -w 4 -b 0.0.0.0:$PORT src.main:app
# - Definir diretório raiz: gabarita-ai-backend
```

#### 1.3 Verificação do Backend
```bash
# Testar endpoints dos jogos
curl https://gabarita-ai-backend.onrender.com/api/jogos/listar
curl https://gabarita-ai-backend.onrender.com/health
```

### 2. Frontend (Vercel)

#### 2.1 Configuração do Ambiente
```bash
# Variáveis de ambiente no Vercel
NEXT_PUBLIC_API_URL=https://gabarita-ai-backend.onrender.com
NEXT_PUBLIC_FIREBASE_API_KEY=AIza...
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=gabarita-ai.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=gabarita-ai
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=gabarita-ai.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=123456789
NEXT_PUBLIC_FIREBASE_APP_ID=1:123456789:web:abc123
```

#### 2.2 Deploy do Frontend
```bash
# 1. Instalar dependências
cd gabarita-ai-frontend
npm install

# 2. Build local para testar
npm run build
npm run start

# 3. Deploy no Vercel
# - Conectar repositório no Vercel Dashboard
# - Configurar diretório raiz: gabarita-ai-frontend
# - Build Command: npm run build
# - Output Directory: .next
```

#### 2.3 Verificação do Frontend
- ✅ Página de jogos carrega corretamente
- ✅ Jogos são filtrados por plano do usuário
- ✅ Roleta da sorte funciona
- ✅ Navegação entre jogos funciona

### 3. Firebase

#### 3.1 Configuração do Firestore
```javascript
// Estrutura de coleções necessárias:

// users/{userId}
{
  email: string,
  nome: string,
  plano: 'trial' | 'premium' | 'ate_final_concurso',
  bloco: string,
  estatisticas_jogos: {
    pontos_total: number,
    jogos_jogados: number,
    vitorias: number,
    melhor_sequencia: number
  },
  roleta: {
    tentativas_hoje: number,
    ultima_tentativa: timestamp,
    premios_ganhos: array
  }
}

// sessoes_jogos/{sessaoId}
{
  tipo: string,
  usuario_id: string,
  bloco: string,
  status: 'ativo' | 'finalizado',
  pontos: number,
  tempo_inicio: timestamp,
  tempo_limite: number,
  dados_jogo: object // específico para cada tipo de jogo
}

// ranking_jogos/{periodo}
{
  usuarios: [{
    usuario_id: string,
    nome: string,
    pontos: number,
    jogos_jogados: number
  }],
  atualizado_em: timestamp
}
```

#### 3.2 Regras de Segurança
```javascript
// firestore.rules
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Usuários podem ler/escrever apenas seus próprios dados
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Sessões de jogos
    match /sessoes_jogos/{sessaoId} {
      allow read, write: if request.auth != null && 
        resource.data.usuario_id == request.auth.uid;
    }
    
    // Ranking é público para leitura
    match /ranking_jogos/{document} {
      allow read: if request.auth != null;
      allow write: if false; // Apenas via Cloud Functions
    }
  }
}
```

### 4. Landing Page

#### 4.1 Atualização dos Planos
```html
<!-- Adicionar na seção de planos -->
<div class="plano-feature">
  <h4>🎮 Sistema de Jogos Educativos</h4>
  <ul>
    <li class="trial">Jogo da Forca</li>
    <li class="premium">Quiz Rápido</li>
    <li class="premium">Jogo da Memória</li>
    <li class="premium">Palavras Cruzadas</li>
    <li class="premium">Roleta da Sorte</li>
    <li class="premium">Ranking e Estatísticas</li>
  </ul>
</div>
```

#### 4.2 Deploy da Landing Page
```bash
# 1. Atualizar arquivos HTML/CSS/JS
# 2. Fazer upload via FTP ou Git
# 3. Verificar se as alterações estão visíveis
```

### 5. Configurações de Produção

#### 5.1 CORS e Segurança
```python
# backend/src/main.py
from flask_cors import CORS

CORS(app, origins=[
    "https://gabarita-ai-frontend.vercel.app",
    "https://www.gabarita-ai.com",
    "https://gabarita-ai.com"
])
```

#### 5.2 Rate Limiting
```python
# Implementar rate limiting para APIs dos jogos
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/jogos/iniciar', methods=['POST'])
@limiter.limit("10 per minute")
def iniciar_jogo():
    # ...
```

## 🧪 Testes de Produção

### 1. Testes Funcionais
```bash
# Testar cada jogo individualmente
# 1. Jogo da Forca
# 2. Quiz Rápido  
# 3. Jogo da Memória
# 4. Palavras Cruzadas
# 5. Roleta da Sorte
```

### 2. Testes de Planos
```bash
# Criar usuários de teste para cada plano
# Verificar restrições de acesso
# Testar upgrade/downgrade de planos
```

### 3. Testes de Performance
```bash
# Testar com múltiplos usuários simultâneos
# Verificar tempo de resposta das APIs
# Monitorar uso de recursos
```

## 📊 Monitoramento

### 1. Métricas Importantes
- Número de jogos iniciados por dia
- Taxa de conclusão dos jogos
- Tempo médio de jogo
- Uso da roleta da sorte
- Erros de API

### 2. Logs
```python
# Configurar logging adequado
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
```

## 🔧 Manutenção

### 1. Backup dos Dados
```bash
# Configurar backup automático do Firestore
# Exportar dados de sessões de jogos regularmente
```

### 2. Atualizações
```bash
# Processo para atualizações:
# 1. Testar em ambiente de desenvolvimento
# 2. Deploy em staging
# 3. Testes de regressão
# 4. Deploy em produção
# 5. Monitoramento pós-deploy
```

## 🚨 Troubleshooting

### Problemas Comuns

1. **Jogos não carregam**
   - Verificar se o backend está online
   - Checar configurações de CORS
   - Validar variáveis de ambiente

2. **Roleta não funciona**
   - Verificar rate limiting
   - Checar regras do Firestore
   - Validar lógica de probabilidades

3. **Planos não são respeitados**
   - Verificar middleware de autenticação
   - Checar dados do usuário no Firebase
   - Validar lógica de restrições

## 📞 Contatos de Suporte

- **Desenvolvedor Principal**: [seu-email@exemplo.com]
- **DevOps**: [devops@exemplo.com]
- **Suporte**: [suporte@gabarita-ai.com]

---

## ⚠️ IMPORTANTE - ATIVAÇÃO DO SISTEMA

**Este sistema está pronto para deploy, mas aguardando aprovação para ativação.**

Para ativar completamente:

1. ✅ Fazer deploy do backend no Render
2. ✅ Fazer deploy do frontend no Vercel  
3. ✅ Configurar Firebase com as novas coleções
4. ✅ Atualizar landing page com novos planos
5. ⏳ **AGUARDANDO**: Aprovação final para ativação

Após aprovação, executar:
```bash
# Ativar sistema de jogos
curl -X POST https://gabarita-ai-backend.onrender.com/api/admin/ativar-jogos \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

**Status**: 🟡 Pronto para ativação
**Última atualização**: $(date)