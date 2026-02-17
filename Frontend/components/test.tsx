"use client";
import { useState, useRef } from "react";
import { motion, useMotionValue, useSpring } from "framer-motion";
import { ChevronLeft, ChevronRight } from "lucide-react";
import Image from "next/image";

export default function BeforeAfterSlider() {
  const [sliderPosition, setSliderPosition] = useState(50);
  const containerRef = useRef<HTMLDivElement>(null);

  // Use motion values for instant updates
  const x = useMotionValue(50);
  const smoothX = useSpring(x, { stiffness: 1000, damping: 50, mass: 0.1 });

  const handleMove = (clientX: number) => {
    if (!containerRef.current) return;

    const rect = containerRef.current.getBoundingClientRect();
    const xPos = clientX - rect.left;
    const percentage = (xPos / rect.width) * 100;

    const clampedPercentage = Math.min(Math.max(percentage, 0), 100);

    // Update motion value instantly
    x.set(clampedPercentage);
    setSliderPosition(clampedPercentage);
  };

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    handleMove(e.clientX);
  };

  const handleTouchMove = (e: React.TouchEvent<HTMLDivElement>) => {
    handleMove(e.touches[0].clientX);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black flex items-center justify-center p-4">
      <div className="max-w-4xl w-full space-y-6">
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold text-white">
            Before & After Slider
          </h1>
          <p className="text-gray-400">
            Move your cursor over the image to compare
          </p>
        </div>

        <div
          ref={containerRef}
          className="relative w-full aspect-video rounded-2xl overflow-hidden shadow-2xl cursor-col-resize select-none"
          onMouseMove={handleMouseMove}
          onTouchMove={handleTouchMove}
        >
          {/* After Image (Background) */}
          <div className="absolute inset-0">
            <Image
              fill
              src="/after.jpg"
              alt="After"
              className="w-full h-full object-cover pointer-events-none"
              draggable="false"
            />
            <div className="absolute top-4 right-4 bg-black/70 backdrop-blur-sm px-4 py-2 rounded-full pointer-events-none">
              <span className="text-white font-semibold">After</span>
            </div>
          </div>

          {/* Before Image (Overlay with clip) */}
          <motion.div
            className="absolute inset-0 pointer-events-none"
            style={{
              clipPath: `inset(0 ${100 - sliderPosition}% 0 0)`,
            }}
          >
            <Image
              fill
              src="/before.jpg"
              alt="Before"
              className="w-full h-full object-cover"
              draggable="false"
            />
            <div className="absolute top-4 left-4 bg-black/70 backdrop-blur-sm px-4 py-2 rounded-full">
              <span className="text-white font-semibold">Before</span>
            </div>
          </motion.div>

          {/* Slider Handle - Follows Cursor Perfectly */}
          <motion.div
            className="absolute top-0 bottom-0 w-1 bg-white pointer-events-none"
            style={{ left: smoothX.get() + "%" }}
            animate={{ left: `${sliderPosition}%` }}
            transition={{ duration: 0 }}
          >
            {/* Slider Button - Perfectly Synced */}
            <motion.div
              className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-12 h-12 bg-white rounded-full shadow-lg flex items-center justify-center"
              whileHover={{ scale: 1.05 }}
              transition={{ duration: 0.1 }}
            >
              <ChevronLeft className="w-5 h-5 text-gray-800 absolute left-1" />
              <ChevronRight className="w-5 h-5 text-gray-800 absolute right-1" />
            </motion.div>
          </motion.div>
        </div>

        {/* Info Card */}
        <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-xl p-6">
          <h2 className="text-xl font-semibold text-white mb-3">How to use:</h2>
          <ul className="space-y-2 text-gray-300">
            <li className="flex items-center gap-2">
              <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
              Simply move your cursor over the image
            </li>
            <li className="flex items-center gap-2">
              <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
              The slider follows your cursor perfectly with zero lag
            </li>
            <li className="flex items-center gap-2">
              <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
              Works on touch devices - just slide your finger!
            </li>
          </ul>
        </div>

        {/* Position Indicator */}
        <div className="text-center">
          <div className="inline-flex items-center gap-3 bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-full px-6 py-3">
            <span className="text-gray-400 text-sm">Position:</span>
            <span className="text-white font-mono font-semibold">
              {sliderPosition.toFixed(1)}%
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
