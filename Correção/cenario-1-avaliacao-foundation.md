# Skill de Avaliação — Foundation

> **Programa:** Trilha de Certificação AI First — Engenharia de Software Agêntica (DGS / DB1 Global Software)
> **Tipo:** Skill de avaliação dos exercícios práticos da trilha de formação
> **Escopo:** Cenário-Âncora 1 — Fase de Entendimento e Contexto (exercícios 1.1, 1.2, 1.3 de cada papel)
> **Tópicos avaliados:** Fundamentos de IA Generativa, Engenharia de Prompt, Engenharia de Contexto, RAG
> **Uso:** Fornecido como contexto para um LLM (Claude, ChatGPT, Copilot) junto com a skill do papel e o entregável do participante. Também pode ser usado por avaliadores humanos como rubrica.
> **Dependências:** Usar em conjunto com `avaliacao-[papel].md` e `prompt-avaliacao.md`.

---

## 5 Dimensões de Avaliação (escala 1–3 cada)

### D1 — Domínio Conceitual

| 1 | 2 | 3 |
|---|---|---|
| Conceitos ausentes, incorretos ou superficiais. Ex: menciona "alucinação" sem demonstrar entendimento. | Conceitos corretos mas genéricos — aplicados sem especificidade ao domínio NovaTech. | Conceitos corretos, específicos ao domínio, com nuance. Ex: identifica que PROC-042 vs v2 gera risco de mistura de multiplicadores. |

### D2 — Uso de Ferramentas

| 1 | 2 | 3 |
|---|---|---|
| Ferramenta não usada, ou prompt genérico único sem iteração. Output aceito acriticamente. | Ferramenta usada com evidência. Alguma iteração, mas refinamento superficial. | Prompts específicos, iteração demonstrada, output refinado com análise crítica. Ciclo gerar → avaliar → iterar visível. |

### D3 — Qualidade do Entregável

| 1 | 2 | 3 |
|---|---|---|
| Incompleto, com erros factuais, ou inutilizável. | Completo e correto, mas genérico — funcionaria para qualquer projeto. | Completo, correto, específico ao NovaTech, acionável. Outro membro do time usaria sem pedir esclarecimentos. |

### D4 — Pensamento Crítico

| 1 | 2 | 3 |
|---|---|---|
| Aceitação acrítica do output da IA. Sem análise própria. | Alguma análise, mas superficial. Identifica problemas óbvios mas não os sutis. | Análise profunda. Identifica erros não-óbvios. Nos exercícios "humano primeiro", demonstra competência independente. |

### D5 — Aplicabilidade ao Projeto

| 1 | 2 | 3 |
|---|---|---|
| Desconectado do projeto. Poderia ser sobre qualquer sistema. | Conectado mas com gaps de contexto. Ex: ignora que a NovaTech já tem Azure. | Profundamente conectado. Referencia dados específicos (320 chamados/dia, tiers, multiplicadores, prazos). |

---

## Score e Classificação

**Score do exercício:** Média das 5 dimensões (1.0 a 3.0).

| Score | Classificação |
|-------|---------------|
| 2.5–3.0 | Aprovado com distinção |
| 2.0–2.4 | Aprovado |
| 1.5–1.9 | Aprovado com ressalvas — reforçar tópicos deficientes |
| < 1.5 | Não aprovado — refazer após reforço |

---

## Regras que cortam nota automaticamente

| Situação | Consequência |
|----------|-------------|
| Exercício "humano primeiro" sem análise própria (ou idêntica ao output da IA) | D4 ≤ 1 |
| Armadilha intencional não identificada (listada nos critérios do exercício) | D4 ≤ 1 |
| Iteração pedida mas v1 ≈ v2 (mudanças cosméticas) | D2 ≤ 1 |
| Evidência de uso de ferramenta ausente quando exigida | D2 ≤ 2 |

---

## Como usar

**Avaliação humana:** Pontue cada dimensão com o checklist da skill do papel. Aplique as regras de corte.

**Avaliação com IA:** Use o prompt padrão em `prompt-avaliacao.md`. Anexe esta Foundation + a skill do papel + o enunciado + o entregável.
