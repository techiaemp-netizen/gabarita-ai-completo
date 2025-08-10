# Solução para Erro da API OpenAI no Render

## 🚨 Problema Identificado

O deploy no Render está falhando com o erro:
```
OpenAIError: The api_key client option must be set either by passing api_key to the client or by setting the OPENAI_API_KEY environment variable
```

## 🔍 Causa do Problema

1. **Chave da API não configurada**: A variável `OPENAI_API_KEY` não está sendo definida corretamente no Render
2. **Formato incorreto**: Pode haver problemas com caracteres especiais ou formatação
3. **Variáveis duplicadas**: Conflitos entre variáveis de ambiente

## ✅ Solução Passo a Passo

### Passo 1: Limpar Variáveis Existentes
1. Acesse o dashboard do Render
2. Vá em **Environment Variables**
3. **DELETE TODAS** as variáveis existentes (clique no ícone de lixeira)
4. Confirme a exclusão

### Passo 2: Usar Arquivo Limpo
1. Use o arquivo `.env.render.clean` (sem comentários)
2. Copie TODO o conteúdo do arquivo
3. No Render, clique em **Add from .env**
4. Cole o conteúdo na caixa de texto

### Passo 3: Substituir Valores de Exemplo
**IMPORTANTE**: Substitua os valores de exemplo pelas suas chaves reais:

```env
# ❌ ERRADO (valor de exemplo)
OPENAI_API_KEY=sk-sua_chave_openai_aqui

# ✅ CORRETO (sua chave real)
OPENAI_API_KEY=sk-proj-abc123def456...
```

### Passo 4: Verificar Chaves Essenciais
Certifique-se de que estas variáveis estão corretas:
- `OPENAI_API_KEY` - Deve começar com `sk-`
- `PERPLEXITY_API_KEY` - Deve começar com `pplx-`
- `SECRET_KEY` - Use uma chave forte e única
- `PORT` - Deve ser `10000`

### Passo 5: Salvar e Deploy
1. Clique em **Add Variables**
2. Clique em **Save and Deploy**
3. Aguarde o deploy automático

## 🔧 Verificação Adicional

### Se o erro persistir:

1. **Verifique a chave da OpenAI**:
   - Acesse https://platform.openai.com/api-keys
   - Verifique se a chave está ativa
   - Gere uma nova chave se necessário

2. **Teste a chave localmente**:
   ```bash
   curl -H "Authorization: Bearer sua_chave_aqui" https://api.openai.com/v1/models
   ```

3. **Verifique logs do Render**:
   - Vá em **Logs** no dashboard
   - Procure por erros relacionados à OpenAI

## 📋 Checklist Final

- [ ] Todas as variáveis antigas foram removidas
- [ ] Arquivo `.env.render.clean` foi usado
- [ ] Chave `OPENAI_API_KEY` foi substituída pela real
- [ ] Chave `PERPLEXITY_API_KEY` foi substituída pela real
- [ ] `SECRET_KEY` foi definida com valor único
- [ ] Deploy foi executado com sucesso
- [ ] Logs não mostram erros da OpenAI

## 🆘 Se Ainda Não Funcionar

1. **Recrie o serviço no Render**:
   - Delete o serviço atual
   - Crie um novo serviço
   - Configure as variáveis desde o início

2. **Verifique a conta da OpenAI**:
   - Confirme que tem créditos disponíveis
   - Verifique se a API está habilitada
   - Teste com uma chave nova

3. **Contato para suporte**:
   - Verifique se todas as chaves estão corretas
   - Confirme que não há caracteres especiais problemáticos

---

**Lembre-se**: Nunca compartilhe suas chaves de API reais. Mantenha-as seguras e privadas!