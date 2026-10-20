import { useRef, useState } from "react";
import { Canvas, type ThreeEvent } from "@react-three/fiber";
import { Grid, OrbitControls } from "@react-three/drei";
import type { OrbitControls as OrbitControlsImpl } from "three-stdlib";
import { doorZone, snapInside } from "../lib/geometry";
import type { FurnitureItem, PlacedItem, Room } from "../lib/types";

interface SceneProps {
  room: Room;
  placed: PlacedItem[];
  items: Record<string, FurnitureItem>;
  invalid: Set<number>;
  selected: string | null;
  onSelect: (uid: string | null) => void;
  onMove: (uid: string, x: number, z: number) => void;
}

const WALL_T = 0.08;

export function Scene({ room, placed, items, invalid, selected, onSelect, onMove }: SceneProps) {
  const controls = useRef<OrbitControlsImpl>(null);
  const [dragging, setDragging] = useState<string | null>(null);
  const cx = room.width / 2;
  const cz = room.length / 2;
  const span = Math.max(room.width, room.length);

  const startDrag = (uid: string) => (e: ThreeEvent<PointerEvent>) => {
    e.stopPropagation();
    onSelect(uid);
    setDragging(uid);
    if (controls.current) controls.current.enabled = false;
  };

  const endDrag = () => {
    setDragging(null);
    if (controls.current) controls.current.enabled = true;
  };

  const onFloorMove = (e: ThreeEvent<PointerEvent>) => {
    if (!dragging) return;
    const p = placed.find((it) => it.uid === dragging);
    const item = p && items[p.item_id];
    if (!p || !item) return;
    const [x, z] = snapInside(item, room, e.point.x, e.point.z, p.rotation);
    onMove(dragging, x, z);
  };

  return (
    <Canvas shadows camera={{ position: [cx + span * 0.9, span * 1.5, cz + span * 1.6], fov: 40 }} onPointerUp={endDrag}>
      <color attach="background" args={["#eef1f5"]} />
      <ambientLight intensity={0.6} />
      <directionalLight position={[cx + 3, 6, cz + 4]} intensity={1.1} castShadow shadow-mapSize={[1024, 1024]} />

      {/* Floor: also the drag plane */}
      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[cx, 0, cz]}
        receiveShadow
        onPointerMove={onFloorMove}
        onPointerDown={(e) => {
          if (!dragging && e.button === 0) onSelect(null);
        }}
      >
        <planeGeometry args={[room.width, room.length]} />
        <meshStandardMaterial color="#d9c7a7" />
      </mesh>
      {/* Larger invisible plane so dragging keeps working near the walls */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[cx, -0.001, cz]} onPointerMove={onFloorMove} visible={false}>
        <planeGeometry args={[room.width * 3, room.length * 3]} />
        <meshBasicMaterial />
      </mesh>
      <Grid
        position={[cx, 0.002, cz]}
        args={[room.width, room.length]}
        cellSize={0.5}
        sectionSize={1}
        cellColor="#b8a688"
        sectionColor="#8f7d60"
        fadeDistance={50}
      />

      <Walls room={room} />

      {room.doors.map((door, i) => {
        const z = doorZone(room, door);
        return (
          <mesh key={i} rotation={[-Math.PI / 2, 0, 0]} position={[(z.x0 + z.x1) / 2, 0.004, (z.z0 + z.z1) / 2]}>
            <planeGeometry args={[z.x1 - z.x0, z.z1 - z.z0]} />
            <meshBasicMaterial color="#4f8edc" transparent opacity={0.25} />
          </mesh>
        );
      })}

      {placed.map((p, i) => {
        const item = items[p.item_id];
        if (!item) return null;
        return (
          <FurnitureMesh
            key={p.uid}
            item={item}
            placement={p}
            invalid={invalid.has(i)}
            selected={selected === p.uid}
            onPointerDown={startDrag(p.uid)}
          />
        );
      })}

      <OrbitControls ref={controls} target={[cx, 0, cz]} maxPolarAngle={Math.PI / 2.1} makeDefault />
    </Canvas>
  );
}

function Walls({ room }: { room: Room }) {
  // Back and left walls are full height; front and right are drawn low so they
  // never hide the furniture from the default camera.
  const low = 0.12;
  const segments: [number, number, number, number, number][] = [
    // x, z, sizeX, sizeZ, height
    [room.width / 2, -WALL_T / 2, room.width + 2 * WALL_T, WALL_T, room.height],
    [-WALL_T / 2, room.length / 2, WALL_T, room.length, room.height],
    [room.width / 2, room.length + WALL_T / 2, room.width + 2 * WALL_T, WALL_T, low],
    [room.width + WALL_T / 2, room.length / 2, WALL_T, room.length, low],
  ];
  return (
    <>
      {segments.map(([x, z, sx, sz, h], i) => (
        <mesh key={i} position={[x, h / 2, z]} receiveShadow>
          <boxGeometry args={[sx, h, sz]} />
          <meshStandardMaterial color="#f4f1ec" />
        </mesh>
      ))}
    </>
  );
}

interface FurnitureMeshProps {
  item: FurnitureItem;
  placement: PlacedItem;
  invalid: boolean;
  selected: boolean;
  onPointerDown: (e: ThreeEvent<PointerEvent>) => void;
}

function FurnitureMesh({ item, placement, invalid, selected, onPointerDown }: FurnitureMeshProps) {
  const rotationY = (placement.rotation * Math.PI) / 180;
  return (
    <group position={[placement.x, 0, placement.z]} rotation={[0, rotationY, 0]} onPointerDown={onPointerDown}>
      <mesh position={[0, item.height / 2, 0]} castShadow>
        <boxGeometry args={[item.width, item.height, item.depth]} />
        <meshStandardMaterial
          color={item.color}
          emissive={invalid ? "#d62828" : selected ? "#2a6fdb" : "#000000"}
          emissiveIntensity={invalid || selected ? 0.45 : 0}
        />
      </mesh>
      {/* Front marker so the orientation is visible */}
      <mesh position={[0, item.height * 0.5, item.depth / 2 + 0.005]}>
        <planeGeometry args={[item.width * 0.6, Math.min(0.08, item.height * 0.2)]} />
        <meshBasicMaterial color="#ffffff" />
      </mesh>
    </group>
  );
}
