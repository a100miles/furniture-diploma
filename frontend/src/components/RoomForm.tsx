import type { Room, RoomType, Style, Wall } from "../lib/types";
import { ROOM_TYPES, STYLES } from "../lib/types";

interface Props {
  room: Room;
  onRoomChange: (room: Room) => void;
  roomType: RoomType;
  onRoomTypeChange: (t: RoomType) => void;
  style: Style;
  onStyleChange: (s: Style) => void;
  budget: number;
  onBudgetChange: (b: number) => void;
}

const WALLS: Wall[] = ["back", "front", "left", "right"];

export function RoomForm({ room, onRoomChange, roomType, onRoomTypeChange, style, onStyleChange, budget, onBudgetChange }: Props) {
  const num = (key: "width" | "length" | "height", min: number, max: number) => (
    <label>
      {key[0].toUpperCase() + key.slice(1)} (m)
      <input
        type="number"
        step={0.1}
        min={min}
        max={max}
        value={room[key]}
        onChange={(e) => {
          const v = Number(e.target.value);
          if (v >= min && v <= max) onRoomChange({ ...room, [key]: v });
        }}
      />
    </label>
  );
  const door = room.doors[0];

  return (
    <section className="panel">
      <h2>1. Room</h2>
      <div className="row">
        {num("width", 2, 10)}
        {num("length", 2, 10)}
        {num("height", 2.2, 4)}
      </div>
      <div className="row">
        <label>
          Door wall
          <select
            value={door?.wall ?? "none"}
            onChange={(e) =>
              onRoomChange({
                ...room,
                doors: e.target.value === "none" ? [] : [{ wall: e.target.value as Wall, offset: door?.offset ?? 0.6, width: 0.9 }],
              })
            }
          >
            <option value="none">No door</option>
            {WALLS.map((w) => (
              <option key={w} value={w}>{w}</option>
            ))}
          </select>
        </label>
        {door && (
          <label>
            Door offset (m)
            <input
              type="number"
              step={0.1}
              min={0.45}
              value={door.offset}
              onChange={(e) => onRoomChange({ ...room, doors: [{ ...door, offset: Number(e.target.value) }] })}
            />
          </label>
        )}
      </div>
      <h2>2. Preferences</h2>
      <div className="row">
        <label>
          Room type
          <select value={roomType} onChange={(e) => onRoomTypeChange(e.target.value as RoomType)}>
            {ROOM_TYPES.map((t) => (
              <option key={t.value} value={t.value}>{t.label}</option>
            ))}
          </select>
        </label>
        <label>
          Style
          <select value={style} onChange={(e) => onStyleChange(e.target.value as Style)}>
            {STYLES.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </label>
      </div>
      <label>
        Budget (₸)
        <input type="number" step={10000} min={10000} value={budget} onChange={(e) => onBudgetChange(Number(e.target.value))} />
      </label>
    </section>
  );
}
