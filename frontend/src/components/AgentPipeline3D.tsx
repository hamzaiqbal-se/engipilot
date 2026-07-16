"use client";

import { useRef, useMemo } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { OrbitControls, Text, Line, Stars, Html } from "@react-three/drei";
import { EffectComposer, Bloom } from "@react-three/postprocessing";
import * as THREE from "three";

const AGENT_LABELS: Record<string, string> = {
  engineering_agent: "Engineering",
  risk_agent: "Risk",
  planning_agent: "Planning",
  qa_agent: "QA",
  documentation_agent: "Docs",
  reporting_agent: "Reporting",
  automation_agent: "Automation",
};

const AGENT_ORDER = [
  "engineering_agent",
  "risk_agent",
  "planning_agent",
  "qa_agent",
  "documentation_agent",
  "reporting_agent",
  "automation_agent",
];

// Gradient across the pipeline: blue -> purple -> pink
function nodeColor(index: number, total: number) {
  const c1 = new THREE.Color("#3b82f6");
  const c2 = new THREE.Color("#8b5cf6");
  const c3 = new THREE.Color("#ec4899");
  const t = index / (total - 1);
  return t < 0.5 ? c1.clone().lerp(c2, t * 2) : c2.clone().lerp(c3, (t - 0.5) * 2);
}

function FlowParticles({ start, end, color }: { start: [number, number, number]; end: [number, number, number]; color: string }) {
  const particles = useRef<THREE.Mesh[]>([]);
  const count = 3;

  useFrame(({ clock }) => {
    particles.current.forEach((p, i) => {
      if (!p) return;
      const t = ((clock.getElapsedTime() * 0.4 + i / count) % 1);
      p.position.lerpVectors(new THREE.Vector3(...start), new THREE.Vector3(...end), t);
      const mat = p.material as THREE.MeshBasicMaterial;
      mat.opacity = Math.sin(t * Math.PI);
    });
  });

  return (
    <>
      {Array.from({ length: count }).map((_, i) => (
        <mesh key={i} ref={(el) => { if (el) particles.current[i] = el; }}>
          <sphereGeometry args={[0.045, 8, 8]} />
          <meshBasicMaterial color={color} transparent opacity={0.8} />
        </mesh>
      ))}
    </>
  );
}

function Node({
  position,
  label,
  active,
  index,
  color,
}: {
  position: [number, number, number];
  label: string;
  active: boolean;
  index: number;
  color: THREE.Color;
}) {
  const coreRef = useRef<THREE.Mesh>(null);
  const glowRef = useRef<THREE.Mesh>(null);

  useFrame(({ clock }) => {
    if (!active) return;
    const pulse = 1 + Math.sin(clock.getElapsedTime() * 2 + index) * 0.1;
    coreRef.current?.scale.setScalar(pulse);
    if (glowRef.current) {
      const glowPulse = 1.3 + Math.sin(clock.getElapsedTime() * 1.5 + index) * 0.15;
      glowRef.current.scale.setScalar(glowPulse);
    }
  });

  const hex = "#" + color.getHexString();

  return (
    <group position={position}>
      {active && (
        <mesh ref={glowRef}>
          <sphereGeometry args={[0.42, 24, 24]} />
          <meshBasicMaterial color={hex} transparent opacity={0.18} />
        </mesh>
      )}
      <mesh ref={coreRef}>
        <sphereGeometry args={[0.28, 32, 32]} />
        <meshStandardMaterial
          color={active ? hex : "#1f2937"}
          emissive={active ? hex : "#000000"}
          emissiveIntensity={active ? 1.1 : 0}
          roughness={0.25}
          metalness={0.6}
        />
      </mesh>
      <Text
        position={[0, -0.72, 0]}
        fontSize={0.13}
        color={active ? "#f1f5f9" : "#64748b"}
        anchorX="center"
        anchorY="middle"
        letterSpacing={0.05}
        outlineWidth={0.008}
        outlineColor="#0a0e17"
        outlineOpacity={0.9}
        fontWeight={active ? 600 : 400}
      >
        {label}
      </Text>
      {active && (
        <Html position={[0, 0.5, 0]} center distanceFactor={8} occlude>
          <div className="px-2 py-0.5 rounded-full text-[9px] font-medium whitespace-nowrap"
               style={{ background: hex + "22", color: hex, border: `1px solid ${hex}55` }}>
            complete
          </div>
        </Html>
      )}
    </group>
  );
}

function Pipeline({ agentTrace }: { agentTrace: string[] }) {
  const groupRef = useRef<THREE.Group>(null);
  const n = AGENT_ORDER.length;

  const positions = useMemo(() => {
    const spacing = 1.3;
    const totalWidth = (n - 1) * spacing;
    return AGENT_ORDER.map((_, i) => {
      const x = i * spacing - totalWidth / 2;
      const z = Math.sin((i / (n - 1)) * Math.PI) * -0.4;
      const y = Math.sin((i / (n - 1)) * Math.PI) * 0.3;
      return [x, y, z] as [number, number, number];
    });
  }, [n]);

  useFrame(({ clock }) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = Math.sin(clock.getElapsedTime() * 0.1) * 0.08;
    }
  });

  return (
    <group ref={groupRef}>
      {positions.slice(0, -1).map((pos, i) => {
        const nextPos = positions[i + 1];
        const bothActive = agentTrace.includes(AGENT_ORDER[i]) && agentTrace.includes(AGENT_ORDER[i + 1]);
        const color = nodeColor(i, n);
        const hex = "#" + color.getHexString();
        return (
          <group key={i}>
            <Line points={[pos, nextPos]} color={bothActive ? hex : "#1f2937"} lineWidth={1.5} transparent opacity={bothActive ? 0.5 : 0.25} />
            {bothActive && <FlowParticles start={pos} end={nextPos} color={hex} />}
          </group>
        );
      })}

      {positions.map((pos, i) => (
        <Node
          key={AGENT_ORDER[i]}
          position={pos}
          label={AGENT_LABELS[AGENT_ORDER[i]]}
          active={agentTrace.includes(AGENT_ORDER[i])}
          index={i}
          color={nodeColor(i, n)}
        />
      ))}
    </group>
  );
}

export default function AgentPipeline3D({ agentTrace }: { agentTrace: string[] }) {
  return (
    <div className="glass-card p-4 h-[300px] md:h-[340px] overflow-hidden relative">
      <div className="absolute top-3 left-4 z-10 pointer-events-none">
        <p className="text-xs text-slate-500 uppercase tracking-wider">Live Agent Pipeline</p>
      </div>
      <Canvas camera={{ position: [0, 2.4, 6.5], fov: 42 }} dpr={[1, 1.5]} gl={{ antialias: true, alpha: true }}>
        <ambientLight intensity={0.4} />
        <pointLight position={[3, 4, 5]} intensity={1} color="#3b82f6" />
        <pointLight position={[-3, 2, -3]} intensity={0.5} color="#ec4899" />
        <Stars radius={20} depth={30} count={800} factor={1.5} fade speed={0.5} />
        <Pipeline agentTrace={agentTrace} />
        <OrbitControls
          enableZoom={false}
          enablePan={false}
          minPolarAngle={Math.PI / 3.5}
          maxPolarAngle={Math.PI / 2.5}
          minAzimuthAngle={-0.35}
          maxAzimuthAngle={0.35}
        />
        <EffectComposer>
          <Bloom intensity={0.6} luminanceThreshold={0.2} luminanceSmoothing={0.9} mipmapBlur />
        </EffectComposer>
      </Canvas>
    </div>
  );
}