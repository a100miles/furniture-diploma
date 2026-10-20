import type { FurnitureItem, LayoutResponse, Placement, RecommendationResponse, Room, RoomType, Style } from "./types";

const BASE = import.meta.env.VITE_API_URL ?? "";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    throw new Error(`${res.status} ${res.statusText}: ${await res.text()}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  catalog: () => request<FurnitureItem[]>("/api/catalog"),
  recommend: (body: { room: Room; room_type: RoomType; style: Style; budget: number }) =>
    request<RecommendationResponse>("/api/recommendations", { method: "POST", body: JSON.stringify(body) }),
  layout: (room: Room, item_ids: string[]) =>
    request<LayoutResponse>("/api/layout", { method: "POST", body: JSON.stringify({ room, item_ids }) }),
  saveProject: (body: { name: string; room: Room; placements: Placement[]; style: Style; budget: number }) =>
    request<{ id: string }>("/api/projects", { method: "POST", body: JSON.stringify(body) }),
  loadProject: (id: string) =>
    request<{ id: string; name: string; room: Room; placements: Placement[]; style: Style | null; budget: number | null }>(
      `/api/projects/${encodeURIComponent(id)}`,
    ),
};
