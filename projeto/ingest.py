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

import re
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb

PROJECT_ROOT = Path(__file__).resolve().parent
DOCS_DIR = PROJECT_ROOT / "docs"
CHROMA_PATH = PROJECT_ROOT / "chroma_db"
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
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))

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