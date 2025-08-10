# Solução para Problemas de Autenticação Firebase

## Problemas Identificados

### 1. Erro `auth/popup-blocked`
**Causa**: O navegador está bloqueando popups, especialmente comum em:
- Navegadores móveis
- Navegadores integrados de aplicativos (Instagram, Facebook, etc.)
- Configurações de bloqueio de popup ativadas

### 2. Erro `auth/invalid-credential`
**Causa**: Credenciais inválidas fornecidas durante o login

## Soluções Implementadas

### 1. Fallback de Popup para Redirect

**Arquivo**: `src/services/authService.js`

```javascript
// Tentar signInWithPopup primeiro, se falhar usar signInWithRedirect
let result;
try {
  result = await signInWithPopup(auth, provider);
} catch (popupError) {
  console.log('Popup bloqueado, tentando redirect:', popupError.code);
  if (popupError.code === 'auth/popup-blocked' || popupError.code === 'auth/popup-closed-by-user') {
    // Usar redirect como fallback
    await signInWithRedirect(auth, provider);
    return { success: true, redirect: true };
  }
  throw popupError;
}
```

**Benefícios**:
- Funciona em todos os navegadores
- Compatível com navegadores móveis
- Fallback automático quando popup é bloqueado

### 2. Verificação de Resultado do Redirect

**Método adicionado**: `checkRedirectResult()`

```javascript
async checkRedirectResult() {
  try {
    const result = await getRedirectResult(auth);
    if (result) {
      const user = result.user;
      // Processar login bem-sucedido
      return { success: true, user: userData };
    }
    return null;
  } catch (error) {
    console.error('Erro ao verificar resultado do redirect:', error);
    return { success: false, error: this.getErrorMessage(error.code) };
  }
}
```

### 3. Inicialização Automática no App

**Arquivo**: `src/App.jsx`

```javascript
useEffect(() => {
  const verificarAuth = async () => {
    try {
      // Verificar resultado do redirect primeiro
      const redirectResult = await authService.checkRedirectResult();
      
      if (redirectResult && redirectResult.success) {
        console.log('✅ Login via redirect detectado');
        setUsuario(redirectResult.user);
      } else if (authService.currentUser) {
        setUsuario(authService.currentUser);
      }
    } catch (error) {
      console.error('Erro ao verificar autenticação:', error);
    } finally {
      setCarregando(false);
    }
  };

  setTimeout(verificarAuth, 1000);
}, []);
```

### 4. Mensagens de Erro Melhoradas

**Códigos de erro adicionados**:
- `auth/popup-blocked`: "Popup bloqueado pelo navegador. Tentando método alternativo..."
- `auth/popup-closed-by-user`: "Login cancelado pelo usuário"
- `auth/cancelled-popup-request`: "Solicitação de popup cancelada"
- `auth/invalid-credential`: "Credenciais inválidas. Verifique seu e-mail e senha"

## Configurações Necessárias no Firebase Console

### 1. Domínios Autorizados

No Firebase Console:
1. Vá para **Authentication** > **Settings** > **Authorized domains**
2. Adicione os domínios:
   - `localhost` (para desenvolvimento)
   - `127.0.0.1` (para desenvolvimento)
   - `gabarit-ai.firebaseapp.com` (domínio do projeto)
   - Seu domínio personalizado (se houver)

### 2. Configuração do Google OAuth

1. No Firebase Console, vá para **Authentication** > **Sign-in method**
2. Habilite **Google**
3. Configure o **Web SDK configuration**
4. Adicione domínios autorizados

### 3. Google Cloud Console

1. Vá para [Google Cloud Console](https://console.cloud.google.com/)
2. Selecione seu projeto Firebase
3. Vá para **APIs & Services** > **Credentials**
4. Edite a **Web client** OAuth 2.0
5. Adicione os domínios em **Authorized JavaScript origins**:
   - `http://localhost:5173`
   - `http://127.0.0.1:5173`
   - `https://gabarit-ai.firebaseapp.com`

## Fluxo de Autenticação

### Cenário 1: Popup Funciona
1. Usuário clica em "Continuar com Google"
2. `signInWithPopup` é executado
3. Popup abre com Google OAuth
4. Usuário faz login
5. Popup fecha e retorna resultado
6. Usuário é logado na aplicação

### Cenário 2: Popup Bloqueado
1. Usuário clica em "Continuar com Google"
2. `signInWithPopup` falha com `auth/popup-blocked`
3. Sistema automaticamente chama `signInWithRedirect`
4. Usuário é redirecionado para Google OAuth
5. Após login, usuário retorna à aplicação
6. `checkRedirectResult` detecta o login
7. Usuário é logado na aplicação

## Testes

### Para testar popup bloqueado:
1. Abra as configurações do navegador
2. Bloqueie popups para localhost
3. Tente fazer login com Google
4. Verifique se o redirect funciona

### Para testar credenciais inválidas:
1. Tente fazer login com email/senha incorretos
2. Verifique se a mensagem de erro é clara

## Benefícios da Solução

1. **Compatibilidade Universal**: Funciona em todos os navegadores e dispositivos
2. **Experiência do Usuário**: Fallback transparente sem interrupção
3. **Robustez**: Trata múltiplos cenários de erro
4. **Manutenibilidade**: Código organizado e bem documentado
5. **Performance**: Não adiciona overhead significativo

## Monitoramento

Para monitorar os problemas de autenticação:

```javascript
// Logs automáticos implementados
console.log('Popup bloqueado, tentando redirect:', popupError.code);
console.log('✅ Login via redirect detectado');
console.error('Erro ao verificar resultado do redirect:', error);
```

Estes logs ajudam a identificar padrões de uso e problemas recorrentes.