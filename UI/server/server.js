const express = require('express');
const app = express();
const PORT = 3001;
const cors = require('cors')
var genuuid = require('uuid');
const sessions = require('express-session')
const cookieParser = require('cookie-parser')
var MongoClient = require('mongodb').MongoClient;
const uri = "mongodb://localhost:27017/";
const bcrypt = require('bcrypt');
const client = new MongoClient(uri);
const path = require('path');
const { connect } = require('http2');
const  path_build =  "/Users/skost/coding-s/ProjectGAN/UI/client/build"


app.use(sessions({
    secret: "test",
    saveUninitialized:false,//when false the cookie only gets stored in the Brwoser when it get's modified by for example setting req.session.authentication = true;
    cookie: { maxAge: 1000000 },//milliseconds
    resave:false,
    secure:false,//if this is true the cookie only gets send over a https secure connection
    })
)


app.use(cookieParser())// don't need this because express-session includes it 
app.use(express.json())// <==== parse request body as JSON
app.use(cors({
  origin: "http://localhost:3000",//alows requests from this PORT
  credentials: true}))
//For more information look at the note in Notablitiy






async function connectDB(){
    await client.connect();
    const database = client.db("ProjectGAN");
    const Projects = database.collection("Projects");
    return Projects;
}



async function createProject(ID, req){
  const Projects = await connectDB();
  const user_obj = {
      ID,
      sessionID: req.sessionID
    }


  Projects.insertOne(user_obj);
  req.session.authenticated = true;
}


async function compareDB(ID, req, res){
    const Projects = await connectDB();
    const Project = await Projects.findOne({ID})
    Projects.updateOne({_id: Project._id}, {$set: {sessionID: req.sessionID}})
    req.session.authenticated = true;
    res.send(true)
    console.log("login worked")
        
}



app.post("/create",async (req,res) => {
  let data = req.body;
  const ID = data.ID

  try{
      await createProject(ID, req)
      res.send(true)
      console.log('creating Project worked')
    }
  catch{
      res.send(false)
      console.log("creating Project didn't work")
    }
  })




app.post("/login",async (req,res) => {
  const data = req.body
  const ID = data.ID

  try{
      await compareDB(ID, req, res)
    }

  catch(error){
      res.send(false)
      console.log("login failed:Project_ID was wrong")
    }

  console.log(req.sessionID)
})



app.use(express.static(path_build))

app.get(['/create', '/login'], async (req,res) => {
  res.sendFile(path.join(path_build, "index.html"));
})






app.get("/project",async (req,res) => {
  try{
    const sessionID = req.sessionID
    const Projects = await connectDB();
    const Project = await Projects.findOne({sessionID})
    if(Project == null){
        res.redirect('/login')
        console.log("Project_ID has to be entered")
    }
    else{
        res.sendFile(path.join(path_build, "index.html"))
        console.log("user is authenticated"+user)
    }
  }
  catch{
    res.redirect('/login')
  }
})


app.listen(PORT, ()=> {console.log("server is listening on Port:"+PORT)});

