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
