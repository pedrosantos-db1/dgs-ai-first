# Skill de Avaliação — Foundation (Cenário 3)

> **Programa:** Trilha de Certificação AI First — Engenharia de Software Agêntica (DGS / DB1 Global Software)
> **Tipo:** Skill de avaliação dos exercícios práticos da trilha de formação
> **Escopo:** Cenário-Âncora 3 — Fase de Governança e Validação (2 exercícios por papel: 3.1 e 3.2)
> **Tópicos avaliados:** Harness Engineering (HITL e Structured Outputs), Revisão Crítica de Outputs de IA
> **Pré-requisitos do participante:** Cenários 1 e 2 da trilha (Fundamentos→RAG; MCP→Skills)
> **Uso:** Fornecido como contexto para um LLM (Claude, ChatGPT, Copilot) junto com a skill do papel e o entregável do participante.
> **Dependências:** Usar em conjunto com `avaliacao-[papel].md` e `prompt-avaliacao.md`.

---

## Estrutura do cenário 3

Diferente dos cenários 1 e 2 (3 exercícios por papel), o cenário 3 tem **2 exercícios por papel**: um focado em **Harness Engineering** e outro em **Revisão Crítica de Outputs de IA**. O nível é deliberadamente mais acessível que o material original — a avaliação deve considerar isso e não penalizar a ausência de profundidade que o exercício não pediu.

---

## 5 Dimensões de Avaliação (escala 1–3 cada)

### D1 — Domínio Conceitual

| 1 | 2 | 3 |
|---|---|---|
| Conceitos ausentes ou incorretos. Ex: confunde structured output com prompt; não entende o que é HITL. | Conceitos corretos mas genéricos. | Conceitos corretos, específicos ao projeto. Ex: explica por que structured output (campo obrigatório validado) é mais confiável que pedir a fonte no prompt. |

### D2 — Uso de Ferramentas

| 1 | 2 | 3 |
|---|---|---|
| Ferramenta não usada, ou prompt único sem iteração. Output aceito acriticamente. | Ferramenta usada com evidência. | Ferramenta usada com prompts específicos e análise crítica do output. Nos exercícios com Copilot: evidência de geração + revisão. |

### D3 — Qualidade do Entregável

| 1 | 2 | 3 |
|---|---|---|
| Incompleto, com erros, ou inutilizável. | Completo e correto, mas genérico. | Completo, correto, específico ao NovaTech, e acionável. Código funcional quando exigido. |

### D4 — Pensamento Crítico

| 1 | 2 | 3 |
|---|---|---|
| Aceitação acrítica. Sem análise própria. Não identifica armadilhas. | Alguma análise; identifica problemas óbvios mas não os sutis. | Análise profunda. Identifica as armadilhas do exercício. Nos exercícios "humano primeiro", demonstra competência independente da IA. |

### D5 — Aplicabilidade ao Projeto

| 1 | 2 | 3 |
|---|---|---|
| Desconectado do projeto. | Conectado mas com gaps. Ex: ignora artefatos dos cenários 1 e 2. | Profundamente conectado. Referencia ADRs, guardrails do cenário 2, AGENTS.md, context budget. |

---

## Score e Classificação

**Score do exercício:** Média das 5 dimensões (1.0 a 3.0).
**Score do cenário:** Média dos 2 exercícios.

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
| Exercício "humano primeiro" sem análise própria (ou idêntica ao output da IA) | D4 ≤ 1 |
| Armadilha intencional não identificada (listada nos critérios do exercício) | D4 ≤ 1 |
| Exercício com Copilot sem evidência de geração/revisão | D2 ≤ 1 |
| Código que deveria bloquear respostas inválidas mas só loga (Dev 3.1, TL 3.1) | D3 ≤ 2 |
| Artefato ignora decisões dos cenários 1 e 2 quando deveria referenciá-las | D5 ≤ 2 |

---

## Como usar

**Avaliação humana:** Pontue cada dimensão com o checklist da skill do papel. Aplique as regras de corte.

**Avaliação com IA:** Use o prompt padrão em `prompt-avaliacao.md`. Anexe esta Foundation + a skill do papel + o enunciado + o entregável.
