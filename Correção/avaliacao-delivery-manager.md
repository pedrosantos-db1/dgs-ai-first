# Skill de Avaliação — Delivery Manager (Cenário 3)

> **Programa:** Trilha de Certificação AI First — DGS / DB1 Global Software
> **Escopo:** Cenário-Âncora 3 — Fase de Governança e Validação (exercícios 3.1 e 3.2)
> **Referência:** Usar com `avaliacao-foundation.md` para dimensões e escala.

**Perfil:** Define critérios de go-live e observabilidade. Demonstra que entende o harness como sistema de governança e que sabe traduzir confiabilidade técnica em decisões de gestão.

**Ferramentas esperadas:** Claude (chat) + Claude Cowork em ambos.

---

## Exercício 3.1 — Critérios de go-live com harness de governança

**Tópico:** Harness Engineering

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Organizado pelas 5 camadas | Cada camada (orchestration, verification, context, guardrails, observability) tem critério específico | Lista genérica sem organização por camada |
| Bloqueante vs desejável | Distinção pragmática (ex: "coverage 75% bloqueante, 80% desejável") | Tudo bloqueante, ou tudo desejável |
| Ponto de HITL concreto | Define quais decisões exigem humano (ex: baixa confiança sobre carga perigosa) | "Ter supervisão humana" sem especificar |
| Dashboard (Cowork) | Verde/amarelo/vermelho, responsável, data-alvo | Tabela sem status visual |
| Plano de rollback | Trigger + responsável + ação | "Avaliar a situação" |

---

## Exercício 3.2 — Plano de observabilidade e melhoria contínua

**Tópico:** Revisão Crítica (aplicada a monitoramento)

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| 4 dimensões de métricas | Uso, qualidade, técnicas, conteúdo — todas presentes | Apenas técnicas (latência, uptime) |
| Alertas com thresholds | "Se feedback negativo > 15% em 24h, notificar" | "Monitorar se piora" |
| Feedback loop completo | Do atendente → investigação → correção no assistente | Feedback coletado sem ação definida |
| Template de relatório (Cowork) | Executivo entende em 2 min, mostra tendência (melhorou/piorou) | Relatório técnico denso ou ausente |
