const express = require("express");
const app = express();
const PORT = 3001;
const cors = require("cors");
var genuuid = require("uuid");
const fs = require("fs");
const sessions = require("express-session");
const cookieParser = require("cookie-parser");
var MongoClient = require("mongodb").MongoClient;
const uri = "mongodb://localhost:27017/";
const bcrypt = require("bcrypt");
const client = new MongoClient(uri);
const http = require("http");
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"],
  },
});
const path = require("path");
const { connect } = require("http2");
const path_build = "/Users/skost/coding-s/ProjectGAN/UI/client/build";

io.on("connection", (socket) => {
  //receive a message from the client
  socket.on("/send_s", (data) => {
    // send data to the client
    socket.broadcast.emit("/send_c", data);
  });
});

/////////////functions

async function connectDB() {
  await client.connect();
  const database = client.db("ProjectGAN");
  const Projects = database.collection("Projects");
  return Projects;
}

async function createProject(ID, req) {
  const Projects = await connectDB();
  const user_obj = {
    ID,
    sessionID: req.sessionID, //this is done so that the server saves the sessionID in the datbase
  };

  Projects.insertOne(user_obj); //saves created Project to the DB
  req.session.authenticated = true; //this is done so that the browser saves the sessionID
}

async function compareDB(ID, req, res) {
  const Projects = await connectDB();
  const Project = await Projects.findOne({ ID });
  Projects.updateOne(
    { _id: Project._id },
    { $set: { sessionID: req.sessionID } }
  );
  req.session.authenticated = true;
  res.send(true);
  console.log("login worked");
}

async function open_socket() {
  await io.on("connection", (socket) => {
    //receive a message from the client
    socket.on("/send_s", (data) => {
      // send data to the client
      socket.broadcast.emit("/send_c", data);
    });
  });
}

///////////////////////

///////////////////////app.use
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

app.get(["/create", "/login"], async (req, res) => {
  res.sendFile(path.join(path_build, "index.html"));
});

////////////////////////

////////////////////////Endpoints
app.post("/create", async (req, res) => {
  let data = req.body;
  const ID = data.ID;

  try {
    await createProject(ID, req); //saves created Project in the DB and the linked sessionID which gets also stored in the Browser
    res.send(true);
    console.log("creating Project worked");
  } catch {
    res.send(false);
    console.log("creating Project didn't work");
  }
});

app.post("/login", async (req, res) => {
  const data = req.body;
  const ID = data.ID;

  try {
    await compareDB(ID, req, res);
    await open_socket();
  } catch (error) {
    res.send(false);
    console.log("login failed:Project_ID was wrong");
  }

  console.log(req.sessionID);
});

app.get("/project", async (req, res) => {
  try {
    const sessionID = req.sessionID;
    console.log(sessionID);
    const Projects = await connectDB();
    const Project = await Projects.findOne({ sessionID });
    if (Project == null) {
      res.redirect("/login");
      console.log("Project_ID has to be entered");
    } else {
      res.sendFile(path.join(path_build, "index.html"));
      await open_socket();
      console.log("user is authenticated" + Project);
    }
  } catch {
    res.redirect("/login");
  }
});

app.post("/plot", async (req, res) => {
  plot = req.body;
  res.end(); //need to send response to finish request process in python
});
app.get("/plot", async (req, res) => {
  res.send(plot);
});

app.listen(PORT, () => {
  console.log("server is listening on Port:" + PORT);
});

server.listen(3000, () => {
  console.log("listening on *:3000");
});
