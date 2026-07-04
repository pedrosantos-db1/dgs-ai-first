# Skill de Avaliação — Tech Lead (Cenário 3)

> **Programa:** Trilha de Certificação AI First — DGS / DB1 Global Software
> **Escopo:** Cenário-Âncora 3 — Fase de Governança e Validação (exercícios 3.1 e 3.2)
> **Referência:** Usar com `avaliacao-foundation.md` para dimensões e escala.

**Perfil:** Projeta o harness do projeto e revisa riscos de artefatos gerados por IA. Demonstra visão de sistema (5 camadas) e julgamento sobre o que é seguro levar a produção.

**Ferramentas esperadas:** Claude (chat) em ambos; GitHub Copilot no 3.1.

---

## Exercício 3.1 — Design do harness do projeto

**Tópico:** Harness Engineering

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| 5 camadas cobertas | Orchestration, verification, context & memory, guardrails, observability — cada uma com o que tem / falta / como fechar | Falta mais de 1 camada |
| Context & memory conecta à ADR-0002 | Reconhece o context budget definido no cenário 1, não reinventa | Reinventa a estratégia de contexto |
| Guardrails mencionam structured outputs + HITL | Indica onde structured output entra e ao menos 1 ponto de HITL | Sem menção a structured output ou HITL |
| Função de verificação implementada | Checa se source_document está na lista de docs válidos (identificadores curtos: POL-001, etc.). Funcional, com Copilot | Apenas descrita, não implementada |
| Concretude | Prescreve implementações, não descreve conceitos | "Adicionar verificações" sem dizer quais |

**Nota de calibração:** A versão reduzida pede UMA verificação simples (fonte na lista), não o verification loop completo. Não penalizar por não implementar schema + lookup table + confidence score + roteamento HITL.

---

## Exercício 3.2 — Revisão crítica da arquitetura gerada com IA

**Tópico:** Revisão Crítica de Outputs de IA

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Skills sem refinamento = risco | Identifica que as 2 skills não testadas podem gerar outputs inconsistentes | Não identifica |
| Prompt sem changelog = risco de governança | 6 iterações sem documentação = impossível rollback informado | Não identifica |
| Análise própria ANTES do Claude | Avaliação de riscos independente, por artefato | Análise vazia |
| Priorização pragmática | Foca nas verificações de maior impacto nas 2 semanas; aceita risco residual explícito | Quer verificar tudo, ou não prioriza |
| Comparação com Claude honesta | Reconhece riscos adicionais que o Claude levantou | "Já sabia tudo" |
