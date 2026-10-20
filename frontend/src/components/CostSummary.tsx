import { kzt } from "../lib/format";
import type { FurnitureItem, PlacedItem } from "../lib/types";

export function CostSummary({ placed, items, budget }: { placed: PlacedItem[]; items: Record<string, FurnitureItem>; budget: number }) {
  const total = placed.reduce((sum, p) => sum + (items[p.item_id]?.price ?? 0), 0);
  const over = total > budget;
  return (
    <span className={over ? "cost over" : "cost"}>
      {placed.length} items · <b>{kzt(total)}</b> of {kzt(budget)}
      {over && ` · ${kzt(total - budget)} over budget`}
    </span>
  );
}
