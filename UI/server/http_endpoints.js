const http_endpoints = (app, prjs_db_data) => {
  app.post("/create", async (req, res) => {
    let data = req.body;
    const ID = data.ID;
    try {
      await prjs_db_data.create_prj(ID, req); //saves created Project in the DB and the linked sessionID which gets also stored in the Browser
    } catch {
      res.send(false);
      console.log("creating project didn't work");
    }
  });

  app.post("/login", async (req, res) => {
    let data = req.body;
    const ID = data.ID;
    try {
      await prjs_db_data.get_prj(ID, req, res);
      req.session.authenticated = true;
      res.send(true);
      console.log("login worked");
    } catch (error) {
      res.send(false);
      console.log("login failed:Project_ID was wrong");
    }

    console.log(req.sessionID);
  });

  app.get("/project", async (req, res) => {
    try {
      const sessionID = req.sessionID;
      const prj_db_data = await prjs_db_data.findOne({ sessionID });
      if (prj_db_data == null) {
        res.redirect("/login");
        console.log("project_ID has to be entered");
      } else {
        res.sendFile(path.join(path_build, "index.html"));
        console.log("user is authenticated" + prj_db_data);
      }
    } catch {
      res.redirect("/login");
    }
  });
};

export default http_endpoints;
