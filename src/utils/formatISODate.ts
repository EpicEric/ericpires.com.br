import { format } from "date-fns";

export function formatISODate(date?: string | Date) {
  if (!date) {
    return "????-??-??";
  }
  date = new Date(date);
  return format(
    new Date(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()),
    "yyyy-MM-dd"
  );
}
