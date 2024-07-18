const http_endpoints = (app, db) => {
  app.post("/login", async (req, res) => {
    let prj = await db.get_prj(req.body.prj_name)
    if (prj) {
      res.send(prj);
    } else {
      res.send(false);
    }
  });

  app.post("/create", async (req, res) => {
    if (await db.get_prj(req.body.prj_name)) {
      res.send(false)
    }
    else {
      res.send(await db.create_prj(req.body.prj_name))
    }
  })
};

export default http_endpoints;
