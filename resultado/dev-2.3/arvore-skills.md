# Exercício 2.3 — Estratégia de Skills do Projeto NovaTech Assistant

---

## 1. Árvore de Skills (Foundation → Domain → Artifact)

```
skills/
├── foundation/
│   ├── typescript-conventions.md      ← BASE: consumida por todas as outras skills
│   ├── error-handling.md
│   └── project-structure.md
│
├── domain/
│   ├── azure-functions-endpoint.md
│   ├── azure-ai-search-integration.md
│   ├── react-components.md
│   └── testing-patterns.md
│
└── artifact/
    ├── create-rag-endpoint.md
    ├── create-integration-test.md
    └── create-react-card.md
```

---

## 2. Mapeamento de Skills — Criação e Consumo

### Foundation

| Skill | Descrição / Frase-ativação | Quem cria | Quem consome | Agentes | Frequência |
|---|---|---|---|---|---|
| `typescript-conventions` | "Gere código TypeScript seguindo as convenções do projeto NovaTech" | Tech Lead | Todos os devs | Copilot, Claude Code | Toda geração de código |
| `error-handling` | "Adicione tratamento de erro robusto a este módulo" | Tech Lead | Dev Pleno, Dev Sênior | Copilot, Claude Code | Toda função com chamada externa |
| `project-structure` | "Crie um novo módulo/service seguindo a estrutura do repositório" | Tech Lead | Todos os devs | Copilot, Claude Code | Ao criar novos arquivos/módulos |

### Domain

| Skill | Descrição / Frase-ativação | Quem cria | Quem consome | Agentes | Frequência |
|---|---|---|---|---|---|
| `azure-functions-endpoint` | "Crie um Azure Function HTTP trigger seguindo o padrão do projeto" | Tech Lead | Dev Pleno, Dev Sênior | Copilot, Claude Code | A cada novo endpoint (5+ previstos) |
| `azure-ai-search-integration` | "Implemente a integração com Azure AI Search para busca por embedding" | Dev Sênior | Dev Pleno, Dev Sênior | Copilot, Claude Code | Para cada serviço que acessa o índice |
| `react-components` | "Crie um componente React para o painel web seguindo os padrões do projeto" | Dev Sênior | Dev Pleno | Copilot | Para cada novo componente do dashboard |
| `testing-patterns` | "Escreva testes para este módulo seguindo os padrões de teste do projeto" | QA + Dev Sênior | Dev Pleno, Dev Sênior, QA | Copilot, Claude Code | Para cada módulo implementado |

### Artifact

| Skill | Descrição / Frase-ativação | Quem cria | Quem consome | Agentes | Frequência |
|---|---|---|---|---|---|
| `create-rag-endpoint` | "Crie um endpoint RAG completo para o assistente NovaTech" | Tech Lead + Dev Sênior | Dev Pleno, Dev Sênior | Copilot, Claude Code | Alta — cada novo endpoint do assistente |
| `create-integration-test` | "Crie testes de integração para este endpoint/serviço" | QA + Dev Sênior | Dev Pleno, Dev Sênior, QA | Copilot, Claude Code | Alta — para cada módulo entregue |
| `create-react-card` | "Crie um card de resposta React para o painel web" | Dev Sênior | Dev Pleno | Copilot | Média — para cada tipo de resposta exibida |

---

## 3. Relação de Dependência entre Skills

```
create-rag-endpoint
  └── depende de: azure-functions-endpoint
        └── depende de: typescript-conventions, error-handling, project-structure

create-integration-test
  └── depende de: testing-patterns
        └── depende de: typescript-conventions, project-structure

create-react-card
  └── depende de: react-components
        └── depende de: typescript-conventions, project-structure

azure-ai-search-integration
  └── depende de: error-handling, typescript-conventions
```

---

## 4. Skill mais importante do nível Foundation

A skill `typescript-conventions` é a base de toda a hierarquia. Toda outra skill assume que o agente já a leu. É a única que todos os agentes consomem em toda geração de código.

---
