import React from "react";
export default function SamplesTT({ training_samples, test_samples }) {
  return (
    <div className="flex relative top-48 bg-dark-gray">
      {training_samples && (
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
          {training_samples.map((training_sample, index) => (
            <React.Fragment key={index}>
              <div className="font-serif text-2xl subpixel-antialiased bg-dark-gray text-white-brown">
                {index}
              </div>

              <img
                src={
                  training_samples[index]
                    ? `data:image/png;base64,${training_samples[index]}`
                    : "/placeholder.png"
                }
                className="relative l-16 w-64 h-64"
                alt="Training Sample"
              />

              <img
                src={
                  test_samples[index]
                    ? `data:image/png;base64,${test_samples[index]}`
                    : "/placeholder.png"
                }
                className="relative l-16 w-64 h-64"
                alt="Test Sample"
              />
            </React.Fragment>
          ))}
        </div>
      )}
    </div>
  );
}
