import { app, HttpRequest, HttpResponseInit } from "@azure/functions";
import { CosmosClient } from "@azure/cosmos";
import { logger } from "../../shared/logger.js";
import { feedbackInputSchema } from "./validator.js";

const cosmosClient = new CosmosClient(process.env.COSMOS_CONNECTION_STRING ?? "");
const feedbackContainer = cosmosClient.database("novatech").container("feedbacks");

export async function feedbackHandler(request: HttpRequest): Promise<HttpResponseInit> {
  let rawBody: unknown;
  try {
    rawBody = await request.json();
  } catch {
    return { status: 400, jsonBody: { error: "Corpo da requisição não é um JSON válido." } };
  }

  const parsed = feedbackInputSchema.safeParse(rawBody);
  if (!parsed.success) {
    logger.warn({ issues: parsed.error.issues }, "Feedback rejeitado na validação");
    return { status: 400, jsonBody: { error: "Payload de feedback inválido.", issues: parsed.error.issues } };
  }

  const feedback = {
    ...parsed.data,
    timestamp: new Date().toISOString(),
  };

  try {
    await feedbackContainer.items.create(feedback);
  } catch (err) {
    logger.error({ err }, "Falha ao persistir feedback no Cosmos DB");
    return { status: 500, jsonBody: { error: "Não foi possível registrar o feedback." } };
  }

  logger.info({ feedback }, "Feedback recebido");

  return { status: 201, jsonBody: { status: "ok" } };
}

app.http("feedback", {
  methods: ["POST"],
  handler: feedbackHandler,
});
