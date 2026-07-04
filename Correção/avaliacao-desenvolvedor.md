# Skill de Avaliação — Desenvolvedor (Cenário 3)

> **Programa:** Trilha de Certificação AI First — DGS / DB1 Global Software
> **Escopo:** Cenário-Âncora 3 — Fase de Governança e Validação (exercícios 3.1 e 3.2)
> **Referência:** Usar com `avaliacao-foundation.md` para dimensões e escala.

**Perfil:** Implementa structured outputs e verificações determinísticas (harness de código), e revisa código gerado por IA. Demonstra que sabe transformar guardrails de produto em código que realmente bloqueia respostas ruins.

**Ferramentas esperadas:** Claude (chat) + GitHub Copilot em ambos.

---

## Exercício 3.1 — Structured output e verificações determinísticas

**Tópico:** Harness Engineering

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Schema de structured output | Schema Zod válido com campos obrigatórios (answer, source_document, confidence_score), tipos corretos | Schema ausente, ou sem validação Zod |
| Guardrail 1 (source_document) | Bloqueia de fato respostas sem fonte e retorna mensagem padrão | Apenas loga, não bloqueia |
| Guardrail 2 (carga perigosa + devolução) | Detecta a combinação e bloqueia se não houver negativa | Não implementado ou trivialmente burlável |
| Code review com Claude | Identifica 2+ problemas reais (ex: schema aceita campos extras, regex não cobre variações) e corrige | Problemas inventados, ou sem correção |
| Probabilístico vs determinístico | Demonstra que structured output + código (determinístico) complementam o prompt (probabilístico) | Confunde os conceitos |

**Nota de calibração:** A versão reduzida pede 2 guardrails (não 4) e code review "rápido". Não penalizar por não implementar lookup table de valores numéricos — isso não foi pedido.

---

## Exercício 3.2 — Revisão crítica de código gerado por IA

**Tópico:** Revisão Crítica de Outputs de IA

### Armadilhas obrigatórias no código simulado

| Violação | Tipo | Se não identificou |
|----------|------|--------------------|
| `as any` sem validação Zod | Violação AGENTS.md | D4 ≤ 2 |
| `console.log` em vez de pino | Violação AGENTS.md | D4 ≤ 2 |
| `require` dinâmico | Violação AGENTS.md | D4 ≤ 2 |
| `attendantEmail` (dado pessoal) logado | Problema de segurança | D4 ≤ 1 se não identificou |

**Para score 3 em D4:** identificar os 4 problemas na análise própria (antes do Claude).

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Análise própria ANTES do Claude | Identifica a maioria dos problemas independentemente | Análise própria vazia |
| Comparação humano vs Claude | Honesta sobre o que cada um encontrou | "Concordamos em tudo" |
| Código reescrito | Segue o AGENTS.md integralmente (Zod, pino, import estático, sem logar e-mail) | Reescrita ainda com violações |
