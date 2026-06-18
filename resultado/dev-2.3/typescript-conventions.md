# SKILL: typescript-conventions
**Nível:** Foundation  
**Frase-ativação:** "Gere código TypeScript seguindo as convenções do projeto NovaTech"  
**Criado por:** Tech Lead  
**Consumido por:** Dev Pleno, Dev Sênior — e por todas as skills de nível Domain e Artifact como dependência base  
**Dependências:** nenhuma (é a skill base)

---

## Contexto

Esta skill define as convenções de TypeScript para o projeto `novatech-assistant`. Toda geração de código por agentes (Copilot, Claude Code) deve respeitar estas regras antes de qualquer outra consideração. Skills de Domain e Artifact assumem que estas convenções já foram lidas.

O projeto usa TypeScript com `strict: true`. Isso não é opcional. Qualquer código gerado que não compile com `strict: true` está errado.

---

## Regras Prescritivas

### Tipos e Interfaces

**DEVE** usar tipos explícitos em parâmetros de função e retornos públicos. TypeScript inferência é aceita apenas em variáveis locais simples.

**DEVE** usar `type` para unions e intersections, `interface` para shapes de objetos que podem ser extendidos.

**NÃO DEVE** usar `any`. Use `unknown` e faça narrowing explícito. Se o tipo vier de uma API externa não tipada, use Zod para validar e inferir o tipo.

**NÃO DEVE** usar `!` (non-null assertion) sem comentário explicando por que o valor nunca é null naquele ponto.

### Imports

**DEVE** usar `import type` para importar apenas tipos, separado de imports de runtime.

**DEVE** organizar imports na ordem: node built-ins → pacotes externos → módulos internos (`src/`). Cada grupo separado por linha em branco.

**NÃO DEVE** usar `import * as` exceto para módulos que não têm named exports (raro).

### Funções e Async

**DEVE** marcar como `async` apenas funções que de fato usam `await`. Funções síncronas não devem ser `async`.

**DEVE** usar `Promise<T>` com tipo explícito no retorno de funções async públicas.

**NÃO DEVE** usar callbacks. Use `async/await` consistentemente.

### Logging

**DEVE** usar o logger pino de `src/shared/logger.ts`. Nunca `console.log`, `console.error` ou `console.warn`.

**DEVE** usar log estruturado: passar dados como objeto no primeiro argumento, mensagem como segundo.

**NÃO DEVE** logar dados sensíveis (tokens, chaves de API, CPF, dados pessoais de clientes).

### Erros

**DEVE** usar os custom errors de `src/shared/errors.ts`. Não lançar `new Error("mensagem genérica")`.

**DEVE** capturar erros no boundary correto (handler da Azure Function). Serviços internos propagam erros — não silenciam.

**NÃO DEVE** usar `try/catch` vazio ou `catch(e) { /* ignore */ }`.

---

## Exemplos

### DO — Tipos explícitos, imports corretos, pino

```typescript
import type { Chunk } from "../../shared/types";

import { SearchClient } from "@azure/search-documents";
import { logger } from "../../shared/logger";
import { SearchError } from "../../shared/errors";

export async function searchChunks(embedding: number[]): Promise<Chunk[]> {
  const log = logger.child({ service: "search" });

  try {
    const results = await searchClient.search("*", {
      vectors: [{ value: embedding, fields: ["embedding"], kNearestNeighborsCount: 5 }],
    });

    const chunks: Chunk[] = [];
    for await (const result of results.results) {
      chunks.push(result.document as Chunk);
    }

    log.info({ count: chunks.length }, "chunks retrieved");
    return chunks;
  } catch (error) {
    log.error({ err: error }, "search failed");
    throw new SearchError("Failed to retrieve chunks from Azure AI Search", { cause: error });
  }
}
```

### DON'T — `any`, `console.log`, retorno sem tipo, captura genérica

```typescript
// ERRADO: any, console.log, sem tipo de retorno, catch silencioso
export async function searchChunks(embedding: any) {
  try {
    const results = await searchClient.search("*", { vectors: [embedding] });
    console.log("got results", results);
    return results;
  } catch (e) {
    // silently ignore
  }
}
```

---

### DO — `unknown` com narrowing explícito em vez de `any`

```typescript
// Validando dado externo com Zod em vez de usar any
import { z } from "zod";

const externalResponseSchema = z.object({
  answer: z.string(),
  confidence: z.enum(["high", "low"]),
});

function parseExternalResponse(raw: unknown) {
  return externalResponseSchema.parse(raw); // lança se inválido, infere tipo se válido
}
```

### DON'T — `any` para dado externo

```typescript
// ERRADO: any "resolve" o problema de tipo mas esconde bugs de runtime
function parseExternalResponse(raw: any) {
  return raw.answer; // pode ser undefined, pode crashar, TypeScript não avisa
}
```

---

### DO — `import type` separado de import de runtime

```typescript
import type { QueryResponse, Chunk } from "../../shared/types";

import { z } from "zod";
import { logger } from "../../shared/logger";
```

### DON'T — misturar tipo e runtime no mesmo import

```typescript
// ERRADO: mistura tipo e valor — confunde o compilador com isolatedModules
import { QueryResponse, logger } from "../../shared/types";
```

---

## Anti-padrões que o Copilot costuma gerar (sem esta skill)

### Anti-padrão 1 — `console.log` em vez de pino

O Copilot usa `console.log` por padrão em quase todo código que gera. Sem esta skill, todo endpoint terá `console.log("Processing query:", question)` em produção, que não é estruturado e não integrável com o sistema de logs do Azure Functions.

**O que acontece:** Logs sem correlationId, sem level, sem dados estruturados. Impossível filtrar por invocationId ou sessionId.

### Anti-padrão 2 — `async` em funções síncronas

O Copilot frequentemente marca como `async` funções que não têm `await`, especialmente quando está "completando" um handler. Isso cria promessas desnecessárias e confunde o type checker.

```typescript
// Copilot gera isso:
export async function buildErrorResponse(message: string): Promise<HttpResponseInit> {
  return { status: 400, jsonBody: { error: message } }; // sem await — async desnecessário
}

// Deveria ser:
export function buildErrorResponse(message: string): HttpResponseInit {
  return { status: 400, jsonBody: { error: message } };
}
```

### Anti-padrão 3 — `try/catch` que engole o erro

O Copilot frequentemente gera blocos `catch` que apenas logam sem relançar, especialmente em serviços internos. O resultado é que o handler recebe `undefined` em vez de um erro, e retorna HTTP 200 com resposta vazia.

```typescript
// Copilot gera isso em services:
async function callOpenAI(prompt: string) {
  try {
    return await client.complete(prompt);
  } catch (error) {
    console.error(error); // engoliu o erro — handler não sabe que falhou
  }
}
```

### Anti-padrão 4 — `interface` para unions

```typescript
// Copilot gera isso:
interface ConfidenceLevel {
  level: "high" | "low";
}

// Deveria ser:
type ConfidenceLevel = "high" | "low";
```

### Anti-padrão 5 — Não usar `authLevel` correto no app.http

O Copilot tende a usar `authLevel: "anonymous"` para facilitar os testes, mas este projeto usa `"function"` em produção. Sem esta skill, o Copilot gera endpoints sem autenticação que seriam deployados expostos.
