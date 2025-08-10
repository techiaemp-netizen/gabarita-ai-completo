# 🔌 Documentação da API - Gabarita.AI

## 📋 Visão Geral

A API do Gabarita.AI é uma API RESTful construída com Flask que fornece todos os endpoints necessários para o funcionamento da plataforma de estudos.

**Base URL:** `https://j6h5i7c0x703.manus.space`
**Versão:** 1.0.0

## 🔐 Autenticação

A API utiliza autenticação baseada em tokens JWT fornecidos pelo Firebase Auth.

### Headers Obrigatórios
```http
Authorization: Bearer <firebase_token>
Content-Type: application/json
```

## 📚 Endpoints

### 🏥 Health Check

#### GET /health
Verifica o status da API.

**Resposta:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-23T17:30:00.000Z",
  "version": "1.0.0"
}
```

### 👤 Autenticação

#### POST /api/auth/login
Realiza login do usuário.

**Payload:**
```json
{
  "email": "usuario@email.com",
  "password": "senha123"
}
```

**Resposta:**
```json
{
  "success": true,
  "user": {
    "id": "user_123",
    "nome": "João Silva",
    "email": "usuario@email.com",
    "cargo": "Enfermeiro",
    "bloco": "Saúde"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### POST /api/auth/register
Registra novo usuário.

**Payload:**
```json
{
  "nome": "João Silva",
  "email": "usuario@email.com",
  "password": "senha123",
  "cargo": "Enfermeiro",
  "bloco": "Saúde",
  "cidade": "São Paulo",
  "estado": "SP"
}
```

#### POST /api/auth/logout
Realiza logout do usuário.

### 📝 Questões

#### POST /api/questoes/gerar
Gera uma nova questão usando IA.

**Payload:**
```json
{
  "cargo": "Enfermeiro",
  "tema": "SUS",
  "dificuldade": "medio",
  "conteudo_especifico": "Atenção Primária à Saúde"
}
```

**Resposta:**
```json
{
  "success": true,
  "questao": {
    "id": "q_123",
    "enunciado": "Sobre a Atenção Primária à Saúde no SUS...",
    "alternativas": [
      {
        "id": "A",
        "texto": "É responsabilidade exclusiva dos municípios"
      },
      {
        "id": "B",
        "texto": "Deve ser ofertada apenas em UBS"
      },
      {
        "id": "C",
        "texto": "É a porta de entrada preferencial do sistema"
      },
      {
        "id": "D",
        "texto": "Atende apenas casos de baixa complexidade"
      },
      {
        "id": "E",
        "texto": "Não inclui ações de promoção da saúde"
      }
    ],
    "gabarito": "C",
    "explicacao": "A Atenção Primária à Saúde é definida como...",
    "tema": "SUS",
    "subtema": "Atenção Primária",
    "dificuldade": "medio",
    "fonte": "ChatGPT",
    "tempo_geracao": 3.2,
    "created_at": "2025-01-23T17:30:00.000Z"
  }
}
```

#### GET /api/questoes/{questao_id}
Obtém detalhes de uma questão específica.

#### POST /api/questoes/{questao_id}/responder
Submete resposta para uma questão.

**Payload:**
```json
{
  "resposta": "C",
  "tempo_resposta": 45
}
```

**Resposta:**
```json
{
  "success": true,
  "correto": true,
  "gabarito": "C",
  "explicacao": "Explicação detalhada da resposta correta...",
  "estatisticas": {
    "acertos_consecutivos": 5,
    "taxa_acerto_geral": 78.5,
    "xp_ganho": 10,
    "vida_alteracao": 2
  }
}
```

#### POST /api/questoes/{questao_id}/favoritar
Adiciona/remove questão das favoritas.

#### POST /api/questoes/{questao_id}/comentar
Adiciona comentário a uma questão.

**Payload:**
```json
{
  "comentario": "Excelente questão sobre APS!",
  "parent_id": null
}
```

### 🎯 Simulados

#### POST /api/simulados/criar
Cria um novo simulado.

**Payload:**
```json
{
  "nome": "Simulado SUS - Janeiro 2025",
  "num_questoes": 30,
  "tempo_limite": 45,
  "materias": ["SUS", "Atenção Primária", "Epidemiologia"],
  "dificuldade": "medio"
}
```

**Resposta:**
```json
{
  "success": true,
  "simulado": {
    "id": "sim_123",
    "nome": "Simulado SUS - Janeiro 2025",
    "questoes": ["q_1", "q_2", "q_3"],
    "tempo_limite": 45,
    "created_at": "2025-01-23T17:30:00.000Z"
  }
}
```

#### GET /api/simulados/{simulado_id}
Obtém detalhes de um simulado.

#### POST /api/simulados/{simulado_id}/iniciar
Inicia um simulado.

#### POST /api/simulados/{simulado_id}/finalizar
Finaliza um simulado e calcula resultados.

**Resposta:**
```json
{
  "success": true,
  "resultado": {
    "nota": 8.5,
    "acertos": 25,
    "erros": 5,
    "tempo_total": 42,
    "percentil": 85.2,
    "aprovado": true,
    "detalhes_por_materia": {
      "SUS": {
        "acertos": 8,
        "total": 10,
        "percentual": 80
      }
    }
  }
}
```

### 📊 Rankings

#### GET /api/rankings
Obtém rankings segmentados.

**Query Parameters:**
- `tipo`: geral, cargo, bloco, regiao
- `periodo`: hoje, semana, mes, geral
- `cargo`: filtro por cargo específico
- `limit`: número de resultados (padrão: 50)

**Resposta:**
```json
{
  "success": true,
  "ranking": [
    {
      "posicao": 1,
      "usuario": {
        "id": "user_123",
        "nome": "Maria Silva",
        "avatar": "https://...",
        "cargo": "Enfermeiro"
      },
      "estatisticas": {
        "questoes_respondidas": 1247,
        "taxa_acerto": 89.5,
        "xp_total": 15420,
        "nivel": 23
      }
    }
  ],
  "minha_posicao": {
    "posicao": 15,
    "percentil": 92.3
  }
}
```

### 👤 Perfil do Usuário

#### GET /api/usuarios/perfil
Obtém perfil do usuário autenticado.

#### PUT /api/usuarios/perfil
Atualiza perfil do usuário.

**Payload:**
```json
{
  "nome": "João Silva Santos",
  "telefone": "(11) 99999-9999",
  "cidade": "São Paulo",
  "estado": "SP",
  "biografia": "Enfermeiro há 5 anos..."
}
```

#### GET /api/usuarios/estatisticas
Obtém estatísticas detalhadas do usuário.

**Resposta:**
```json
{
  "success": true,
  "estatisticas": {
    "questoes_respondidas": 1247,
    "acertos": 1056,
    "taxa_acerto": 84.7,
    "sequencia_atual": 12,
    "melhor_sequencia": 28,
    "xp_total": 15420,
    "nivel": 23,
    "vida": 85,
    "energia": 75,
    "conquistas": 15,
    "tempo_estudo_total": 4320,
    "por_materia": {
      "SUS": {
        "questoes": 450,
        "acertos": 380,
        "taxa": 84.4
      }
    }
  }
}
```

### 🔔 Notificações

#### GET /api/notificacoes
Lista notificações do usuário.

**Query Parameters:**
- `tipo`: todas, nao_lidas, alta_prioridade
- `limit`: número de resultados
- `offset`: paginação

#### PUT /api/notificacoes/{notificacao_id}/marcar-lida
Marca notificação como lida.

#### DELETE /api/notificacoes/{notificacao_id}
Remove notificação.

### 🤖 IA e Sugestões

#### POST /api/ia/sugestoes-estudo
Obtém sugestões personalizadas de estudo.

**Resposta:**
```json
{
  "success": true,
  "sugestoes": [
    {
      "tipo": "foco_fraqueza",
      "titulo": "Fortalecer Epidemiologia",
      "descricao": "Sua taxa de acerto em Epidemiologia está 15% abaixo da média...",
      "prioridade": "alta",
      "tempo_estimado": 120,
      "dificuldade": "medio",
      "impacto_esperado": "+15% taxa de acerto"
    }
  ]
}
```

#### POST /api/ia/chat
Chat com IA para dúvidas.

**Payload:**
```json
{
  "mensagem": "Como funciona o SUS?",
  "contexto": "duvida_geral"
}
```

### 📈 Analytics

#### GET /api/analytics/dashboard
Dados para dashboard personalizado.

#### GET /api/analytics/desempenho
Análise de desempenho por período.

**Query Parameters:**
- `periodo`: 7d, 30d, 90d, 1y
- `materia`: filtro por matéria específica

## 🚨 Códigos de Erro

### Códigos HTTP
- `200` - Sucesso
- `201` - Criado com sucesso
- `400` - Requisição inválida
- `401` - Não autorizado
- `403` - Acesso negado
- `404` - Não encontrado
- `429` - Muitas requisições
- `500` - Erro interno do servidor

### Estrutura de Erro
```json
{
  "success": false,
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Dados de entrada inválidos",
    "details": {
      "field": "email",
      "reason": "Formato de email inválido"
    }
  }
}
```

### Códigos de Erro Específicos
- `AUTH_REQUIRED` - Autenticação necessária
- `INVALID_TOKEN` - Token inválido ou expirado
- `USER_NOT_FOUND` - Usuário não encontrado
- `QUESTION_NOT_FOUND` - Questão não encontrada
- `SIMULATION_NOT_FOUND` - Simulado não encontrado
- `RATE_LIMIT_EXCEEDED` - Limite de requisições excedido
- `AI_SERVICE_UNAVAILABLE` - Serviço de IA indisponível

## 🔄 Rate Limiting

A API implementa rate limiting para proteger contra abuso:

- **Geral:** 1000 requisições por hora por usuário
- **Geração de Questões:** 50 requisições por hora
- **Chat IA:** 100 mensagens por hora
- **Login:** 10 tentativas por minuto

Headers de resposta:
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642694400
```

## 📝 Webhooks

### Configuração
Configure webhooks para receber notificações de eventos importantes.

### Eventos Disponíveis
- `user.registered` - Novo usuário registrado
- `question.answered` - Questão respondida
- `simulation.completed` - Simulado finalizado
- `achievement.unlocked` - Conquista desbloqueada

### Estrutura do Webhook
```json
{
  "event": "user.registered",
  "timestamp": "2025-01-23T17:30:00.000Z",
  "data": {
    "user_id": "user_123",
    "email": "usuario@email.com"
  }
}
```

## 🧪 Ambiente de Testes

**Base URL de Teste:** `https://test-api.gabarita-ai.com`

### Dados de Teste
```json
{
  "test_user": {
    "email": "teste@gabarita-ai.com",
    "password": "teste123"
  }
}
```

## 📚 SDKs e Bibliotecas

### JavaScript/TypeScript
```javascript
import { GabaritaAI } from '@gabarita-ai/sdk';

const client = new GabaritaAI({
  apiKey: 'your-api-key',
  baseURL: 'https://j6h5i7c0x703.manus.space'
});

// Gerar questão
const questao = await client.questoes.gerar({
  cargo: 'Enfermeiro',
  tema: 'SUS'
});
```

### Python
```python
from gabarita_ai import GabaritaAI

client = GabaritaAI(
    api_key='your-api-key',
    base_url='https://j6h5i7c0x703.manus.space'
)

# Gerar questão
questao = client.questoes.gerar(
    cargo='Enfermeiro',
    tema='SUS'
)
```

---

**Última atualização:** Janeiro 2025
**Versão da API:** 1.0.0

