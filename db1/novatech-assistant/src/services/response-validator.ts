import { z } from "zod";
import { logger } from "../shared/logger.js";

/**
 * Structured output contract for assistant responses (Ex. 3.1).
 * `.strict()` rejects unknown fields instead of silently dropping them —
 * an extra field from the model (e.g. a hallucinated `sources` array) is
 * itself a signal something is off with the completion and should fail loud.
 */
export const structuredResponseSchema = z.object({
  answer: z.string().min(1, "answer não pode ser vazio"),
  source_document: z.string().min(1, "source_document não pode ser vazio"),
  confidence_score: z.number().min(0).max(1),
}).strict();

export type StructuredResponse = z.infer<typeof structuredResponseSchema>;

export const SAFE_FALLBACK_RESPONSE: StructuredResponse = {
  answer:
    "Não foi possível validar esta resposta com segurança. Por favor, contate um atendente humano.",
  source_document: "N/A",
  confidence_score: 0,
};

export interface ValidationResult {
  ok: boolean;
  response: StructuredResponse;
  blockedReason?: string;
}

/**
 * Matches "carga(s) perigosa(s)" and "devolu(ção|ções|ir|ida)" anywhere in the
 * text, independent of order, case or accents — the guardrail must catch the
 * combination however the model phrases it, not just the literal seed phrase.
 */
const DANGEROUS_CARGO_PATTERN = /carga[s]?\s+perigosa[s]?/i;
const RETURN_PATTERN = /devolu[cç][aã]o|devolu[cç][oõ]es|devolv|devolut[oó]ri/i;

/**
 * A denial contains an explicit negative near the return/dangerous-cargo
 * language: "não", "não é elegível", "não pode", "vedad[ao]", "não é possível".
 * Without this, an affirmative sentence that merely mentions both keywords
 * (e.g. "cargas perigosas podem ser devolvidas") would pass undetected.
 */
const EXPLICIT_DENIAL_PATTERN = /\b(n[aã]o|vedad[ao]|imposs[ií]vel|indispon[ií]vel)\b/i;

function normalize(text: string): string {
  return text.normalize("NFC");
}

function violatesDangerousCargoGuardrail(answer: string): boolean {
  const text = normalize(answer);
  const mentionsBoth =
    DANGEROUS_CARGO_PATTERN.test(text) && RETURN_PATTERN.test(text);
  if (!mentionsBoth) return false;
  return !EXPLICIT_DENIAL_PATTERN.test(text);
}

/**
 * Applies deterministic guardrails on top of the structured-output schema.
 * The prompt is responsible for getting these right *most* of the time;
 * this function is the backstop for when it doesn't — every failure here
 * is logged with a reason and swapped for a safe, generic response instead
 * of ever reaching the end user or the Teams bot.
 */
export function validateResponse(raw: unknown): ValidationResult {
  const parsed = structuredResponseSchema.safeParse(raw);

  if (!parsed.success) {
    logger.warn(
      { issues: parsed.error.issues },
      "response-validator: schema validation failed",
    );
    return {
      ok: false,
      response: SAFE_FALLBACK_RESPONSE,
      blockedReason: "invalid_schema",
    };
  }

  const response = parsed.data;

  if (violatesDangerousCargoGuardrail(response.answer)) {
    logger.warn(
      { source_document: response.source_document },
      "response-validator: blocked by dangerous-cargo-return guardrail (POL-001 3.2)",
    );
    return {
      ok: false,
      response: SAFE_FALLBACK_RESPONSE,
      blockedReason: "dangerous_cargo_return_guardrail",
    };
  }

  return { ok: true, response };
}
