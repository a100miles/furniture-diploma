import { describe, expect, it } from "vitest";
import { footprint, invalidIndices, snapInside } from "./geometry";
import type { FurnitureItem, Room } from "./types";

const sofa: FurnitureItem = {
  id: "sofa", name: "Sofa", category: "sofa", styles: ["modern"],
  width: 2, depth: 0.9, height: 0.8, price: 1, color: "#000", against_wall: true,
};
const table: FurnitureItem = { ...sofa, id: "table", category: "coffee_table", width: 1, depth: 0.6 };
const items = { sofa, table };
const room: Room = { width: 4, length: 3.5, height: 2.7, doors: [] };

describe("geometry", () => {
  it("rotates footprints", () => {
    const r = footprint(sofa, { item_id: "sofa", x: 2, z: 2, rotation: 90 });
    expect(r.x1 - r.x0).toBeCloseTo(0.9);
    expect(r.z1 - r.z0).toBeCloseTo(2);
  });

  it("flags overlaps and out-of-bounds, accepts valid layouts", () => {
    const valid = [
      { item_id: "sofa", x: 2, z: 0.45, rotation: 0 },
      { item_id: "table", x: 2, z: 1.5, rotation: 0 },
    ];
    expect(invalidIndices(room, valid, items).size).toBe(0);
    const overlap = [valid[0], { item_id: "table", x: 2, z: 0.8, rotation: 0 }];
    expect([...invalidIndices(room, overlap, items)]).toEqual([0, 1]);
    const outside = [{ item_id: "sofa", x: 0.2, z: 0.45, rotation: 0 }];
    expect([...invalidIndices(room, outside, items)]).toEqual([0]);
  });

  it("flags items in a door swing zone", () => {
    const withDoor: Room = { ...room, doors: [{ wall: "back", offset: 2, width: 0.9 }] };
    expect(invalidIndices(withDoor, [{ item_id: "table", x: 2, z: 0.3, rotation: 0 }], items).size).toBe(1);
  });

  it("snaps and clamps inside the room", () => {
    expect(snapInside(sofa, room, -3, 1.234, 0)).toEqual([1, 1.25]);
  });
});
