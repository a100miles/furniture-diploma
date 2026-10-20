import { kzt, label } from "../lib/format";
import type { FurnitureItem, RecommendationResponse } from "../lib/types";

interface Props {
  recs: RecommendationResponse;
  onAdd: (item: FurnitureItem) => void;
  onPlaceBundle: () => void;
  busy: boolean;
}

export function RecommendationPanel({ recs, onAdd, onPlaceBundle, busy }: Props) {
  return (
    <section className="panel">
      <h2>3. Recommendations</h2>
      <div className={recs.within_budget ? "bundle ok" : "bundle over"}>
        <div>
          Suggested set: <b>{kzt(recs.bundle_price)}</b> {recs.within_budget ? "· within budget" : "· over budget"}
        </div>
        <button className="primary" onClick={onPlaceBundle} disabled={busy || !recs.bundle.length}>
          Place set &amp; auto-arrange
        </button>
      </div>
      {recs.categories.map((c) => (
        <div key={c.category} className="category">
          <h3>{label(c.category)}</h3>
          {c.options.length === 0 && <p className="muted">Nothing fits this room and budget.</p>}
          {c.options.map((r) => (
            <div key={r.item.id} className={`card ${recs.bundle.includes(r.item.id) ? "in-bundle" : ""}`}>
              <div className="card-head">
                <span className="swatch" style={{ background: r.item.color }} />
                <b>{r.item.name}</b>
                <span className="score" title="Match score">{Math.round(r.score * 100)}%</span>
              </div>
              <ul className="reasons">
                {r.reasons.map((reason) => (
                  <li key={reason}>{reason}</li>
                ))}
              </ul>
              <div className="card-foot">
                <span>{kzt(r.item.price)} · {r.item.width}×{r.item.depth} m</span>
                <button onClick={() => onAdd(r.item)}>Add</button>
              </div>
            </div>
          ))}
        </div>
      ))}
    </section>
  );
}
