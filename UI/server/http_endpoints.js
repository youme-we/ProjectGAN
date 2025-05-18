const http_endpoints = (app, db) => {
  app.post("/get_prj_overview", async (req, res) => {
    prj_overview = await db.get_prj_overview(req.body.prj_name);
    console.log(prj_overview);
    if (prj_overview) {
      res.send(prj_overview);
    } else {
      res.send(false);
    }
  });

  app.post("/create", async (req, res) => {
    if (await db.get_prj_overview(req.body.prj_name)) {
      res.send(false);
    } else {
      const prj = await db.create_prj_overview(req.body.prj_name);
      res.send(prj);
    }
  });
};

export default http_endpoints;
