const http_endpoints = (app, db) => {
  app.post("/login", async (req, res) => {
    try {
      await db.check_prj_existence(req.body.ID)
      res.send(true);
    } catch {
      res.send(false);
    }
  });

  app.post("/create", async (req, res) => {
    try {
      await db.check_prj_existence(req.body.ID)
      res.send(false)
    }
    catch {
      await db.create_prj(req.body.ID)
      res.send(true)
    }
  })
};

export default http_endpoints;
