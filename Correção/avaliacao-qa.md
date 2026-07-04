# Skill de Avaliação — QA (Cenário 3)

> **Programa:** Trilha de Certificação AI First — DGS / DB1 Global Software
> **Escopo:** Cenário-Âncora 3 — Fase de Governança e Validação (exercícios 3.1 e 3.2)
> **Referência:** Usar com `avaliacao-foundation.md` para dimensões e escala.

**Perfil:** Aplica revisão crítica sistemática a respostas do assistente e a testes gerados por IA. Demonstra que sabe avaliar qualidade de IA com rubrica consistente e identificar testes que dão falsa segurança.

**Ferramentas esperadas:** Claude (chat) em ambos; Claude Cowork no 3.1.

---

## Exercício 3.1 — Revisão crítica das respostas do assistente

**Tópico:** Revisão Crítica de Outputs de IA

### Armadilhas obrigatórias (verificar no Anexo A)

| Resposta | Avaliação correta | Se não identificou |
|----------|-------------------|--------------------|
| **#6 — Frete sem destino** | **Reprovada.** Assumiu "Sudeste" sem o atendente informar o destino. | D4 ≤ 2 |
| **#8 — Idioma** | **Reprovada.** Respondeu em inglês quando deveria ser português (guardrail de idioma). | D4 ≤ 2 |

As respostas 1, 2, 3, 4, 5 e 7 devem ser avaliadas como aprovadas (incluindo a #4, que reconhece corretamente que o tier não existe, e a #7, que recusa pergunta fora de escopo).

### Critérios

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Avaliação própria ANTES do Claude | Identifica as reprovações #6 e #8 de forma independente | Análise própria não identifica reprovações |
| Rubrica aplicada consistentemente | Mesma régua para as 8 respostas; scores comparáveis | Respostas similares com scores divergentes |
| Relatório (Cowork) | Score médio, reprovações com motivo, parecer de go-live | Apenas lista de scores |
| Parecer de go-live fundamentado | Baseado nos dados, pragmático (nem "perfeito" nem "vai assim") | Parecer sem fundamentação |

---

## Exercício 3.2 — Revisão crítica dos testes gerados por IA

**Tópico:** Revisão Crítica de Outputs de IA

### Armadilhas obrigatórias nos 3 testes

| Teste | Problema | Se não identificou |
|-------|----------|--------------------|
| **#1 — assertions vagas** | `toBeDefined()` testa existência, não correção. Não verifica se a resposta está CERTA. | D4 ≤ 2 |
| **#2 — dados irreais** | Edge case de input vazio é válido, mas nenhum teste exercita o domínio (pergunta real de logística). | D4 ≤ 2 |
| **#3 — mock que mascara bug** | Mock tão permissivo que o teste passa mesmo se a validação de input não existir. | D4 ≤ 1 |

**Ponto de atenção:** Os testes usam `jest` (spyOn, fn, mock), mas o projeto usa **Vitest** (ver Anexo C / AGENTS.md). Identificar essa inconsistência demonstra atenção ao contexto, não só ao código isolado.

### Critérios

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Análise própria ANTES do Claude | Identifica os 3 problemas principais independentemente | Análise vazia |
| Inconsistência jest/Vitest | Identificada (ponto extra de atenção ao contexto) | Não notada (não bloqueia score 3 se o resto estiver forte) |
| Teste 1 reescrito | Verifica conteúdo da resposta (ex: contém o prazo correto + cita fonte), não apenas que existe | Reescrita ainda com assertion vaga |
| Comparação com Claude honesta | Reconhece o que cada um encontrou | "Concordamos em tudo" |
