# Corpus de retrieval (fonte para o filesystem MCP server)

Chunks de referência do pipeline de RAG (Anexo B), incluindo o mapa de cobertura
pergunta → chunks. O agente "recupera" lendo este corpus via MCP **read-only**.
Substitui o Azure AI Search — nenhum serviço externo é necessário.
