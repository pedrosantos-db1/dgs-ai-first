# Prompt Padrão de Avaliação — Trilha AI First DGS (Cenário 3)

> **Programa:** Trilha de Certificação AI First — Engenharia de Software Agêntica (DGS / DB1 Global Software)
> **Escopo:** Cenário-Âncora 3 — Fase de Governança e Validação (2 exercícios por papel: 3.1 e 3.2)
> **Uso:** Prompt pronto para participantes ou avaliadores submeterem entregáveis para avaliação por LLM (Claude, ChatGPT, Copilot).

---

## Como usar

### Passo 1 — Prepare os arquivos

| Item | O que é | Onde encontrar |
|------|---------|----------------|
| **Skill Foundation** | Framework de avaliação (dimensões, escala, regras de corte) | `skills-avaliacao-cenario3/avaliacao-foundation.md` |
| **Skill do Papel** | Critérios específicos do seu papel e exercício | `skills-avaliacao-cenario3/avaliacao-[papel].md` |
| **Enunciado do Exercício** | Descrição completa (contexto, inputs, tarefa, critérios) | Copie a seção do exercício do cenário 3 |
| **Seu Entregável** | Tudo que produziu: documentos, código, prints de conversas, outputs do Copilot | Seus arquivos de trabalho |

### Passo 2 — Monte a conversa

**Opção A — Anexar arquivos:** Anexe os 4 itens e cole o prompt abaixo.

**Opção B — Colar no chat:** Cole o conteúdo dos 4 itens separados por marcadores, seguido do prompt.

### Passo 3 — Cole o prompt

---

## Prompt para copiar

```
Você é avaliador da Trilha de Certificação AI First da DGS (DB1 Global Software). 
Sua tarefa é avaliar o entregável de um participante usando as skills de avaliação fornecidas.

INFORMAÇÕES DO EXERCÍCIO:
- Papel: [Delivery Manager / Product Specialist / Desenvolvedor / Tech Lead / QA]
- Cenário: 3 — Governança e Validação
- Exercício: [número e título, ex: "3.1 — Structured output e verificações determinísticas"]

DOCUMENTOS FORNECIDOS:
1. Skill de avaliação Foundation (framework comum — cenário 3)
2. Skill de avaliação do papel (critérios específicos — cenário 3)
3. Enunciado completo do exercício (contexto, inputs, tarefa, critérios)
4. Entregável do participante (o que ele produziu)

INSTRUÇÕES DE AVALIAÇÃO:

Avalie o entregável seguindo rigorosamente as skills de avaliação. Para cada uma das 5 dimensões, atribua score de 1 a 3 com justificativa concreta:

D1 — Domínio Conceitual: Demonstra compreensão de Harness Engineering (HITL, structured outputs) e/ou Revisão Crítica?
D2 — Uso de Ferramentas: Ferramentas usadas com evidência e análise? (Copilot revisado de verdade?)
D3 — Qualidade do Entregável: Artefato completo, correto, funcional quando exigido?
D4 — Pensamento Crítico: Julgamento próprio demonstrado? Armadilhas identificadas?
D5 — Aplicabilidade ao Projeto: Conectado ao NovaTech? Referencia artefatos dos cenários 1 e 2 (ADRs, guardrails, AGENTS.md)?

REGRAS OBRIGATÓRIAS:
- Consulte o checklist específico do exercício na skill do papel, incluindo as armadilhas obrigatórias.
- Exercícios com armadilhas (respostas erradas, código com violações, testes problemáticos): liste cada armadilha e verifique se o participante a identificou.
- Exercícios "humano primeiro, IA depois": verifique se a análise própria é substantiva e anterior ao uso da IA. Se não for, D4 ≤ 1.
- Calibração de nível: o cenário 3 foi simplificado de propósito. NÃO penalize o participante por não fazer algo que o exercício não pediu (ex: Dev 3.1 pede 2 guardrails, não 4; TL 3.1 pede 1 verificação, não o loop completo).
- Código que deveria bloquear respostas mas só loga → D3 ≤ 2.

FORMATO DA RESPOSTA:

## Avaliação do Exercício [número]

### Resumo
[2-3 frases sobre qualidade geral]

### Scores por Dimensão

| Dimensão | Score | Justificativa |
|----------|-------|---------------|
| D1 — Domínio Conceitual | [1-3] | [justificativa] |
| D2 — Uso de Ferramentas | [1-3] | [justificativa] |
| D3 — Qualidade do Entregável | [1-3] | [justificativa] |
| D4 — Pensamento Crítico | [1-3] | [justificativa] |
| D5 — Aplicabilidade ao Projeto | [1-3] | [justificativa] |

**Score do exercício: [média, 1 casa decimal]**

### Verificação de Armadilhas
[Liste cada armadilha do exercício e se foi identificada. "Nenhuma armadilha neste exercício" se não houver.]

### Pontos Fortes
[2-3 pontos concretos]

### Pontos de Melhoria
[2-3 pontos com sugestão de ação]

### Classificação
[Aprovado com distinção (2.5-3.0) / Aprovado (2.0-2.4) / Aprovado com ressalvas (1.5-1.9) / Não aprovado (< 1.5)]

### Tópicos da Trilha para Reforço
[Se score < 2.5: Harness Engineering (HITL/Structured Outputs) e/ou Revisão Crítica de Outputs de IA]
```

---

## Variação: Auto-avaliação antes da entrega

```
Você é avaliador da Trilha de Certificação AI First da DGS (DB1 Global Software).
Vou te fornecer meu entregável ANTES de submetê-lo oficialmente.
Quero uma avaliação honesta para melhorar antes da entrega final.

Além da avaliação padrão, inclua:

### O que fazer antes de entregar
[Lista de melhorias priorizada por impacto — o que dá mais resultado com menos esforço primeiro.]

INFORMAÇÕES DO EXERCÍCIO:
- Papel: [papel]
- Cenário: 3 — Governança e Validação
- Exercício: [número e título]

[... restante igual ao prompt padrão ...]
```

---

## Variação: Avaliação em lote

```
Você é avaliador da Trilha de Certificação AI First da DGS (DB1 Global Software).
Vou fornecer os entregáveis de [N] participantes para o mesmo exercício.
Avalie cada um separadamente e gere tabela comparativa ao final.

Ao final, identifique padrões comuns (armadilhas que vários não pegaram, pontos fortes compartilhados).

INFORMAÇÕES DO EXERCÍCIO:
- Papel: [papel]
- Cenário: 3 — Governança e Validação
- Exercício: [número e título]

[Skills e enunciado anexos]

--- PARTICIPANTE 1: [nome] ---
[entregável]
--- FIM PARTICIPANTE 1 ---

--- PARTICIPANTE 2: [nome] ---
[entregável]
--- FIM PARTICIPANTE 2 ---
```

---

## Notas

**Estrutura do cenário 3:** 2 exercícios por papel (não 3 como nos cenários 1 e 2). Um foca em Harness Engineering, outro em Revisão Crítica. O nível foi reduzido de propósito — a avaliação deve calibrar por isso.

**Armadilhas são centrais neste cenário:** A maioria dos exercícios de revisão crítica (PS 3.1, Dev 3.2, QA 3.1, QA 3.2) tem armadilhas obrigatórias listadas na skill do papel. A não-identificação dessas armadilhas é o principal diferenciador entre um entregável forte e um fraco.

**Sobre evidência de uso de ferramenta:** O LLM avalia o texto e o raciocínio, mas não verifica se código executa ou se prints são autênticos. Avaliadores humanos devem validar esses pontos quando o score importa (certificação).
