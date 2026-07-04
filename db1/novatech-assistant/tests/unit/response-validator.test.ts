import { describe, expect, it } from "vitest";
import {
  SAFE_FALLBACK_RESPONSE,
  validateResponse,
} from "../../src/services/response-validator.js";

describe("validateResponse — schema (structured output)", () => {
  it("aceita uma resposta válida", () => {
    const result = validateResponse({
      answer: "O prazo de devolução padrão é de 7 dias úteis.",
      source_document: "POL-001-politica-devolucao.md",
      confidence_score: 0.92,
    });

    expect(result.ok).toBe(true);
    expect(result.response.source_document).toBe(
      "POL-001-politica-devolucao.md",
    );
  });

  it("rejeita quando source_document está ausente (guardrail 1)", () => {
    const result = validateResponse({
      answer: "O prazo de devolução padrão é de 7 dias úteis.",
      confidence_score: 0.92,
    });

    expect(result.ok).toBe(false);
    expect(result.blockedReason).toBe("invalid_schema");
    expect(result.response).toEqual(SAFE_FALLBACK_RESPONSE);
  });

  it("rejeita source_document vazio", () => {
    const result = validateResponse({
      answer: "Resposta qualquer.",
      source_document: "",
      confidence_score: 0.5,
    });

    expect(result.ok).toBe(false);
    expect(result.blockedReason).toBe("invalid_schema");
  });

  it("rejeita confidence_score fora do intervalo [0,1]", () => {
    const result = validateResponse({
      answer: "Resposta qualquer.",
      source_document: "POL-001-politica-devolucao.md",
      confidence_score: 1.5,
    });

    expect(result.ok).toBe(false);
    expect(result.blockedReason).toBe("invalid_schema");
  });

  it("rejeita campos extras não previstos no schema", () => {
    const result = validateResponse({
      answer: "Resposta qualquer.",
      source_document: "POL-001-politica-devolucao.md",
      confidence_score: 0.8,
      sources: ["campo-alucinado.md"],
    });

    expect(result.ok).toBe(false);
    expect(result.blockedReason).toBe("invalid_schema");
  });
});

describe("validateResponse — guardrail carga perigosa + devolução (POL-001 3.2)", () => {
  it("permite a negativa correta (caso normal)", () => {
    const result = validateResponse({
      answer:
        "Cargas perigosas não são elegíveis para devolução pelo processo padrão. Contate a Gestão de Riscos.",
      source_document: "POL-001-politica-devolucao.md",
      confidence_score: 0.95,
    });

    expect(result.ok).toBe(true);
  });

  it("bloqueia quando a resposta afirma que a devolução é possível", () => {
    const result = validateResponse({
      answer: "Sim, cargas perigosas podem ser devolvidas normalmente.",
      source_document: "POL-001-politica-devolucao.md",
      confidence_score: 0.7,
    });

    expect(result.ok).toBe(false);
    expect(result.blockedReason).toBe("dangerous_cargo_return_guardrail");
    expect(result.response).toEqual(SAFE_FALLBACK_RESPONSE);
  });

  it("bloqueia variações de singular/plural e conjugação", () => {
    const result = validateResponse({
      answer: "A carga perigosa pode ser devolvida sem restrições.",
      source_document: "POL-001-politica-devolucao.md",
      confidence_score: 0.6,
    });

    expect(result.ok).toBe(false);
    expect(result.blockedReason).toBe("dangerous_cargo_return_guardrail");
  });

  it("não bloqueia respostas que não mencionam os dois temas juntos", () => {
    const result = validateResponse({
      answer: "O prazo geral de devolução é de 7 dias úteis.",
      source_document: "POL-001-politica-devolucao.md",
      confidence_score: 0.9,
    });

    expect(result.ok).toBe(true);
  });
});
