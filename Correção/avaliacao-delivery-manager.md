# Skill de Avaliação — Delivery Manager (Cenário 2)

> **Programa:** Trilha de Certificação AI First — DGS / DB1 Global Software
> **Escopo:** Cenário-Âncora 2 — Fase de Estruturação do Trabalho (exercícios 2.1, 2.2, 2.3)
> **Referência:** Usar com `avaliacao-foundation.md` para dimensões e escala.

**Perfil:** Define como o time trabalha no modelo AI First — workflow, governance de specs, e regras de gestão consumíveis por agentes.

**Ferramentas esperadas:** Claude (chat) em todos; Claude Cowork nos exercícios 2.1 e 2.2.

---

## Exercício 2.1 — Workflow de desenvolvimento AI First

**Tópicos avaliados:** MCP (quais ferramentas cada papel usa), SDD (fluxo Spec→Plan→Tasks).

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Ferramentas diferenciadas por papel | Copilot para devs, Cowork para gestão, Design para produto — não mistura | Todos usam tudo sem distinção |
| Validation gates específicos | Cada gate: quem aprova, o que verifica, critério de aprovação concreto | "Revisar antes de continuar" |
| Equilíbrio velocidade/segurança | Gates proporcionais ao risco (merge na main > draft de spec) | Sem gates, ou gates em tudo |
| Checklist (Cowork) executável | Qualquer membro do time sabe o que fazer ao chegar num gate | Lista genérica |

---

## Exercício 2.2 — Governança de specs no modelo SDD

**Tópicos avaliados:** SDD (specs como contratos executáveis), AGENTS.md (governança de artefatos).

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Specs como artefatos vivos | Processo com ciclo de vida (rascunho → revisão → aprovação → implementação → validação) | Specs escritas uma vez e esquecidas |
| Atribuição coerente por papel | PS → requirements, TL → plan, Dev → tasks | Todos fazem tudo, ou um faz tudo |
| Change management explícito | O que acontece se spec muda após início de implementação: quem aprova, como afeta tasks | Sem menção a mudanças |
| Board de tracking (Cowork) prático | 5 módulos com status visual, filtráveis, com responsável | Tabela estática |
| Referencia Anexo C | Specs seguem a estrutura de diretórios do repositório | Estrutura inventada inconsistente com Anexo C |

---

## Exercício 2.3 — Seção "Project Management Rules" do AGENTS.md

**Tópicos avaliados:** AGENTS.md (machine-readable), SDD (nomenclatura e rastreabilidade).

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Machine-readable | Regras prescritivas (DEVE/NÃO DEVE), parseáveis por agente | Texto narrativo, descritivo |
| Específico ao NovaTech | Referencia caminhos do repo (`/docs/adr/`), módulos do projeto | Genérico para qualquer projeto |
| Consistente com gates fornecidos | Validation gates do input simulado refletidos no AGENTS.md | Contradiz ou ignora os gates |
| Regras de nomenclatura concretas | Formato de título, labels obrigatórias, convenção de commit | "Nomear de forma clara" |
