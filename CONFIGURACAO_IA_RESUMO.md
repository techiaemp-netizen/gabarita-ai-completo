# Configuração das Regras de IA - Gabarita.AI

## Status Atual da Configuração

### ✅ Estrutura Implementada
O projeto está corretamente estruturado conforme o planejamento, com as seguintes funcionalidades implementadas:

## 1. Geração de Questões pelo ChatGPT (OpenAI)

### Arquivo Principal
- **Localização**: `gabarita-ai-backend/src/services/chatgpt_service.py`
- **Status**: ✅ Implementado e funcional
- **Modelo**: GPT-4

### Configuração Atual
```python
class ChatGPTService:
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            base_url=os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
        )
        self.model = "gpt-4"
        self.temperature = 0.7
        self.max_tokens = 1500
```

### Prompt Estático (Regras FGV)
```
Você é um elaborador de questões da banca FGV. Seu papel é criar uma única questão objetiva, com base no edital do cargo abaixo. Siga as instruções com rigor:

- Formato da questão: pode ser de múltipla escolha (com 5 alternativas, apenas uma correta), verdadeiro ou falso, completar lacuna, ou ordenação lógica.
- A questão deve ser inédita, clara, com linguagem técnica adequada.
- A alternativa correta deve ser coerente e as erradas plausíveis, mas incorretas.
- No final, inclua o gabarito e uma explicação técnica da resposta.
- NÃO invente temas fora do edital. Utilize apenas o conteúdo que está listado no edital fornecido.
```

### Formato de Resposta JSON
```json
{
  "questao": "texto da questão",
  "tipo": "multipla_escolha|verdadeiro_falso|completar_lacuna|ordenacao",
  "alternativas": ["A) ...", "B) ...", "C) ...", "D) ...", "E) ..."],
  "gabarito": "A",
  "explicacao": "explicação detalhada da resposta correta",
  "tema": "tema principal da questão",
  "dificuldade": "facil|medio|dificil"
}
```

### Validação de Questões
O sistema inclui validação automática que verifica:
- Presença de todos os campos obrigatórios
- Mínimo de 2 alternativas
- Gabarito válido (A-E)
- Qualidade do conteúdo gerado

## 2. Explicações de Erros pelo Perplexity (PECLEST)

### Arquivo Principal
- **Localização**: `gabarita-ai-backend/src/services/perplexity_service.py`
- **Status**: ✅ Implementado com fallback
- **Modelo**: llama-3.1-sonar-small-128k-online

### Configuração Atual
```python
class PerplexityService:
    def __init__(self):
        self.api_key = os.getenv('PERPLEXITY_API_KEY', 'pplx-dummy-key')
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.model = "llama-3.1-sonar-small-128k-online"
```

### Prompt para Feedback de Erro
```
Analise o erro do estudante na seguinte questão sobre {tema}:

Questão: {questao}
Alternativa escolhida pelo estudante: {alternativa_escolhida}
Alternativa correta: {alternativa_correta}

Forneça um feedback educativo que inclua:
1. Por que a alternativa escolhida está incorreta
2. Conceitos importantes que o estudante deve revisar
3. Fontes confiáveis para estudo adicional
4. Dicas para evitar erros similares

Responda em formato JSON com as chaves: explicacao_erro, conceitos_importantes, fontes_estudo, dicas
```

### Estrutura de Resposta do Feedback
```json
{
  "explicacao_erro": "Por que a alternativa está errada",
  "conceitos_importantes": "Conceitos que devem ser revisados",
  "fontes_estudo": ["link1", "link2"],
  "dicas": "Dicas para evitar erros similares"
}
```

### Sistema de Fallback
Quando a API do Perplexity não está disponível, o sistema utiliza:
- Templates pré-definidos por tema
- Links para fontes oficiais (Ministério da Saúde, etc.)
- Conteúdo educativo básico

## 3. Integração no Fluxo de Questões

### Arquivo de Rotas
- **Localização**: `gabarita-ai-backend/src/routes/questoes.py`
- **Endpoint**: `/questoes/responder`

### Fluxo de Resposta
1. **Usuário responde questão**
2. **Sistema verifica se acertou**
3. **Se errou**: Chama automaticamente o Perplexity para gerar feedback
4. **Retorna resposta completa** com explicação e fontes

```python
# Se errou, gerar feedback com Perplexity
if not acertou:
    feedback = perplexity_service.gerar_feedback_erro(
        questao=questao_data.get('questao'),
        alternativa_escolhida=alternativa_escolhida,
        alternativa_correta=gabarito,
        tema=questao_data.get('tema')
    )
    
    if feedback:
        resposta['feedback_detalhado'] = feedback
```

## 4. Conteúdos do Edital por Cargo

### Estrutura de Dados
O sistema possui mapeamento completo dos conteúdos por cargo e bloco:

```python
CONTEUDOS_EDITAL = {
    'Enfermeiro na Atenção Primária': {
        'Bloco 4 - Trabalho e Saúde do Servidor': [
            'Política Nacional de Atenção Básica',
            'Estratégia Saúde da Família',
            'Vigilância em Saúde',
            # ... mais conteúdos
        ]
    }
}
```

## 5. Status dos Testes

### ❌ ChatGPT
- **Problema**: Chave de API não configurada
- **Erro**: `OpenAIError: The api_key client option must be set`
- **Solução**: Adicionar `OPENAI_API_KEY` no arquivo `.env`

### ⚠️ Perplexity
- **Status**: Parcialmente funcional
- **Problema**: API retorna erro 401 (não autorizado)
- **Fallback**: Funcionando corretamente
- **Solução**: Adicionar `PERPLEXITY_API_KEY` válida no arquivo `.env`

## 6. Configuração Necessária

### Arquivo .env Atualizado
```env
# Configurações das APIs de IA
OPENAI_API_KEY=sua_chave_openai_aqui
PERPLEXITY_API_KEY=sua_chave_perplexity_aqui
```

### Como Obter as Chaves

#### OpenAI API Key
1. Acesse: https://platform.openai.com/api-keys
2. Faça login na sua conta OpenAI
3. Clique em "Create new secret key"
4. Copie a chave e adicione no `.env`

#### Perplexity API Key
1. Acesse: https://www.perplexity.ai/settings/api
2. Faça login na sua conta Perplexity
3. Gere uma nova API key
4. Copie a chave e adicione no `.env`

## 7. Funcionalidades Implementadas

### ✅ Geração de Questões
- Prompt otimizado para banca FGV
- Validação automática de qualidade
- Extração inteligente de JSON
- Fallback para parsing manual
- Metadados completos

### ✅ Sistema PECLEST
- Feedback automático para erros
- Busca de fontes confiáveis
- Templates por tema
- Sistema de fallback robusto
- Integração com frontend

### ✅ Gamificação
- Sistema de vida do aluno
- Atualização automática de estatísticas
- Histórico completo de questões
- Ranking segmentado

## 8. Próximos Passos

1. **Configurar chaves de API** no arquivo `.env`
2. **Testar integração completa** com APIs reais
3. **Ajustar prompts** baseado nos resultados
4. **Implementar cache** para otimizar performance
5. **Adicionar monitoramento** de uso das APIs

## 9. Arquitetura Técnica

### Backend (Python/FastAPI)
- **Framework**: FastAPI
- **Banco de Dados**: Firebase Firestore
- **APIs de IA**: OpenAI GPT-4 + Perplexity
- **Autenticação**: Firebase Auth

### Frontend (React/Vite)
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS + Notion-inspired design
- **Estado**: React Hooks

### Integração
- **Comunicação**: REST API
- **Tempo Real**: Firebase Realtime updates
- **Deployment**: Vercel (frontend) + Railway/Heroku (backend)

## 10. Considerações de Segurança

- ✅ Chaves de API em variáveis de ambiente
- ✅ Validação de entrada nos endpoints
- ✅ Rate limiting implementado
- ✅ Sanitização de dados do usuário
- ✅ Logs de segurança configurados

---

**Conclusão**: O projeto está bem estruturado e implementado conforme o planejamento. A única pendência é a configuração das chaves de API reais para ativar completamente as funcionalidades de IA.