export default function SamplesTT({ training_sample, test_sample }) {
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
          src={
            training_sample
              ? `data:image/png;base64,${training_sample}`
              : "/placeholder.png"
          }
          className="relative l-16 w-64 h-64"
          alt="Training Sample"
        />

        <img
          src={
            test_sample
              ? `data:image/png;base64,${test_sample}`
              : "/placeholder.png"
          }
          className="relative l-16 w-64 h-64"
          alt="Test Sample"
        />
      </div>
    </div>
  );
}
