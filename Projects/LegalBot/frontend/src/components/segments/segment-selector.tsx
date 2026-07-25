"use client";

import { useState } from "react";

const SEGMENTS = [
  { id: "s1-consumer", name: "Consumer & E-commerce", icon: "🛒" },
  { id: "s2-property", name: "Property & Land", icon: "🏠" },
  { id: "s3-family", name: "Family Law", icon: "👨‍👩‍👧" },
  { id: "s4-cybercrime", name: "Cybercrime", icon: "💻" },
  { id: "s5-employment", name: "Employment", icon: "💼" },
  { id: "s6-police", name: "Police & FIR", icon: "👮" },
  { id: "s7-women-child", name: "Women & Child Safety", icon: "🛡️" },
  { id: "s8-seniors", name: "Senior Citizens", icon: "👴" },
  { id: "s9-rti", name: "RTI & Govt", icon: "📋" },
  { id: "s10-msme", name: "MSME & Business", icon: "🏢" },
];

export function SegmentSelector() {
  const [selected, setSelected] = useState<string | null>(null);

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Choose Your Legal Issue</h2>
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        {SEGMENTS.map((segment) => (
          <button
            key={segment.id}
            onClick={() => setSelected(segment.id)}
            className={`p-4 rounded-lg border-2 transition-all ${
              selected === segment.id
                ? "border-blue-600 bg-blue-50"
                : "border-gray-200 hover:border-gray-300 bg-white"
            }`}
          >
            <div className="text-3xl mb-2">{segment.icon}</div>
            <div className="text-sm font-medium">{segment.name}</div>
          </button>
        ))}
      </div>
    </div>
  );
}
