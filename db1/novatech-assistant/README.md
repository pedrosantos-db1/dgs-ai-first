# novatech-assistant — Starter Repo (Anexo D)

> Repositório Git **local** para os exercícios do Cenário-Âncora 2 (Fase de Estruturação).
> O prefixo `db1/` citado no cenário é apenas narrativo: **não há remoto, push, GitHub nem Azure**.
> Tudo roda localmente e de graça.

## O que vem pronto neste starter

- A estrutura de diretórios do projeto (espelha o Anexo C), com arquivos **vazios/stub** que os exercícios vão preencher (AGENTS.md, specs, skills, prompts, código).
- `docs/novatech/` — os 5 documentos de negócio da NovaTech (Anexo A). É a fonte que o **filesystem MCP server** expõe no lugar do Confluence.
- `data/retrieval-corpus/` — os chunks de referência (Anexo B). É a fonte que o **filesystem MCP server** expõe no lugar do Azure AI Search.
- `.mcp/mcp.json` — scaffold vazio. Configurá-lo é a tarefa do Dev 2.1.

## Setup (uma vez)

```bash
git init
git add -A && git commit -m "chore: starter repo (Anexo D)"
```

Isso já basta para o **git MCP server** ter histórico para ler.

## MCP servers usados (todos gratuitos, locais e mantidos como reference servers)

| Papel no projeto            | Server          | Aponta para            |
|-----------------------------|-----------------|------------------------|
| Ler/editar código + docs    | `filesystem`    | `./src ./specs ./skills ./docs ./data` |
| Histórico/branches do repo  | `git`           | este repositório local |
| Glossário/decisões (memória)| `memory`        | grafo local persistente |
| Explorar primitivas de MCP  | `everything`    | — (aprendizado)        |

Invocação típica: `filesystem`/`memory`/`everything` via `npx @modelcontextprotocol/server-...`;
`git` via `uvx mcp-server-git`. **Confirme os nomes/comandos atuais no README oficial do repo
`modelcontextprotocol/servers` antes de configurar** — a lista evolui (ler a doc do server é parte do exercício).

## O que NÃO é necessário

- ❌ Conta/Token GitHub (o server de GitHub foi arquivado; usamos `filesystem`+`git` locais)
- ❌ Azure (OpenAI, AI Search, DevOps, Functions, Cosmos) — o "estado provisionado em dev" no Anexo C é ficção narrativa
- ❌ Confluence — a documentação de negócio vive em `docs/novatech/`
- ❌ Qualquer serviço pago ou externo
