# Skill de Avaliação — Desenvolvedor (Cenário 1)

> **Programa:** Trilha de Certificação AI First — DGS / DB1 Global Software
> **Escopo:** Cenário-Âncora 1 — Fase de Entendimento e Contexto (exercícios 1.1, 1.2, 1.3)
> **Referência:** Usar com `avaliacao-foundation.md` para dimensões e escala.

**Perfil:** Opera na camada de implementação — análise técnica, prototipação, código, construção de pipelines. Usa IA como ferramenta de desenvolvimento (Copilot) mantendo julgamento técnico próprio. Entende RAG como sistema de engenharia de dados.

**Ferramentas esperadas:** Claude (chat) em todos; GitHub Copilot nos exercícios 1.2 (não) e 1.3 (sim).

---

## Exercício 1.1 — Análise de viabilidade técnica com fundamentos de LLM e engenharia de contexto

**Tópicos avaliados:** Fundamentos de IA (tokens, context window), Engenharia de Contexto (orçamento de atenção, lost in the middle), RAG (desafios de extração).

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Desafios por tipo de fonte | Cada tipo (PDFs tabelas, escaneados, wiki, planilhas) com desafio + estratégia específicos | "Converter tudo para texto" |
| Estimativa de tokens razoável | Cálculo mostra trabalho. Total na ordem de 8-15M tokens é razoável | Número sem cálculo, ou erro grosseiro |
| Orçamento de contexto | Calcula quantos chunks cabem (128K - ~2K system ≈ 126K úteis). Justifica número de chunks por query (5-10 é prático) | Sem análise, ou "usar todo o contexto" |
| Chunking justificado | Considera tipo de pergunta + lost in the middle + formato dos documentos | "512 tokens fixos" sem motivo |
| Iteração com Claude | Claude identificou pontos fracos; Dev incorporou | Sem iteração |

---

## Exercício 1.2 — Prototipação de prompt com engenharia de contexto

**Tópicos avaliados:** Engenharia de Prompt (system prompt), Engenharia de Contexto (estático vs dinâmico, anatomia do contexto).

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| System prompt específico | Identidade + regras + formato + instruções para chunks. Não genérico | "Você é um assistente útil" |
| Mapeamento estático/dinâmico | Estático (system prompt, guardrails) vs dinâmico (chunks, pergunta, tier, histórico). Com estimativa de tokens | Apenas "o prompt" sem decomposição |
| 3 perguntas testadas | Resultados reais documentados com evidência | Respostas inventadas |
| Iteração v1 → v2 | Melhoria concreta e verificável entre versões | V1 = V2 |

**Armadilha obrigatória:** Pergunta "prazo de devolução para carga perigosa" → resposta correta é "NÃO é elegível para devolução" (POL-001, seção 3.2). Se o system prompt v1 gera resposta errada e o Dev não identifica como falha → D4 ≤ 1.

---

## Exercício 1.3 — Construção de pipeline de RAG com ferramentas open-source

**Tópicos avaliados:** RAG (pipeline completo: ingestão, embedding, retrieval), Engenharia de Contexto (chunks como unidade de contexto).

**Exercício mais pesado da trilha. Peso maior em D3 (código funcional).**

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Pipeline funcional | Código roda: ingere documentos, gera embeddings, busca por similaridade, retorna chunks | Não roda, ou pseudocódigo |
| Chunking justificado | Explica tamanho/overlap escolhidos. Tabelas não cortadas | Chunking fixo sem justificativa |
| 5 testes com gabarito | Pergunta → chunks recuperados → comparação com Anexo B. Ao menos 3/5 corretos | < 3 testes, ou sem comparação |
| 2+ problemas reais | Derivados dos testes (chunk errado, tabela cortada, versões misturadas) | Problemas inventados |
| Copilot evidenciado | Prompts/completions do Copilot na geração do código | Sem evidência |

**Sobre stack:** Qualquer stack free é aceitável (ChromaDB, FAISS, Qdrant, Ollama). Se usou LangChain sem entender o que está abstraído → D1 ≤ 2.
