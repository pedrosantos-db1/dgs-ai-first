# Cenário-Âncora 3 — Fase de Governança e Validação

## Tópicos cobertos
- Harness Engineering: HITL (Human-in-the-Loop) e Structured Outputs
- Revisão Crítica de Outputs de IA

## Ferramentas disponíveis para os participantes
- **Claude** (chat) — todos os papéis
- **GitHub Copilot** — desenvolvedores e Tech Lead
- **Claude Cowork** — Delivery Manager, Product Specialist, QA
- **Claude Design** — Product Specialist

## Documentos de apoio
- **Anexo A — Documentação Simulada da NovaTech:** Fonte de verdade para avaliação de respostas do assistente e design de guardrails.
- **Anexo B — Chunks de Referência do Pipeline de RAG:** Chunks e mapa de cobertura para testes de regressão e avaliação de retrieval.
- **Anexo C — Estrutura do Repositório:** Mapa de diretórios e convenções, relevante para exercícios de harness e revisão de código.

---

## O Cenário (continuação)

O assistente de IA da NovaTech está em desenvolvimento. O pipeline de RAG está funcional, os primeiros endpoints foram implementados, e o bot do Teams responde perguntas de teste. Mas antes do go-live, o time precisa garantir que o sistema é confiável e governável.

Esta fase usa os artefatos produzidos nas fases anteriores: as ADRs e o pipeline de RAG da fase de entendimento (cenário 1), e o AGENTS.md, as specs SDD, as skills e os guardrails da fase de estruturação (cenário 2). O harness que será trabalhado agora amarra tudo isso num sistema de governança.

### O que foi construído até agora

- O pipeline de ingestão processa 847 documentos e os indexa no Azure AI Search.
- O query endpoint recebe perguntas via POST, busca chunks, e retorna respostas com citação de fonte.
- O bot do Teams funciona em ambiente de staging, acessível por 5 atendentes-piloto.
- O AGENTS.md (construído pelo time no cenário 2), as specs SDD e as skills estão no repositório e sendo usadas pelo Copilot.
- Os guardrails de produto foram formalizados pelo Product Specialist (cenário 2) em DEVE / NÃO DEVE / QUANDO EM DÚVIDA.
- Testes de integração cobrem ~75% do código.

### O que foi descoberto durante o desenvolvimento

- Em testes internos, **12% das respostas estavam incorretas**: alucinação, documento desatualizado, e chunk incorreto recuperado.
- As respostas do assistente são retornadas como texto livre. Não há um formato estruturado garantindo que campos obrigatórios (fonte, confiança) sempre estejam presentes — quando o modelo "esquece" de incluir a fonte, nada impede a resposta de seguir.
- Um desenvolvedor gerou com o Copilot um módulo de feedback que ignorou regras do AGENTS.md (não usou Zod, logou dados sensíveis do atendente).
- A NovaTech pediu uma demonstração para a diretoria em 2 semanas.

### O desafio desta fase

O time precisa:
1. Reforçar o harness — o conjunto de verificações e limites que torna o assistente confiável, usando **structured outputs** (forçar o modelo a responder em formato validável) e **human-in-the-loop** (pontos onde um humano valida antes de prosseguir).
2. Aplicar revisão crítica ao que foi gerado por IA: código, respostas do assistente, testes.

### Conceitos-chave desta fase

- **Structured Outputs:** Em vez de deixar o modelo responder em texto livre, define-se um formato (JSON) que a resposta DEVE seguir, com campos obrigatórios (ex: `answer`, `source_document`, `confidence_score`). Respostas que não seguem o formato são rejeitadas programaticamente. Reduz campos faltantes e facilita a validação automática.
- **Human-in-the-Loop (HITL):** Pontos do fluxo onde a validação final é de um humano, não do modelo. O harness define onde HITL é obrigatório, com base no risco da decisão (ex: respostas de baixa confiança sobre temas sensíveis).

---

## Exercícios por Papel

> Cada papel tem 2 exercícios neste cenário: um focado em **Harness Engineering** e outro em **Revisão Crítica de Outputs de IA**.

---

<details>

### DELIVERY MANAGER

#### Exercício 3.1 — Critérios de go-live com harness de governança

**Tópico:** Harness Engineering

**Contexto:** A demo para a diretoria da NovaTech é em 2 semanas. Você precisa definir o que precisa estar funcionando para que o go-live seja autorizado.

**Ferramentas a utilizar:** Claude (chat) + Claude Cowork

**Inputs fornecidos:**
- O cenário completo acima.
- O framework de harness (5 camadas): *"(1) Tool orchestration — coordenação de ferramentas e agentes. (2) Verification loops — verificação automática de outputs. (3) Context & memory — manutenção de contexto entre interações. (4) Guardrails — limites que o sistema não pode ultrapassar, incluindo pontos de human-in-the-loop. (5) Observability — visibilidade do que acontece em produção."*

**Tarefa:**
1. Usando o **Claude**, defina critérios de go-live organizados pelas 5 camadas do harness. Para cada camada, especifique o que precisa estar pronto e classifique cada critério como **bloqueante** (sem isso não vai ao ar) ou **desejável** (pode ir ao ar sem). Inclua ao menos um ponto de human-in-the-loop (ex: respostas de baixa confiança sobre carga perigosa passam por revisão humana antes de chegar ao atendente).

2. Usando o **Claude Cowork**, crie um dashboard de readiness do go-live mostrando o status de cada critério (verde/amarelo/vermelho), responsável, e data-alvo.

3. Defina um plano de rollback simples: qual o sinal de que algo deu errado, quem decide desligar, e qual a ação.

**Entregável:** Os critérios de go-live, o dashboard do Cowork, e o plano de rollback.

**Critérios de avaliação:**
- Os critérios são organizados pelas 5 camadas do harness (não é lista genérica).
- A distinção bloqueante vs desejável demonstra pragmatismo.
- Há ao menos um ponto de HITL concreto.
- O plano de rollback tem trigger, responsável e ação (não é "avaliar a situação").

---

#### Exercício 3.2 — Plano de observabilidade e melhoria contínua

**Tópico:** Revisão Crítica de Outputs de IA (aplicada a monitoramento)

**Contexto:** Após o go-live, o assistente precisa ser monitorado. Você garante que o time saiba quando algo dá errado e tenha processo para corrigir.

**Ferramentas a utilizar:** Claude (chat) + Claude Cowork

**Inputs fornecidos:**
- O cenário completo.
- As dimensões de observabilidade: *"métricas de uso (perguntas/dia, tempo de resposta), métricas de qualidade (% de feedback negativo, % de escalações), métricas técnicas (latência, taxa de erro), e métricas de conteúdo (documentos mais consultados, perguntas sem resposta)."*
- A expectativa da NovaTech: *"Queremos um relatório semanal que mostre se o assistente está melhorando ou piorando."*

**Tarefa:**
1. Usando o **Claude**, defina um plano de observabilidade com: quais métricas coletar (cobrindo as 4 dimensões), 2-3 alertas com thresholds concretos (ex: "se feedback negativo > 15% em 24h, notificar o time"), e como o feedback dos atendentes vira melhoria do assistente (feedback loop simples).

2. Usando o **Claude Cowork**, crie o template do relatório semanal para a NovaTech: 1 página com KPIs principais, tendência (melhorou/piorou), e ações planejadas.

**Entregável:** O plano de observabilidade, e o template de relatório gerado pelo Cowork.

**Critérios de avaliação:**
- As métricas cobrem as 4 dimensões.
- Os alertas têm thresholds concretos (não "monitorar se piora").
- O feedback loop conecta o atendente à correção no assistente.
- O template é claro para um executivo entender em 2 minutos.

---

### PRODUCT SPECIALIST

#### Exercício 3.1 — Revisão crítica das respostas do assistente

**Tópico:** Revisão Crítica de Outputs de IA

**Contexto:** Antes do go-live, você valida uma amostra de respostas do assistente para garantir que atendem aos requisitos de produto.

**Ferramentas a utilizar:** Claude (chat)

**Inputs fornecidos:**
- O cenário completo.
- A documentação da NovaTech (ver **Anexo A**) como fonte de verdade.
- 6 pares de pergunta/resposta do assistente em staging (simulados):

| # | Pergunta | Resposta | Fonte Citada | Confiança |
|---|----------|---------|--------------|-----------|
| 1 | "Qual o prazo de devolução para produtos standard?" | "O prazo é de 7 dias úteis após o recebimento. O cliente deve abrir chamado no portal e anexar fotos." | POL-001, seção 3.2 | Alta |
| 2 | "Meu cliente é Silver. Qual o prazo de resolução?" | "O cliente Silver tem resolução em até 48h." | SLA-2024 | Alta |
| 3 | "Posso devolver carga perigosa classe 3?" | "Não. Cargas perigosas (classes 1 a 6 da ANTT) não podem ser devolvidas pelo processo padrão. Recomendo escalar para o supervisor." | POL-001, seção 3.2 | Alta |
| 4 | "Qual a política para carga danificada durante transporte?" | "A política de danos prevê reembolso integral quando comprovada negligência da transportadora, mediante laudo técnico e fotos." | Nenhuma | Alta |
| 5 | "Qual o SLA do cliente Enterprise?" | "O tier Enterprise não foi encontrado na documentação. Os tiers documentados são Gold, Silver e Standard. Sugiro confirmar a classificação ou escalar ao supervisor." | — | Baixa |
| 6 | "Posso enviar carga perigosa com frete expresso?" | "Sim, cargas perigosas podem ser enviadas via frete expresso mediante autorização prévia do compliance e documentação ANTT atualizada." | FAQ-Atendimento, item 32 | Alta |

**Tarefa:**
1. Avalie cada resposta por conta própria: correta, parcialmente correta, ou incorreta? Justifique com base no Anexo A.

2. Depois, use o **Claude** como segundo avaliador e compare com a sua avaliação.

3. Para as respostas com problema, classifique o tipo de erro (alucinação, fonte não confiável, informação incompleta) e proponha um ajuste de produto (prompt, interface, ou pipeline) para preveni-lo.

**Entregável:** Sua avaliação, a avaliação do Claude, a comparação, e as propostas de ajuste.

**Critérios de avaliação:**
- A resposta 4 é identificada como alucinação (não há documento sobre política de danos na base — o assistente inventou com confiança alta).
- A resposta 6 é identificada como problemática (fonte é o FAQ informal sem validação — informação sobre carga perigosa deveria vir de documento formal).
- As respostas 1, 2, 3 e 5 são corretamente avaliadas como adequadas.
- A comparação com o Claude é honesta sobre concordâncias e divergências.

---

#### Exercício 3.2 — Harness de produto para melhoria contínua

**Tópico:** Harness Engineering

**Contexto:** O assistente vai evoluir após o go-live. Você define, do ponto de vista de produto, como garantir que ele melhore sem degradar.

**Ferramentas a utilizar:** Claude (chat)

**Inputs fornecidos:**
- O cenário completo.
- O conceito de harness de produto: *"Define quais métricas de qualidade são monitoradas, como o feedback de usuários é processado, e como mudanças no assistente são validadas antes de ir a produção (regression testing de produto)."*
- Os guardrails formalizados no cenário 2 (DEVE / NÃO DEVE / QUANDO EM DÚVIDA), que o harness deve preservar ao longo da evolução.

**Tarefa:**
Usando o **Claude**, projete um harness de produto que cubra:
1. **Processo de feedback:** como o feedback do atendente vira melhoria (novo documento? ajuste de prompt? reindexação?).
2. **Regression testing de produto:** antes de mudar o prompt ou adicionar documentos, como verificar que as respostas existentes não pioraram E que os guardrails do cenário 2 continuam sendo respeitados.
3. **Ponto de human-in-the-loop:** quais mudanças no assistente exigem aprovação humana antes de ir a produção, e quem aprova.

**Entregável:** O documento do harness de produto.

**Critérios de avaliação:**
- O processo de feedback é completo (do atendente até a melhoria efetiva).
- O regression testing reconhece que mudanças em IA podem ter efeitos colaterais e verifica que os guardrails não regridem.
- O ponto de HITL é concreto (define o que precisa de aprovação humana e quem aprova).

---

</details>

### DESENVOLVEDOR

#### Exercício 3.1 — Structured output e verificações determinísticas (harness de código)

**Tópico:** Harness Engineering

**Contexto:** Hoje as respostas do assistente são texto livre — nada garante que a fonte sempre venha preenchida. Você vai (a) forçar um structured output com formato validável e (b) adicionar duas verificações determinísticas que complementam o que o prompt faz de forma probabilística.

**Ferramentas a utilizar:** Claude (chat) + GitHub Copilot

**Inputs fornecidos:**
- O cenário completo.
- A documentação da NovaTech (ver **Anexo A**) — use para entender as regras que os guardrails protegem (ex: a exceção de carga perigosa na POL-001).
- A estrutura do repositório (ver **Anexo C**) — o módulo vai em `/src/services/response-validator.ts`.
- Os 2 guardrails a implementar (subconjunto dos guardrails que o PS formalizou no cenário 2):
  1. *"Toda resposta DEVE conter o campo `source_document` — se não tiver, a resposta é rejeitada e substituída por mensagem padrão."*
  2. *"Respostas que mencionam 'carga perigosa' junto com 'devolução' DEVEM conter a negativa — se afirmarem que a devolução é possível, a resposta é bloqueada."*
- Conceito de structured output: *"Em vez de texto livre, o modelo responde em JSON com formato fixo: { answer, source_document, confidence_score }. Valida-se com Zod. Se não bate com o formato, rejeita-se antes de checar o conteúdo."*

**Tarefa:**
1. Usando o **GitHub Copilot**, defina o schema Zod do structured output (campos: answer, source_document, confidence_score).

2. Usando o **GitHub Copilot**, implemente o `response-validator.ts` que: valida a resposta contra o schema, e aplica os 2 guardrails. Em qualquer falha, registra o motivo em log e retorna uma resposta padrão segura.

3. Usando o **Claude**, faça um code review rápido do que o Copilot gerou: identifique ao menos 2 problemas (ex: o schema aceita campos extras? o regex de "carga perigosa + devolução" cobre variações?) e corrija.

**Entregável:** O schema Zod, o código do response-validator, e o code review com as correções.

**Critérios de avaliação:**
- O schema de structured output é válido e usa Zod corretamente.
- Os 2 guardrails realmente bloqueiam respostas inválidas (não apenas logam).
- O code review identifica problemas reais (não inventados).
- A distinção entre prompt (probabilístico) e código (determinístico) fica clara.

---

#### Exercício 3.2 — Revisão crítica de código gerado por IA

**Tópico:** Revisão Crítica de Outputs de IA

**Contexto:** O Copilot gerou um módulo de feedback. O Tech Lead pediu que você revise antes do merge.

**Ferramentas a utilizar:** Claude (chat) + GitHub Copilot

**Inputs fornecidos:**
- O cenário completo.
- A estrutura do repositório (ver **Anexo C**) — o código deveria estar em `/src/functions/feedback/handler.ts`.
- O módulo gerado pelo Copilot (simulado):

```typescript
// feedback-handler.ts — gerado pelo Copilot
import { app, HttpRequest, HttpResponseInit } from '@azure/functions';

export async function feedbackHandler(
  request: HttpRequest
): Promise<HttpResponseInit> {
  const body = await request.json() as any;

  const feedback = {
    queryId: body.queryId,
    rating: body.rating,
    comment: body.comment,
    attendantEmail: body.attendantEmail,
    timestamp: new Date().toISOString()
  };

  console.log('Feedback recebido:', JSON.stringify(feedback));

  const { CosmosClient } = require('@azure/cosmos');
  const client = new CosmosClient(process.env.COSMOS_CONNECTION_STRING);
  const database = client.database('novatech');
  const container = database.container('feedbacks');

  await container.items.create(feedback);

  return { status: 200, body: 'OK' };
}

app.http('feedback', {
  methods: ['POST'],
  handler: feedbackHandler
});
```

- O AGENTS.md do projeto, construído no cenário 2 (resumo): *"TypeScript strict mode. Zod para validação de input. pino para logging (nunca console.log). Nunca logar dados pessoais (e-mail, nome). Imports estáticos no topo (nunca require dinâmico)."*

**Tarefa:**
1. Faça sua própria revisão ANTES de usar o Claude. Liste os problemas, classificando cada um (violação do AGENTS.md, problema de segurança, ou bug potencial).

2. Use o **Claude** para uma segunda revisão e compare as listas.

3. Usando o **GitHub Copilot**, reescreva o módulo corrigindo os problemas. O código final deve seguir o AGENTS.md.

**Entregável:** Sua revisão, a revisão do Claude, a comparação, e o código reescrito.

**Critérios de avaliação:**
- São identificados no mínimo: `as any` sem validação Zod, `console.log` em vez de pino, `require` dinâmico, e o `attendantEmail` (dado pessoal) sendo logado.
- A comparação humano vs Claude é honesta.
- O código reescrito resolve os problemas e segue o AGENTS.md.

---

<details>

### TECH LEAD

#### Exercício 3.1 — Design do harness do projeto

**Tópico:** Harness Engineering

**Contexto:** Você precisa projetar o harness que envolve o assistente — o que diferencia um protótipo de um sistema de produção.

**Ferramentas a utilizar:** Claude (chat) + GitHub Copilot

**Inputs fornecidos:**
- O cenário completo.
- O framework de 5 camadas do harness:
  1. **Tool orchestration** — coordenação de ingestão, retrieval e geração.
  2. **Verification loops** — verificação de outputs (fonte válida? schema do structured output respeitado?).
  3. **Context & memory** — manutenção de contexto, respeitando o context budget da ADR-0002 (cenário 1).
  4. **Guardrails** — limites via structured outputs + código (determinísticos) e via prompt (probabilísticos), com pontos de human-in-the-loop.
  5. **Observability** — logs, métricas, alertas.

**Tarefa:**
1. Usando o **Claude**, projete o harness pelas 5 camadas. Para cada uma, diga o que já está implementado, o que falta, e como fechar o gap. Seja concreto. Na camada de Context & memory, conecte ao context budget da ADR-0002. Na de Guardrails, indique onde structured outputs e human-in-the-loop entram.

2. Usando o **GitHub Copilot**, implemente **uma** verificação simples da camada de Verification loops: uma função que recebe a resposta do modelo e verifica se a fonte citada (`source_document`) existe na lista de documentos válidos da NovaTech. A lista usa os identificadores curtos dos documentos: `POL-001`, `PROC-042`, `PROC-042-v2`, `SLA-2024`, `FAQ-Atendimento` (não o título completo). Se a fonte citada não estiver na lista, marca a resposta como suspeita.

**Entregável:** O design do harness (5 camadas) e a função de verificação implementada.

**Critérios de avaliação:**
- O harness cobre as 5 camadas (não apenas guardrails).
- A camada Context & memory conecta-se à ADR-0002 (não reinventa a estratégia de contexto).
- A camada Guardrails menciona structured outputs e ao menos um ponto de HITL.
- A função de verificação é funcional e checa a fonte contra a lista de documentos válidos.

---

#### Exercício 3.2 — Revisão crítica da arquitetura gerada com IA

**Tópico:** Revisão Crítica de Outputs de IA

**Contexto:** Vários artefatos do projeto foram gerados com apoio de IA. Antes do go-live, você faz uma revisão de riscos.

**Ferramentas a utilizar:** Claude (chat)

**Inputs fornecidos:**
- O cenário completo.
- Resumo dos artefatos gerados com IA:
  - *"O AGENTS.md foi gerado pelo Claude e refinado 4 vezes. A última versão tem 15 páginas."*
  - *"3 skills foram criadas. A Foundation foi refinada após testes; as outras duas foram usadas sem refinamento."*
  - *"O pipeline de ingestão e o query endpoint foram ~60-70% gerados pelo Copilot."*
  - *"O system prompt foi iterado 6 vezes, sem documentar por que cada mudança foi feita."*

**Tarefa:**
1. Faça sua própria avaliação de riscos ANTES de usar o Claude. Para cada artefato: qual o risco de ter sido gerado por IA, e o que verificar antes do go-live.

2. Use o **Claude** como co-reviewer e compare as listas.

3. Priorize: dado que você tem 2 semanas, o que verifica primeiro? O que aceita como risco residual?

**Entregável:** Sua avaliação, a complementação do Claude, e a priorização.

**Critérios de avaliação:**
- Identifica que as 2 skills sem refinamento são um risco (podem gerar outputs inconsistentes).
- Identifica que o system prompt sem documentação de mudanças é risco de governança (sem rollback informado).
- A priorização é pragmática (foca no que reduz mais risco no tempo disponível).
- A comparação humano vs Claude é honesta.

---

### QA

#### Exercício 3.1 — Revisão crítica das respostas do assistente

**Tópico:** Revisão Crítica de Outputs de IA

**Contexto:** Antes do go-live, você executa uma bateria de avaliação sobre as respostas do assistente e produz um parecer.

**Ferramentas a utilizar:** Claude (chat) + Claude Cowork

**Inputs fornecidos:**
- O cenário completo.
- A documentação da NovaTech (ver **Anexo A**) como fonte de verdade.
- A rubrica de avaliação que você criou no cenário 2 (simulada — 4 dimensões: precisão factual, citação de fonte, aderência a guardrails, completude, escala 1-3 cada).
- 8 respostas do assistente em staging (simuladas):

| # | Pergunta | Resposta Resumida | Fonte | Esperado |
|---|----------|-------------------|-------|----------|
| 1 | "Prazo de devolução?" | 7 dias, exceto perigosas | POL-001 | Aprovada |
| 2 | "Devolução carga perigosa?" | Não é possível, escalar supervisor | POL-001 | Aprovada |
| 3 | "SLA Gold resolução?" | 24h | SLA-2024 | Aprovada |
| 4 | "SLA Platinum?" | Tier não encontrado, sugere verificar | — | Aprovada (reconheceu) |
| 5 | "Frete 600kg Manaus?" | Multiplicador 1.8 | PROC-042-v2 | Aprovada |
| 6 | "Frete 600kg sem destino?" | "O frete para o Sudeste é 1.1" (assumiu Sudeste sem ser informado) | PROC-042-v2 | Reprovada (assumiu dado) |
| 7 | "Receita de bolo?" | "Não tenho informações sobre receitas. Posso ajudar com logística." | — | Aprovada (escopo) |
| 8 | "What is the return policy?" | Responde em inglês | POL-001 | Reprovada (idioma) |

**Tarefa:**
1. Aplique a rubrica a cada uma das 8 respostas. Pontue as dimensões e calcule o score.

2. Faça isso PRIMEIRO por conta própria, DEPOIS use o **Claude** para uma segunda avaliação e compare.

3. Usando o **Claude Cowork**, gere um relatório de qualidade curto: score médio, respostas reprovadas com motivo, e seu parecer de go-live (pronto? com quais ressalvas?).

**Entregável:** Sua avaliação, a do Claude, a comparação, e o relatório do Cowork com parecer.

**Critérios de avaliação:**
- As respostas 6 e 8 são identificadas como reprovadas (assunção indevida e idioma errado).
- A rubrica é aplicada de forma consistente (mesma régua para todas).
- O parecer de go-live é fundamentado nos dados e pragmático.

---

#### Exercício 3.2 — Revisão crítica dos testes gerados por IA

**Tópico:** Revisão Crítica de Outputs de IA

**Contexto:** Alguns testes de integração foram gerados pelo Copilot. Você revisa se realmente testam o que deveriam.

**Ferramentas a utilizar:** Claude (chat)

**Inputs fornecidos:**
- O cenário completo.
- A estrutura do repositório (ver **Anexo C**) — o projeto usa **Vitest** como framework de teste (não jest).
- 3 testes simulados:

```typescript
// Teste 1 — assertions vagas
describe('query endpoint', () => {
  it('should return a response', async () => {
    const res = await request(app).post('/api/query').send({ question: 'prazo devolução' });
    expect(res.status).toBe(200);
    expect(res.body).toBeDefined();
  });
});

// Teste 2 — dados irreais (não exercitam o domínio)
describe('query endpoint edge cases', () => {
  it('should handle empty question', async () => {
    const res = await request(app).post('/api/query').send({ question: '' });
    expect(res.status).toBe(400);
  });
});

// Teste 3 — mock que mascara bug
describe('feedback endpoint', () => {
  it('should save feedback', async () => {
    const mockCreate = jest.fn().mockResolvedValue({ id: '123' });
    const res = await request(app).post('/api/feedback').send({
      queryId: 'q1', rating: 5, comment: 'great'
    });
    expect(res.status).toBe(200);
    expect(mockCreate).toHaveBeenCalled();
  });
});
```

**Tarefa:**
1. Avalie cada teste por conta própria: o que testa, o que falha em testar, e qual o risco se o teste "passar" mas o código estiver errado.

2. Use o **Claude** para uma segunda revisão e compare.

3. Reescreva o Teste 1 numa versão melhor (assertion que verifica o conteúdo da resposta, não só que existe).

**Entregável:** Sua revisão dos 3 testes, a revisão do Claude, a comparação, e o Teste 1 reescrito.

**Critérios de avaliação:**
- Teste 1: identificado como insuficiente (verifica que retorna algo, não que retorna a resposta CERTA).
- Teste 2: identificado como incompleto (edge case de input válido, mas não exercita o domínio — nenhuma pergunta real de logística).
- Teste 3: identificado como perigoso (o mock é tão permissivo que o teste passaria mesmo sem validação de input).
- Ponto de atenção: os testes usam `jest`, mas o projeto usa Vitest (inconsistência com o AGENTS.md). Identificar isso demonstra atenção ao contexto.
- O Teste 1 reescrito verifica conteúdo (ex: que a resposta contém o prazo correto e cita a fonte).

</details>