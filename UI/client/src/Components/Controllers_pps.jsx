import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import PlayDisabledIcon from "@mui/icons-material/PlayDisabled";
import PauseIcon from "@mui/icons-material/Pause";

export default function Controllers_pps({ socket }) {
  const pps = (pause, save, run) => {
    socket.emit("/pps_s", {
      pause: pause,
      save: save,
      run: run,
    });
  };

  const ButtonStyle = {
    width: "30px",
    height: "auto",
    color: "black",
  };

  return (
    <div className="m-2 border-4 border-dark-black border-solid rounded w-max">
      <PlayArrowIcon
        onClick={() => pps(false, false, true)}
        style={ButtonStyle}
        className="fill-dark-gray"
      />

      <PauseIcon onClick={() => pps(true, false, true)} style={ButtonStyle} />
      <PlayDisabledIcon
        onClick={() => pps(false, true, false)}
        style={ButtonStyle}
      />
    </div>
  );
}
