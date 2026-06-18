import { app, HttpRequest, HttpResponseInit, InvocationContext } from "@azure/functions";
import { z } from "zod";
import { logger } from "../../shared/logger";

const querySchema = z.object({
  question: z.string().min(1, "Question cannot be empty").max(500, "Question exceeds 500 characters"),
  sessionId: z.string().optional(),
});

export type QueryInput = z.infer<typeof querySchema>;

export async function queryHandler(
  request: HttpRequest,
  context: InvocationContext
): Promise<HttpResponseInit> {
  const log = logger.child({
    functionName: "query",
    invocationId: context.invocationId,
  });

  const startTime = Date.now();

  let body: unknown;
  try {
    body = await request.json();
  } catch {
    log.warn({ path: request.url }, "invalid JSON body received");
    return {
      status: 400,
      jsonBody: {
        error: "VALIDATION_ERROR",
        message: "Request body must be valid JSON",
      },
    };
  }

  const parsed = querySchema.safeParse(body);
  if (!parsed.success) {
    const firstIssue = parsed.error.issues[0];
    log.warn({ issues: parsed.error.issues }, "request validation failed");
    return {
      status: 400,
      jsonBody: {
        error: "VALIDATION_ERROR",
        message: firstIssue.message,
        field: firstIssue.path.join("."),
      },
    };
  }

  const { question, sessionId } = parsed.data;
  log.info({ questionLength: question.length, sessionId }, "query received");

  try {
    // Pipeline: embed → search → buildPrompt → complete → buildResponse
    // TASK-002 through TASK-005 connect here once implemented.
    // Returning 501 explicitly so integration tests fail loudly, not silently.
    log.warn("query pipeline not yet implemented — returning 501");
    return {
      status: 501,
      jsonBody: {
        error: "NOT_IMPLEMENTED",
        message: "Query pipeline is not yet connected. Pending TASK-002 through TASK-005.",
      },
    };
  } catch (error) {
    // Never expose stack traces to callers.
    log.error({ err: error }, "unhandled error in query handler");
    return {
      status: 500,
      jsonBody: {
        error: "INTERNAL_ERROR",
        message: "An unexpected error occurred. Please try again later.",
      },
    };
  } finally {
    log.info({ durationMs: Date.now() - startTime }, "query handler completed");
  }
}

app.http("query", {
  methods: ["POST"],
  // authLevel "function" requires x-functions-key header in production.
  // Override to "anonymous" only for local test environments via env var.
  authLevel: (process.env.FUNCTIONS_AUTH_LEVEL as "function" | "anonymous") ?? "function",
  route: "query",
  handler: queryHandler,
});
