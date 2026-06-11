# Skill de Avaliação — Delivery Manager (Cenário 1)

> **Programa:** Trilha de Certificação AI First — DGS / DB1 Global Software
> **Escopo:** Cenário-Âncora 1 — Fase de Entendimento e Contexto (exercícios 1.1, 1.2, 1.3)
> **Referência:** Usar com `avaliacao-foundation.md` para dimensões e escala.

**Perfil:** Opera na camada de gestão — viabilidade, comunicação com cliente, planejamento. Deve entender conceitos técnicos o suficiente para tomar decisões de gestão informadas.

**Ferramentas esperadas:** Claude (chat) em todos; Claude Cowork nos exercícios 1.2 e 1.3.

---

## Exercício 1.1 — Avaliação de viabilidade com fundamentos de IA

**Tópicos avaliados:** Fundamentos de IA Generativa, Engenharia de Contexto (context rot).

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Riscos específicos de IA | Exemplo concreto do domínio (ex: PROC-042 vs v2 mistura multiplicadores) | Riscos genéricos: "a IA pode errar" |
| Risco de contexto presente | Ao menos 1 risco sobre context rot ou volume de docs vs capacidade do modelo | Nenhuma menção a contexto |
| Mitigações acionáveis | Ação concreta com responsável implícito para cada risco | "Monitorar", "ter cuidado" |
| Perguntas ao Tech Lead | Revelam que RAG depende de dados, não só de modelo | "Quanto tempo vai levar?" |
| Iteração com Claude | Ao menos 2 rodadas de refinamento no histórico | Prompt único, output aceito integralmente |

**Armadilhas:** Nenhuma intencional. Avaliar pela profundidade.

---

## Exercício 1.2 — Comunicação de expectativas com o cliente

**Tópicos avaliados:** Fundamentos de IA Generativa (explicar para não-técnicos), RAG (conceito simplificado).

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Linguagem acessível | Analogias sem jargão ("tokens", "embeddings" não aparecem no e-mail) | Texto técnico para executivo |
| RAG correto | Assistente busca em documentos, não "sabe" ou "aprende" | Implica que assistente "entende" |
| Critérios de sucesso mensuráveis | Números (% respostas com fonte, tempo médio) | "Funcionar bem" |
| One-pager (Cowork) | Executivo entende em 2 min, com hierarquia visual | Texto corrido ou ausente |
| Tom equilibrado | Valida entusiasmo sem prometer 100% de acerto | Pessimista demais ou otimista demais |

---

## Exercício 1.3 — Planejamento de discovery com IA

**Tópicos avaliados:** Fundamentos de IA (o que IA faz bem vs mal), AI Agents (preview).

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Separação agente vs humano | Agentes: catalogar, comparar, resumir. Humanos: validar, priorizar, decidir | Agentes fazendo tudo, ou sem papel claro |
| Sequência lógica | Intent (IA) → Discovery (humano) → Validação | Tudo em paralelo sem dependências |
| Cronograma realista | 2 semanas com atividades dimensionadas | 40+ atividades em 2 semanas |
| Requisitos ao cliente | O que a NovaTech fornece (acessos, pessoas) e quando | Sem dependências externas |
