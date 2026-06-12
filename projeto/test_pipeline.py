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