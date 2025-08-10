## Relatório de Validação - Gabarit-ai

### 1. Validação Frontend-Backend

#### 1.1. Autenticação e Cadastro

**Análise:**

O frontend, especificamente nos arquivos `src/pages/Login.jsx` e `src/pages/Cadastro.jsx`, utiliza `localStorage` e `setTimeout` para simular as operações de login e cadastro. As funções `handleSubmit` e `handleGoogleLogin` em `Login.jsx`, e `handleSubmit` em `Cadastro.jsx`, não fazem chamadas diretas ao backend.

Por outro lado, o backend possui rotas bem definidas para autenticação e cadastro em `src/main.py` (rotas `/api/auth/login`, `/api/questoes/gerar`, `/api/questoes/<questao_id>/responder`, `/api/perplexity/explicacao`) e `src/routes/auth.py` (rotas `/auth/login`, `/auth/cadastro`, `/auth/verificar-token`, `/auth/google-auth`, `/auth/complete-profile`, `/auth/logout`).

O arquivo `src/services/authService.js` no frontend contém a lógica para interagir com o Firebase Auth e Firestore, incluindo métodos como `login`, `loginWithGoogle`, `register`, `logout`, `resetPassword`, `saveUserData`, `getUserData` e `updateUserData`. No entanto, esses métodos *não estão sendo chamados* pelos componentes `Login.jsx` e `Cadastro.jsx` no fluxo atual do código.

**Apontamento:**

Existe uma desconexão entre o frontend e o backend no que diz respeito à autenticação e cadastro. O frontend está operando em um modo de simulação, enquanto o backend está pronto para lidar com autenticação real (via Firebase ou simulação interna do Flask). Para que o sistema funcione como esperado, as chamadas no `Login.jsx` e `Cadastro.jsx` precisam ser atualizadas para utilizar o `authService.js` e, consequentemente, as rotas do backend.

**Recomendação:**

1.  **Modificar `Login.jsx`:** Substituir as chamadas `setTimeout` e `localStorage` nas funções `handleSubmit` (para login) e `handleGoogleLogin` para utilizar `authService.login` e `authService.loginWithGoogle`, respectivamente.
2.  **Modificar `Cadastro.jsx`:** Substituir as chamadas `localStorage` na função `handleSubmit` para utilizar `authService.register`.
3.  **Configuração do Firebase:** Garantir que as credenciais do Firebase estejam corretamente configuradas no frontend (`src/config/firebase.js`) e no backend (`src/config/firebase_config.py`) para que a autenticação e o armazenamento de dados funcionem conforme o esperado. O backend já possui lógica para lidar com Firebase ou fallback para simulação, mas o frontend precisa ser configurado para usar o Firebase de fato.

#### 1.2. Geração e Resposta de Questões

**Análise:**

O backend possui as seguintes rotas relacionadas a questões:
*   `POST /api/questoes/gerar` (em `main.py`)
*   `POST /api/questoes/<questao_id>/responder` (em `main.py`)

No frontend, o arquivo `src/services/questoesService.js` provavelmente contém a lógica para interagir com essas rotas. Será necessário analisar este arquivo e os componentes que o utilizam (provavelmente `Painel.jsx` ou outros relacionados à exibição de questões) para verificar se as chamadas estão corretas.

**Apontamento:**

(A ser preenchido após a análise do `questoesService.js` e componentes relacionados)

**Recomendação:**

(A ser preenchido após a análise do `questoesService.js` e componentes relacionados)

#### 1.3. Explicação de Questões (Perplexity/ChatGPT)

**Análise:**

O backend possui a rota:
*   `POST /api/perplexity/explicacao` (em `main.py`)

No frontend, será necessário analisar o `src/services/questoesService.js` ou um serviço similar para verificar como essa rota é consumida.

**Apontamento:**

(A ser preenchido após a análise do `questoesService.js` e componentes relacionados)

**Recomendação:**

(A ser preenchido após a análise do `questoesService.js` e componentes relacionados)

### 2. Avaliação das Fórmulas de Gamificação

**Análise:**

As fórmulas de gamificação parecem ser calculadas e armazenadas no `localStorage` no frontend (`Cadastro.jsx` inicializa `gabarita_stats` com `questoesRespondidas`, `acertos`, `sequenciaAtual`, `xp`, `nivel`). O `authService.js` também lida com `pontuacao`, `nivel` e `xp` ao salvar/atualizar dados do usuário no Firestore.

Será necessário identificar onde esses valores são atualizados no frontend (provavelmente em componentes relacionados à resposta de questões) e verificar a lógica de cálculo.

**Apontamento:**

(A ser preenchido após a análise dos componentes que atualizam as estatísticas de gamificação)

**Recomendação:**

(A ser preenchido após a análise dos componentes que atualizam as estatísticas de gamificação)




#### 1.2. Geração e Resposta de Questões

**Análise:**

O frontend, através do `src/services/questoesService.js`, tenta se comunicar com as seguintes rotas do backend:
*   `POST /api/questoes/gerar`: Utilizado pelo método `gerarQuestao` para obter uma nova questão. Se a chamada à API falhar, ele retorna uma questão de fallback (`getQuestaoFallback`).
*   `POST /api/questoes/responder`: Utilizado pelo método `responderQuestao` para registrar a resposta do usuário. Se a chamada à API falhar, ele tenta salvar a resposta diretamente no Firestore (se configurado) ou simula a resposta (`simularResposta`).
*   `GET /api/questoes/estatisticas/<usuarioId>`: Utilizado pelo método `buscarEstatisticas` para obter as estatísticas do usuário. Se a chamada à API falhar, ele retorna estatísticas simuladas (`getEstatisticasSimuladas`).

**Apontamento:**

As chamadas para as rotas de geração, resposta e estatísticas de questões estão presentes no `questoesService.js`. No entanto, a dependência de `import.meta.env.VITE_API_BASE_URL` para a URL base da API e a presença de lógica de fallback indicam que o frontend pode estar operando em um modo de desenvolvimento/simulação se a variável de ambiente não estiver configurada ou se o backend não estiver acessível. É crucial garantir que o `VITE_API_BASE_URL` esteja apontando para o endereço correto do backend.

**Recomendação:**

1.  **Configuração da Variável de Ambiente:** Assegurar que a variável de ambiente `VITE_API_BASE_URL` no ambiente de execução do frontend esteja configurada para a URL correta do backend (ex: `http://localhost:5000` para desenvolvimento local, ou a URL de produção).
2.  **Verificação de Chamadas:** Confirmar nos componentes que utilizam `questoesService` (provavelmente `Painel.jsx` e `Desempenho.jsx`) que os métodos `gerarQuestao`, `responderQuestao` e `buscarEstatisticas` estão sendo invocados corretamente e que o fluxo de dados entre frontend e backend está funcionando conforme o esperado.

#### 1.3. Explicação de Questões (Perplexity/ChatGPT)

**Análise:**

O backend possui a rota:
*   `POST /api/perplexity/explicacao` (em `main.py`)

No frontend, o `src/services/questoesService.js` não contém uma chamada explícita para `/api/perplexity/explicacao`. No entanto, o backend em `main.py` utiliza `chatgpt_service.gerar_explicacao` para gerar a explicação, o que sugere que a lógica de explicação é tratada internamente no backend, possivelmente com base em um prompt construído a partir dos dados da questão.

**Apontamento:**

Não há uma chamada direta do frontend para a rota `/api/perplexity/explicacao` no `questoesService.js`. A explicação é retornada como parte da resposta da API de `responderQuestao` ou é gerada internamente no backend quando a rota `/api/perplexity/explicacao` é chamada (o que não parece ser o caso a partir do frontend).

**Recomendação:**

1.  **Clarificar Fluxo de Explicação:** Se a intenção é que o frontend solicite explicitamente uma explicação via `/api/perplexity/explicacao`, então um método correspondente precisa ser adicionado ao `questoesService.js` e invocado pelos componentes do frontend. Caso contrário, se a explicação já vem na resposta de `responderQuestao`, o fluxo atual pode ser suficiente, mas a rota `/api/perplexity/explicacao` no backend estaria sem uso direto pelo frontend.





#### 1.4. Análise do `Painel.jsx`

**Análise:**

O componente `Painel.jsx` é o centro da interação do usuário com as questões. Ele contém a lógica para:

*   **Carregamento de Dados do Usuário e Estatísticas:** No `useEffect`, ele tenta carregar `userData` e `gabarita_stats` do `localStorage`. Se `userData` não for encontrado, ele cria dados padrão.
*   **Geração de Questões:** A função `gerarNovaQuestaoComDados` faz uma chamada `fetch` para `http://127.0.0.1:5000/api/questoes/gerar`. Esta é a chamada esperada para o backend. Em caso de falha na conexão com o backend, ele utiliza um conjunto de questões simuladas localmente.
*   **Resposta de Questões:** A função `responderQuestao` *não* faz uma chamada direta ao backend. Em vez disso, ela atualiza as estatísticas (`questoesRespondidas`, `acertos`, `sequenciaAtual`, `xp`, `nivel`) diretamente no estado local e no `localStorage`. O feedback da resposta (se acertou ou errou) e a explicação são baseados na `questaoAtual` carregada, que pode ser do backend ou simulada.

**Apontamento:**

1.  **Geração de Questões:** A chamada para `/api/questoes/gerar` está correta, mas a URL (`http://127.0.0.1:5000`) está hardcoded. Idealmente, deveria usar a variável de ambiente `VITE_API_BASE_URL` como o `questoesService.js` faz, para maior flexibilidade e consistência.
2.  **Resposta de Questões:** Há uma desconexão crítica aqui. O `Painel.jsx` não está utilizando o `questoesService.responderQuestao` para persistir as respostas no backend (Firestore ou API). Toda a lógica de atualização de estatísticas e feedback é local, o que significa que os dados de desempenho do usuário não estão sendo salvos ou processados pelo backend. O `questoesService.js` possui a lógica para `responderQuestao` que interage com o backend ou Firestore, mas o `Painel.jsx` não a invoca.

**Recomendação:**

1.  **Geração de Questões:** Modificar `Painel.jsx` para usar `questoesService.gerarQuestao` em vez de uma chamada `fetch` direta, garantindo que a configuração da URL base da API seja consistente em todo o frontend.
2.  **Resposta de Questões:** Refatorar a função `responderQuestao` no `Painel.jsx` para chamar `questoesService.responderQuestao`. Isso garantirá que as respostas dos usuários e as atualizações de estatísticas sejam enviadas para o backend/Firestore, permitindo a persistência e o cálculo correto das métricas de gamificação no lado do servidor. O retorno de `questoesService.responderQuestao` deve ser usado para atualizar o estado do `Painel.jsx` (feedback, estatísticas).





#### 1.5. Análise do `Desempenho.jsx`

**Análise:**

O componente `Desempenho.jsx` é responsável por exibir as estatísticas de desempenho do usuário e o progresso da gamificação. Ele carrega os dados do usuário (`gabarita_user`) e as estatísticas (`gabarita_stats`) diretamente do `localStorage` no `useEffect`.

Este componente não realiza chamadas diretas ao backend para buscar ou atualizar dados de desempenho. Ele depende inteiramente dos dados que foram salvos no `localStorage` pelo `Painel.jsx` (e, indiretamente, pelo `Cadastro.jsx`).

**Apontamento:**

A dependência exclusiva do `localStorage` para as estatísticas de desempenho significa que, se o usuário limpar o cache do navegador ou acessar o sistema de um dispositivo diferente, suas estatísticas de gamificação serão perdidas ou não estarão sincronizadas. Isso compromete a persistência e a integridade dos dados de gamificação.

**Recomendação:**

1.  **Centralização de Estatísticas:** A lógica de atualização de estatísticas deve ser centralizada no backend (Firestore ou banco de dados). O `questoesService.js` já possui o método `atualizarEstatisticasUsuario` que interage com o Firestore. O `Painel.jsx` deve chamar `questoesService.responderQuestao`, que por sua vez, deve garantir que `atualizarEstatisticasUsuario` seja invocado.
2.  **Busca de Estatísticas no Backend:** O `Desempenho.jsx` deve ser modificado para buscar as estatísticas do usuário diretamente do backend (via `questoesService.buscarEstatisticas`) em vez de depender apenas do `localStorage`. Isso garantirá que as estatísticas exibidas sejam sempre as mais atualizadas e persistentes.

### 2. Avaliação das Fórmulas de Gamificação

**Análise:**

As fórmulas de gamificação são calculadas e atualizadas principalmente no `Painel.jsx` e armazenadas no `localStorage` sob a chave `gabarita_stats`. As métricas envolvidas são:

*   `questoesRespondidas`: Incrementada em 1 a cada questão respondida.
*   `acertos`: Incrementada em 1 se a resposta estiver correta.
*   `sequenciaAtual`: Incrementada em 1 se a resposta estiver correta, resetada para 0 se a resposta estiver incorreta.
*   `xp`: Incrementada em 10 para acertos e 3 para erros.
*   `nivel`: Calculado como `Math.floor(xp / 100) + 1`.

No `Desempenho.jsx`, a `taxa_acerto` é calculada como `(acertos / questoesRespondidas) * 100`. A `notaCorte` é uma simulação baseada no `progressoGeral` (que é a `taxa_acerto`). As insígnias são desbloqueadas com base em `acertos`, `sequenciaAtual`, `questoesRespondidas` e `nivel`.

**Apontamento:**

As fórmulas de cálculo de `questoesRespondidas`, `acertos`, `sequenciaAtual`, `xp` e `nivel` estão implementadas no frontend (`Painel.jsx`). Embora a lógica matemática esteja correta para os cálculos propostos, a principal fragilidade é que esses cálculos são feitos *apenas no frontend* e armazenados no `localStorage`. Isso significa que:

*   **Não persistência:** Os dados podem ser perdidos se o usuário limpar o cache ou usar outro dispositivo.
*   **Inconsistência:** Se o backend for implementado para calcular e armazenar essas métricas, haverá uma inconsistência entre os dados do frontend e do backend.
*   **Segurança:** Cálculos de gamificação no frontend são suscetíveis a manipulação por parte do usuário.

O `questoesService.js` possui um método `atualizarEstatisticasUsuario` que já atualiza `questoes_respondidas`, `acertos`, `xp` e `nivel` no Firestore. No entanto, a `sequenciaAtual` não está sendo persistida no backend/Firestore por este método.

**Recomendação:**

1.  **Mover Lógica de Gamificação para o Backend:** É altamente recomendável que a lógica de cálculo e atualização de todas as métricas de gamificação (`questoesRespondidas`, `acertos`, `sequenciaAtual`, `xp`, `nivel`) seja movida para o backend. Isso garante persistência, integridade e segurança dos dados.
2.  **Atualizar `atualizarEstatisticasUsuario`:** O método `atualizarEstatisticasUsuario` no `questoesService.js` (e sua contraparte no backend, se houver) deve ser estendido para incluir a atualização da `sequenciaAtual` no Firestore/banco de dados.
3.  **Frontend Apenas Exibe:** O frontend (`Painel.jsx` e `Desempenho.jsx`) deve apenas *exibir* as estatísticas que são retornadas pelo backend, em vez de calculá-las e armazená-las localmente.
4.  **Validação de Cálculos no Backend:** Uma vez que a lógica de gamificação for movida para o backend, os cálculos devem ser validados no lado do servidor para garantir que estejam corretos e que a lógica de progressão de nível e pontuação esteja funcionando conforme o esperado.

### Conclusão

O projeto Gabarit-ai possui uma estrutura clara de frontend e backend, mas há uma desconexão significativa na forma como a autenticação e, principalmente, as estatísticas de gamificação são tratadas. O frontend atualmente simula muitas dessas operações localmente, o que impede a persistência e a integridade dos dados. A refatoração para que o frontend consuma os serviços do backend de forma consistente e para que a lógica de gamificação seja centralizada no backend é crucial para a robustez e funcionalidade do sistema.

**Próximos Passos Sugeridos:**

1.  Implementar as recomendações de conexão frontend-backend para autenticação e questões.
2.  Mover a lógica de gamificação para o backend e garantir que todas as métricas sejam persistidas.
3.  Atualizar o frontend para consumir as estatísticas de gamificação do backend.
4.  Realizar testes abrangentes para validar a comunicação entre frontend e backend e a correção dos cálculos de gamificação.


