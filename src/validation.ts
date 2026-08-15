import { z } from "zod";
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA_PATH = join(__dirname, "..", "data", "dataset.json");

export const CensusRecordSchema = z.object({
  id: z.string(),
  age: z.number().int().min(0).max(120),
  education: z.string(),
  education_num: z.number().int().min(1).max(16),
  occupation: z.string(),
  marital_status: z.string(),
  race: z.string(),
  sex: z.enum(["Male", "Female"]),
  capital_gain: z.number().min(0),
  capital_loss: z.number().min(0),
  hours_per_week: z.number().int().min(0).max(100),
  native_country: z.string(),
  relationship: z.string(),
  income_bracket: z.enum(["<=50K", ">50K"]),
  income_amount: z.number().min(0),
});

export const DatasetSchema = z.array(CensusRecordSchema);
export type CensusRecord = z.infer<typeof CensusRecordSchema>;

export function loadAndValidate(): { valid: CensusRecord[]; errors: z.ZodError[] } {
  const raw = JSON.parse(readFileSync(DATA_PATH, "utf-8"));
  const valid: CensusRecord[] = [];
  const errors: z.ZodError[] = [];
  for (const item of raw) {
    const result = CensusRecordSchema.safeParse(item);
    if (result.success) {
      valid.push(result.data);
    } else {
      errors.push(result.error);
    }
  }
  return { valid, errors };
}

export function validateRecord(record: unknown): record is CensusRecord {
  return CensusRecordSchema.safeParse(record).success;
}
