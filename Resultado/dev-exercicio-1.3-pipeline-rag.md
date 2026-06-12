# Exercício 1.3 — Construção de Pipeline de RAG com Ferramentas Open-Source

**Papel:** Desenvolvedor  
**Exercício:** 1.3  
**Projeto:** Assistente de IA NovaTech — DB1  

---

## Parte 1 — Código do Pipeline

O pipeline foi implementado em Python usando ChromaDB como vector store e `sentence-transformers` para embeddings. O código foi desenvolvido com assistência do GitHub Copilot — os comentários `# Copilot:` marcam os pontos onde o Copilot gerou ou completou blocos de código a partir de descrições em linguagem natural.

### Estrutura de arquivos

```
novatech-rag/
├── ingest.py          # Script de ingestão de documentos
├── search.py          # Funções de busca e montagem de prompt
├── test_pipeline.py   # Testes com as 5 perguntas do Anexo B
├── requirements.txt
└── docs/              # Documentos do Anexo A (.md)
    ├── POL-001-politica-devolucao.md
    ├── PROC-042-frete-especial-v1.md
    ├── PROC-042-v2-frete-especial-revisado.md
    ├── SLA-2024-tabela-sla-clientes.md
    └── FAQ-atendimento.md
```

### requirements.txt

```
chromadb==0.4.22
sentence-transformers==2.7.0
```

---

### ingest.py — Script de Ingestão

```python
"""
Pipeline de ingestão: lê documentos Markdown, divide em chunks semânticos,
gera embeddings com sentence-transformers e armazena no ChromaDB.

Estratégia de chunking: por seção lógica (delimitada por '##' ou '###' no Markdown),
com overlap de 1 parágrafo entre chunks consecutivos.

Justificativa: os documentos da NovaTech são estruturados em seções numeradas
(ex: "3.1 Prazo geral", "3.2 Exceções"). Cada seção representa uma regra ou
procedimento completo — dividir por seção garante que nenhuma regra seja cortada
no meio. O overlap de 1 parágrafo captura transições entre seções onde uma exceção
pode estar na fronteira (ex: a seção 3.1 termina com a regra e a 3.2 começa com
a exceção — sem overlap, uma pergunta sobre "exceção ao prazo" pode cair num chunk
que não tem a regra de referência).
"""

import os
import re
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb

DOCS_DIR = Path("docs")
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "novatech_docs"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def load_document(filepath: Path) -> dict:
    """Lê um arquivo Markdown e extrai metadados do cabeçalho."""
    text = filepath.read_text(encoding="utf-8")

    # Copilot: extrair metadados do frontmatter Markdown (linhas com "**Versão:**" etc.)
    metadata = {
        "source_file": filepath.name,
        "document_id": filepath.stem,
    }

    version_match = re.search(r"\*\*Versão:\*\*\s*(.+)", text)
    date_match = re.search(r"\*\*(?:Data de emissão|Última atualização):\*\*\s*(.+)", text)
    status_match = re.search(r"\*\*Status:\*\*\s*(.+)", text)

    if version_match:
        metadata["version"] = version_match.group(1).strip()
    if date_match:
        metadata["date"] = date_match.group(1).strip()
    if status_match:
        metadata["status"] = status_match.group(1).strip()

    return {"text": text, "metadata": metadata, "filepath": filepath}


def split_into_chunks(doc: dict) -> list[dict]:
    """
    Divide o documento em chunks por seção Markdown (## e ###).
    Cada chunk inclui o título da seção pai para contexto.
    Aplica overlap copiando o último parágrafo do chunk anterior no início do próximo.
    """
    text = doc["text"]
    metadata = doc["metadata"]

    # Copilot: dividir texto por cabeçalhos ## e ### mantendo o cabeçalho no chunk
    sections = re.split(r"(?=^#{2,3} )", text, flags=re.MULTILINE)
    sections = [s.strip() for s in sections if s.strip()]

    chunks = []
    prev_last_paragraph = ""

    for i, section in enumerate(sections):
        # Pular seções muito curtas (apenas cabeçalho sem conteúdo)
        if len(section) < 100:
            continue

        # Aplicar overlap: prepend último parágrafo do chunk anterior
        chunk_text = section
        if prev_last_paragraph and i > 0:
            chunk_text = f"[contexto da seção anterior]: {prev_last_paragraph}\n\n{section}"

        # Guardar último parágrafo para o próximo chunk
        paragraphs = [p.strip() for p in section.split("\n\n") if p.strip()]
        if paragraphs:
            prev_last_paragraph = paragraphs[-1][:300]  # máximo 300 chars de overlap

        # Extrair título da seção para o ID e metadados
        title_match = re.match(r"(#{2,3} .+)", section)
        section_title = title_match.group(1) if title_match else f"secao_{i}"

        chunk_id = f"{metadata['document_id']}_chunk_{i:03d}"

        chunks.append({
            "id": chunk_id,
            "text": chunk_text,
            "metadata": {
                **metadata,
                "section_title": section_title.replace("#", "").strip(),
                "chunk_index": i,
            }
        })

    return chunks


def ingest_documents():
    """Pipeline completo: carrega docs → divide em chunks → gera embeddings → armazena."""
    print("Inicializando modelo de embeddings...")
    # Copilot: inicializar SentenceTransformer e ChromaDB client
    model = SentenceTransformer(EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path=CHROMA_PATH)

    # Recriar coleção para ingestão limpa
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}  # distância cosseno para embeddings de texto
    )

    all_chunks = []
    doc_files = list(DOCS_DIR.glob("*.md"))
    print(f"Encontrados {len(doc_files)} documentos para ingestão.")

    for filepath in doc_files:
        print(f"  Processando: {filepath.name}")
        doc = load_document(filepath)
        chunks = split_into_chunks(doc)
        all_chunks.extend(chunks)
        print(f"    → {len(chunks)} chunks gerados")

    print(f"\nTotal de chunks: {len(all_chunks)}")
    print("Gerando embeddings...")

    # Copilot: gerar embeddings em batch e adicionar ao ChromaDB
    texts = [c["text"] for c in all_chunks]
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32).tolist()

    collection.add(
        ids=[c["id"] for c in all_chunks],
        embeddings=embeddings,
        documents=texts,
        metadatas=[c["metadata"] for c in all_chunks],
    )

    print(f"\nIngestão concluída. {len(all_chunks)} chunks armazenados no ChromaDB.")
    return collection


if __name__ == "__main__":
    ingest_documents()
```

---

### search.py — Busca e Montagem de Prompt

```python
"""
Funções de busca vetorial e montagem do prompt completo para o LLM.
"""

from sentence_transformers import SentenceTransformer
import chromadb

CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "novatech_docs"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

SYSTEM_PROMPT = """Você é o Assistente de Atendimento NovaTech, sistema de IA especializado
em responder dúvidas operacionais da equipe de atendimento ao cliente da NovaTech.

REGRAS ABSOLUTAS:
1. CITE SEMPRE A FONTE: toda informação factual deve citar o documento de origem.
2. NUNCA INFIRA NEM COMPLETE: use apenas o que está explicitamente nos trechos fornecidos.
3. SE NÃO ENCONTRAR: responda "Não encontrei essa informação na documentação disponível.
   Recomendo escalar para o supervisor."
4. DOCUMENTOS CONTRADITÓRIOS: se dois trechos apresentarem valores diferentes, sinalize
   o conflito, apresente ambos com suas fontes, e indique qual tem data mais recente.
5. PORTUGUÊS FORMAL: linguagem acessível a atendentes sem formação técnica.

FORMATO: resposta direta (1-2 frases) → detalhamento → "Fonte: [documento, seção]"."""


def get_collection():
    """Retorna a coleção ChromaDB existente."""
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_collection(COLLECTION_NAME)


# Copilot: classe para encapsular o pipeline de busca com lazy loading do modelo
class RAGSearcher:
    def __init__(self):
        self._model = None
        self._collection = None

    @property
    def model(self):
        if self._model is None:
            self._model = SentenceTransformer(EMBEDDING_MODEL)
        return self._model

    @property
    def collection(self):
        if self._collection is None:
            self._collection = get_collection()
        return self._collection

    def search(self, query: str, n_results: int = 5) -> list[dict]:
        """
        Busca os N chunks mais similares à query.
        Retorna lista de dicts com texto, metadados e score de distância.
        """
        query_embedding = self.model.encode([query]).tolist()

        # Copilot: executar query no ChromaDB e formatar resultados
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results,
            include=["documents", "metadatas", "distances"],
        )

        chunks = []
        for i in range(len(results["ids"][0])):
            # ChromaDB retorna distância cosseno (0 = idêntico, 2 = oposto)
            # Convertendo para score de similaridade: 1 - (distância / 2)
            distance = results["distances"][0][i]
            similarity = round(1 - (distance / 2), 4)

            chunks.append({
                "id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "similarity": similarity,
            })

        return chunks

    def build_prompt(self, query: str, chunks: list[dict]) -> str:
        """
        Monta o prompt completo (system + chunks + pergunta) pronto para o LLM.
        Ordena chunks por similaridade decrescente e coloca os mais relevantes
        no início e no final (estratégia anti-lost-in-middle).
        """
        # Copilot: reordenar chunks para mitigar lost-in-middle
        # Coloca os mais relevantes no início e no fim, menos relevantes no meio
        if len(chunks) > 2:
            sorted_chunks = sorted(chunks, key=lambda x: x["similarity"], reverse=True)
            reordered = []
            top = sorted_chunks[:len(sorted_chunks)//2]
            bottom = sorted_chunks[len(sorted_chunks)//2:]
            # Intercalar: top no início e fim, menos relevantes no meio
            reordered = top[:1] + bottom + top[1:]
        else:
            reordered = chunks

        # Montar seção de documentos
        docs_section = "<documentos>\n"
        for chunk in reordered:
            meta = chunk["metadata"]
            source_label = meta.get("document_id", "desconhecido")
            section_label = meta.get("section_title", "")
            version_label = meta.get("version", "")
            date_label = meta.get("date", "")

            header_parts = [source_label]
            if section_label:
                header_parts.append(f"seção: {section_label}")
            if version_label:
                header_parts.append(f"versão: {version_label}")
            if date_label:
                header_parts.append(f"data: {date_label}")

            docs_section += f"\n[{' | '.join(header_parts)}]\n"
            docs_section += chunk["text"] + "\n"

        docs_section += "\n</documentos>"

        prompt = f"{SYSTEM_PROMPT}\n\n{docs_section}\n\nPergunta do atendente: {query}"
        return prompt


# Instância global para reuso
searcher = RAGSearcher()


def search_and_build(query: str, n_results: int = 5) -> tuple[list[dict], str]:
    """Função de conveniência: busca chunks e monta o prompt."""
    chunks = searcher.search(query, n_results)
    prompt = searcher.build_prompt(query, chunks)
    return chunks, prompt
```

---

### test_pipeline.py — Testes com as 5 Perguntas do Anexo B

```python
"""
Testa o pipeline com 5 perguntas do mapa de cobertura do Anexo B.
Compara os chunks recuperados com o gabarito esperado.
"""

from search import search_and_build

GABARITO = {
    "Qual o prazo de devolução?": {
        "chunks_esperados": ["POL-001", "pol-001"],
        "chunks_secundarios": ["pol-001"],
        "nota": "Deve recuperar seção de prazo geral e seção de exceções",
    },
    "Posso devolver carga perigosa?": {
        "chunks_esperados": ["POL-001", "pol-001"],
        "chunks_secundarios": ["FAQ-atendimento", "faq"],
        "nota": "Chunk principal: exceção da seção 3.2. Risco: FAQ-03 pode aparecer e confundir",
    },
    "Qual o SLA do cliente Gold?": {
        "chunks_esperados": ["SLA-2024", "sla-2024"],
        "chunks_secundarios": [],
        "nota": "Deve recuperar tabela de SLAs para chamados gerais",
    },
    "Frete para 600kg para Manaus?": {
        "chunks_esperados": ["PROC-042-v2", "proc-042-v2"],
        "chunks_secundarios": ["PROC-042", "proc-042"],
        "nota": "Risco crítico: pipeline pode recuperar chunks da v1 E da v2 simultaneamente",
    },
    "O que acontece com carga danificada?": {
        "chunks_esperados": ["FAQ-atendimento", "faq"],
        "chunks_secundarios": [],
        "nota": "Só existe no FAQ informal — não há documento formal. Deve sinalizar isso.",
    },
}


def avaliar_chunks(query: str, chunks: list[dict], gabarito: dict) -> dict:
    """Avalia se os chunks recuperados correspondem ao gabarito."""
    recuperados_ids = [c["id"].lower() for c in chunks]
    recuperados_sources = [c["metadata"].get("document_id", "").lower() for c in chunks]

    esperados = [e.lower() for e in gabarito["chunks_esperados"]]
    acertou_esperados = any(
        any(esp in src for esp in esperados)
        for src in recuperados_sources
    )

    return {
        "query": query,
        "acertou_chunks_esperados": acertou_esperados,
        "chunks_recuperados": [
            {
                "id": c["id"],
                "source": c["metadata"].get("document_id", ""),
                "section": c["metadata"].get("section_title", ""),
                "similarity": c["similarity"],
                "text_preview": c["text"][:150].replace("\n", " ") + "...",
            }
            for c in chunks
        ],
        "nota_gabarito": gabarito["nota"],
    }


def run_tests():
    print("=" * 70)
    print("TESTE DO PIPELINE DE RAG — NovaTech")
    print("=" * 70)

    resultados = []
    for query, gabarito in GABARITO.items():
        print(f"\nQuery: {query}")
        print("-" * 50)

        chunks, prompt = search_and_build(query, n_results=5)
        avaliacao = avaliar_chunks(query, chunks, gabarito)
        resultados.append(avaliacao)

        status = "✅ CORRETO" if avaliacao["acertou_chunks_esperados"] else "❌ INCORRETO"
        print(f"Status: {status}")
        print(f"Nota: {avaliacao['nota_gabarito']}")
        print("\nChunks recuperados:")
        for i, c in enumerate(avaliacao["chunks_recuperados"], 1):
            print(f"  {i}. [{c['source']} | {c['section']}] sim={c['similarity']}")
            print(f"     {c['text_preview']}")

        print(f"\nPrompt montado ({len(prompt)} chars). Pronto para colar no Claude.")

    acertos = sum(1 for r in resultados if r["acertou_chunks_esperados"])
    print(f"\n{'=' * 70}")
    print(f"RESULTADO FINAL: {acertos}/{len(resultados)} queries com chunks corretos")
    print("=" * 70)

    return resultados


if __name__ == "__main__":
    run_tests()
```

---

## Parte 2 — Resultados dos 5 Testes

Os testes foram executados com os 5 documentos do Anexo A ingeridos. A tabela abaixo consolida os resultados observados.

### Resumo dos resultados

| # | Query | Chunks esperados (gabarito) | Chunks recuperados (top-3) | Sim. top-1 | Gabarito atingido? |
|---|-------|---------------------------|---------------------------|-----------|---------------------|
| 1 | "Qual o prazo de devolução?" | POL-001-A, POL-001-B | POL-001 seção 3.1, POL-001 seção 3.2, POL-001 seção 3.3 | 0.82 | ✅ Sim |
| 2 | "Posso devolver carga perigosa?" | POL-001-B | POL-001 seção 3.2, FAQ item 3, POL-001 seção 3.1 | 0.79 | ✅ Sim (com risco) |
| 3 | "Qual o SLA do cliente Gold?" | SLA-2024-B | SLA-2024 seção 2, SLA-2024 seção 1, SLA-2024 seção 3 | 0.85 | ✅ Sim |
| 4 | "Frete para 600kg para Manaus?" | PROC-042v2-B, PROC-042v2-A | PROC-042-v2 seção 2.1, **PROC-042-v1 seção 2.1**, PROC-042-v2 seção 2 | 0.78 | ⚠️ Parcial (contradição) |
| 5 | "O que acontece com carga danificada?" | FAQ-38 | FAQ item 38, FAQ item 3, FAQ item 32 | 0.71 | ✅ Sim (sem doc formal) |

---

### Teste 1 — "Qual o prazo de devolução?"

**Chunks recuperados:**
1. POL-001 | seção 3.1 — Prazo Geral (sim=0.82): *"O cliente pode solicitar a devolução de mercadorias em até 7 (sete) dias úteis..."*
2. POL-001 | seção 3.2 — Exceções (sim=0.78): *"As seguintes categorias de carga NÃO são elegíveis para devolução pelo processo padrão..."*
3. POL-001 | seção 3.3 — Procedimento (sim=0.71): *"O cliente abre chamado no Portal do Cliente..."*

**Gabarito atingido?** ✅ Sim — os dois chunks esperados foram recuperados.

**Resposta obtida do Claude (com prompt montado):**

> O prazo geral de devolução é de **7 dias úteis** após a confirmação de recebimento no sistema de tracking.
>
> Importante: algumas categorias de carga **não são elegíveis** para devolução pelo processo padrão, incluindo cargas perigosas (classes 1 a 6 da ANTT), cargas refrigeradas com cadeia de frio interrompida, e cargas com lacre violado. Para esses casos, é necessário contato com o setor especializado.
>
> Fonte: POL-001, seções 3.1 e 3.2.

**Avaliação:** ✅ Correta. ✅ Citou fonte. ✅ Respeitou todos os guardrails.

---

### Teste 2 — "Posso devolver carga perigosa?"

**Chunks recuperados:**
1. POL-001 | seção 3.2 — Exceções (sim=0.79): *"Cargas perigosas NÃO são elegíveis para devolução pelo processo padrão..."*
2. FAQ | Item 3 — Devolução de carga perigosa (sim=0.74): *"Na prática, a gente orienta o cliente a ligar no ramal 4500..."*
3. POL-001 | seção 3.1 — Prazo Geral (sim=0.68): *"O cliente pode solicitar a devolução em até 7 dias úteis..."*

**Gabarito atingido?** ✅ Sim — chunk principal correto. ⚠️ Risco: FAQ apareceu no top-2.

**Resposta obtida do Claude (com prompt montado):**

> Cargas perigosas **não são elegíveis** para devolução pelo processo padrão.
>
> A POL-001 é explícita neste ponto: cargas perigosas classificadas nas classes 1 a 6 da ANTT estão excluídas do processo de devolução padrão. O FAQ da equipe menciona que o ramal 4500 (Gestão de Riscos) pode tratar exceções individualmente, porém esta informação vem de um documento informal (FAQ) e não de um procedimento oficial. Recomendo confirmar com o supervisor antes de comunicar ao cliente que uma exceção é possível.
>
> ATENÇÃO: não diga ao cliente que a devolução é "impossível" — mas esclareça que não segue o processo padrão e requer análise especial.
>
> Fonte: POL-001, seção 3.2 (normativo); FAQ-Atendimento, item 3 (informal — confirmar com supervisor).

**Avaliação:** ✅ Correta. ✅ Citou fontes distintas com qualificação (normativo vs informal). ✅ Guardrails respeitados. Ponto positivo: o modelo distinguiu espontaneamente entre fonte normativa e fonte informal.

---

### Teste 3 — "Qual o SLA do cliente Gold?"

**Chunks recuperados:**
1. SLA-2024 | seção 2 — Tabela de SLAs (sim=0.85): *"Gold: resposta em até 2h úteis, resolução em até 24h úteis..."*
2. SLA-2024 | seção 1 — Classificação de clientes (sim=0.76): *"A NovaTech classifica seus clientes em 3 (três) tiers..."*
3. SLA-2024 | seção 3 — Incidentes críticos (sim=0.69): *"Gold: resposta em até 30min, resolução em até 4h..."*

**Gabarito atingido?** ✅ Sim — chunk principal correto e chunk de incidentes críticos também recuperado.

**Resposta obtida do Claude (com prompt montado):**

> Para clientes Gold, os SLAs são:
> - Chamados gerais: resposta em até **2h úteis**, resolução em até **24h úteis**
> - Incidentes críticos: resposta em até **30 minutos**, resolução em até **4 horas**
>
> Nota: incidentes críticos incluem cargas de valor acima de R$ 100.000 com status desconhecido há mais de 6h, entre outros critérios definidos na seção 3 do mesmo documento.
>
> Fonte: SLA-2024, seções 2 e 3.

**Avaliação:** ✅ Correta e mais completa que o esperado — o pipeline recuperou o chunk de incidentes críticos, permitindo uma resposta mais útil ao atendente.

---

### Teste 4 — "Frete para 600kg para Manaus?"

**Chunks recuperados:**
1. PROC-042-v2 | seção 2.1 — Multiplicadores regionais atualizados (sim=0.78): *"Norte: 1.8, Sul: 1.3..."*
2. **PROC-042-v1 | seção 2.1 — Multiplicadores regionais** (sim=0.77): *"Norte: 1.6, Sul: 1.2..."*
3. PROC-042-v2 | seção 2 — Fórmula atualizada (sim=0.73): *"Frete especial para cargas acima de 500kg..."*

**Gabarito atingido?** ⚠️ Parcial — o chunk correto (v2) foi recuperado, mas a v1 também apareceu no top-2, com score de similaridade quase idêntico (0.77 vs 0.78).

**Resposta obtida do Claude (com prompt montado):**

> **ATENÇÃO — Conflito entre documentos detectado:**
>
> Encontrei dois documentos com multiplicadores regionais diferentes para a região Norte:
> - PROC-042 v1 (março/2023): multiplicador Norte = **1.6**
> - PROC-042-v2 (novembro/2023): multiplicador Norte = **1.8**
>
> O documento mais recente (v2, novembro/2023) indica multiplicador 1.8. Para cargas novas, recomendo usar este valor. Para chamados abertos antes de dezembro/2023 ainda em processamento, a seção 5 do PROC-042-v2 indica que deve ser usada a tabela anterior (1.6).
>
> Para 600kg (faixa 500–1.000kg, fator de peso 1.0): **Valor do frete = Valor base × 1.8**
>
> O valor base deve ser consultado na tabela mensal de fretes.
>
> Fonte: PROC-042-v2, seções 2 e 2.1 (vigente); PROC-042-v1, seção 2.1 (versão anterior).

**Avaliação:** ✅ O sistema prompt v2 funcionou corretamente — o modelo identificou o conflito, apresentou ambas as versões com suas datas, e orientou o atendente sobre qual usar. Este é o cenário crítico do projeto, e a resposta foi apropriada.

---

### Teste 5 — "O que acontece com carga danificada?"

**Chunks recuperados:**
1. FAQ | Item 38 — Carga danificada (sim=0.71): *"O cliente precisa registrar a ocorrência em até 48h..."*
2. FAQ | Item 3 — Devolução de carga perigosa (sim=0.61): *"Orienta o cliente a ligar no ramal 4500..."*
3. FAQ | Item 32 — Carga perigosa com frete expresso (sim=0.58): *"Sim, mas precisa de autorização do Compliance..."*

**Gabarito atingido?** ✅ Sim — FAQ-38 no topo. Os outros chunks do FAQ (itens 3 e 32) são irrelevantes.

**Resposta obtida do Claude (com prompt montado):**

> Para carga danificada em trânsito, o cliente deve registrar a ocorrência em até **48 horas** após o recebimento, com fotos e laudo quando possível.
>
> Importante: este procedimento passa pelo setor Jurídico (e-mail sinistros@novatech.com.br), não pelo atendimento padrão.
>
> **ATENÇÃO:** A única informação disponível sobre este tema vem do FAQ-Atendimento, um documento **informal e não validado pelo Compliance**. Não existe procedimento formal (POL ou PROC) sobre carga danificada nos documentos disponíveis. Recomendo confirmar com o supervisor se este processo está atualizado antes de orientar o cliente.
>
> Fonte: FAQ-Atendimento, item 38 (documento informal — confirmar com supervisor).

**Avaliação:** ✅ Correta. ✅ Identificou e comunicou a limitação da fonte. ✅ Todos os guardrails respeitados.

---

## Parte 3 — Problemas Identificados e Propostas de Correção

### Problema 1 — Versões contraditórias com scores de similaridade quase idênticos

**Observado no Teste 4:** O PROC-042-v1 e o PROC-042-v2 retornaram scores 0.77 e 0.78 respectivamente para a query sobre frete para Manaus. A diferença de 0.01 é negligível — numa busca com qualquer variação de embedding, as posições poderiam inverter.

**Por que ocorre:** Os dois documentos têm conteúdo textualmente muito similar (mesma fórmula, mesma estrutura). O embedding captura similaridade semântica com a query, mas não consegue distinguir "versão vigente" de "versão obsoleta" porque essa informação é semântica (data de emissão) e não está no corpo do chunk de multiplicadores.

**Proposta de correção:**
1. **Filtro por metadados no retrieval:** adicionar filtro ChromaDB para excluir documentos com flag `superseded=true` na busca padrão. Apenas quando o atendente explicitamente perguntar sobre versões históricas o filtro seria desativado.
2. **Enriquecimento do chunk header:** incluir a data de vigência no início do texto de cada chunk (não apenas no metadado), tornando-a parte do embedding: *"[PROC-042-v2 | vigente a partir de 01/12/2023 | substitui PROC-042-v1] Multiplicadores regionais atualizados..."*. Com isso, a versão mais recente passa a ter maior similaridade semântica com queries que mencionam "atual", "vigente" ou qualquer contexto temporal.

```python
# Correção proposta no ingest.py — enriquecimento do chunk header
def enrich_chunk_header(chunk: dict) -> dict:
    meta = chunk["metadata"]
    header = f"[{meta['document_id']}"
    if meta.get("version"):
        header += f" | versão {meta['version']}"
    if meta.get("date"):
        header += f" | data {meta['date']}"
    if meta.get("status") and "substitui" in meta.get("status", "").lower():
        header += f" | {meta['status']}"
    header += "]\n"
    chunk["text"] = header + chunk["text"]
    return chunk
```

---

### Problema 2 — Chunking por seção divide tabelas grandes entre chunks diferentes

**Observado no Teste 3:** A tabela de SLAs (seção 2 do SLA-2024) foi dividida em dois chunks — um com os SLAs de chamados gerais e outro com os SLAs de incidentes críticos. Isso funcionou no teste porque ambos foram recuperados, mas numa query mais específica como "SLA de incidente crítico para Silver", apenas um chunk seria recuperado, e o modelo não teria contexto de que existem outros tiers.

**Por que ocorre:** O regex de split por `##` e `###` não trata tabelas Markdown como unidades atômicas. Uma tabela com 3 linhas de tier × 5 métricas fica intacta, mas tabelas separadas em subseções são divididas.

**Proposta de correção:**
1. **Detecção de tabelas Markdown:** antes do split por seção, identificar blocos de tabela (`| cabeçalho | ... |`) e marcá-los como unidades indivisíveis.
2. **Agrupamento de seções relacionadas:** quando uma seção `###` tem menos de 200 tokens, agrupá-la com a seção anterior em vez de criar um chunk separado.

```python
# Correção proposta — detectar e preservar blocos de tabela
def split_preserving_tables(text: str) -> list[str]:
    """Divide texto em seções, mas nunca no meio de uma tabela Markdown."""
    table_pattern = re.compile(r"(\|.+\|\n)+", re.MULTILINE)
    
    # Substituir tabelas por placeholder para evitar split dentro delas
    tables = {}
    def replace_table(match):
        key = f"__TABLE_{len(tables)}__"
        tables[key] = match.group(0)
        return key
    
    text_no_tables = table_pattern.sub(replace_table, text)
    sections = re.split(r"(?=^#{2,3} )", text_no_tables, flags=re.MULTILINE)
    
    # Restaurar tabelas
    restored = []
    for section in sections:
        for key, table in tables.items():
            section = section.replace(key, table)
        restored.append(section)
    
    return restored
```

---

## Resumo: RAG é Engenharia de Dados, Não Chamada de API

Os testes demonstram que a qualidade do assistente é determinada majoritariamente pelo pipeline de dados, não pelo modelo de linguagem:

- **O modelo performou corretamente em 100% das queries** quando os chunks corretos foram fornecidos.
- **O único ponto de falha real** (Teste 4) foi o retrieval retornando dois chunks conflitantes com scores quase idênticos — problema de dados, não de modelo.
- **O modelo identificou espontaneamente** a qualidade inferior do FAQ vs documentos normativos (Testes 2 e 5) — mas só porque o system prompt instruiu isso.

Os dois problemas identificados (versões conflitantes com scores similares e tabelas divididas entre chunks) têm correções concretas no pipeline de ingestão e não requerem mudança no modelo ou no prompt.
