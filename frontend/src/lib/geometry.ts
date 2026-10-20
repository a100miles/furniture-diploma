// Client-side mirror of backend/app/geometry.py, used for instant feedback while dragging.
import type { Door, FurnitureItem, Placement, Room } from "./types";

export interface Rect {
  x0: number;
  z0: number;
  x1: number;
  z1: number;
}

const EPS = 1e-6;

export function footprintSize(item: FurnitureItem, rotation: number): [number, number] {
  return rotation % 180 === 0 ? [item.width, item.depth] : [item.depth, item.width];
}

export function footprint(item: FurnitureItem, p: Placement): Rect {
  const [sx, sz] = footprintSize(item, p.rotation);
  return { x0: p.x - sx / 2, z0: p.z - sz / 2, x1: p.x + sx / 2, z1: p.z + sz / 2 };
}

export function intersects(a: Rect, b: Rect): boolean {
  return a.x0 < b.x1 - EPS && b.x0 < a.x1 - EPS && a.z0 < b.z1 - EPS && b.z0 < a.z1 - EPS;
}

export function inside(r: Rect, room: Room): boolean {
  return r.x0 >= -EPS && r.z0 >= -EPS && r.x1 <= room.width + EPS && r.z1 <= room.length + EPS;
}

export function doorZone(room: Room, door: Door): Rect {
  const h = door.width / 2;
  const d = door.width;
  switch (door.wall) {
    case "back":
      return { x0: door.offset - h, z0: 0, x1: door.offset + h, z1: d };
    case "front":
      return { x0: door.offset - h, z0: room.length - d, x1: door.offset + h, z1: room.length };
    case "left":
      return { x0: 0, z0: door.offset - h, x1: d, z1: door.offset + h };
    case "right":
      return { x0: room.width - d, z0: door.offset - h, x1: room.width, z1: door.offset + h };
  }
}

/** Returns the indices of placements that break a hard constraint. */
export function invalidIndices(room: Room, placements: Placement[], items: Record<string, FurnitureItem>): Set<number> {
  const bad = new Set<number>();
  const rects = placements.map((p) => (items[p.item_id] ? footprint(items[p.item_id], p) : null));
  const doors = room.doors.map((d) => doorZone(room, d));
  rects.forEach((r, i) => {
    if (!r) return;
    if (!inside(r, room) || doors.some((d) => intersects(r, d))) bad.add(i);
    for (let j = i + 1; j < rects.length; j++) {
      const o = rects[j];
      if (o && intersects(r, o)) {
        bad.add(i);
        bad.add(j);
      }
    }
  });
  return bad;
}

/** Snap to a 5 cm grid and clamp the item inside the room. */
export function snapInside(item: FurnitureItem, room: Room, x: number, z: number, rotation: number): [number, number] {
  const [sx, sz] = footprintSize(item, rotation);
  const snap = (v: number) => Math.round(v / 0.05) * 0.05;
  const clamp = (v: number, lo: number, hi: number) => Math.min(Math.max(v, lo), hi);
  return [clamp(snap(x), sx / 2, room.width - sx / 2), clamp(snap(z), sz / 2, room.length - sz / 2)];
}
