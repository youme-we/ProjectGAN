export default function Inputfields_project_config({
  section_name,
  project_config_section,
  onChange_project_config,
  onTune_project_config,
}) {
  return (
    <div className="relative object-center basis-1/8">
      {Object.keys(project_config_section).map((keyname, index) => (
        <div key={keyname}>
          <div className="font-serif text-lg subpixel-antialiased text-white-brown">
            {keyname}
          </div>
          <input
            id={`inputfield_${section_name}_${keyname}`}
            className="font-serif text-lg subpixel-antialiased bg-dark-gray text-white-brown"
            type={typeof project_config_section[keyname]}
            value={project_config_section[keyname]}
            onChange={(e) => {
              onChange_project_config(e, section_name, keyname);
            }}
            onKeyDown={(e) => {
              onTune_project_config(e, section_name, keyname);
            }}
          />
          <p></p>
        </div>
      ))}
    </div>
  );
}
