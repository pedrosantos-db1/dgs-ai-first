import { z } from "zod";

export const feedbackInputSchema = z.object({
  queryId: z.string().min(1),
  rating: z.number().int().min(1).max(5),
  comment: z.string().max(2000).optional(),
  attendantEmail: z.string().email(),
});

export type FeedbackInput = z.infer<typeof feedbackInputSchema>;
