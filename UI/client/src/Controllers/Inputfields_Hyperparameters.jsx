export default function Inputfields_Hyperparameters({
  project_config,
  setproject_config,
  project_config_template,
  socket,
}) {
  const onTune_project_config = (e, keyname) => {
    if (e.key === "Enter") {
      sessionStorage.setItem("project_config", JSON.stringify(project_config));
      socket.emit("tune_s", {
        project_config: JSON.stringify(project_config),
      });
      document.getElementById(`inputfield_${keyname}`).blur();
    }
  };

  const onChange_project_config = (e, keyname) => {
    setproject_config((draft) => {
      draft.hyperparameters[keyname] = parseFloat(e.target.value);
    });
  };

  return (
    <div className="relative basis-1/4 space-y-4">
      {Object.keys(project_config.hyperparameters).map((keyname, index) => (
        <div key={index} className="space-y-1">
          {/* Label */}
          <label
            htmlFor={`inputfield_${keyname}`}
            className="block text-sm font-medium text-gray-300 tracking-wide"
          >
            {keyname}
          </label>

          {/* Input Field */}
          <input
            id={`inputfield_${keyname}`}
            className="w-full px-3 py-2 rounded-md bg-gray-800 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent transition-all duration-200"
            type={project_config_template.hyperparameters[keyname].type}
            min={project_config_template.hyperparameters[keyname].min}
            max={project_config_template.hyperparameters[keyname].max}
            step={project_config_template.hyperparameters[keyname].step}
            value={project_config.hyperparameters[keyname]}
            onChange={(e) => onChange_project_config(e, keyname)}
            onKeyDown={(e) => onTune_project_config(e, keyname)}
          />
        </div>
      ))}
    </div>
  );
}
