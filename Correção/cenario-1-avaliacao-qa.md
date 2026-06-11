# Skill de Avaliação — QA (Cenário 1)

> **Programa:** Trilha de Certificação AI First — DGS / DB1 Global Software
> **Escopo:** Cenário-Âncora 1 — Fase de Entendimento e Contexto (exercícios 1.1, 1.2, 1.3)
> **Referência:** Usar com `avaliacao-foundation.md` para dimensões e escala.

**Perfil:** Opera na camada de verificação — cenários de falha, critérios de aceite, planos de teste. Sabe testar sistemas de IA (não-determinísticos, graus de qualidade) e diferencia falhas de alucinação, contexto, guardrail e retrieval.

**Ferramentas esperadas:** Claude (chat) em todos; Claude Cowork nos exercícios 1.2 e 1.3.

---

## Exercício 1.1 — Identificação de cenários de falha de IA (incluindo falhas de contexto)

**Tópicos avaliados:** Fundamentos de IA (alucinação), Engenharia de Contexto (context rot, lost in the middle, chunk errado, overflow).

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| 10+ cenários em 5 categorias | Alucinação (3+), desatualizada/contraditória (2+), falha de contexto (3+), recusa inadequada (1+), falha de guardrail (1+) | < 8 cenários ou categorias faltantes |
| Específicos ao domínio | "Pergunta sobre SLA Platinum → inventa tier" (específico) | "IA pode errar" (genérico) |
| Categoria "falha de contexto" | Ex: "5ª pergunta na sessão Teams ignora chunks e usa histórico" (context rot) | Categoria ausente ou rasa |
| Análise própria ANTES do Claude | Lista inicial com ao menos 4 cenários substanciais | Lista vazia ou idêntica à do Claude |
| Verificação automatizável | Ao menos 5 cenários com proposta de automação | Apenas verificação manual |

---

## Exercício 1.2 — Design de critérios de aceitação para respostas de IA

**Tópicos avaliados:** Fundamentos de IA (alucinação), Revisão Crítica (avaliar outputs).

### Armadilhas obrigatórias

| Resposta | Avaliação correta | Se não identificou |
|----------|-------------------|--------------------|
| **#3 — SLA Platinum** | **Incorreta.** Tier Platinum não existe na SLA-2024 (só Gold/Silver/Standard). Assistente alucionou tier E valores. | D4 = 1 |
| **#4 — Devolução carga perigosa** | **Incorreta.** POL-001 seção 3.2: cargas perigosas NÃO são elegíveis. Assistente inverteu a regra. | D4 = 1 |

A justificativa deve referenciar documentos específicos do Anexo A. Sem referência → D5 ≤ 2.

### Critérios adicionais

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Avaliação própria ANTES da rubrica | 5 respostas avaliadas com justificativa baseada no Anexo A | Feita após a rubrica |
| Rubrica com 4 dimensões, escala 1-3 | Cada nível descrito concretamente. Dois QAs chegariam a scores similares | Escala binária ou dimensões vagas |
| Respostas 1, 2 e 5 | Corretamente avaliadas como corretas (#1 devolução, #2 frete Manaus v2, #5 multiplicador Sudeste) | Erro em respostas corretas |
| Template (Cowork) reutilizável | Funciona para qualquer lote de respostas, não só estas 5 | One-off ou ausente |

---

## Exercício 1.3 — Plano de testes para pipeline de RAG

**Tópicos avaliados:** RAG (pipeline por etapas), Engenharia de Contexto (testes de contexto).

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| 6 categorias de teste | Ingestão, retrieval, geração, contexto, ponta a ponta, regressão | Falta > 1 categoria |
| Retrieval com dados do Anexo B | 5+ pares pergunta → chunk esperado do mapa de cobertura | Perguntas genéricas |
| Testes de contexto | Context rot em sessões longas, lost in the middle, orçamento | Categoria ausente |
| Testes não-binários | Graus de qualidade (parcialmente correto ≠ totalmente errado) | Tudo pass/fail |
| Artefato (Cowork) prático | Checklist com categorias, status, responsável. Reutilizável | Documento estático |
