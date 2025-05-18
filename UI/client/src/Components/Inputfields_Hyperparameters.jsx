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
    <div className="relative object-center basis-1/8">
      {Object.keys(overview.hyperparameters).map((keyname, index) => (
        <div key={index}>
          {console.log(keyname)}
          <div className="font-serif text-lg subpixel-antialiased text-white-brown">
            {keyname}
          </div>
          <input
            id={`inputfield_${keyname}`}
            className="font-serif text-lg subpixel-antialiased bg-dark-gray text-white-brown"
            type={overview_template.hyperparameters[keyname].type}
            min={overview_template.hyperparameters[keyname].min}
            max={overview_template.hyperparameters[keyname].max}
            step={overview_template.hyperparameters[keyname].step}
            value={overview.hyperparameters[keyname]}
            onChange={(e) => {
              onChange_overview(e, keyname);
            }}
            onKeyDown={(e) => {
              onTune_overview(e, keyname);
            }}
          />
          <p></p>
        </div>
      ))}
    </div>
  );
}
