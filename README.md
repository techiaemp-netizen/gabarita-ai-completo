<<<<<<< HEAD
# 🎯 Gabarita.AI - Plataforma Inteligente para Concursos Públicos

## 📋 Visão Geral

O **Gabarita.AI** é uma plataforma completa de estudos para concursos públicos da área da saúde, desenvolvida com tecnologias modernas e inteligência artificial. A plataforma oferece uma experiência gamificada e personalizada para maximizar o desempenho dos candidatos.

## 🚀 URLs de Produção

- **Frontend:** https://kjjorqly.manus.space
- **Backend:** https://j6h5i7c0x703.manus.space

## ✨ Funcionalidades Principais

### 🎮 Sistema de Gamificação
- **Barra de Vida e Energia:** Sistema dinâmico que reflete o desempenho
- **XP e Níveis:** Progressão baseada em atividades de estudo
- **Conquistas e Badges:** Recompensas por marcos alcançados
- **Power-ups:** Itens especiais para potencializar os estudos

### 🤖 Inteligência Artificial
- **Geração de Questões:** ChatGPT e Perplexity criam questões personalizadas
- **Sugestões Inteligentes:** IA analisa desempenho e sugere planos de estudo
- **FAQ Inteligente:** Sistema de perguntas frequentes com chat IA

### 📊 Analytics e Desempenho
- **Dashboard Personalizado:** Widgets configuráveis com métricas importantes
- **Ranking Segmentado:** Comparação por cargo, bloco e região
- **Nota de Corte Simulada:** Previsão de aprovação baseada no desempenho
- **Histórico Completo:** Análise detalhada de todas as atividades

### 🎯 Ferramentas de Estudo
- **Simulados Cronometrados:** Configuráveis com diferentes parâmetros
- **Sistema de Favoritas:** Organização de questões por listas personalizadas
- **Correção Inteligente:** Feedback educativo com explicações detalhadas
- **Comentários Sociais:** Interação com outros usuários

## 📊 APIs Dinâmicas do Dashboard

### 1. Estatísticas Gerais (`/dashboard/estatisticas-gerais/<usuario_id>`)

**Fórmulas de Cálculo:**

- **Taxa de Acerto**: `(questões_corretas / questões_respondidas) × 100`
- **Nível Atual**: `(xp_atual ÷ 100) + 1` (100 XP por nível)
- **XP Próximo Nível**: `nivel_atual × 100`
- **Posição no Ranking**: `ranking_total × (100 - percentil) ÷ 100`
- **Percentil**: `min(taxa_acerto + 10, 99.9)` (baseado na taxa de acerto)
- **Média Tempo por Questão**: `(tempo_total_estudo × 60) ÷ questões_respondidas` (em segundos)
- **Questões Hoje**: `min(questões_respondidas % 25, 20)` (simulado)
- **Progresso Semanal**: `min((questões_hoje × 7 ÷ meta_semanal) × 100, 100)`

### 2. Desempenho Semanal (`/dashboard/desempenho-semanal/<usuario_id>`)

**Fórmulas de Cálculo:**

- **Questões por Dia**:
  - Dias úteis: `base_questoes + random(-5, 8)` onde `base_questoes = 20`
  - Fim de semana: `base_questoes - random(5, 10)`
- **Taxa de Acerto por Dia**: `max(50, min(100, taxa_acerto_media + variacao))` onde `variacao = random(-10, 10)`
- **Acertos por Dia**: `questoes × taxa_dia ÷ 100`
- **Tempo Médio**: `random(30, 60)` segundos por questão

### 3. Evolução Mensal (`/dashboard/evolucao-mensal/<usuario_id>`)

**Fórmulas de Cálculo:**

- **Taxa de Acerto Mensal**: `min(95, taxa_acerto_base + crescimento + variacao)`
  - `crescimento = mês_index × 2` (2% de crescimento por mês)
  - `variacao = random(-3, 3)`
- **Questões por Mês**: `400 + random(-50, 100)`

### 4. Metas do Usuário (`/dashboard/metas/<usuario_id>`)

**Fórmulas de Progresso:**

- **Meta Questões**: `(questões_respondidas ÷ meta_questoes_mes) × 100`
  - Meta padrão: 500 questões/mês
- **Meta Taxa de Acerto**: `(taxa_atual ÷ meta_taxa_acerto) × 100`
  - Meta padrão: 90%
- **Meta Tempo de Estudo**: `(tempo_total_estudo ÷ meta_tempo_mes) × 100`
  - Meta padrão: 1200 minutos/mês (20 horas)
- **Meta Dias Consecutivos**: `(dias_consecutivos ÷ meta_dias_consecutivos) × 100`
  - Meta padrão: 30 dias

### 5. Atividades Recentes (`/dashboard/atividades-recentes/<usuario_id>`)

**Cálculo de Tempo Relativo:**

```python
diff = datetime.now() - timestamp
if diff.days > 0:
    tempo_relativo = f'{diff.days}d atrás'
elif diff.seconds > 3600:
    horas = diff.seconds // 3600
    tempo_relativo = f'{horas}h atrás'
else:
    minutos = diff.seconds // 60
    tempo_relativo = f'{minutos}min atrás'
```

### 6. Notificações (`/dashboard/notificacoes/<usuario_id>`)

**Lógica de Geração:**

- **Meta Diária**: Ativada quando `questoes_hoje < meta_diaria`
- **Sequência de Acertos**: Ativada quando `sequencia_atual >= 10`
- **Próximo Nível**: Ativada quando `xp_atual >= xp_proximo_nivel - 50`
- **Baixo Desempenho**: Ativada quando taxa de acerto em matéria < 70%

### 7. Matérias por Cargo/Bloco (`/materias/<cargo>/<bloco>`)

**Simulação de Performance:**

- **Taxa de Acerto**: `70 + random(0, 25)` (70-95%)
- **Questões Respondidas**: `random(15, 45)`
- **Tempo Médio**: `random(30, 90)` segundos
- **Acertos**: `int(questoes × taxa_acerto ÷ 100)`

## 📈 Estrutura de Dados Firebase

### Coleção `usuarios`
```javascript
{
  uid: string,
  nome: string,
  email: string,
  cargo: string,
  bloco: string,
  questoes_respondidas: number,
  questoes_corretas: number,
  tempo_total_estudo: number, // em minutos
  dias_consecutivos: number,
  melhor_sequencia: number,
  xp_atual: number,
  sequencia_atual: number,
  questoes_hoje: number,
  materias_performance: object
}
```

### Coleção `questoes_respondidas`
```javascript
{
  usuario_id: string,
  questao_id: string,
  materia: string,
  correta: boolean,
  tempo_resposta: number, // em segundos
  timestamp: datetime
}
```

## 🔄 Fluxo de Dados Dinâmicos

1. **Usuário responde questão** → Dados salvos no Firebase
2. **Dashboard carrega** → APIs buscam dados reais do usuário
3. **Cálculos executados** → Fórmulas aplicadas aos dados brutos
4. **Interface atualizada** → Componentes React recebem dados processados
5. **Fallback ativado** → Dados simulados em caso de erro

## 🛠️ Tecnologias Utilizadas

### Frontend
- **React 19** com Vite
- **Tailwind CSS** para estilização
- **Lucide React** para ícones
- **React Router** para navegação
- **Recharts** para gráficos

### Backend
- **Flask** (Python 3.11)
- **Firebase** para autenticação e banco de dados
- **OpenAI API** para geração de questões
- **Perplexity API** para pesquisas inteligentes
- **Flask-CORS** para integração frontend/backend

## 📁 Estrutura do Projeto

```
gabarita-ai/
├── gabarita-ai-frontend/          # Aplicação React
│   ├── src/
│   │   ├── components/            # Componentes React
│   │   │   ├── Dashboard.jsx      # Dashboard principal
│   │   │   ├── GeradorQuestoes.jsx # Geração de questões IA
│   │   │   ├── Simulado.jsx       # Sistema de simulados
│   │   │   ├── Ranking.jsx        # Rankings segmentados
│   │   │   ├── Perfil.jsx         # Perfil do usuário
│   │   │   ├── BarraVida.jsx      # Sistema de gamificação
│   │   │   ├── Notificacoes.jsx   # Sistema de notificações
│   │   │   ├── FAQComIA.jsx       # FAQ com IA
│   │   │   └── ...                # Outros 8 módulos
│   │   ├── App.jsx                # Componente principal
│   │   └── main.jsx               # Entry point
│   ├── package.json               # Dependências do frontend
│   └── vite.config.js             # Configuração do Vite
├── gabarita-ai-backend/           # API Flask
│   ├── src/
│   │   ├── main.py                # Aplicação principal
│   │   ├── config/                # Configurações
│   │   ├── services/              # Serviços (IA, Firebase)
│   │   ├── routes/                # Rotas da API
│   │   └── models/                # Modelos de dados
│   ├── .env                       # Variáveis de ambiente
│   └── requirements.txt           # Dependências do backend
├── docs/                          # Documentação
├── README.md                      # Este arquivo
└── gabarita_ai_architecture.md    # Arquitetura técnica
```

## 🎯 16 Módulos Implementados

### Core (Módulos 1-8)
1. **Cadastro e Perfil do Usuário** - Sistema completo de perfil com edição
2. **Geração de Questões IA** - ChatGPT gera questões personalizadas
3. **Resposta e Correção** - Sistema inteligente de correção com feedback
4. **Comentário com Feedback** - Interação social entre usuários
5. **Ranking Segmentado** - Rankings por cargo, bloco e região
6. **Nota de Corte Simulada** - Previsão de aprovação em tempo real
7. **Barra de Progresso (Vida)** - Sistema de gamificação completo
8. **Histórico e Revisão** - Análise completa do desempenho

### Avançados (Módulos 9-16)
9. **Favoritar e Revisar Depois** - Listas personalizadas de questões
10. **Simulado Cronometrado** - Sistema completo de simulados
11. **Painel do Usuário (Dashboard)** - Dashboard personalizável
12. **Área de Perfil com Edição** - Gerenciamento completo do perfil
13. **Sugestões de Estudo** - IA sugere planos personalizados
14. **Sistema de Notificações** - Notificações inteligentes
15. **FAQ com IA** - Suporte automatizado com chat IA
16. **Configurações Avançadas** - Personalização completa da experiência

## 🚀 Como Executar Localmente

### Pré-requisitos
- Node.js 20+
- Python 3.11+
- npm/pnpm

### Frontend
```bash
cd gabarita-ai-frontend
pnpm install
pnpm dev
```

### Backend
```bash
cd gabarita-ai-backend
pip install -r requirements.txt
python src/main.py
```

## 🔧 Configuração

### Variáveis de Ambiente (.env)
```env
OPENAI_API_KEY=sua_chave_openai
PERPLEXITY_API_KEY=sua_chave_perplexity
FIREBASE_PROJECT_ID=seu_projeto_firebase
```

## 📱 Recursos Principais

### 🎯 Para Estudantes
- Questões personalizadas por IA
- Simulados realistas
- Gamificação motivacional
- Analytics detalhados
- Comunidade de estudos

### 🏆 Para Administradores
- Dashboard de analytics
- Gestão de usuários
- Configurações avançadas
- Relatórios de desempenho

## 🔒 Segurança

- Autenticação Firebase
- Criptografia de dados sensíveis
- CORS configurado adequadamente
- Validação de entrada em todas as APIs

## 📈 Performance

- Build otimizado com Vite
- Lazy loading de componentes
- Cache inteligente
- CDN para assets estáticos

## 🤝 Contribuição

Este é um projeto proprietário desenvolvido especificamente para concursos da área da saúde. Para sugestões ou melhorias, entre em contato com a equipe de desenvolvimento.

## 📄 Licença

Todos os direitos reservados. Este software é proprietário e não pode ser redistribuído sem autorização expressa.

## 🛠️ Tecnologias Backend

- Python 3.11
- Flask
- Firebase Admin SDK
- OpenAI API
- Perplexity API

## 📞 Suporte

Para suporte técnico ou dúvidas sobre o sistema, utilize o FAQ com IA integrado na plataforma ou entre em contato através dos canais oficiais.

---

**Desenvolvido com ❤️ para revolucionar os estudos para concursos públicos da área da saúde.**
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
>>>>>>> 8f9c51bd11df4ae06def811e74a9ab476dda57f2
