# Configuração do Render - Gabarita AI

## Como configurar as variáveis de ambiente no Render

### Opção 1: Usando o arquivo .env.render (RECOMENDADO)

1. **Abra o arquivo `.env.render`** que foi criado na raiz do projeto
2. **Substitua os valores de exemplo** pelas suas chaves reais:
   - `OPENAI_API_KEY`: Sua chave da OpenAI
   - `PERPLEXITY_API_KEY`: Sua chave da Perplexity
   - `MERCADO_PAGO_ACCESS_TOKEN`: Seu token do Mercado Pago
   - `MERCADO_PAGO_PUBLIC_KEY`: Sua chave pública do Mercado Pago
   - Credenciais do Firebase (todas as variáveis FIREBASE_*)

3. **No dashboard do Render**:
   - Vá para seu serviço backend
   - Clique em "Environment"
   - **IMPORTANTE**: Remova todas as variáveis existentes primeiro
   - Copie e cole as variáveis do arquivo `.env.render` uma por vez
   - Clique em "Save and Deploy"

### Opção 2: Configuração manual

Se preferir configurar manualmente, adicione estas variáveis essenciais primeiro:

```
SECRET_KEY=sua_chave_secreta_super_forte_aqui_123456789
PORT=10000
OPENAI_API_KEY=sk-sua_chave_openai_aqui
PERPLEXITY_API_KEY=pplx-sua_chave_perplexity_aqui
FIREBASE_PROJECT_ID=gabarita-ai
```

## Dicas importantes:

1. **Não cole tudo de uma vez** - O Render pode dar erro
2. **Remova duplicatas** - Especialmente a variável `PORT`
3. **Use "Save and Deploy"** após cada grupo de 5 variáveis
4. **Verifique os logs** após o deploy para confirmar que não há erros

## Solução de problemas:

- **Erro "There are some errors above"**: Limpe todas as variáveis e adicione uma por vez
- **Erro de PORT**: Certifique-se de ter apenas `PORT=10000`
- **Erro de API**: Verifique se as chaves estão corretas e sem espaços extras

## Ordem recomendada para adicionar as variáveis:

1. Primeiro grupo (essenciais):
   - SECRET_KEY
   - PORT
   - OPENAI_API_KEY
   - PERPLEXITY_API_KEY
   - FIREBASE_PROJECT_ID

2. Segundo grupo (Firebase):
   - FIREBASE_PRIVATE_KEY_ID
   - FIREBASE_PRIVATE_KEY
   - FIREBASE_CLIENT_EMAIL
   - FIREBASE_CLIENT_ID

3. Terceiro grupo (URLs e Mercado Pago):
   - FRONTEND_URL
   - BACKEND_URL
   - MERCADO_PAGO_ACCESS_TOKEN
   - MERCADO_PAGO_PUBLIC_KEY

Clique em "Save and Deploy" após cada grupo!