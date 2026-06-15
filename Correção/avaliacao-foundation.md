# Skill de Avaliação — Foundation (Cenário 2)

> **Programa:** Trilha de Certificação AI First — Engenharia de Software Agêntica (DGS / DB1 Global Software)
> **Tipo:** Skill de avaliação dos exercícios práticos da trilha de formação
> **Escopo:** Cenário-Âncora 2 — Fase de Estruturação do Trabalho (exercícios 2.1, 2.2, 2.3 de cada papel)
> **Tópicos avaliados:** MCP, Recorte de Domínio e SDD, AGENTS.md, Skills
> **Pré-requisitos do participante:** Tópicos 1–4 da trilha (cenário 1) + Tópicos 4 (MCP), 6, 7, 8
> **Uso:** Fornecido como contexto para um LLM (Claude, ChatGPT, Copilot) junto com a skill do papel e o entregável do participante.
> **Dependências:** Usar em conjunto com `avaliacao-[papel].md` e `prompt-avaliacao.md`.

---

## 5 Dimensões de Avaliação (escala 1–3 cada)

### D1 — Domínio Conceitual

| 1 | 2 | 3 |
|---|---|---|
| Conceitos ausentes ou incorretos. Ex: confunde MCP tools com resources, ou escreve AGENTS.md como documento narrativo. | Conceitos corretos mas genéricos — não reflete o contexto NovaTech. | Conceitos corretos, específicos ao projeto, e com nuance. Ex: define permissões MCP de least privilege — filesystem server com escopo mínimo de pastas e as fontes de negócio (`docs/novatech/`) em read-only. |

### D2 — Uso de Ferramentas

| 1 | 2 | 3 |
|---|---|---|
| Ferramenta não usada, ou prompt único sem iteração. Output aceito acriticamente. | Ferramenta usada com evidência. Alguma iteração. | Prompts específicos, iteração documentada, output refinado. Nos exercícios com Copilot: evidência de teste real (geração → avaliação → reescrita). |

### D3 — Qualidade do Entregável

| 1 | 2 | 3 |
|---|---|---|
| Incompleto, com erros, ou inutilizável. Ex: AGENTS.md que o Copilot não conseguiria seguir. | Completo e correto, mas genérico. | Completo, correto, específico ao NovaTech, e acionável. Outro membro do time usaria sem pedir esclarecimentos. Artefatos machine-readable quando exigido. |

### D4 — Pensamento Crítico

| 1 | 2 | 3 |
|---|---|---|
| Aceitação acrítica. Sem análise própria. | Alguma análise, mas superficial. | Análise profunda. Identifica limitações dos artefatos gerados. Nos exercícios de teste com Copilot: documenta o que foi seguido/ignorado com honestidade. |

### D5 — Aplicabilidade ao Projeto

| 1 | 2 | 3 |
|---|---|---|
| Desconectado do projeto. Poderia ser sobre qualquer sistema. | Conectado mas com gaps. Ex: ignora decisões do cenário 1 (ADRs, context budget). | Profundamente conectado. Referencia ADRs da fase anterior, usa linguagem ubíqua do domínio, respeita a estrutura do repositório (Anexo C). |

---

## Score e Classificação

**Score do exercício:** Média das 5 dimensões (1.0 a 3.0).

| Score | Classificação |
|-------|---------------|
| 2.5–3.0 | Aprovado com distinção |
| 2.0–2.4 | Aprovado |
| 1.5–1.9 | Aprovado com ressalvas |
| < 1.5 | Não aprovado — refazer |

---

## Regras de corte

| Situação | Consequência |
|----------|-------------|
| Exercício de teste com Copilot sem evidência real de geração/avaliação | D2 ≤ 1 |
| Dev 2.1 (MCP) ou TL 2.2 (health check) sem evidência de execução real dos servers locais | D2 ≤ 1 |
| Iteração pedida mas v1 ≈ v2 (mudanças cosméticas) | D2 ≤ 1 |
| AGENTS.md ou skill narrativo em vez de prescritivo | D3 ≤ 1 |
| Evidência de uso de ferramenta ausente quando exigida | D2 ≤ 2 |
| Artefato ignora decisões do cenário 1 (ADRs, context budget) quando deveria referenciá-las | D5 ≤ 2 |
