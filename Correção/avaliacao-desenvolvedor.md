# Skill de Avaliação — Desenvolvedor (Cenário 2)

> **Programa:** Trilha de Certificação AI First — DGS / DB1 Global Software
> **Escopo:** Cenário-Âncora 2 — Fase de Estruturação do Trabalho (exercícios 2.1, 2.2, 2.3)
> **Referência:** Usar com `avaliacao-foundation.md` para dimensões e escala.

**Perfil:** Configura a infraestrutura de agentes (MCP), implementa specs com SDD, e define a estratégia de skills. Usa Copilot como ferramenta de implementação mantendo julgamento próprio.

**Ferramentas esperadas:** Claude (chat) em todos; GitHub Copilot nos exercícios 2.1 (agente com os MCP servers ativos), 2.2 e 2.3.

---

## Exercício 2.1 — Configuração de MCP servers

**Tópicos avaliados:** MCP (servers, tools, resources, permissões).

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Mapeamento necessidade → server local | Cada necessidade (código/specs/skills, docs de negócio, corpus de retrieval, histórico, memória) mapeada a um *reference server* local e gratuito (filesystem, git, memory, everything), com tools/resources e escopo | Usa servers pagos/externos (Azure, Confluence, GitHub remoto); < 3 servers; ou sem distinção tools/resources |
| Least privilege concreto | filesystem com escopo mínimo de pastas; `docs/novatech/` e `data/retrieval-corpus/` como read-only; justificativa por server | Escopo amplo demais; fontes de negócio com escrita; sem justificativa |
| Evidência de uso real | Servers no ar: o agente lê um doc de `docs/novatech/`, recupera um chunk de `data/retrieval-corpus/` (coerente com o mapa do Anexo B) e lê o histórico via git | Só o arquivo de config, sem evidência de execução |
| Riscos de segurança do setup local | Ex: filesystem com escopo amplo expõe `.env`/segredos; server com escrita deixa o agente alterar arquivos sem revisão | "Alguém pode hackear" |
| `.mcp/mcp.json` válido e coerente | Sintaticamente correto, coerente com o mapeamento/escopos, partindo do exemplo do Anexo C | Ausente, com erros, ou inconsistente com o mapeamento |

---

## Exercício 2.2 — Implementação com SDD (plan → tasks → código)

**Tópicos avaliados:** SDD (decomposição em tasks atômicas), Skills (padrões de código).

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Tasks atômicas | Cada task implementável e testável isoladamente. ID, dependências, critérios de aceite | Tasks grandes e interdependentes |
| Critérios de aceite verificáveis | "Endpoint retorna 400 para body sem campo question" | "Endpoint funciona" |
| Código segue padrões do plan | TypeScript, Zod, Azure Functions v4, pino, conforme definido | JavaScript, sem validação, console.log |
| Código segue Anexo C | Arquivo no path correto (`/src/functions/query/`) | Path inventado |
| Revisão crítica real | 2+ problemas reais no código do Copilot (não inventados) | Problemas cosméticos inventados |
| Conecta com cenário 1 | Reconhece que protótipo open-source (Dev 1.3) validou a abordagem; agora é produção | Ignora o trabalho anterior |

---

## Exercício 2.3 — Estratégia de skills do projeto

**Tópicos avaliados:** Skills (hierarquia Foundation → Domain → Artifact), AGENTS.md (como skills se conectam).

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Árvore coerente com projeto | Skills que o projeto realmente usaria (RAG endpoint, integration test, React card) | Skills teóricas que ninguém consumiria |
| Criação/consumo multi-papel | PS cria skill de spec, QA cria skill de teste, não é só para devs | Tudo criado e consumido por devs |
| SKILL.md Foundation concreto | Exemplos de código TypeScript reais (DO/DON'T), anti-padrões que Copilot geraria | Texto abstrato sem código |
| Anti-padrões úteis | Coisas que LLMs realmente geram errado: `as any`, `console.log`, require dinâmico | Anti-padrões genéricos |
| Referencia Anexo C | Skills na hierarquia `/skills/foundation/`, `/skills/domain/`, `/skills/artifact/` | Estrutura inventada |
