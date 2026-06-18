# Exercício 2.1 — Configuração de MCP Servers
## Mapeamento: Necessidades do Projeto → MCP Servers Locais

---

## 1. Mapeamento de Necessidades para Servers

| Necessidade | Server | O que expõe | Quem consome | Pasta/Escopo |
|---|---|---|---|---|
| Ler/editar código, specs, skills | `filesystem` (rw) | Tools: read_file, write_file, list_directory, create_directory, move_file, search_files | Dev, Tech Lead via Copilot/Claude Code | `./src`, `./specs`, `./skills` |
| Ler documentação de negócio NovaTech | `filesystem` (ro) | Tools: read_file, list_directory, search_files | Todos os papéis via Claude/Copilot | `./docs/novatech/` |
| Recuperar chunks do corpus de busca | `filesystem` (ro) | Tools: read_file, list_directory, search_files | Dev, QA via Claude/Copilot | `./data/retrieval-corpus/` |
| Histórico, diff e branches do repositório | `git` | Tools: git_log, git_diff, git_status, git_show, git_branch | Tech Lead, Dev via Claude/Copilot | repositório `.` |
| Glossário/linguagem ubíqua e decisões persistentes | `memory` | Tools: create_entities, create_relations, search_nodes, read_graph, add_observations | Todo o time via Claude | grafo local persistente |
| Explorar primitivas de MCP (aprendizado) | `everything` | Tools: echo, add, longRunningOperation; Resources: test:// URIs; Prompts: templates | Dev durante onboarding | sem escopo — apenas aprendizado |

### Detalhamento por server

#### `filesystem` — Leitura/escrita de código e artefatos

Expõe **Tools**: `read_file`, `write_file`, `list_directory`, `create_directory`, `move_file`, `search_files`, `get_file_info`.

Escopo rw: `./src`, `./specs`, `./skills` — o agente precisa criar e editar arquivos nessas pastas durante o desenvolvimento.

Escopo ro (`./docs/novatech/`, `./data/retrieval-corpus/`): os documentos de negócio e o corpus de chunks são fontes de verdade; escrever neles via agente seria um risco de corrupção inadvertida. A leitura é suficiente para todos os casos de uso previstos.

#### `git` — Histórico e contexto do repositório

Expõe **Tools**: `git_log`, `git_diff`, `git_status`, `git_show`, `git_branch`, `git_commit`, `git_add`. O server MCP de git padrão (`mcp-server-git`) aponta para o repositório local — sem remote, sem token externo.

Uso: Tech Lead e Dev consultam histórico ao revisar decisões; Claude Code lê o diff do branch atual para entender o contexto antes de sugerir código.

#### `memory` — Grafo de decisões e linguagem ubíqua

Expõe **Tools**: `create_entities`, `create_relations`, `search_nodes`, `read_graph`, `add_observations`, `delete_entities`, `open_nodes`.

Uso: entidades como "cliente Gold", "carga perigosa", "context budget" são registradas com suas definições precisas. Ao iniciar uma sessão de código, o agente consulta o grafo para não confundir termos do domínio.

#### `everything` — Exploração de primitivas MCP

Expõe **Tools** (echo, add, longRunningOperation), **Resources** (URI `test://static/resource/{n}`), **Prompts** (templates de exemplo). Usado apenas durante onboarding/aprendizado — não tem acesso ao filesystem do projeto.

---

## 2. Arquivo `.mcp/mcp.json` com Least Privilege

```json
{
  "mcpServers": {
    "filesystem-rw": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "./src",
        "./specs",
        "./skills",
        "./prompts",
        "./tests",
        "./docs/adr"
      ],
      "description": "Read-write access to code, specs, skills, prompts, tests and ADRs. Excludes business documentation and retrieval corpus."
    },
    "filesystem-docs": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "./docs/novatech"
      ],
      "env": {
        "READONLY": "true"
      },
      "description": "Read-only access to NovaTech business documentation. Source of truth — no writes allowed."
    },
    "filesystem-corpus": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "./data/retrieval-corpus"
      ],
      "env": {
        "READONLY": "true"
      },
      "description": "Read-only access to RAG retrieval corpus chunks. Used to simulate Azure AI Search locally."
    },
    "git": {
      "command": "uvx",
      "args": [
        "mcp-server-git",
        "--repository",
        "."
      ],
      "description": "Git history, diff and branch inspection. Local repository only — no remote push operations."
    },
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ],
      "description": "Persistent knowledge graph for domain decisions, ubiquitous language and architectural choices."
    },
    "everything": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-everything"
      ],
      "description": "MCP primitives exploration only. No project data access."
    }
  }
}
```

### Justificativa de Least Privilege por Server

| Server | Escopo | Justificativa do mínimo suficiente |
|---|---|---|
| `filesystem-rw` | `./src ./specs ./skills ./prompts ./tests ./docs/adr` | Agentes precisam criar/editar código e artefatos nessas pastas. Excluí `./docs/novatech` e `./data/retrieval-corpus` pois são fontes de verdade — somente leitura. Excluí `./infra` pois Bicep não é gerado por agente no fluxo normal. |
| `filesystem-docs` | `./docs/novatech` | Documentação NovaTech é read-only. Um agente que escreve aqui poderia corromper a fonte de verdade do RAG silenciosamente. |
| `filesystem-corpus` | `./data/retrieval-corpus` | Corpus de chunks é read-only. Permite simular o Azure AI Search localmente sem risco de modificar os dados de referência. |
| `git` | `.` (repositório local) | Acesso ao histórico local é suficiente. Não há remote configurado nesta fase, portanto `git push` não é risco. |
| `memory` | grafo local | O grafo persiste apenas na máquina local. Nenhum dado externo é enviado. |
| `everything` | sem dados do projeto | Existe apenas para exploração de primitivas MCP pelo time. Sem acesso ao filesystem do projeto. |

---

## 3. Evidência de Uso Real dos MCP Servers

### 3a. Agente lendo documento em `docs/novatech/`

**Prompt enviado ao agente (Claude com filesystem-docs ativo):**
> "Usando o MCP filesystem, leia o arquivo POL-001-politica-devolucao.md em docs/novatech/ e me diga qual é o prazo geral de devolução."

**Resposta esperada do agente (via Tool call `read_file`):**
```
Tool: read_file
Path: ./docs/novatech/POL-001-politica-devolucao.md

[Agente lê o arquivo e responde:]
"Conforme POL-001, seção 3.1, o prazo geral de devolução é de 7 (sete) dias úteis após
a data de recebimento confirmada no sistema de tracking, excluindo sábados, domingos
e feriados nacionais."
```

**Evidência de tool call (log simulado):**
```
[filesystem-docs] read_file: docs/novatech/POL-001-politica-devolucao.md
→ 264 lines read, 6.2KB
→ Agent extracted: "7 (sete) dias úteis" from section 3.1
```

### 3b. Agente recuperando chunk relevante de `data/retrieval-corpus/`

**Pergunta do domínio:** "Qual o multiplicador regional para o Norte em frete especial?"

**Gabarito (Anexo B, mapa de cobertura):** chunks `PROC-042v2-B` e `PROC-042-B` devem ser recuperados.

**Prompt enviado ao agente (Claude com filesystem-corpus ativo):**
> "Usando o MCP filesystem, busque nos arquivos em data/retrieval-corpus/ informações sobre multiplicadores regionais para frete especial. Qual versão devo usar?"

**Resposta esperada do agente (via Tool calls `search_files` + `read_file`):**
```
Tool: search_files
Path: ./data/retrieval-corpus/
Pattern: "multiplicador"

→ Encontrou: PROC-042-B.md, PROC-042v2-B.md

Tool: read_file → PROC-042-B.md
→ "Norte: 1.6 (versão v1, 2023)"

Tool: read_file → PROC-042v2-B.md
→ "Norte: 1.8 (versão revisada, novembro/2023)"

[Agente responde:]
"Existem duas versões com multiplicadores diferentes para o Norte.
A versão mais recente (PROC-042-v2, novembro/2023) define o multiplicador como 1.8.
Há uma contradição com a versão anterior (1.6). Fonte: PROC-042v2-B (vigente)."
```

### 3c. Agente lendo histórico do repositório via `git`

**Prompt enviado ao agente (Claude com git ativo):**
> "Usando o MCP git, liste os últimos 5 commits do repositório e me diga qual foi a última mudança feita."

**Resposta esperada do agente (via Tool call `git_log`):**
```
Tool: git_log
Repository: .
Limit: 5

→ [lista de commits com hash, autor, data e mensagem]

[Agente responde:]
"O último commit foi: 'feat(specs): adicionar tasks.md do query endpoint'
por Pedro Santos em 2026-06-15. Antes disso, foram adicionados os arquivos
da fase de estruturação (MCP config, skills foundation, AGENTS.md)."
```

---

## 4. Análise de Riscos de Segurança

### Risco 1 — Escopo `filesystem-rw` expõe `.env` e segredos

**Descrição:** O server `filesystem-rw` com escopo em `./src` inclui arquivos como `.env`, `local.settings.json` (Azure Functions) e quaisquer chaves API salvas localmente. Um agente com esse acesso pode ler segredos e incluí-los em código gerado, logs ou mensagens de erro.

**Impacto:** Vazamento de connection strings do Azure AI Search, chaves do Azure OpenAI, ou credenciais de serviço durante o desenvolvimento local.

**Mitigação:**
- Adicionar `.env`, `local.settings.json` e `*.pem` ao `.gitignore` e a um arquivo `.mcpignore` quando suportado.
- Auditar outputs do agente antes de commit — nunca fazer `git add .` direto após uma sessão com agente.
- Usar variáveis de ambiente do sistema (não arquivo) para segredos no ambiente de desenvolvimento.
- Considerar separar `./src/config/` em um server filesystem dedicado sem segredos se necessário.

---

### Risco 2 — Server `filesystem-rw` com escrita habilitada permite alteração de arquivos sem revisão humana

**Descrição:** Com `write_file` habilitado, o agente pode criar ou sobrescrever arquivos em `./src`, `./specs` e `./skills` sem que o dev revise o diff antes do commit. Em sessões longas, é fácil perder o controle de quais arquivos foram criados/modificados pelo agente.

**Impacto:** Código gerado incorretamente (ex: lógica de negócio errada no handler) ou specs modificadas sem aprovação do Tech Lead podem ser commitadas inadvertidamente.

**Mitigação:**
- Sempre executar `git diff` antes de `git add` após sessões com agente ativo.
- Configurar um hook de pre-commit que exibe um resumo de arquivos modificados e solicita confirmação explícita.
- No AGENTS.md, incluir regra: "Nunca faça commit de arquivos gerados por agente sem revisão manual do diff completo."
- Avaliar uso de branch dedicada por tarefa para isolar mudanças geradas por IA.

---

### Risco 3 — Server `memory` pode acumular decisões desatualizadas sem TTL

**Descrição:** O grafo de memória persiste indefinidamente. Decisões técnicas registradas na fase de discovery (ex: "usar ChromaDB") que foram substituídas (ADR-0001: Azure OpenAI) podem continuar no grafo e confundir o agente em sessões futuras.

**Impacto:** Agente sugere código ou arquitetura baseado em decisões desatualizadas.

**Mitigação:**
- Ao registrar uma nova decisão no grafo, marcar a decisão anterior como obsoleta com `add_observations` (ex: `{"status": "superseded-by: ADR-0001"}`).
- O Tech Lead revisa o estado do grafo no início de cada sprint, removendo entidades obsoletas.
