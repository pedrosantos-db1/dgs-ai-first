# Skill de Avaliação — Product Specialist (Cenário 3)

> **Programa:** Trilha de Certificação AI First — DGS / DB1 Global Software
> **Escopo:** Cenário-Âncora 3 — Fase de Governança e Validação (exercícios 3.1 e 3.2)
> **Referência:** Usar com `avaliacao-foundation.md` para dimensões e escala.

**Perfil:** Avalia respostas do assistente do ponto de vista de produto e projeta o harness de evolução. Demonstra revisão crítica aplicada e compreensão de como o produto melhora sem degradar.

**Ferramentas esperadas:** Claude (chat) em ambos.

---

## Exercício 3.1 — Revisão crítica das respostas do assistente

**Tópico:** Revisão Crítica de Outputs de IA

### Armadilhas obrigatórias (verificar no Anexo A)

| Resposta | Avaliação correta | Se não identificou |
|----------|-------------------|--------------------|
| **#4 — Política de carga danificada** | **Alucinação.** Não existe documento formal sobre danos em transporte na base (ver "Gaps identificados" no Anexo A). Assistente inventou com confiança alta. | D4 ≤ 1 |
| **#6 — Carga perigosa + frete expresso** | **Fonte não confiável.** Vem do FAQ-Atendimento (informal, não validado). Informação sobre carga perigosa deveria vir de documento formal. | D4 ≤ 2 |

### Critérios

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Avaliação própria ANTES do Claude | Identifica as armadilhas #4 e #6 de forma independente | Análise própria ausente |
| Respostas corretas bem avaliadas | #1, #2, #3, #5 reconhecidas como adequadas | Erro em respostas corretas |
| Classificação do tipo de erro | Alucinação vs fonte não confiável vs incompleta — corretamente aplicada | Classificação genérica |
| Propostas de ajuste concretas | Para cada erro, ajuste específico (prompt, interface, pipeline) | "Melhorar o modelo" |
| Comparação com Claude honesta | Reconhece concordâncias e divergências | "Concordamos em tudo" |

---

## Exercício 3.2 — Harness de produto para melhoria contínua

**Tópico:** Harness Engineering

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Processo de feedback completo | Do atendente até a melhoria efetiva (novo doc / ajuste de prompt / reindexação) | Feedback coletado sem processo de correção |
| Regression testing de produto | Antes de mudar prompt/docs, verifica que respostas não pioraram E que guardrails do cenário 2 não regridem | Sem menção a regressão, ou ignora guardrails |
| Ponto de HITL | Define quais mudanças exigem aprovação humana e quem aprova | Sem HITL, ou vago |
| Preserva guardrails do cenário 2 | Reconhece os guardrails DEVE/NÃO DEVE/QUANDO EM DÚVIDA como invariantes a manter | Ignora os guardrails existentes |
