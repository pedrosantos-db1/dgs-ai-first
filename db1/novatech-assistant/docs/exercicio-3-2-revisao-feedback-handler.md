# Exercício 3.2 — Revisão crítica do módulo de feedback gerado por IA

## 1. Minha revisão (antes de usar o Claude)

Leitura rápida do `feedback-handler.ts` gerado pelo Copilot, comparando linha a linha com o resumo do AGENTS.md.

| # | Problema | Classificação |
|---|----------|----------------|
| 1 | `const body = await request.json() as any;` — nenhuma validação de schema, apenas um cast. Qualquer payload malformado (campos faltando, tipos errados) passa direto. | Violação do AGENTS.md (exige Zod) + bug potencial |
| 2 | `console.log('Feedback recebido:', JSON.stringify(feedback))` | Violação do AGENTS.md (exige pino) |
| 3 | O `console.log` acima serializa o objeto `feedback` inteiro, que inclui `attendantEmail` — dado pessoal indo para stdout/logs. | Violação do AGENTS.md + problema de segurança (exposição de dado pessoal) |
| 4 | `const { CosmosClient } = require('@azure/cosmos');` — `require` dinâmico dentro da função, com import estático do `@azure/functions` já presente no topo. | Violação do AGENTS.md (imports estáticos no topo) |
| 5 | Não há `try/catch` em nenhum ponto. Se `request.json()` falhar (JSON inválido) ou `container.items.create` falhar (Cosmos fora do ar, `rating` de tipo incompatível com o schema do container etc.), a função lança uma exceção não tratada. | Bug potencial |

**Observação:** essa primeira passada focou nos quatro pontos que o enunciado já sinalizava (`as any`, `console.log`, `require`, e-mail logado) mais o `try/catch` ausente, que salta aos olhos por não existir nenhum tratamento de erro no arquivo.

---

## 2. Revisão do Claude (segunda revisão)

Reexaminando o mesmo arquivo com mais profundidade, além de confirmar os 5 pontos acima, encontrei problemas adicionais que uma leitura rápida tende a não pegar:

| # | Problema | Classificação |
|---|----------|----------------|
| 6 | `CosmosClient` é instanciado dentro do handler — uma conexão nova a cada requisição, em vez de um client reutilizado no escopo do módulo (padrão recomendado pelo SDK do Azure Functions para evitar exaustão de conexões e latência extra por invocação). | Bug potencial (performance/escalabilidade) |
| 7 | A função sempre retorna `{ status: 200, body: 'OK' }`, mesmo que o payload seja inválido ou o `rating` esteja fora de um intervalo esperado. Não há diferenciação entre sucesso, erro de validação (400) e erro interno (500) — o cliente (bot do Teams / painel) não tem como saber se o feedback foi realmente persistido. | Bug potencial |
| 8 | Sem validação de conteúdo: `rating` pode ser qualquer coisa (string, número fora de 1–5, `undefined`), `comment` não tem limite de tamanho, `queryId` não é verificado como referência válida. Dados inconsistentes chegam ao Cosmos DB sem checagem. | Bug potencial (consequência direta da falta de Zod, mas vale listar separadamente pelo impacto em dados) |
| 9 | `@azure/cosmos` é importado (via `require`) mas não consta em `package.json` (`dependencies` só tem `pino` e `zod`); `@azure/functions` também não está listado. O build/instalação falhará antes mesmo de rodar. | Bug potencial (build quebrado) — não é um item do AGENTS.md, mas é um problema real e verificável no repositório |
| 10 | Se `request.json()` ou o `container.items.create` lançarem, a exceção não tratada pode propagar o stack trace/mensagem de erro do Cosmos (incluindo detalhes internos, como connection string mal formatada) para a resposta HTTP, dependendo de como o host do Azure Functions trata exceções não capturadas. | Problema de segurança (potencial vazamento de detalhes internos) |

---

## 3. Comparação (honesta)

- **Sobreposição:** os itens 1–5 (o `as any` sem Zod, o `console.log`, o e-mail logado, o `require` dinâmico e a ausência de `try/catch`) foram identificados nas duas passadas — são os problemas "óbvios" quando se compara o código linha a linha com o AGENTS.md.
- **O que a segunda revisão (Claude) acrescentou:** os itens 6–10 não vieram de comparar o código com uma regra explícita do AGENTS.md, e sim de avaliar comportamento em produção (reuso de conexão, ausência de status codes diferenciados, dados não validados no Cosmos, dependências faltando no `package.json`, vazamento de stack trace). Esses são exatamente o tipo de problema que passa despercebido numa leitura rápida focada em "bater a lista de regras", porque exigem simular o que acontece quando algo dá errado, não apenas o caminho feliz.
- **Nenhum item da minha primeira lista foi refutado** pela segunda revisão — todos os 5 continuam válidos. A segunda passada foi estritamente aditiva.
- **Conclusão prática:** comparar o código com uma checklist (AGENTS.md) pega as violações de convenção rapidamente, mas não substitui perguntar "o que acontece se isso falhar?" e "esse import realmente existe no projeto?". As duas revisões juntas cobrem o que uma sozinha deixaria passar.

---

## 4. Código reescrito

Ver [`src/functions/feedback/validator.ts`](../src/functions/feedback/validator.ts) e [`src/functions/feedback/handler.ts`](../src/functions/feedback/handler.ts).

Resumo das correções aplicadas:
- Schema Zod (`feedbackInputSchema`) valida `queryId`, `rating` (inteiro 1–5), `comment` (opcional, com limite de tamanho) e `attendantEmail` (formato de e-mail) antes de qualquer uso do payload — substitui o `as any`.
- `pino` (via `shared/logger.ts`, que já tem `redact` configurado para `attendantEmail`/`email`/`comment`) substitui o `console.log`.
- `CosmosClient` importado estaticamente no topo e instanciado uma única vez no escopo do módulo (fora do handler), reaproveitado entre invocações.
- `try/catch` cobre parsing do body, validação Zod e escrita no Cosmos, retornando 400 para payload inválido e 500 (com mensagem genérica, sem detalhes internos) para falhas inesperadas — nunca mais sempre-200.
- `package.json` precisa incluir `@azure/functions` e `@azure/cosmos` nas dependências (apontado na revisão, não é algo que o código por si resolve).
