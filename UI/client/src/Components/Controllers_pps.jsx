import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import PlayDisabledIcon from "@mui/icons-material/PlayDisabled";
import PauseIcon from "@mui/icons-material/Pause";

export default function Controllers_pps({ socket }) {
  const pps = (pause, save, run) => {
    socket.emit("/pps_s", {
      pause_trainer: pause,
      save_trainer: save,
      break_trainer: run,
    });
  };

  const ButtonStyle = {
    width: "30px",
    height: "auto",
    color: "black",
  };

  return (
    <div className="m-4 p-4 bg-white-brown rounded-2xl shadow flex gap-4 items-center w-max">
      {[
        {
          icon: "M8 5v14l11-7z",
          action: () => pps(false, false, false),
          label: "Play",
        },
        {
          icon: "M6 19h4V5H6v14zm8-14v14h4V5h-4z",
          action: () => pps(true, false, false),
          label: "Pause",
        },
        {
          icon: "M3 6h18M8 6v12a2 2 0 002 2h4a2 2 0 002-2V6m-6 0V4a1 1 0 011-1h2a1 1 0 011 1v2",
          action: () => pps(false, false, true),
          label: "Stop",
        },
      ].map(({ icon, action, label }) => (
        <button
          key={label}
          onClick={action}
          title={label}
          className="bg-dark-gray text-white rounded-full w-10 h-10 flex items-center justify-center hover:bg-black transition duration-200 shadow hover:shadow-xl hover:scale-105"
        >
          <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
            <path d={icon} />
          </svg>
        </button>
      ))}
    </div>
  );
}
