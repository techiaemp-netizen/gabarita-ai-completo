# Gabarita.AI - Arquitetura do Sistema

**Autor:** Manus AI  
**Data:** 23 de julho de 2025  
**Versão:** 1.0  

## Visão Geral do Projeto

O Gabarita.AI é um sistema de simulado inteligente desenvolvido especificamente para o Concurso Nacional Unificado (CNU 2025), baseado na metodologia e padrões da banca FGV. O sistema utiliza inteligência artificial para gerar questões personalizadas, fornecer feedback detalhado e acompanhar o progresso dos candidatos de forma gamificada.

### Objetivos Principais

O sistema foi projetado para atender três necessidades fundamentais dos candidatos ao CNU 2025:

1. **Preparação Personalizada**: Geração de questões específicas para cada cargo e bloco, baseadas no edital oficial
2. **Feedback Inteligente**: Explicações detalhadas dos erros com fontes confiáveis para estudo complementar
3. **Acompanhamento de Progresso**: Sistema gamificado que motiva o estudo contínuo e identifica pontos de melhoria

### Arquitetura Tecnológica

A arquitetura do Gabarita.AI segue o padrão **Firebase + Bot + Interface Web**, proporcionando escalabilidade, confiabilidade e facilidade de manutenção. Os componentes principais incluem:

- **Frontend**: Interface web responsiva desenvolvida em React
- **Backend**: APIs REST utilizando Firebase Functions
- **Banco de Dados**: Firebase Firestore para armazenamento NoSQL
- **Inteligência Artificial**: Integração com ChatGPT para geração de questões e Perplexity para pesquisa de conteúdo
- **Autenticação**: Firebase Authentication para gerenciamento de usuários

## Módulos do Sistema

### Módulo 1: Cadastro e Perfil do Usuário

Este módulo fundamental estabelece a base para toda a personalização do sistema. O cadastro coleta informações essenciais que direcionam a geração de conteúdo específico para cada usuário.

**Campos do Perfil:**
- Nome completo
- E-mail (usado para autenticação)
- Cargo pretendido no CNU 2025
- Bloco de conhecimento escolhido
- Nível de escolaridade
- Status atual no sistema
- Pontuação acumulada
- Vida (sistema de gamificação)
- Histórico de erros por tema

**Estrutura de Dados no Firebase:**
```json
{
  "usuarios": {
    "userId": {
      "nome": "string",
      "email": "string",
      "cargo": "string",
      "bloco": "string",
      "nivelEscolaridade": "string",
      "status": "ativo|inativo",
      "vida": "number (0-100)",
      "pontuacao": "number",
      "errosPorTema": {
        "tema1": "number",
        "tema2": "number"
      },
      "dataCriacao": "timestamp",
      "ultimoAcesso": "timestamp"
    }
  }
}
```

### Módulo 2: Geração de Questões com Prompt GPT

O coração do sistema reside na capacidade de gerar questões personalizadas que simulam fielmente o padrão da banca FGV. Este módulo combina prompts estáticos e dinâmicos para criar conteúdo relevante e desafiador.

**Prompt Estático (Base FGV):**
O prompt estático estabelece as diretrizes fundamentais que garantem a qualidade e o padrão das questões geradas:

```
Você é um elaborador de questões da banca FGV. Seu papel é criar uma única questão objetiva, com base no edital do cargo abaixo. Siga as instruções com rigor:

- Formato da questão: pode ser de múltipla escolha (com 5 alternativas, apenas uma correta), verdadeiro ou falso, completar lacuna, ou ordenação lógica.
- A questão deve ser inédita, clara, com linguagem técnica adequada.
- A alternativa correta deve ser coerente e as erradas plausíveis, mas incorretas.
- No final, inclua o gabarito e uma explicação técnica da resposta.
- NÃO invente temas fora do edital. Utilize apenas o conteúdo que está listado no edital fornecido.
```

**Prompt Dinâmico (Personalização):**
O sistema injeta informações específicas do usuário para personalizar cada questão:

```
Cargo do aluno: [cargo_usuario]
Conteúdo do edital a ser cobrado: [conteudo_edital_especifico]
Tipo de questão desejada: [tipo_questao]
```

**Fluxo de Geração:**
1. Sistema consulta o perfil do usuário no Firebase
2. Seleciona conteúdo do edital baseado no cargo e bloco
3. Combina prompt estático com dados dinâmicos
4. Envia requisição para ChatGPT
5. Processa resposta e estrutura dados
6. Armazena questão vinculada ao usuário

### Módulo 3: Resposta e Correção

Este módulo processa as respostas dos usuários e atualiza métricas de desempenho em tempo real. O sistema registra não apenas acertos e erros, mas também padrões de comportamento que informam futuras recomendações de estudo.

**Métricas Coletadas:**
- Tempo de resposta por questão
- Acertos e erros por tema
- Sequências de acertos consecutivos
- Padrões de erro recorrentes
- Evolução temporal do desempenho

**Algoritmo de Atualização da Vida:**
```javascript
function atualizarVida(acertou, vidaAtual, acertosConsecutivos) {
  if (acertou) {
    const bonus = Math.min(acertosConsecutivos * 2, 10);
    return Math.min(vidaAtual + 5 + bonus, 100);
  } else {
    const penalidade = Math.max(10 - acertosConsecutivos, 5);
    return Math.max(vidaAtual - penalidade, 0);
  }
}
```

### Módulo 4: Comentário com Feedback de Estudo (Perplexity)

Quando um usuário comete um erro, o sistema automaticamente gera feedback educativo utilizando o Perplexity para buscar explicações detalhadas e fontes confiáveis de estudo.

**Prompt para Perplexity:**
```
Explique por que a alternativa [alternativa_escolhida] da seguinte questão está errada. Forneça fontes confiáveis com links clicáveis para estudo aprofundado. 

Questão: [texto_questao]
Tema da questão: [tema]
Alternativa correta: [alternativa_correta]
Alternativa escolhida pelo aluno: [alternativa_escolhida]
```

**Estrutura da Resposta:**
- Explicação clara do erro
- Conceito correto explicado
- Links para fontes oficiais
- Sugestões de material complementar
- Temas relacionados para aprofundamento

### Módulo 5: Ranking Segmentado

O sistema de ranking cria competição saudável entre candidatos do mesmo cargo e bloco, proporcionando motivação adicional e referência de desempenho.

**Critérios de Classificação:**
1. Percentual de acertos geral
2. Média de tempo de resposta
3. Consistência (menor variação de desempenho)
4. Atividade recente (peso maior para atividade dos últimos 7 dias)

**Segmentação:**
- Por cargo específico
- Por bloco de conhecimento
- Por região (opcional)
- Por tempo de estudo

### Módulo 6: Nota de Corte Simulada

Utilizando dados históricos e estatísticas de concursos anteriores, o sistema calcula estimativas de nota de corte para cada cargo, ajudando candidatos a estabelecer metas realistas.

**Fatores Considerados:**
- Número de vagas por cargo
- Histórico de notas de corte em concursos similares
- Desempenho médio dos usuários ativos
- Tendências de dificuldade das questões
- Sazonalidade e proximidade da prova

### Módulo 7: Barra de Progresso (Vida do Aluno)

O sistema de gamificação utiliza o conceito de "vida" para manter os usuários engajados e motivados. A vida funciona como um indicador visual do progresso e consistência nos estudos.

**Mecânica da Vida:**
- Valor inicial: 80%
- Máximo: 100%
- Mínimo: 0%
- Ganho por acerto: 5% + bônus por sequência
- Perda por erro: 5-15% (dependendo da sequência de acertos)
- Regeneração por tempo: 1% por dia de estudo consecutivo

### Módulo 8: Histórico e Revisão de Questões

Permite aos usuários revisar todas as questões respondidas, com acesso completo aos gabaritos, explicações e materiais de estudo sugeridos.

**Funcionalidades:**
- Filtros por tema, data, resultado
- Busca por palavra-chave
- Exportação de relatórios
- Marcação de questões para revisão
- Estatísticas detalhadas por período




### Módulo 9: Favoritar e Revisar Depois

Este módulo permite que os usuários marquem questões importantes para revisão posterior, criando um sistema personalizado de estudo baseado em suas necessidades específicas.

**Funcionalidades Principais:**
- Marcação de questões como favoritas durante ou após a resolução
- Lista dedicada de questões favoritas com filtros avançados
- Agendamento de revisões com notificações
- Categorização personalizada (difícil, importante, revisar antes da prova)
- Exportação de listas de favoritos para estudo offline

**Estrutura de Dados:**
```json
{
  "favoritos": {
    "userId": {
      "questaoId": {
        "dataFavoritada": "timestamp",
        "categoria": "string",
        "observacoes": "string",
        "proximaRevisao": "timestamp"
      }
    }
  }
}
```

### Módulo 10: Simulado Cronometrado

O simulado cronometrado replica as condições reais da prova, permitindo que os candidatos pratiquem sob pressão temporal e desenvolvam estratégias de gerenciamento de tempo.

**Configurações do Simulado:**
- Número de questões: 10, 20 ou 30 questões
- Tempo limite: baseado no tempo real da prova (3 minutos por questão)
- Temas: todos os temas do cargo ou seleção específica
- Dificuldade: adaptativa baseada no histórico do usuário

**Métricas Coletadas:**
- Tempo total utilizado
- Tempo médio por questão
- Questões respondidas vs. não respondidas
- Acertos por bloco temático
- Comparação com simulados anteriores
- Posição no ranking de simulados

**Relatório Pós-Simulado:**
- Nota final calculada
- Percentual de acertos por tema
- Análise temporal (questões mais demoradas)
- Recomendações de estudo baseadas no desempenho
- Comparação com outros usuários do mesmo cargo

### Módulo 11: Painel do Usuário (Dashboard)

O dashboard centraliza todas as informações relevantes do usuário em uma interface intuitiva e informativa, proporcionando uma visão completa do progresso nos estudos.

**Componentes do Dashboard:**

**Seção de Status Atual:**
- Vida atual com indicador visual
- Streak de dias estudando consecutivamente
- Questões respondidas hoje/semana/mês
- Posição atual no ranking

**Seção de Desempenho:**
- Gráfico de evolução de acertos ao longo do tempo
- Distribuição de acertos por tema (gráfico de pizza)
- Comparação com a média dos usuários do mesmo cargo
- Tempo médio de resposta por questão

**Seção de Metas e Objetivos:**
- Progresso em direção à nota de corte estimada
- Metas diárias/semanais de questões
- Temas que precisam de mais atenção
- Próximos marcos de gamificação

**Seção de Atividade Recente:**
- Últimas questões respondidas
- Simulados realizados recentemente
- Conquistas desbloqueadas
- Notificações pendentes

### Módulo 12: Área de Perfil com Edição

Permite que os usuários mantenham seus dados atualizados e alterem configurações que impactam a personalização do conteúdo gerado.

**Dados Editáveis:**
- Informações pessoais (nome, e-mail)
- Cargo e bloco pretendido
- Preferências de estudo (horários, frequência de notificações)
- Configurações de privacidade
- Metas pessoais de estudo

**Impacto das Alterações:**
- Mudança de cargo: recalcula todo o histórico de desempenho
- Alteração de bloco: ajusta geração de questões futuras
- Modificação de metas: atualiza dashboard e notificações

### Módulo 13: Sugestões de Estudo

O sistema analisa o padrão de erros e acertos do usuário para gerar recomendações personalizadas de estudo, otimizando o tempo de preparação.

**Algoritmo de Recomendação:**
1. Identifica temas com maior índice de erro
2. Considera a frequência de aparição de cada tema nas provas
3. Analisa o tempo desde a última revisão de cada tópico
4. Prioriza conteúdos com base na proximidade da prova
5. Sugere sequência otimizada de estudo

**Tipos de Sugestões:**
- **Revisão Urgente**: Temas com muitos erros recentes
- **Reforço Necessário**: Conteúdos com desempenho abaixo da média
- **Manutenção**: Temas dominados que precisam de revisão periódica
- **Exploração**: Novos tópicos ainda não estudados

**Formato das Recomendações:**
```
🔴 REVISÃO URGENTE
Política Nacional de Saúde - 6 erros nos últimos 7 dias
Sugestão: Dedique 2 horas hoje para revisar este tema
Material recomendado: [links para fontes]

🟡 REFORÇO NECESSÁRIO  
Estratégia Saúde da Família - 60% de acertos (meta: 80%)
Sugestão: Resolva 10 questões específicas deste tema
```

### Módulo 14: Sistema de Notificações

Mantém os usuários engajados através de notificações inteligentes e personalizadas, enviadas via web push ou integração com Telegram.

**Tipos de Notificações:**

**Notificações de Estudo:**
- Lembrete diário para resolver questões
- Sugestão de temas baseada no histórico
- Alerta de meta diária não cumprida
- Parabenização por sequências de acertos

**Notificações de Progresso:**
- Subida de posição no ranking
- Conquista de novos marcos de gamificação
- Melhoria significativa em temas específicos
- Atingimento de metas estabelecidas

**Notificações de Conteúdo:**
- Nova questão do dia disponível
- Atualização de nota de corte estimada
- Novos materiais de estudo adicionados
- Dicas baseadas em erros comuns

**Configurações de Personalização:**
- Frequência de notificações (diária, semanal)
- Horários preferenciais para recebimento
- Tipos de notificação ativados/desativados
- Canal preferencial (web, Telegram, e-mail)

### Módulo 15: FAQ com IA

Sistema de ajuda inteligente que utiliza processamento de linguagem natural para responder dúvidas sobre o sistema, edital e estratégias de estudo.

**Base de Conhecimento:**
- Instruções completas de uso do sistema
- Informações detalhadas sobre o edital do CNU 2025
- Estratégias de estudo comprovadas
- Dúvidas frequentes sobre a prova
- Troubleshooting técnico

**Funcionalidades:**
- Busca semântica por palavras-chave
- Respostas contextualizadas baseadas no perfil do usuário
- Sugestões de perguntas relacionadas
- Feedback sobre a utilidade das respostas
- Escalação para suporte humano quando necessário

### Módulo 16: Últimas Notícias (PECLECST)

Mantém os usuários informados sobre atualizações relevantes do CNU 2025 através de busca automatizada de notícias utilizando o Perplexity.

**Automação de Busca:**
- Execução diária às 08h00
- Prompt otimizado: "Quais as últimas novidades sobre o Concurso Nacional Unificado (CNU 2025)?"
- Filtragem de conteúdo relevante
- Verificação de fontes confiáveis

**Apresentação das Notícias:**
- Resumo executivo das principais atualizações
- Links diretos para fontes originais
- Categorização por tipo (edital, cronograma, resultados)
- Notificação para usuários sobre atualizações importantes
- Arquivo histórico de todas as notícias coletadas

## Integrações Técnicas

### Firebase Firestore

O Firestore serve como banco de dados principal, oferecendo escalabilidade automática e sincronização em tempo real.

**Coleções Principais:**
```
/usuarios/{userId}
/questoes/{questaoId}
/respostas/{respostaId}
/simulados/{simuladoId}
/rankings/{cargoId}
/noticias/{noticiaId}
/favoritos/{userId}/questoes/{questaoId}
```

**Regras de Segurança:**
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /usuarios/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    match /questoes/{questaoId} {
      allow read: if request.auth != null;
      allow write: if false; // Apenas via Cloud Functions
    }
  }
}
```

### ChatGPT Integration

**Configuração da API:**
- Modelo: GPT-4 para máxima qualidade
- Temperatura: 0.7 para criatividade controlada
- Max tokens: 1500 para questões completas
- Sistema de retry para falhas temporárias

**Prompt Engineering:**
- Templates pré-definidos por tipo de questão
- Validação de resposta via regex
- Sistema de fallback para prompts alternativos
- Cache de respostas para otimização

### Perplexity Integration

**Configuração:**
- Modelo: Perplexity Pro para acesso a fontes atualizadas
- Timeout: 30 segundos por consulta
- Rate limiting: 100 consultas por hora
- Processamento de markdown para formatação

**Processamento de Respostas:**
- Extração automática de links
- Validação de fontes confiáveis
- Formatação para exibição web
- Cache de explicações por tema

## Arquitetura de Deploy

### Frontend (React)

**Estrutura de Pastas:**
```
src/
├── components/
│   ├── common/
│   ├── questoes/
│   ├── dashboard/
│   └── simulado/
├── pages/
├── services/
├── hooks/
├── utils/
└── styles/
```

**Tecnologias:**
- React 18 com Hooks
- Material-UI para componentes
- React Router para navegação
- Axios para requisições HTTP
- Chart.js para gráficos

### Backend (Firebase Functions)

**Estrutura de Functions:**
```
functions/
├── src/
│   ├── auth/
│   ├── questoes/
│   ├── usuarios/
│   ├── simulados/
│   └── integracoes/
├── package.json
└── firebase.json
```

**APIs Principais:**
- `/api/questoes/gerar` - Geração de nova questão
- `/api/questoes/responder` - Processamento de resposta
- `/api/simulados/criar` - Criação de simulado
- `/api/ranking/obter` - Consulta de ranking
- `/api/noticias/buscar` - Busca de notícias

### Monitoramento e Analytics

**Métricas de Sistema:**
- Tempo de resposta das APIs
- Taxa de erro por endpoint
- Uso de recursos Firebase
- Custos de APIs externas

**Métricas de Usuário:**
- Tempo de sessão médio
- Questões respondidas por sessão
- Taxa de retenção diária/semanal
- Conversão de cadastro para uso ativo

## Considerações de Segurança

### Proteção de Dados

**LGPD Compliance:**
- Consentimento explícito para coleta de dados
- Direito ao esquecimento implementado
- Criptografia de dados sensíveis
- Logs de auditoria para acesso aos dados

**Segurança de API:**
- Rate limiting por usuário
- Validação rigorosa de inputs
- Sanitização de dados
- Monitoramento de tentativas de abuso

### Prevenção de Fraudes

**Anti-Cheating:**
- Detecção de padrões suspeitos de resposta
- Limite de tempo mínimo por questão
- Randomização de alternativas
- Análise de comportamento anômalo

## Roadmap de Desenvolvimento

### Fase 1: MVP Core (Semana 1)
- Módulos 1-4: Cadastro, questões, respostas, feedback
- Interface básica funcional
- Integração ChatGPT e Perplexity

### Fase 2: Gamificação (Semana 2)
- Módulos 5-8: Ranking, nota de corte, vida, histórico
- Dashboard básico
- Sistema de notificações

### Fase 3: Funcionalidades Avançadas (Semana 3)
- Módulos 9-12: Favoritos, simulados, dashboard completo, perfil
- Interface refinada
- Otimizações de performance

### Fase 4: Inteligência e Automação (Semana 4)
- Módulos 13-16: Sugestões, notificações, FAQ, notícias
- Testes completos
- Deploy de produção

### Fase 5: Marketplace (Futuro)
- Módulo 17: Sistema de monetização
- Integração com pagamentos
- Painel para professores

## Conclusão

O Gabarita.AI representa uma solução completa e inovadora para preparação ao CNU 2025, combinando inteligência artificial, gamificação e personalização para maximizar o desempenho dos candidatos. A arquitetura modular permite desenvolvimento incremental e facilita futuras expansões, enquanto as integrações com ChatGPT e Perplexity garantem conteúdo de alta qualidade e sempre atualizado.

O sistema foi projetado para escalar automaticamente conforme o crescimento da base de usuários, mantendo performance e confiabilidade através das melhores práticas de desenvolvimento e infraestrutura cloud-native.

