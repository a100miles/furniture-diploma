import { useCallback, useEffect, useMemo, useState } from "react";
import { Scene } from "./components/Scene";
import { RoomForm } from "./components/RoomForm";
import { RecommendationPanel } from "./components/RecommendationPanel";
import { CatalogPanel } from "./components/CatalogPanel";
import { CostSummary } from "./components/CostSummary";
import { api } from "./lib/api";
import { invalidIndices, snapInside } from "./lib/geometry";
import type { FurnitureItem, PlacedItem, Placement, RecommendationResponse, Room, RoomType, Style } from "./lib/types";

let nextUid = 1;
const withUid = (p: Placement): PlacedItem => ({ ...p, uid: `p${nextUid++}` });

export default function App() {
  const [room, setRoom] = useState<Room>({ width: 4, length: 3.5, height: 2.7, doors: [{ wall: "front", offset: 0.6, width: 0.9 }] });
  const [roomType, setRoomType] = useState<RoomType>("living_room");
  const [style, setStyle] = useState<Style>("scandinavian");
  const [budget, setBudget] = useState(600000);
  const [catalog, setCatalog] = useState<FurnitureItem[]>([]);
  const [placed, setPlaced] = useState<PlacedItem[]>([]);
  const [selected, setSelected] = useState<string | null>(null);
  const [recs, setRecs] = useState<RecommendationResponse | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const items = useMemo(() => Object.fromEntries(catalog.map((i) => [i.id, i])), [catalog]);
  const invalid = useMemo(() => invalidIndices(room, placed, items), [room, placed, items]);

  useEffect(() => {
    api.catalog().then(setCatalog).catch(() => setMessage("Cannot reach the backend. Start it with: uvicorn app.main:app --reload"));
  }, []);

  const run = async (label: string, fn: () => Promise<void>) => {
    setBusy(true);
    setMessage(null);
    try {
      await fn();
    } catch (e) {
      setMessage(`${label} failed: ${(e as Error).message}`);
    } finally {
      setBusy(false);
    }
  };

  const addItem = useCallback(
    (item: FurnitureItem) => {
      const [x, z] = snapInside(item, room, room.width / 2, room.length / 2, 0);
      const p = withUid({ item_id: item.id, x, z, rotation: 0 });
      setPlaced((prev) => [...prev, p]);
      setSelected(p.uid);
    },
    [room],
  );

  const getRecommendations = () =>
    run("Recommendation", async () => setRecs(await api.recommend({ room, room_type: roomType, style, budget })));

  const autoLayout = (ids: string[]) =>
    run("Auto-layout", async () => {
      const res = await api.layout(room, ids);
      setPlaced(res.placements.map(withUid));
      setSelected(null);
      if (res.unplaced.length) {
        setMessage(`Not enough free space for: ${res.unplaced.map((id) => items[id]?.name ?? id).join(", ")}`);
      }
    });

  const rotateSelected = () =>
    setPlaced((prev) =>
      prev.map((p) => {
        if (p.uid !== selected) return p;
        const rotation = (p.rotation + 90) % 360;
        const [x, z] = snapInside(items[p.item_id], room, p.x, p.z, rotation);
        return { ...p, rotation, x, z };
      }),
    );

  const removeSelected = () => {
    setPlaced((prev) => prev.filter((p) => p.uid !== selected));
    setSelected(null);
  };

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (!selected || (e.target as HTMLElement).tagName === "INPUT") return;
      if (e.key === "r" || e.key === "R") rotateSelected();
      if (e.key === "Delete" || e.key === "Backspace") removeSelected();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  });

  const save = () =>
    run("Save", async () => {
      const placements = placed.map(({ uid: _uid, ...p }) => p);
      const res = await api.saveProject({ name: "My room", room, placements, style, budget });
      setMessage(`Saved. Project id: ${res.id}`);
    });

  const load = () => {
    const id = window.prompt("Project id");
    if (!id) return;
    run("Load", async () => {
      const p = await api.loadProject(id.trim());
      setRoom(p.room);
      setPlaced(p.placements.map(withUid));
      if (p.style) setStyle(p.style);
      if (p.budget) setBudget(p.budget);
    });
  };

  const selectedItem = placed.find((p) => p.uid === selected);

  return (
    <div className="app">
      <aside className="sidebar">
        <h1>AI Furniture Planner</h1>
        <RoomForm
          room={room}
          onRoomChange={(r) => {
            setRoom(r);
            setPlaced((prev) => prev.map((p) => {
              const [x, z] = snapInside(items[p.item_id], r, p.x, p.z, p.rotation);
              return { ...p, x, z };
            }));
          }}
          roomType={roomType}
          onRoomTypeChange={setRoomType}
          style={style}
          onStyleChange={setStyle}
          budget={budget}
          onBudgetChange={setBudget}
        />
        <button className="primary" onClick={getRecommendations} disabled={busy || !catalog.length}>
          ✨ Recommend furniture
        </button>
        {recs && (
          <RecommendationPanel
            recs={recs}
            onAdd={addItem}
            onPlaceBundle={() => autoLayout(recs.bundle)}
            busy={busy}
          />
        )}
        <CatalogPanel catalog={catalog} onAdd={addItem} />
      </aside>

      <main className="viewport">
        <div className="toolbar">
          <button onClick={() => autoLayout(placed.map((p) => p.item_id))} disabled={busy || !placed.length}>
            Auto-arrange
          </button>
          <button onClick={rotateSelected} disabled={!selected}>Rotate (R)</button>
          <button onClick={removeSelected} disabled={!selected}>Remove (Del)</button>
          <span className="spacer" />
          <button onClick={save} disabled={busy}>Save</button>
          <button onClick={load} disabled={busy}>Load</button>
        </div>
        {message && <div className="message">{message}</div>}
        {invalid.size > 0 && <div className="warning">⚠ {invalid.size} item(s) overlap, block a door or leave the room (shown in red)</div>}
        <Scene
          room={room}
          placed={placed}
          items={items}
          invalid={invalid}
          selected={selected}
          onSelect={setSelected}
          onMove={(uid, x, z) => setPlaced((prev) => prev.map((p) => (p.uid === uid ? { ...p, x, z } : p)))}
        />
        <div className="footer">
          {selectedItem ? (
            <span>
              <b>{items[selectedItem.item_id]?.name}</b> · x {selectedItem.x.toFixed(2)} m · z {selectedItem.z.toFixed(2)} m ·{" "}
              {selectedItem.rotation}° — drag to move
            </span>
          ) : (
            <span>Drag furniture to move it · drag empty space to orbit · scroll to zoom</span>
          )}
          <CostSummary placed={placed} items={items} budget={budget} />
        </div>
      </main>
    </div>
  );
}
