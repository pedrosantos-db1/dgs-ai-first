# Prompt Padrão de Avaliação — Trilha AI First DGS

> **Programa:** Trilha de Certificação AI First — Engenharia de Software Agêntica (DGS / DB1 Global Software)
> **O que é:** Prompt pronto para ser usado por participantes ou avaliadores da trilha. Permite que um LLM (Claude, ChatGPT, Copilot, ou outro) avalie os entregáveis dos exercícios práticos usando as skills de avaliação como referência.
> **Versão atual:** Cenário-Âncora 1 — Fase de Entendimento e Contexto (exercícios 1.1, 1.2, 1.3 de cada papel). As skills de avaliação para cenários 2 e 3 estão em versão preliminar e serão finalizadas após revisão.

---

## Como usar

### Passo 1 — Prepare os arquivos

Você vai precisar de 4 itens para cada avaliação:

| Item | O que é | Onde encontrar |
|------|---------|----------------|
| **Skill Foundation** | Framework comum de avaliação (dimensões, escala, regras) | `skills-avaliacao/avaliacao-foundation.md` |
| **Skill do Papel** | Critérios específicos para o seu papel e exercício | `skills-avaliacao/avaliacao-[papel].md` |
| **Enunciado do Exercício** | A descrição completa do exercício (contexto, inputs, tarefa, critérios) | Copie a seção do exercício do cenário correspondente |
| **Seu Entregável** | Tudo que você produziu: documentos, código, prints de conversas, histórico de iteração | Seus arquivos de trabalho |

### Passo 2 — Monte a conversa

**Opção A — Anexar arquivos (Claude, ChatGPT com upload):**
Anexe os 4 itens como arquivos e cole o prompt abaixo.

**Opção B — Colar no chat (qualquer LLM):**
Cole o conteúdo dos 4 itens diretamente no chat, separados por marcadores claros, seguido do prompt abaixo.

### Passo 3 — Cole o prompt

Use o prompt da seção "Prompt para copiar" abaixo, preenchendo os campos entre colchetes.

---

## Prompt para copiar

```
Você é avaliador da Trilha de Certificação AI First da DGS (DB1 Global Software). 
Sua tarefa é avaliar o entregável de um participante usando as skills de avaliação fornecidas.

INFORMAÇÕES DO EXERCÍCIO:
- Papel: [Delivery Manager / Product Specialist / Desenvolvedor / Tech Lead / QA]
- Cenário: 1 — Entendimento e Contexto
- Exercício: [número e título, ex: "1.1 — Avaliação de viabilidade com fundamentos de IA"]

DOCUMENTOS FORNECIDOS:
1. Skill de avaliação Foundation (framework comum)
2. Skill de avaliação do papel (critérios específicos)
3. Enunciado completo do exercício (contexto, inputs, tarefa, critérios)
4. Entregável do participante (o que ele produziu)

INSTRUÇÕES DE AVALIAÇÃO:

Avalie o entregável seguindo rigorosamente as skills de avaliação. Para cada uma das 5 dimensões abaixo, atribua um score de 1 a 3 com justificativa concreta baseada no entregável:

D1 — Domínio Conceitual: O participante demonstra compreensão real dos tópicos da trilha?
D2 — Uso de Ferramentas: As ferramentas foram usadas de forma efetiva, com evidência e iteração?
D3 — Qualidade do Entregável: O artefato é completo, correto e utilizável?
D4 — Pensamento Crítico: O participante demonstrou julgamento próprio, não apenas delegação para IA?
D5 — Aplicabilidade ao Projeto: O entregável faz sentido no contexto do projeto NovaTech?

REGRAS OBRIGATÓRIAS:
- Consulte o checklist específico do exercício na skill do papel. Cada critério deve ser verificado.
- Se o exercício tem armadilhas intencionais (respostas erradas, código com violações, tiers inexistentes), verifique explicitamente se o participante as identificou. Liste cada armadilha e se foi encontrada.
- Se o exercício usa o padrão "humano primeiro, IA depois", verifique se a análise humana é substantiva e anterior ao uso da IA. Se não for, D4 ≤ 1.
- Se o exercício pede iteração (v1 → v2), verifique se há diferença concreta entre versões. Se v1 ≈ v2, D2 ≤ 1.

FORMATO DA RESPOSTA:

## Avaliação do Exercício [número]

### Resumo
[2-3 frases sobre a qualidade geral do entregável]

### Scores por Dimensão

| Dimensão | Score | Justificativa |
|----------|-------|---------------|
| D1 — Domínio Conceitual | [1-3] | [justificativa concreta] |
| D2 — Uso de Ferramentas | [1-3] | [justificativa concreta] |
| D3 — Qualidade do Entregável | [1-3] | [justificativa concreta] |
| D4 — Pensamento Crítico | [1-3] | [justificativa concreta] |
| D5 — Aplicabilidade ao Projeto | [1-3] | [justificativa concreta] |

**Score do exercício: [média das 5 dimensões, 1 casa decimal]**

### Verificação de Armadilhas
[Lista cada armadilha do exercício e se foi identificada. "Nenhuma armadilha neste exercício" se não houver.]

### Pontos Fortes
[O que o participante fez bem — 2-3 pontos concretos]

### Pontos de Melhoria
[O que precisa melhorar — 2-3 pontos concretos com sugestão de ação]

### Classificação
[Aprovado com distinção (2.5-3.0) / Aprovado (2.0-2.4) / Aprovado com ressalvas (1.5-1.9) / Não aprovado (< 1.5)]

### Tópicos da Trilha para Reforço
[Se score < 2.5, liste quais tópicos da trilha AI First o participante deveria revisitar, baseado nos gaps identificados]
```

---

## Exemplo de uso completo

Abaixo, um exemplo de como a conversa ficaria na prática. O participante (um QA) está pedindo avaliação do exercício 1.2 do cenário-âncora 1 (Fase de Entendimento e Contexto).

```
[Participante cola ou anexa: avaliacao-foundation.md]
[Participante cola ou anexa: avaliacao-qa.md]
[Participante cola ou anexa: seção do exercício 1.2 do cenário-âncora 1]

Você é avaliador da Trilha de Certificação AI First da DGS (DB1 Global Software). 
Sua tarefa é avaliar o entregável de um participante usando as skills de avaliação fornecidas.

INFORMAÇÕES DO EXERCÍCIO:
- Papel: QA
- Cenário: 1 — Entendimento e Contexto
- Exercício: 1.2 — Design de critérios de aceitação para respostas de IA

DOCUMENTOS FORNECIDOS:
1. Skill de avaliação Foundation (framework comum)
2. Skill de avaliação do QA (critérios específicos)
3. Enunciado completo do exercício 1.2
4. Meu entregável (abaixo)

[... restante do prompt padrão ...]

--- INÍCIO DO MEU ENTREGÁVEL ---

[Avaliação manual das 5 respostas]
[Rubrica criada com o Claude]
[Template gerado pelo Cowork]
[Pontuações aplicadas]
[Histórico de conversa com o Claude - prints/exports]

--- FIM DO MEU ENTREGÁVEL ---
```

---

## Variação: Avaliação em lote (para avaliadores/mentores)

Se você é mentor ou coordenador e precisa avaliar múltiplos participantes, use esta variação:

```
Você é avaliador da Trilha de Certificação AI First da DGS (DB1 Global Software).
Vou fornecer os entregáveis de [N] participantes para o mesmo exercício.
Avalie cada um separadamente usando as skills fornecidas.

Ao final, gere uma tabela comparativa com os scores dos [N] participantes 
e identifique padrões comuns (erros recorrentes, pontos fortes compartilhados).

INFORMAÇÕES DO EXERCÍCIO:
- Papel: [papel]
- Cenário: [cenário]
- Exercício: [número e título]

[Skills e enunciado anexos]

--- PARTICIPANTE 1: [nome] ---
[entregável]
--- FIM PARTICIPANTE 1 ---

--- PARTICIPANTE 2: [nome] ---
[entregável]
--- FIM PARTICIPANTE 2 ---

[...]
```

---

## Variação: Auto-avaliação antes da entrega

Participantes podem usar este prompt para se auto-avaliar antes de submeter o entregável:

```
Você é avaliador da Trilha de Certificação AI First da DGS (DB1 Global Software).
Vou te fornecer meu entregável ANTES de submetê-lo oficialmente.
Quero uma avaliação honesta para que eu possa melhorar antes da entrega final.

Além da avaliação padrão nas 5 dimensões, inclua uma seção adicional:

### O que fazer antes de entregar
[Lista concreta de melhorias que elevariam o score. Priorizada: o que dá mais impacto com menos esforço primeiro.]

INFORMAÇÕES DO EXERCÍCIO:
- Papel: [papel]
- Cenário: [cenário]  
- Exercício: [número e título]

[... restante do prompt padrão ...]
```

---

## Notas importantes

**Sobre o modelo usado para avaliação:** O prompt funciona em Claude, ChatGPT, Copilot ou qualquer LLM com janela de contexto suficiente (~50K tokens para acomodar as 2 skills + enunciado + entregável). Para entregáveis que incluem código extenso ou muitos prints, pode ser necessário resumir as evidências.

**Sobre limitações da avaliação por IA:** O LLM avalia o texto e o raciocínio, mas não pode verificar se código realmente executa, se prints são autênticos, ou se a análise humana foi genuinamente feita antes da IA. Avaliadores humanos devem validar esses pontos quando o score importa (aprovação/certificação).

**Sobre consistência entre avaliadores:** Se múltiplos avaliadores (humanos ou IA) avaliarem o mesmo entregável, scores podem variar ±0.3 pontos. Divergências maiores indicam ambiguidade na rubrica — reportar para revisão das skills.
