# tasks.md — Query Endpoint
**Gerado a partir do:** `specs/query-endpoint/plan.md`  
**Responsável:** Dev Sênior  
**Status de aprovação:** Aguardando aprovação do Tech Lead (Gate 2: Tasks → Implement)

---

## Visão Geral

O query endpoint é uma Azure Function HTTP que recebe perguntas de atendentes, busca chunks relevantes no Azure AI Search, monta um prompt dentro do context budget definido na ADR-0002, e retorna uma resposta com citação de fonte obrigatória.

---

## Tasks

---

### TASK-001 — Setup do endpoint HTTP com validação de input
**Estimativa:** P (Pequeno — ~2h)  
**Dependências:** nenhuma

**Descrição:**  
Criar a estrutura do Azure Function HTTP trigger para o endpoint `POST /api/query`, incluindo validação de input com Zod e resposta de erro padronizada para inputs inválidos.

**Critérios de aceite:**
- [ ] Arquivo `src/functions/query/handler.ts` criado com Azure Functions v4 HTTP trigger.
- [ ] Schema Zod definido em `src/functions/query/validator.ts` com campo `question: string` (min 1, max 500 chars) e `sessionId?: string`.
- [ ] Requisição com `question` vazia retorna HTTP 400 com body `{ error: "VALIDATION_ERROR", message: "..." }`.
- [ ] Requisição com body inválido (não JSON) retorna HTTP 400.
- [ ] Requisição válida retorna HTTP 200 (mesmo que a resposta seja placeholder).
- [ ] Nenhum `console.log` no código — usar logger pino (ver `src/shared/logger.ts`).
- [ ] Arquivo exporta a função conforme a convenção do projeto (ver `skills/domain/azure-functions-endpoint.md`).

---

### TASK-002 — Integração com Azure OpenAI para geração de embedding
**Estimativa:** M (Médio — ~4h)  
**Dependências:** TASK-001

**Descrição:**  
Implementar o serviço que converte a pergunta do atendente em embedding usando Azure OpenAI (modelo text-embedding-ada-002). Inclui retry com exponential backoff para falhas transitórias.

**Critérios de aceite:**
- [ ] Arquivo `src/services/completion.ts` exporta função `generateEmbedding(question: string): Promise<number[]>`.
- [ ] Função usa o Azure OpenAI SDK configurado via variáveis de ambiente (`AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_EMBEDDING_MODEL`).
- [ ] Implementa retry com exponential backoff: 3 tentativas, delays de 1s, 2s, 4s.
- [ ] Em caso de falha após 3 tentativas, lança `EmbeddingError` (custom error de `src/shared/errors.ts`).
- [ ] Log de info ao gerar embedding (duração da chamada, tamanho do vetor retornado).
- [ ] Testes unitários em `tests/unit/services/completion.test.ts` com mock da chamada Azure OpenAI (msw ou jest mock).

---

### TASK-003 — Integração com Azure AI Search para recuperação de chunks
**Estimativa:** M (Médio — ~4h)  
**Dependências:** TASK-002

**Descrição:**  
Implementar o serviço que recebe o embedding da pergunta e retorna os top-5 chunks mais relevantes do índice Azure AI Search, com metadados de fonte e vigência para tratamento de documentos contraditórios (ADR-0003).

**Critérios de aceite:**
- [ ] Arquivo `src/services/search.ts` exporta função `searchChunks(embedding: number[]): Promise<Chunk[]>`.
- [ ] Retorna exatamente 5 chunks (configurável via env `SEARCH_TOP_K`, default 5).
- [ ] Cada chunk retornado contém: `content: string`, `sourceDocument: string`, `section: string`, `version: string`, `effectiveDate: string`.
- [ ] Chunks de documentos com `effectiveDate` mais recente são priorizados quando dois chunks cobrem o mesmo tópico (ADR-0003).
- [ ] Em caso de falha, lança `SearchError` com retry (mesma estratégia da TASK-002).
- [ ] Testes unitários com mock do SDK do Azure AI Search.

---

### TASK-004 — Construção do prompt com context budget
**Estimativa:** M (Médio — ~3h)  
**Dependências:** TASK-003

**Descrição:**  
Implementar o serviço que monta o prompt final combinando system prompt, chunks recuperados e pergunta do atendente, respeitando o context budget definido na ADR-0002 (~4K tokens para system prompt + ~8K para chunks).

**Critérios de aceite:**
- [ ] Arquivo `src/services/prompt-builder.ts` exporta função `buildPrompt(question: string, chunks: Chunk[]): Promise<PromptPayload>`.
- [ ] Lê o system prompt de `/prompts/system-prompt.md` (não hardcoded).
- [ ] Estima tokens com heurística simples (1 token ≈ 4 chars) antes de enviar ao OpenAI.
- [ ] Se o total exceder o budget total (16K tokens), trunca chunks do final até caber — nunca trunca o system prompt ou a pergunta.
- [ ] Inclui instrução explícita para priorizar documento com data de vigência mais recente quando houver contradição entre chunks.
- [ ] Log de debug com total de tokens estimados por componente (system, chunks, question).
- [ ] Testes unitários verificam que o truncamento funciona e que o system prompt nunca é truncado.

---

### TASK-005 — Chamada ao GPT-4o e montagem da resposta com source_document
**Estimativa:** M (Médio — ~4h)  
**Dependências:** TASK-004

**Descrição:**  
Implementar a chamada ao Azure OpenAI GPT-4o com o prompt montado na TASK-004, e montar o objeto de resposta final com o campo obrigatório `source_document`.

**Critérios de aceite:**
- [ ] Arquivo `src/functions/query/response-builder.ts` exporta função `buildResponse(completion: string, chunks: Chunk[]): QueryResponse`.
- [ ] Tipo `QueryResponse` em `src/shared/types.ts` contém: `answer: string`, `source_document: string`, `confidence: "high" | "low"`, `warnings: string[]`.
- [ ] Campo `source_document` é obrigatório — se o LLM não citar fonte, o campo é populado com o `sourceDocument` do chunk de maior relevância.
- [ ] Quando confiança é baixa (determinado por presença de "não encontrei" ou "não tenho informação" na resposta), `confidence` = `"low"` e `warnings` inclui mensagem de aviso.
- [ ] Chamada ao GPT-4o usa retry (mesma estratégia das tasks anteriores).
- [ ] Testes unitários para a lógica de `buildResponse` com diferentes outputs do LLM.

---

### TASK-006 — Integração end-to-end do handler e testes de integração
**Estimativa:** G (Grande — ~6h)  
**Dependências:** TASK-001, TASK-002, TASK-003, TASK-004, TASK-005

**Descrição:**  
Conectar todos os serviços no handler principal do endpoint, adicionar logging estruturado de ponta a ponta, e criar testes de integração que exercitem o fluxo completo com mocks das APIs externas (msw).

**Critérios de aceite:**
- [ ] `src/functions/query/handler.ts` orquestra a cadeia: validate → embed → search → buildPrompt → complete → buildResponse.
- [ ] Tempo total de execução é logado (para monitorar o SLA de < 30s definido nos requirements).
- [ ] Em qualquer erro não tratado, retorna HTTP 500 com `{ error: "INTERNAL_ERROR" }` — nunca expõe stack trace ao cliente.
- [ ] Testes de integração em `tests/integration/query-endpoint.test.ts` cobrem:
  - Happy path: pergunta válida → resposta com `source_document`.
  - Azure OpenAI indisponível → HTTP 503 após retries esgotados.
  - Azure AI Search retorna 0 chunks → resposta com `confidence: "low"` e warning.
  - Pergunta sobre carga perigosa + devolução → resposta não afirma que pode devolver.
- [ ] Cobertura de linhas do módulo `src/functions/query/` ≥ 80%.

---

## Dependências externas (fora do escopo desta spec)

- Azure AI Search index populado (depende do módulo `pipeline-ingestao`).
- System prompt finalizado em `/prompts/system-prompt.md`.
- Variáveis de ambiente configuradas em `local.settings.json` (não commitado).

---

## Revisão Crítica do Código Gerado pelo Copilot

### Código gerado pelo Copilot (TASK-001 — handler.ts)

```typescript
// Gerado pelo GitHub Copilot com base em AGENTS.md + skills/domain/azure-functions-endpoint.md
import { app, HttpRequest, HttpResponseInit, InvocationContext } from "@azure/functions";
import { z } from "zod";
import { logger } from "../shared/logger";

const querySchema = z.object({
  question: z.string().min(1).max(500),
  sessionId: z.string().optional(),
});

export async function queryHandler(
  request: HttpRequest,
  context: InvocationContext
): Promise<HttpResponseInit> {
  const log = logger.child({ functionName: "query", invocationId: context.invocationId });

  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return {
      status: 400,
      jsonBody: { error: "VALIDATION_ERROR", message: "Request body must be valid JSON" },
    };
  }

  const parsed = querySchema.safeParse(body);
  if (!parsed.success) {
    return {
      status: 400,
      jsonBody: { error: "VALIDATION_ERROR", message: parsed.error.issues[0].message },
    };
  }

  log.info({ question: parsed.data.question }, "query received");

  // TODO: chamar serviços (embed → search → buildPrompt → complete)
  return {
    status: 200,
    jsonBody: { answer: "placeholder", source_document: "" },
  };
}

app.http("query", {
  methods: ["POST"],
  authLevel: "function",
  route: "query",
  handler: queryHandler,
});
```

---

### Ponto de ajuste 1 — `source_document` vazio no placeholder

**Problema identificado:** O placeholder retorna `source_document: ""` — uma string vazia. Se este código fosse para review, um revisor notaria que viola o contrato definido nos requirements: "Toda resposta cita ao menos uma fonte" (VC-02). Um campo vazio passaria por validação Zod mas falharia nos testes de integração.

**Ajuste proposto:** Remover o placeholder de retorno ou substituir por um erro explícito de "não implementado" enquanto as tasks de serviço não estão prontas:
```typescript
return {
  status: 501,
  jsonBody: { error: "NOT_IMPLEMENTED", message: "Query pipeline not yet connected" },
};
```
Isso torna a incompletude explícita e evita que testes de integração passem com dados falsos.

---

### Ponto de ajuste 2 — `authLevel: "function"` requer `x-functions-key` header

**Problema identificado:** O Copilot gerou `authLevel: "function"`, que exige uma chave de autenticação no header `x-functions-key`. Para testes locais com o Azure Functions Core Tools, isso funciona, mas os testes de integração precisarão configurar essa chave ou usar `authLevel: "anonymous"` no ambiente de teste.

**Ajuste proposto:** Adicionar comentário explicativo e/ou configurar `authLevel` via variável de ambiente para facilitar testes locais:
```typescript
app.http("query", {
  methods: ["POST"],
  // authLevel: "function" requires x-functions-key header in production.
  // Use "anonymous" only in local test environments.
  authLevel: (process.env.FUNCTIONS_AUTH_LEVEL as "function" | "anonymous") ?? "function",
  route: "query",
  handler: queryHandler,
});
```
Isso precisa ser documentado no AGENTS.md para que o Copilot não regenere `authLevel: "anonymous"` em produção.
