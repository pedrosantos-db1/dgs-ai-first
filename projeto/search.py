"""
Funções de busca vetorial e montagem do prompt completo para o LLM.
"""

from pathlib import Path

from sentence_transformers import SentenceTransformer
import chromadb

PROJECT_ROOT = Path(__file__).resolve().parent
CHROMA_PATH = PROJECT_ROOT / "chroma_db"
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
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
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