# Prompt Padrão de Avaliação — Trilha AI First DGS (Cenário 2)

> **Programa:** Trilha de Certificação AI First — Engenharia de Software Agêntica (DGS / DB1 Global Software)
> **Escopo:** Cenário-Âncora 2 — Fase de Estruturação do Trabalho (exercícios 2.1, 2.2, 2.3 de cada papel)
> **Uso:** Prompt pronto para participantes ou avaliadores submeterem entregáveis para avaliação por LLM (Claude, ChatGPT, Copilot).

---

## Como usar

### Passo 1 — Prepare os arquivos

| Item | O que é | Onde encontrar |
|------|---------|----------------|
| **Skill Foundation** | Framework de avaliação (dimensões, escala, regras de corte) | `skills-avaliacao-cenario2/avaliacao-foundation.md` |
| **Skill do Papel** | Critérios específicos do seu papel e exercício | `skills-avaliacao-cenario2/avaliacao-[papel].md` |
| **Enunciado do Exercício** | Descrição completa (contexto, inputs, tarefa, critérios) | Copie a seção do exercício do cenário 2 |
| **Seu Entregável** | Tudo que produziu: documentos, código, configs, prints de conversas, outputs do Copilot | Seus arquivos de trabalho |

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
- Cenário: 2 — Estruturação do Trabalho
- Exercício: [número e título, ex: "2.1 — Recorte de domínio e spec SDD"]

DOCUMENTOS FORNECIDOS:
1. Skill de avaliação Foundation (framework comum — cenário 2)
2. Skill de avaliação do papel (critérios específicos — cenário 2)
3. Enunciado completo do exercício (contexto, inputs, tarefa, critérios)
4. Entregável do participante (o que ele produziu)

INSTRUÇÕES DE AVALIAÇÃO:

Avalie o entregável seguindo rigorosamente as skills de avaliação. Para cada uma das 5 dimensões, atribua score de 1 a 3 com justificativa concreta:

D1 — Domínio Conceitual: Demonstra compreensão de MCP, SDD, AGENTS.md e/ou Skills?
D2 — Uso de Ferramentas: Ferramentas usadas com evidência e iteração? (Copilot testado de verdade?)
D3 — Qualidade do Entregável: Artefato completo, correto, machine-readable quando exigido?
D4 — Pensamento Crítico: Julgamento próprio demonstrado? Limitações dos agentes reconhecidas?
D5 — Aplicabilidade ao Projeto: Conectado ao NovaTech? Referencia ADRs e decisões do cenário 1?

REGRAS OBRIGATÓRIAS:
- Consulte o checklist específico do exercício na skill do papel.
- Exercícios que pedem execução real — teste com Copilot (TL 2.1/2.3), MCP servers locais no ar (Dev 2.1) e health check (TL 2.2): verificar a evidência (geração/avaliação/iteração; ou agente lendo doc/chunk/git; ou saída do health check). Sem evidência → D2 ≤ 1.
- Exercícios que pedem iteração (v1 → v2): verificar diferença concreta entre versões. V1 ≈ V2 → D2 ≤ 1.
- AGENTS.md ou skills narrativos em vez de prescritivos → D3 ≤ 1.
- Artefatos que ignoram decisões do cenário 1 (ADRs, context budget) → D5 ≤ 2.

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

### Verificação de Artefatos Machine-Readable
[Para exercícios de AGENTS.md e skills: o artefato é prescritivo? Um agente conseguiria seguir? Cite exemplos do que está bom e do que é narrativo demais.]

### Pontos Fortes
[2-3 pontos concretos]

### Pontos de Melhoria
[2-3 pontos com sugestão de ação]

### Classificação
[Aprovado com distinção (2.5-3.0) / Aprovado (2.0-2.4) / Aprovado com ressalvas (1.5-1.9) / Não aprovado (< 1.5)]

### Tópicos da Trilha para Reforço
[Se score < 2.5: quais tópicos revisitar — MCP, SDD, AGENTS.md, Skills]
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

### Checklist de prescritividade (para exercícios de AGENTS.md/skills)
[Revise cada regra/instrução do artefato e classifique: prescritiva (agente segue) ou narrativa (agente ignora). Sugira reescrita para as narrativas.]

INFORMAÇÕES DO EXERCÍCIO:
- Papel: [papel]
- Cenário: 2 — Estruturação do Trabalho
- Exercício: [número e título]

[... restante igual ao prompt padrão ...]
```

---

## Variação: Avaliação em lote

```
Você é avaliador da Trilha de Certificação AI First da DGS (DB1 Global Software).
Vou fornecer os entregáveis de [N] participantes para o mesmo exercício.
Avalie cada um separadamente e gere tabela comparativa ao final.

Ao final, identifique:
- Padrões comuns (erros recorrentes, pontos fortes compartilhados)
- Se algum artefato de AGENTS.md/skill é narrativo em vez de prescritivo (problema mais comum neste cenário)

INFORMAÇÕES DO EXERCÍCIO:
- Papel: [papel]
- Cenário: 2 — Estruturação do Trabalho
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

**Diferença principal vs cenário 1:** O cenário 2 produz artefatos que serão consumidos por agentes (AGENTS.md, skills, `.mcp/mcp.json`, specs SDD). A avaliação precisa verificar não apenas se o conteúdo está correto, mas se está em formato que um agente consegue processar. A seção "Verificação de Artefatos Machine-Readable" no formato de resposta existe por isso.

**Sobre evidência de execução real:** Vários exercícios exigem evidência de que algo de fato rodou — TL 2.1 e TL 2.3 (teste com Copilot), Dev 2.2 (revisão do código gerado), Dev 2.1 (MCP servers locais no ar: o agente lendo um doc de `docs/novatech/`, recuperando um chunk e lendo o git) e TL 2.2 (health check executado, com saída). A evidência pode ser screenshots, exports de chat ou transcrição/saída de terminal. Sem evidência, o avaliador humano deve questionar — o LLM não tem como verificar autenticidade de prints.
