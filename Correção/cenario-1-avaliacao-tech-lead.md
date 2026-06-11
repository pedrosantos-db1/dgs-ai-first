# Skill de Avaliação — Tech Lead (Cenário 1)

> **Programa:** Trilha de Certificação AI First — DGS / DB1 Global Software
> **Escopo:** Cenário-Âncora 1 — Fase de Entendimento e Contexto (exercícios 1.1, 1.2, 1.3)
> **Referência:** Usar com `avaliacao-foundation.md` para dimensões e escala.

**Perfil:** Opera na camada de decisão técnica — ADRs, arquitetura, estratégia de prompt, revisão técnica. Demonstra julgamento superior: não apenas sabe o que fazer, mas justifica por que e defende contra contra-argumentos.

**Ferramentas esperadas:** Claude (chat) em todos; GitHub Copilot no exercício 1.2.

---

## Exercício 1.1 — Decisões arquiteturais documentadas como 4 ADRs

**Tópicos avaliados:** Fundamentos de IA, Engenharia de Contexto, RAG.

**Score do exercício = média das 4 ADRs.**

### ADR-0001 — Escolha do modelo LLM

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Trade-offs explícitos | Custo vs qualidade vs integração com dados | "GPT-4o porque é o melhor" |
| Estimativa de custo | Cálculo com volume (320 × 60% × tokens/query) | Sem estimativa |
| Alternativas | Ao menos 2 com prós/contras | Sem alternativas |

### ADR-0002 — Estratégia de gerenciamento de contexto

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Context window gerenciada | Define tamanho máximo/query, nº de chunks, orçamento por parte | "Usar todo o contexto" |
| Perguntas multi-domínio | Aborda "SLA + frete + devolução" na mesma pergunta | Sem menção |
| Context rot em sessões Teams | Aborda conversas longas (5+ perguntas) — reset? compaction? | Sem menção |

### ADR-0003 — Documentos contraditórios

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Solução concreta | Metadado de vigência + instrução no prompt + pipeline exclui obsoletos | "O modelo decide" |
| Referencia dados reais | Menciona PROC-042 vs v2 | Genérico |

### ADR-0004 — Build vs buy (pipeline de RAG)

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Considera contexto NovaTech | Azure existente, equipe de 6, prazo de 3 meses | Ignora constraints |
| Trade-off controle vs complexidade | Ambos os lados com prós/contras | Apenas vantagens da opção escolhida |

### Devil's advocate (obrigatório para ≥ 2 ADRs)

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Contra-argumentos substanciais | Forçaram revisão da decisão | Superficiais, não mudam nada |
| Decisão melhorou | Versão final mais robusta que inicial | Idênticas |

---

## Exercício 1.2 — Prompt engineering como artefato de arquitetura

**Tópicos avaliados:** Engenharia de Prompt (prompt como código), Engenharia de Contexto (anatomia do contexto), Harness (preview: probabilístico vs determinístico).

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Prompts como código | Versionados, nomeados, testáveis, com política de alteração | Texto informal |
| Anatomia de contexto | System prompt (estático) + metadados cliente + chunks + pergunta + histórico (dinâmicos). Com estimativa de tokens e orçamento total | Apenas "o prompt" |
| Script de teste (Copilot) | Conceito demonstrado: pergunta → resposta → verificação de critérios | Ausente ou pseudocódigo |
| Probabilístico vs determinístico | Exemplos concretos: "citar fonte = prompt + validação JSON em código" | Sem distinção |

---

## Exercício 1.3 — Revisão crítica de proposta de RAG

**Tópicos avaliados:** RAG (pipeline), Revisão Crítica (humano primeiro), Engenharia de Contexto (chunking).

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| 4+ problemas reais | Chunking fixo sem overlap, 3 chunks insuficiente, ingestão manual, ada-002 para PT-BR | < 3 problemas |
| Análise própria ANTES do Claude | Ao menos 3 problemas independentes | Análise vazia |
| Comparação honesta | Reconhece o que Claude encontrou e ele não, e vice-versa | "Já sabia tudo" |
| Proposta reescrita sem overengineering | Resolve problemas sem complexidade desnecessária | 15 componentes para 4 problemas |
