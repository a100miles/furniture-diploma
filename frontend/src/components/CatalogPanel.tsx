import { useMemo, useState } from "react";
import { kzt, label } from "../lib/format";
import type { FurnitureItem } from "../lib/types";

// The parsed store catalog has thousands of items; render only the first matches.
const MAX_SHOWN = 100;

export function CatalogPanel({ catalog, onAdd }: { catalog: FurnitureItem[]; onAdd: (item: FurnitureItem) => void }) {
  const [category, setCategory] = useState("all");
  const [query, setQuery] = useState("");
  const categories = useMemo(() => [...new Set(catalog.map((i) => i.category))].sort(), [catalog]);
  const matches = useMemo(() => {
    const q = query.trim().toLowerCase();
    return catalog.filter((i) => (category === "all" || i.category === category) && (!q || i.name.toLowerCase().includes(q)));
  }, [catalog, category, query]);
  const shown = matches.slice(0, MAX_SHOWN);

  return (
    <section className="panel">
      <h2>Catalog</h2>
      <select value={category} onChange={(e) => setCategory(e.target.value)}>
        <option value="all">All categories</option>
        {categories.map((c) => (
          <option key={c} value={c}>{label(c)}</option>
        ))}
      </select>
      <input type="search" placeholder="Search by name" value={query} onChange={(e) => setQuery(e.target.value)} />
      <small>
        {matches.length > MAX_SHOWN ? `Showing ${MAX_SHOWN} of ${matches.length}` : `${matches.length} items`}
      </small>
      <ul className="catalog">
        {shown.map((i) => (
          <li key={i.id}>
            <span className="swatch" style={{ background: i.color }} />
            <span className="grow">
              {i.url ? <a href={i.url} target="_blank" rel="noreferrer">{i.name}</a> : i.name}
              <small>{i.styles.join(", ")} · {kzt(i.price)}</small>
            </span>
            <button onClick={() => onAdd(i)}>Add</button>
          </li>
        ))}
      </ul>
    </section>
  );
}
