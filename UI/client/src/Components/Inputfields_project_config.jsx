import { Metrics, socket } from "../traffic_management";
export default function Inputfields_project_config({
  project_config,
  setproject_config,
}) {
  const onTune_project_config = (e, id) => {
    if (e.key === "Enter") {
      document.getElementById(id).blur();
      socket.emit("/tune_s", {
        project_config: JSON.stringify(project_config),
      });
      sessionStorage.setItem("project_config", JSON.stringify(project_config));
    }
  };

  return (
    <div className="relative object-center basis-1/8">
      <div className="font-serif text-lg subpixel-antialiased text-white-brown">
        Learning Rate
      </div>
      <input
        id={`inputfield_hyperparameters_learning_rate`}
        className="font-serif text-lg subpixel-antialiased bg-dark-gray text-white-brown"
        type="number"
        value={project_config["hyperparameters"]["learning_rate"]}
        onChange={(e) => {
          setproject_config((draft) => {
            draft["hyperparameters"]["learning_rate"] = parseFloat(
              e.target.value
            );
          });
        }}
        onKeyDown={(e) => {
          onTune_project_config(e, "inputfield_hyperparameters_learning_rate");
        }}
      />
      <p></p>
    </div>
  );
}
