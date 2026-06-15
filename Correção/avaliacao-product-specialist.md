# Skill de Avaliação — Product Specialist (Cenário 2)

> **Programa:** Trilha de Certificação AI First — DGS / DB1 Global Software
> **Escopo:** Cenário-Âncora 2 — Fase de Estruturação do Trabalho (exercícios 2.1, 2.2, 2.3)
> **Referência:** Usar com `avaliacao-foundation.md` para dimensões e escala.

**Perfil:** Recorta o domínio, escreve specs de produto, formaliza guardrails, e contribui a seção de produto do AGENTS.md. Deve demonstrar que traduz conhecimento de domínio em artefatos consumíveis por humanos e agentes.

**Ferramentas esperadas:** Claude (chat) em todos; Claude Design no exercício 2.1.

---

## Exercício 2.1 — Recorte de domínio e spec SDD do query endpoint

**Tópicos avaliados:** Recorte de Domínio (bounded contexts, linguagem ubíqua), SDD (requirements.md).

**Exercício central de domain recorte da trilha. Avaliar com rigor em D1.**

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Bounded contexts coerentes | Divisões por domínio de negócio (Atendimento, Frete, Devoluções, SLAs), não por camada técnica (frontend/backend) | Contextos técnicos ou apenas 1 contexto |
| Linguagem ubíqua útil | Termos que LLM confundiria sem definição: "Gold = tier de cliente", "carga perigosa = classes 1-6 ANTT", "frete especial = acima de 500kg" | Termos óbvios: "cliente = quem contrata" |
| Linguagem extraída do Anexo A | Termos derivados da documentação real, não inventados | Glossário sem conexão com os documentos |
| Outcomes orientados a resultado | "Atendente recebe resposta em < 30s" (resultado) vs "endpoint retorna JSON" (feature) | Outcomes são features técnicas |
| Scope boundaries derivados dos bounded contexts | "Este módulo cobre Atendimento — não cobre Gestão Documental" | Scope genérico sem relação com os bounded contexts |
| Verification criteria testáveis | QA escreve teste para cada critério (binário: passou/não) | "Resposta deve ser boa" |
| Mockup (Claude Design) | Coerente com requirements, mostra fonte + confiança + feedback | Desconectado ou ausente |
| Prior decisions referenciam cenário 1 | Menciona ADRs, context budget, tratamento de contradições | Ignora decisões anteriores |
| Iteração com "Tech Lead" (Claude) | Feedback sobre ambiguidades incorporado na versão final | Sem iteração |

---

## Exercício 2.2 — Guardrails formalizados

**Tópicos avaliados:** AGENTS.md (artefatos prescritivos), Harness (enforcement probabilístico vs determinístico — preview).

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| 3 categorias presentes | DEVE + NÃO DEVE + QUANDO EM DÚVIDA, todas populadas | Apenas DEVE, ou lista sem categorias |
| Classificação prompt vs código | Cada guardrail classificado com justificativa. Ex: "citar fonte = prompt + validação de source_document em código" | Sem classificação, ou tudo no prompt |
| Rastreabilidade aos 3 incidentes | Cada guardrail mapeia a ao menos 1 incidente que previne | Guardrails sem conexão com incidentes |
| Específicos ao domínio NovaTech | Referencia carga perigosa, tiers, multiplicadores, versões de documentos | Guardrails genéricos de chatbot |

---

## Exercício 2.3 — Seção "Product Rules & Guardrails" do AGENTS.md

**Tópicos avaliados:** AGENTS.md (machine-readable), Skills (glossário consumível por agentes).

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Machine-readable | Regras prescritivas, glossário parsável, referências a paths do repo | Texto narrativo |
| Glossário conectado ao recorte de domínio | Termos consistentes com bounded contexts e linguagem ubíqua do exercício 2.1 (ou do input simulado) | Glossário desconectado |
| Restrições de código concretas | "Toda resposta DEVE incluir campo `source_document`" — influencia Copilot | Restrições vagas |
| Consistente com guardrails fornecidos | Os guardrails simulados (DEVE/NÃO DEVE/QUANDO EM DÚVIDA) estão refletidos | Contradiz os guardrails |
