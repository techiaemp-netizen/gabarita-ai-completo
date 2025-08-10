# Configuração de Variáveis de Ambiente no Render

## Problema Identificado

O servidor `https://gabarita-ai-backend.onrender.com/` está retornando erro 404 porque as variáveis de ambiente necessárias não estão configuradas no Render, causando falha na inicialização do servidor.

## Variáveis Obrigatórias

Para o funcionamento correto do backend, as seguintes variáveis devem ser configuradas no painel do Render:

### 1. OpenAI API Key (OBRIGATÓRIA)
```
OPENAI_API_KEY=sua_chave_openai_aqui
```

### 2. Outras variáveis importantes
```
PERPLEXITY_API_KEY=sua_chave_perplexity_aqui
FLASK_ENV=production
FLASK_DEBUG=False
```

## Como Configurar no Render

1. Acesse o painel do Render (https://dashboard.render.com)
2. Vá para o serviço `gabarita-ai-backend`
3. Clique na aba "Environment"
4. Adicione cada variável de ambiente:
   - Clique em "Add Environment Variable"
   - Insira o nome da variável (ex: `OPENAI_API_KEY`)
   - Insira o valor da variável
   - Clique em "Save Changes"

## Redeploy Automático

Após adicionar as variáveis de ambiente, o Render fará automaticamente um novo deploy do serviço.

## Verificação

Após o deploy, teste os endpoints:
- Health check: `https://gabarita-ai-backend.onrender.com/health`
- Rota raiz: `https://gabarita-ai-backend.onrender.com/`

## Status Atual

- ✅ Código da aplicação está correto
- ✅ Rota raiz (/) foi adicionada ao main.py
- ✅ Configuração render.yaml está correta
- ❌ Variáveis de ambiente não configuradas no Render
- ❌ Servidor falhando na inicialização

## Próximos Passos

1. Configurar OPENAI_API_KEY no painel do Render
2. Aguardar redeploy automático
3. Testar endpoints novamente