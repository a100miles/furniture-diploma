import { useMemo, useState } from "react";
import { kzt, label } from "../lib/format";
import type { FurnitureItem } from "../lib/types";

export function CatalogPanel({ catalog, onAdd }: { catalog: FurnitureItem[]; onAdd: (item: FurnitureItem) => void }) {
  const [category, setCategory] = useState("all");
  const categories = useMemo(() => [...new Set(catalog.map((i) => i.category))].sort(), [catalog]);
  const shown = catalog.filter((i) => category === "all" || i.category === category);

  return (
    <section className="panel">
      <h2>Catalog</h2>
      <select value={category} onChange={(e) => setCategory(e.target.value)}>
        <option value="all">All categories</option>
        {categories.map((c) => (
          <option key={c} value={c}>{label(c)}</option>
        ))}
      </select>
      <ul className="catalog">
        {shown.map((i) => (
          <li key={i.id}>
            <span className="swatch" style={{ background: i.color }} />
            <span className="grow">
              {i.name}
              <small>{i.styles.join(", ")} · {kzt(i.price)}</small>
            </span>
            <button onClick={() => onAdd(i)}>Add</button>
          </li>
        ))}
      </ul>
    </section>
  );
}
