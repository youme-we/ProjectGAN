const http_endpoints = (app, db) => {
  app.post("/login", async (req, res) => {
    const prj = await db.get_prj(req.body.prj_name);
    if (prj) {
      res.send(prj);
    } else {
      res.send(false);
    }
  });

  app.post("/create", async (req, res) => {
    if (await db.get_prj(req.body.prj_name)) {
      res.send(false);
    } else {
      const prj = await db.create_prj(req.body.prj_name);
      res.send(prj);
    }
  });
};

export default http_endpoints;
