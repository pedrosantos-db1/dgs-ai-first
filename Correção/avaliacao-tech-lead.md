# Skill de Avaliação — Tech Lead (Cenário 2)

> **Programa:** Trilha de Certificação AI First — DGS / DB1 Global Software
> **Escopo:** Cenário-Âncora 2 — Fase de Estruturação do Trabalho (exercícios 2.1, 2.2, 2.3)
> **Referência:** Usar com `avaliacao-foundation.md` para dimensões e escala.

**Perfil:** Monta o AGENTS.md, define a arquitetura de MCP, e cria skills técnicas. Testa artefatos com Copilot e itera com base em resultados reais. Demonstra que artefatos para agentes precisam de refinamento empírico, não apenas autoria teórica.

**Ferramentas esperadas:** Claude (chat) em todos; GitHub Copilot em todos (2.1, 2.2, 2.3).

---

## Exercício 2.1 — Construção e teste do AGENTS.md

**Tópicos avaliados:** AGENTS.md (constitution do projeto), Skills (testar se agentes seguem), Engenharia de Contexto (regras de context budget do cenário 1).

**Exercício com ciclo obrigatório de teste real com Copilot. Se não há evidência de teste → D2 ≤ 1.**

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Prescritivo, não descritivo | "DEVE usar Zod para validação" vs "usamos Zod" | Texto narrativo |
| Inclui regras de context budget | ADR-0002 materializada: "~4K tokens system + ~8K chunks por query" | Sem menção a gerenciamento de contexto |
| Teste real com Copilot | Evidência: output do Copilot (endpoint + teste). Análise do que seguiu/ignorou | Sem evidência |
| Iteração v1 → v2 | Seções reescritas, Copilot gera output mais aderente com v2 | V1 = V2 |
| Reconhece limitações | Nem tudo será seguido — documentado honestamente | "AGENTS.md resolve tudo" |
| Referencia ADRs do cenário 1 | Decisões técnicas (TypeScript strict, Zod, Vitest, pino) derivadas das ADRs | Decisões inventadas sem rastreabilidade |

---

## Exercício 2.2 — Arquitetura de MCP

**Tópicos avaliados:** MCP (servers como infraestrutura gerenciada), Harness (monitoramento — preview).

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| MCP como infraestrutura | Versionamento, monitoramento, política de aprovação para novos servers | Configuração ad-hoc |
| Diagrama de conexões | Quem consome o quê, com permissões | Sem diagrama |
| Script de health check executado | Lê o `.mcp/mcp.json`, sobe/consulta cada server local e reporta status, com saída de execução real. Gerado com Copilot | Sem script, não-funcional, ou sem saída de execução |
| Plano de contingência realista | Agente degradado (capacidade reduzida) > agente quebrado (para tudo) | "Se cair, para tudo" |
| Política de aprovação equilibrada | Agilidade com segurança: não burocratiza demais, não libera tudo | Extremos: burocracia ou nenhum controle |

---

## Exercício 2.3 — Criação e teste de skills técnicas

**Tópicos avaliados:** Skills (autoria, teste empírico, maturidade), AGENTS.md (skills como extensão).

**Exercício com ciclo obrigatório de teste com Copilot. Se não há evidência → D2 ≤ 1.**

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| SKILL.md com código real | Exemplos TypeScript de DO/DON'T para Azure Functions endpoint. Anti-padrões com explicação | Texto abstrato sem código |
| Teste real com Copilot | Gerou endpoint com skill presente. Documentou seguido/ignorado | Sem teste real |
| Iteração documentada | Seções reescritas após teste. Output do Copilot melhorou | Sem iteração |
| Critérios de maturidade práticos | "Testada com 3+ gerações, anti-padrões validados, aprovada em review" | "Quando parecer boa" |
| Skills são artefatos vivos | Participante demonstra que skill precisa de refinamento contínuo | Skill escrita uma vez como definitiva |
