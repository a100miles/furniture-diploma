// Mirrors backend/app/models.py

export type Style = "scandinavian" | "modern" | "classic" | "loft" | "minimalist";
export type RoomType = "living_room" | "bedroom" | "office";
export type Wall = "back" | "front" | "left" | "right";

export interface Door {
  wall: Wall;
  offset: number;
  width: number;
}

export interface Room {
  width: number;
  length: number;
  height: number;
  doors: Door[];
}

export interface FurnitureItem {
  id: string;
  name: string;
  category: string;
  styles: Style[];
  width: number;
  depth: number;
  height: number;
  price: number;
  color: string;
  against_wall: boolean;
}

export interface Placement {
  item_id: string;
  x: number;
  z: number;
  rotation: number;
}

/** A placement in the editor; uid distinguishes two copies of the same item. */
export interface PlacedItem extends Placement {
  uid: string;
}

export interface Violation {
  kind: string;
  item_ids: string[];
  message: string;
}

export interface Recommendation {
  item: FurnitureItem;
  score: number;
  reasons: string[];
}

export interface RecommendationResponse {
  categories: { category: string; options: Recommendation[] }[];
  bundle: string[];
  bundle_price: number;
  within_budget: boolean;
}

export interface LayoutResponse {
  placements: Placement[];
  unplaced: string[];
  violations: Violation[];
}

export const STYLES: Style[] = ["scandinavian", "modern", "classic", "loft", "minimalist"];
export const ROOM_TYPES: { value: RoomType; label: string }[] = [
  { value: "living_room", label: "Living room" },
  { value: "bedroom", label: "Bedroom" },
  { value: "office", label: "Home office" },
];
