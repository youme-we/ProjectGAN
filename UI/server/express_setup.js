import express from "express";
import cors from "cors";
import sessions from "express-session";
import cookieParser from "cookie-parser";
import path from "path";
const path_build = "/Users/skost/coding-s/ProjectGAN/UI/client/build";
const setup_express =  () => {
  const app = express();
  app.use(
    sessions({
      secret: "test",
      saveUninitialized: false, //when false the cookie only gets stored in the Brwoser when it get's modified by for example setting req.session.authentication = true;
      cookie: { maxAge: 1000000 }, //milliseconds
      resave: false,
      secure: false, //if this is true the cookie only gets send over a https secure connection
    })
  );

  app.use(cookieParser()); // don't need this because express-session includes it
  app.use(express.json()); // <==== parse request body as JSON
  app.use(
    cors({
      origin: ["http://localhost:3000", "http://localhost:3001"], //alows requests from this PORT
      credentials: true,
    })
  );
  //For more information look at the note in Notablitiy

  //this is serving the React app from the build folder
  app.use(express.static(path_build));
  app.get(["/", "/create", "/login", "/project"], async (req, res) => {
    res.sendFile(path.join(path_build, "index.html"));
  });
  return app;
}

export default setup_express;
