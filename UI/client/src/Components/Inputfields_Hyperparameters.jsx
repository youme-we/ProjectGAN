export default function Inputfields_Hyperparameters({
  overview,
  setoverview,
  overview_template,
  socket,
}) {
  const onTune_overview = (e, keyname) => {
    if (e.key === "Enter") {
      sessionStorage.setItem("overview", JSON.stringify(overview));
      socket.emit("/tune_s", {
        overview: JSON.stringify(overview),
      });
      document.getElementById(`inputfield_${keyname}`).blur();
    }
  };

  const onChange_overview = (e, keyname) => {
    setoverview((draft) => {
      draft.hyperparameters[keyname] = parseFloat(e.target.value);
    });
  };

  return (
    <div className="relative basis-1/4 space-y-4">
      {Object.keys(overview.hyperparameters).map((keyname, index) => (
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
            type={overview_template.hyperparameters[keyname].type}
            min={overview_template.hyperparameters[keyname].min}
            max={overview_template.hyperparameters[keyname].max}
            step={overview_template.hyperparameters[keyname].step}
            value={overview.hyperparameters[keyname]}
            onChange={(e) => onChange_overview(e, keyname)}
            onKeyDown={(e) => onTune_overview(e, keyname)}
          />
        </div>
      ))}
    </div>
  );
}
