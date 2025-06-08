export default function Inputfields_overview({
  section_name,
  overview_section,
  onChange_overview,
  onTune_overview,
}) {
  return (
    <div className="relative object-center basis-1/8">
      {Object.keys(overview_section).map((keyname, index) => (
        <div key={keyname}>
          <div className="font-serif text-lg subpixel-antialiased text-white-brown">
            {keyname}
          </div>
          <input
            id={`inputfield_${section_name}_${keyname}`}
            className="font-serif text-lg subpixel-antialiased bg-dark-gray text-white-brown"
            type={typeof overview_section[keyname]}
            value={overview_section[keyname]}
            onChange={(e) => {
              onChange_overview(e, section_name, keyname);
            }}
            onKeyDown={(e) => {
              onTune_overview(e, section_name, keyname);
            }}
          />
          <p></p>
        </div>
      ))}
    </div>
  );
}
