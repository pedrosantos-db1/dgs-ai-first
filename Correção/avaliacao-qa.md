# Skill de Avaliação — QA (Cenário 2)

> **Programa:** Trilha de Certificação AI First — DGS / DB1 Global Software
> **Escopo:** Cenário-Âncora 2 — Fase de Estruturação do Trabalho (exercícios 2.1, 2.2, 2.3)
> **Referência:** Usar com `avaliacao-foundation.md` para dimensões e escala.

**Perfil:** Define padrões de teste consumíveis por agentes (Testing Standards do AGENTS.md), escreve specs de teste no formato SDD, e cria skills de geração de testes. Demonstra que qualidade de testes gerados por IA depende da qualidade dos padrões que os agentes recebem.

**Ferramentas esperadas:** Claude (chat) em todos; Claude Cowork nos exercícios 2.2 e 2.3.

---

## Exercício 2.1 — Testing Standards para o AGENTS.md

**Tópicos avaliados:** AGENTS.md (seção machine-readable), Skills (padrões de teste).

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Prescritivo para agentes | Copilot que lê esta seção geraria testes melhores que o teste ruim fornecido | Texto narrativo que agente ignoraria |
| Padrão arrange/act/assert | Exigido explicitamente com exemplo | Sem menção a estrutura |
| DEVE e NÃO DEVE claros | "DEVE: assertions específicas ao comportamento. NÃO DEVE: toBeDefined() sozinho" | Apenas recomendações vagas |
| Teste reescrito demonstra padrões | Antes/depois com cada melhoria explicada | Teste reescrito com mesmos problemas |
| 3 critérios de review objetivos | Dois QAs chegariam à mesma conclusão | Critérios subjetivos |

**Verificação rápida do teste reescrito:** O teste original usa `toBeDefined()` e nome genérico. O reescrito deve ter: nome descritivo (describe/it em inglês), arrange/act/assert separados, e assertion que verifica conteúdo da resposta (não apenas existência).

---

## Exercício 2.2 — Spec de testes SDD (query endpoint)

**Tópicos avaliados:** SDD (spec de testes derivada de verification criteria), Harness (testes de robustez de IA).

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Cada VC com 2+ cenários | Happy path + edge case para cada verification criteria | VCs com apenas 1 cenário |
| Dados de teste do domínio | Perguntas: carga perigosa, SLA Gold, frete Manaus — do Anexo A/B | Dados genéricos: "test", "hello" |
| Testes de robustez de IA | Prompt injection, perguntas em inglês, perguntas ambíguas | Sem testes de robustez |
| Rastreabilidade (Cowork) | ID único → VC correspondente. Status rastreável | Sem IDs, sem link para VCs |
| VC-03 exercitado corretamente | Cenário de "carga perigosa + devolução" → negativa explícita | VC-03 com cenário que não exercita o guardrail |

---

## Exercício 2.3 — Skill de geração de testes (`create-integration-test`)

**Tópicos avaliados:** Skills (autoria de artifact skill), AGENTS.md (consistência com Testing Standards).

| Critério | Score 3 | Red flag (≤ 1) |
|----------|---------|-----------------|
| Skill concreta | Template com placeholders, 2 exemplos completos DO/DON'T | Texto abstrato |
| Anti-padrões de IA reais | toBeDefined(), testa implementação (spyOn interno), mocks permissivos demais, dados genéricos | Anti-padrões genéricos de teste |
| Checklist rápido (Cowork) | Verificável em < 2 min, itens sim/não | Checklist demorado ou subjetivo |
| Consistente com Testing Standards | Não contradiz as regras do exercício 2.1 (ou do input simulado) | Contradições |
| Dependências declaradas | Referencia quais skills Foundation/Domain ler antes | Skill isolada sem contexto |
