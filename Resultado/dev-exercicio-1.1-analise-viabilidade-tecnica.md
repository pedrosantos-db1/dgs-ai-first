# Exercício 1.1 — Análise de Viabilidade Técnica com Fundamentos de LLM e Engenharia de Contexto

**Papel:** Desenvolvedor  
**Exercício:** 1.1  
**Projeto:** Assistente de IA NovaTech — DB1  

---

## Parte 1 — Análise Técnica por Tipo de Fonte

### 1.1. PDFs com tabelas complexas (SharePoint — ~800 documentos)

**Desafio para o pipeline de RAG:**  
Tabelas com 15+ colunas perdem sua estrutura relacional ao serem convertidas para texto puro. Um extrator de PDF ingênuo (como PyMuPDF ou pdfminer) converte as células da tabela em sequências de tokens sem indicar qual cabeçalho se relaciona a qual valor. A tabela de multiplicadores regionais do PROC-042, por exemplo, vira texto linear como `"Sul 1.2 Sudeste 1.0 Centro-Oeste 1.3"` — o modelo pode inferir a relação corretamente em condições ideais, mas com tabelas maiores e mais complexas a taxa de erro sobe.

**Impacto na qualidade das respostas:**  
O modelo pode citar o multiplicador da região errada, misturar linhas de tabelas diferentes dentro do mesmo chunk, ou simplesmente não encontrar o chunk correto porque o embedding de texto linearizado tem baixa similaridade com a pergunta original ("qual o frete para Manaus?"). Isto afeta diretamente a precisão das respostas de frete — o caso de uso de maior volume (25% das consultas, conforme dados do projeto).

**Estratégia de tratamento:**  
Usar extração estruturada de tabelas via `camelot` ou `pdfplumber` para capturar a estrutura (linhas × colunas) e serializar em formato Markdown antes do chunking. Para tabelas críticas (multiplicadores de frete, SLAs), criar chunks dedicados com um cabeçalho descritivo explícito: `"Tabela de multiplicadores regionais do PROC-042-v2 (versão novembro/2023): Sul=1.3, Sudeste=1.1, ..."`. Isso aumenta a similaridade semântica com perguntas do usuário.

---

### 1.2. PDFs escaneados com necessidade de OCR (~15% da base ≈ 120 documentos)

**Desafio para o pipeline de RAG:**  
PDFs escaneados são imagens embutidas num container PDF. Nenhuma biblioteca de extração de texto convencional recupera o conteúdo — é necessário OCR (Optical Character Recognition) antes de qualquer chunking ou embedding. Documentos escaneados tendem a ter qualidade variável: fontes em carimbo, texto com inclinação, manchas e baixa resolução são comuns em documentação mais antiga.

**Impacto na qualidade das respostas:**  
OCR de baixa qualidade introduz erros silenciosos (ex: `"1.6"` vira `"l.6"`, `"500kg"` vira `"500 kg"`). Esses erros de caráter passam desapercebidos no pipeline mas degradam os embeddings — um chunk sobre frete Norte com valor `"l.8"` nunca será corretamente recuperado numa busca semântica sobre multiplicador Norte. A taxa de erro de OCR para documentos de logística (com tabelas numéricas) costuma ser de 3-8% mesmo com ferramentas modernas.

**Estratégia de tratamento:**  
Usar Azure AI Document Intelligence (anteriormente Form Recognizer) para OCR de alta precisão, especialmente para documentos com tabelas. Aplicar pós-processamento de validação: verificar se valores numéricos que aparecem frequentemente nos documentos (ex: multiplicadores conhecidos como 1.3, 1.8) estão presentes com formatting correto. Para documentos escaneados com qualidade abaixo de um limiar de confiança do OCR, sinalizar para revisão manual antes de ingestão.

---

### 1.3. Wiki do Confluence com links internos e macros customizadas

**Desafio para o pipeline de RAG:**  
A wiki exportada do Confluence contém macros de layout (`{panel}`, `{info}`, `{toc}`) que geram ruído no texto extraído — o parser produz strings como `"Panel title: Atenção Conteúdo: ..."` misturadas com o conteúdo real. Links internos (`[PROC-042|/wiki/spaces/OPS/pages/123]`) perdem a âncora de referência e ficam como texto literal. O maior risco é que o contexto de uma página depende de outras páginas linkadas que não serão ingeridas junto com ela.

**Impacto na qualidade das respostas:**  
Uma página da wiki pode dizer "consulte os SLAs na tabela de clientes" com um link interno — sem o destino do link no contexto, o modelo ou nega ter a informação ou alucina os valores. O ruído de macros aumenta o tamanho do chunk sem agregar significado semântico, diluindo a qualidade do embedding (efeito de "poluição semântica").

**Estratégia de tratamento:**  
Usar a API REST do Confluence para exportar páginas em formato Markdown estruturado, não o export HTML. Remover macros via pré-processamento com regex específicas para o dialeto Confluence. Para links internos, implementar resolução de referências no momento da ingestão: cada link é expandido com o título e um resumo da página de destino (máximo 100 tokens), criando auto-suficiência parcial do chunk. Versionar a ingestão junto com a data de exportação para rastreabilidade.

---

### 1.4. Planilhas com fórmulas interdependentes (pasta de rede — ~50 arquivos XLSX)

**Desafio para o pipeline de RAG:**  
Planilhas são estruturas bidimensionais com relações implícitas entre células — fórmulas como `=B2*VLOOKUP(C2,$G$1:$H$10,2)` encapsulam lógica de negócio que simplesmente desaparece quando a planilha é convertida para texto. O resultado calculado pode estar na planilha, mas o RAG vai indexar o valor estático do momento da ingestão, que fica obsoleto quando a tabela base é atualizada mensalmente.

**Impacto na qualidade das respostas:**  
A tabela de frete-base atualizada mensalmente (`frete-base-AAAAMM.xlsx`) alimenta os cálculos do PROC-042. Se o pipeline indexar apenas os valores calculados no momento da ingestão, as respostas de cálculo de frete ficarão desatualizadas após qualquer atualização mensal. Além disso, planilhas com múltiplas abas criam ambiguidade: qual aba é a fonte de verdade?

**Estratégia de tratamento:**  
Para planilhas de tabelas de referência (como multiplicadores e tarifas-base): extrair os dados via `openpyxl` e converter para tabelas Markdown com cabeçalhos explícitos, incluindo a data de extração no metadata do chunk. Configurar pipeline de re-ingestão automática mensal alinhado ao calendário de atualização da NovaTech (Comercial atualiza mensalmente). Para planilhas com lógica de cálculo: não tentar indexar as fórmulas — documentar os parâmetros de entrada e saída como texto estruturado, com nota indicando que o cálculo exato deve ser feito no sistema de fretes, não pelo assistente.

---

## Parte 2 — Estimativa do Tamanho da Base em Tokens

### Método de estimativa

Utilizando a regra prática fornecida: **~0.75 palavras por token** (ou inversamente, ~1.33 tokens por palavra), com estimativa de ~250 palavras por página de PDF.

### Cálculo por fonte

| Fonte | Quantidade | Tamanho médio | Total de palavras | Total de tokens (~1.33 tokens/palavra) |
|-------|-----------|---------------|------------------|----------------------------------------|
| PDFs SharePoint | 800 documentos | 10 páginas × 250 palavras = 2.500 palavras/doc | 2.000.000 palavras | **~2.660.000 tokens** |
| Wiki Confluence | 400 páginas | 1.500 palavras/página | 600.000 palavras | **~800.000 tokens** |
| Planilhas (dados tabulares) | 50 arquivos | ~500 palavras equivalentes/planilha (dados extraídos) | 25.000 palavras | **~33.000 tokens** |
| **TOTAL** | | | **~2.625.000 palavras** | **~3.493.000 tokens ≈ 3,5M tokens** |

### Interpretação

A base total estimada é de aproximadamente **3,5 milhões de tokens**. Isso é relevante para:

1. **Custo de ingestão (embedding):** Gerar embeddings para 3,5M tokens com o modelo `text-embedding-ada-002` (Azure OpenAI) custa aproximadamente USD 0,35 por ingestão completa (USD 0,10/1M tokens). Para re-ingestões mensais parciais (~10% da base atualizada), o custo é negligível.

2. **Impossibilidade de contexto completo:** A base total de 3,5M tokens é ~27x maior do que a janela de contexto do GPT-4o (128K tokens). **Nenhuma estratégia de "jogar tudo no prompt" é viável** — o RAG não é uma otimização, é uma necessidade arquitetural.

3. **Importância crítica do retrieval:** Se o pipeline recuperar apenas os 10-15 chunks mais relevantes por query (5.000-7.500 tokens), estará selecionando ~0,2% da base para cada pergunta. A qualidade do retrieval determina a qualidade da resposta.

---

## Parte 3 — Análise de Orçamento de Contexto

### Estrutura do contexto por query

| Componente | Tipo | Tokens estimados |
|-----------|------|-----------------|
| System prompt (identidade, guardrails, instruções de formato) | Estático | ~800 tokens |
| Metadados da sessão (tier do cliente, número do chamado) | Dinâmico por sessão | ~150 tokens |
| Histórico de conversa na sessão Teams | Dinâmico, crescente | 0 – 2.000 tokens |
| Chunks recuperados pelo retrieval | Dinâmico por query | variável |
| Pergunta do atendente | Dinâmico | ~50-150 tokens |
| Instrução de saída (formato da resposta) | Estático | ~200 tokens |
| **Overhead total (exceto chunks)** | | **~1.300–3.300 tokens** |

### Capacidade efetiva para chunks

Com a janela de 128K tokens do GPT-4o e overhead de ~2K tokens (caso médio):

- **Capacidade disponível para chunks:** 128.000 – 2.000 = **126.000 tokens**
- **Com chunks de 500 tokens:** cabem até **252 chunks** por query
- **Com chunks de 1.000 tokens:** cabem até **126 chunks** por query

Na prática, porém, **recuperar 252 chunks é contraproducente**. O efeito *lost in the middle* documentado na literatura (Liu et al., 2023) demonstra que modelos de linguagem processam com maior fidelidade informações no início e no final do contexto, com degradação significativa para informações posicionadas no meio. Em testes práticos, informações relevantes posicionadas entre os chunks 5 e 250 são frequentemente ignoradas ou distorcidas.

### Recomendação de orçamento de chunks

| Cenário | Chunks recomendados | Tokens de chunks | Justificativa |
|---------|--------------------|-----------------|-|
| Query simples (1 domínio) | 3-5 chunks | 1.500-2.500 tokens | Reduz lost-in-middle, resposta focada |
| Query multi-domínio | 6-10 chunks | 3.000-5.000 tokens | Cobre SLA + frete + devolução sem degradação |
| Query com documentos contraditórios | 4-6 chunks | 2.000-3.000 tokens | Inclui ambas as versões do PROC-042 com context explícito |

**Conclusão:** A estratégia de retrieval deve ser seletiva, não exaustiva. Recuperar os 5-7 chunks mais relevantes é melhor do que recuperar os 50 mais relevantes, mesmo que a janela comporte mais.

---

## Parte 4 — Recomendação de Estratégia de Chunking

### Tipo de pergunta que o atendente fará

Com base no cenário (35% prazos de entrega, 25% frete, 20% devoluções, 20% outros):

- **Perguntas factuais pontuais:** "Qual o multiplicador de frete para o Nordeste?" → precisam de 1-2 chunks pequenos e precisos
- **Perguntas de procedimento:** "Como o cliente abre uma solicitação de devolução?" → precisam de um chunk que capture um fluxo completo (3-5 etapas)
- **Perguntas de tabela:** "Qual o SLA do cliente Gold para incidente crítico?" → precisam do chunk que contém a linha correta da tabela
- **Perguntas multi-domínio:** "Meu cliente Gold quer devolver uma carga de 600kg para Manaus, qual o prazo e o custo?" → precisam de chunks de 3 domínios diferentes

### Estratégia recomendada: chunking semântico por seção com overlap

**Tamanho de chunk: 400-600 tokens por chunk**

Justificativa:
- Suficientemente pequeno para representar uma única ideia/regra (boa precisão de embedding)
- Suficientemente grande para incluir contexto imediato (ex: uma exceção junto com a regra principal)
- Compatível com recuperar 5-7 chunks dentro do orçamento de atenção recomendado

**Estratégia de divisão: por seção lógica (não por contagem fixa de tokens)**

Prefere-se dividir nos limites naturais do documento (seções, subseções, itens de lista numerada) em vez de cortar a cada 512 tokens fixos. Um corte fixo no meio de uma tabela de multiplicadores regionais quebra a unidade semântica — o chunk que começa na linha 3 da tabela não tem o cabeçalho e fica semanticamente ambíguo.

**Overlap: 10-15% entre chunks consecutivos (40-90 tokens)**

Justificativa para o efeito *lost in the middle*: quando uma informação está numa fronteira entre dois chunks (ex: uma exceção ao final de uma seção e a regra seguinte no início da próxima), o overlap garante que pelo menos um dos chunks recuperados contenha a informação completa. Sem overlap, o retrieval pode retornar o chunk "errado" e a resposta perde a exceção.

**Chunks especiais para tabelas: um chunk por tabela, com cabeçalho descritivo**

Tabelas críticas (SLA-2024 seção 2, multiplicadores PROC-042-v2) devem ser indexadas como chunks únicos, independente de tamanho, com um cabeçalho textual explícito que enriqueça o embedding: `"Tabela completa de SLAs por tier de cliente (Gold, Silver, Standard) para chamados gerais e incidentes críticos - SLA-2024 seção 2"`.

**Metadados obrigatórios por chunk:**

```json
{
  "source_document": "PROC-042-v2",
  "section": "2.1",
  "version": "2.0",
  "effective_date": "2023-11-10",
  "document_type": "procedimento",
  "supersedes": "PROC-042-v1"
}
```

Esses metadados permitem filtragem no momento do retrieval e instrução explícita ao modelo para priorizar a versão mais recente quando houver conflito.

---

## Parte 5 — Histórico de Iteração com o Claude

### Versão inicial enviada ao Claude para revisão

> *"Fiz uma análise de viabilidade técnica para o assistente de IA da NovaTech. Os PDFs podem ser extraídos com pdfminer, a wiki pode ser exportada em HTML, e as planilhas convertidas para CSV. Estimei 12M tokens no total. Recomendo chunking fixo de 512 tokens com o modelo GPT-4o (128K de contexto). Com esse contexto largo, podemos recuperar bastante chunks por query para garantir cobertura."*

### Feedback do Claude (pontos fracos identificados)

O Claude identificou os seguintes problemas na versão inicial:

1. **Estimativa de 12M tokens parece otimista ou pessimista sem memória:** A estimativa não estava justificada com os parâmetros concretos (qtd de documentos × páginas médias × palavras/página). Sem o detalhamento, é impossível avaliar se está correta. **→ Ação tomada:** Refeita a estimativa com cálculo explícito, chegando a ~3,5M tokens.

2. **"Recuperar mais chunks para garantir cobertura" é um antipadrão:** Aumentar o número de chunks recuperados não aumenta necessariamente a qualidade — o efeito *lost in the middle* implica que chunks no meio do contexto serão processados com menor fidelidade. Um retrieval mais preciso de menos chunks é melhor do que um retrieval mais amplo com mais chunks irrelevantes. **→ Ação tomada:** Incluída análise de orçamento de contexto com recomendação de 5-7 chunks por query.

3. **Chunking fixo de 512 tokens quebra tabelas:** O Claude sinalizou que tabelas de múltiplas linhas (como a tabela de multiplicadores regionais com 5 linhas) são frequentemente maiores que 512 tokens quando serializadas em Markdown — mas mais importante, um corte fixo pode separar cabeçalho de dados, tornando o chunk semanticamente incompleto. **→ Ação tomada:** Mudada a estratégia para chunking semântico por seção com chunks especiais para tabelas.

4. **pdfminer para PDFs escaneados não funciona:** pdfminer extrai texto de PDFs nativos (com camada de texto); PDFs escaneados são imagens e retornam string vazia sem OCR. A versão inicial não mencionava OCR. **→ Ação tomada:** Adicionada seção específica para PDFs escaneados com estratégia de OCR via Azure AI Document Intelligence.

5. **Export HTML da Confluence não foi tratado:** O Claude questionou como as macros customizadas seriam tratadas na conversão HTML→texto. "Exportar em HTML" não é estratégia suficiente — é o ponto de partida. **→ Ação tomada:** Especificada estratégia de uso da API REST e remoção de macros via pré-processamento.

6. **Planilhas com fórmulas: risco de dados obsoletos não mencionado:** A versão inicial convertia planilhas para CSV e indexava os valores calculados, sem mencionar que esses valores ficam obsoletos após a atualização mensal. **→ Ação tomada:** Adicionado risco de obsolescência e estratégia de re-ingestão mensal automática.

### Melhorias incorporadas (versão final vs inicial)

| Aspecto | Versão inicial | Versão final |
|---------|---------------|-------------|
| Estimativa de tokens | "12M tokens" sem justificativa | 3,5M tokens com cálculo por fonte |
| Estratégia de chunking | Fixo de 512 tokens | Semântico por seção com chunks especiais para tabelas |
| Número de chunks por query | "Quanto mais, melhor" | 5-7 chunks com justificativa de lost-in-middle |
| PDFs escaneados | Não mencionado | OCR via Azure AI Document Intelligence |
| Confluence | "Exportar HTML" | API REST + remoção de macros + resolução de links |
| Planilhas | "Converter para CSV" | Extração estruturada + re-ingestão mensal automática |
| Metadados de chunk | Não mencionado | Metadados obrigatórios incluindo versão e data de vigência |

---

## Conclusão

A construção do assistente de IA para a NovaTech é tecnicamente viável, mas a qualidade do sistema depende quase inteiramente da qualidade do pipeline de dados — não da escolha do modelo de LLM. Os principais riscos técnicos não são de capacidade do modelo (a janela de contexto do GPT-4o é mais do que suficiente para o volume de chunks necessário por query), mas sim:

1. **Documentação contraditória sem versionamento explícito** (PROC-042 v1 vs v2) — o pipeline precisa de metadados de vigência antes de qualquer outra feature.
2. **PDFs escaneados sem OCR adequado** — aproximadamente 120 documentos da base estarão silenciosamente ausentes da busca se o OCR não for implementado.
3. **Chunking que quebra tabelas** — o caso de uso de maior volume (cálculo de frete) depende de tabelas sendo indexadas como unidades semânticas inteiras.
4. **Ausência de re-ingestão automática** — com atualização mensal das planilhas e semanal da wiki, o pipeline precisa de agendamento automático desde o dia 1.

O assistente entregará valor real desde que o pipeline de ingestão trate cada tipo de fonte com a estratégia adequada, e que o orçamento de contexto por query seja gerenciado de forma deliberada — não deixado ao acaso.
