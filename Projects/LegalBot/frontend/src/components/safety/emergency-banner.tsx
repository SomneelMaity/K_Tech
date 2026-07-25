"use client";

import { useState } from "react";
import { AlertCircle, X } from "lucide-react";

export function EmergencyBanner() {
  const [isVisible, setIsVisible] = useState(false);

  // In production, this would be shown when emergency is detected
  if (!isVisible) return null;

  return (
    <div className="bg-red-600 text-white px-4 py-3 emergency-pulse">
      <div className="container mx-auto flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <AlertCircle size={24} />
          <div>
            <p className="font-semibold">Emergency Detected</p>
            <p className="text-sm">
              For immediate help, call: 
              <a href="tel:112" className="ml-2 underline font-bold">112 (Police)</a> |
              <a href="tel:181" className="ml-2 underline font-bold">181 (Women)</a> |
              <a href="tel:1930" className="ml-2 underline font-bold">1930 (Cyber)</a>
            </p>
          </div>
        </div>
        <button onClick={() => setIsVisible(false)}>
          <X size={20} />
        </button>
      </div>
    </div>
  );
}
