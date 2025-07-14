import express from "express";
import cors from "cors";
import sessions from "express-session";
const setup_express = () => {
  const app = express();
  app.use(
    sessions({
      secret: "secret-key",
      saveUninitialized: false, //when false the cookie only gets stored in the Brwoser when it get's modified by for example setting req.session.authentication = true;
      cookie: { maxAge: null },
      resave: false,
      secure: false, //if this is true the cookie only gets send over a https secure connection
    })
  );

  app.use(express.json()); // <==== parse request body as JSON
  app.use(
    cors({
      origin: ["http://localhost:3000"],
      credentials: true,
    })
  );
  app.options("*", cors());
  //For more information look at the note in Notablitiy

  //this is serving the React app from the build folder

  return app;
};

export default setup_express;
