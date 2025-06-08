const http_endpoints = (app, db) => {
  app.post("/create_prj_overview", async (req, res) => {
    const status = await db.create_prj_overview(req.body.prj_overview);
    res.send(status);
  });

  app.post("/read_prj_overview", async (req, res) => {
    const prj_overview = await db.read_prj_overview(req.body.prj_name);
    res.send(prj_overview);
  });

  app.post("/update_prj_overview", async (req, res) => {
    const status = await db.update_prj_overview(
      req.body.prj_name,
      req.body.fields
    );
    res.send(status);
  });

  app.post("/delete_prj_overview", async (req, res) => {
    const status = await db.delete_prj_overview(req.body.prj_name);
  });

  app.get("/healthcheck", async (req, res) => {
    res.status(200).send({ message: "OK" });
  });
};

export default http_endpoints;
