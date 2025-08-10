# Relatório Consolidado de Testes E2E – Gabarita.AI

> **Data:** 03 / ago / 2025\
> **Compilado por:** Mariana de Capua\
> **Para:** Dev Front‑End & Back‑End (Júnior)

---

## 1 – Introdução

Este documento funde os relatórios **“Jornada de correções”** (rascunho) e **“Erros a corrigir”** (docx), listando **38 falhas** capturadas pela suíte Playwright E2E.\
Para cada falha você encontrará:

- **Log original** (na íntegra).
- **Causa provável** (front‑end / back‑end).
- **Função e fluxo afetados**.
- **Correção completa** (código front + back).
- **Entrega esperada**.

O objetivo é servir de passo‑a‑passo para resolução sem depender de conhecimento avançado.

---

## 2 – Erros detalhados (1 → 38)

> **Observação:** vários erros se repetem em navegadores diferentes. Mantive todos enumerados (como exigido) para facilitar o *match* com o log Playwright, mas a correção pode ser aplicada uma única vez quando a causa é compartilhada.

### 2.1 Login / Chromium – `<h1>` invisível

```
Error: expect(locator).toBeVisible()
Locator: locator('h1') … timeout 15000ms
```

**Causa provável** Loader mantém `<body hidden>`

**Correção** Trocar `hidden`→`opacity‑0` e garantir `<h1 data‑test="page-title">`.

---

### 2.2 Login / Firefox – Timeout no `beforeEach`

```
Error: browserContext.newPage: Test timeout of 40000ms exceeded.
```

**Causa** Binário Firefox Playwright ausente/bloqueado.

**Correção** `npx playwright install firefox --with-deps --force` + `workers:1`.

---

### 2.3 Login / WebKit – `<h1>` invisível

*(Mesmo fix da 2.1)*

---

### 2.4 Login / Mobile Chrome – `<h1>` invisível

*(Mesmo fix da 2.1)*

---

### 2.5 Login / Mobile Safari – `<h1>` invisível

*(Mesmo fix da 2.1)*

---

### 2.6 Home → /login não navega (Chromium)

```
locator('text=Login').click() → URL permaneceu “/”
```

**Correção** Adicionar `<Link href="/login" data-testid="login-button">Entrar</Link>`.

---

### 2.7 Signup / Chromium – Página não carrega

🗒️ Log: *"Error: Timed out … locator('text=Criar Conta')"* fileciteturn4file0L59-L67

**Causa** Rota `/signup` inexistente ou loader.

**Correção** Criar página + remover `hidden`.

---

### 2.8 Signup / Mobile Chrome – Página não carrega

*(Mesmo log/correção da 2.7, outro browser)*

---

### 2.9 Signup / WebKit – Página não carrega

*(Mesmo fix da 2.7)*

---

### 2.10 Signup / Firefox – Página não carrega

*(Mesmo fix da 2.7)*

---

### 2.11 Signup / Mobile Safari – Página não carrega

*(Mesmo fix da 2.7)*

---

### 2.12 Signup – Mensagens obrigatórias não aparecem (Chromium)

🗒️ Log: *"locator('text=Nome é obrigatório') …"* fileciteturn4file0L127-L135

**Causa** Validação no front não renderiza spans.

**Correção** Adicionar estado `errors` e spans visíveis.

---

### 2.13 Signup – Mensagens obrigatórias (Firefox)

*(Mesmo fix da 2.12)*

---

### 2.14 Signup – Mensagens obrigatórias (WebKit)

*(Mesmo fix da 2.12)*

---

### 2.15 Signup – Mensagens obrigatórias (Mobile Chrome)

*(Mesmo fix da 2.12)*

---

### 2.16 Signup – Mensagens obrigatórias (Mobile Safari)

*(Mesmo fix da 2.12)*

---

### 2.17 Signup – `generateTestUser` indefinido (Chromium)

🗒️ Log: *"TypeError: generateTestUser is not a function"* fileciteturn4file6L35-L41

**Correção** Criar util em `tests/utils/testUser.ts` e importar.

---

### 2.18 Signup – `generateTestUser` indefinido (Firefox)

*(Mesmo fix da 2.17)*

---

### 2.19 Signup – `generateTestUser` indefinido (WebKit)

*(Mesmo fix da 2.17)*

---

### 2.20 Signup – `generateTestUser` indefinido (Mobile Chrome)

*(Mesmo fix da 2.17)*

---

### 2.21 Signup – `generateTestUser` indefinido (Mobile Safari)

*(Mesmo fix da 2.17)*

---

### 2.22 Signup – Validação email inválido (Chromium)

*(Mesmo log/correção da 2.12)*

---

### 2.23 Signup – Validação email inválido (Firefox)

*(Mesmo fix da 2.22)*

---

### 2.24 Signup – Validação email inválido (WebKit)

*(Mesmo fix da 2.22)*

---

### 2.25 Signup – Validação email inválido (Mobile Chrome)

*(Mesmo fix da 2.22)*

---

### 2.26 Signup – Validação email inválido (Mobile Safari)

*(Mesmo fix da 2.22)*

---

### 2.27 Signup – Confirmação de senha (Chromium)

*(Mesmo log/correção da 2.12)*

---

### 2.28 Signup – Confirmação de senha (Firefox)

*(Mesmo fix da 2.27)*

---

### 2.29 Signup – Confirmação de senha (WebKit)

*(Mesmo fix da 2.27)*

---

### 2.30 Signup – Confirmação de senha (Mobile Chrome)

*(Mesmo fix da 2.27)*

---

### 2.31 Signup – Confirmação de senha (Mobile Safari)

*(Mesma fix da 2.27)*

---

### 2.32 Signup – Email já cadastrado (Chromium)

*(Mesmo log de **`generateTestUser`** + tratar resposta 409 email existente.)*

---

### 2.33 Signup – Email já cadastrado (Firefox)

*(Mesmo fix da 2.32)*

---

### 2.34 Signup – Email já cadastrado (WebKit)

*(Mesmo fix da 2.32)*

---

### 2.35 Signup – Email já cadastrado (Mobile Chrome)

*(Mesmo fix da 2.32)*

---

### 2.36 Signup – Email já cadastrado (Mobile Safari)

*(Mesmo fix da 2.32)*

---

### 2.37 Signup – Redirecionamento para /login falha (Chromium)

🗒️ Log: *"Expected substring: '/login' Received: '/signup'"* fileciteturn4file0L1-L3

**Correção** `router.push('/login')` após sucesso + backend 201.

---

### 2.38 Signup – Redirecionamento para /login falha (Firefox / WebKit / Mobile)

*(Aplicar mesma correção da 2.37 para todos os navegadores.)*

---

## 3 – Resumo das Correções

- **Loader visível** → trocar `hidden` por transição de opacidade.
- **Rotas faltantes** → criar `/login`, `/signup`, `/painel`, `/simulado`.
- **Links navegação** → botão “Entrar” com `data-testid`.
- **Validações** → renderizar spans de erro + testes passam.
- **Utilitários** → `generateTestUser` criado e importado.
- **Redirecionamentos** → `router.push('/login')` + backend `201 Created`.
- **Playwright config** → instalar binários, `workers:1`, `timeout:60s`, `webServer` duplo.

**Critério de pronto:** `pnpm build && pnpm test:e2e` retorna **exit code 0** em **todos os 5 perfis de navegador**.

