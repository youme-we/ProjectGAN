import React, { useEffect, useState } from "react";
export default function Samples_TT({ metrics }) {
  console.log(metrics)
  return (
    <div className="flex relative top-48 bg-dark-gray">
      <div className="grid grid-cols-custom gap-x-32 gap-y-16 relative left-64">
        <div className="font-serif text-2xl subpixel-antialiased bg-dark-gray text-white-brown">
          Samples
        </div>
        <div className="font-serif text-2xl subpixel-antialiased bg-dark-gray text-white-brown">
          Training
        </div>
        <div className="font-serif text-2xl subpixel-antialiased bg-dark-gray text-white-brown">
          Test
        </div>
        <div className="font-serif text-2xl subpixel-antialiased bg-dark-gray text-white-brown">
          1.
        </div>
        <img
          src={`data:image/png;base64,${metrics.training_sample}`}
          className="relative l-16 w-64 h-64"
        />
        <img
          src={`data:image/png;base64,${metrics.test_sample}`}
          className="relative l-4 w-64 h-64"
        />
      </div>
    </div>
  )
}

