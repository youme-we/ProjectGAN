import express from "express";
import path from "path";
import { fileURLToPath } from "url";
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const buildPath = path.join(__dirname, "public");

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
      req.body.fields,
    );
    res.send(status);
  });

  app.post("/delete_prj_overview", async (req, res) => {
    const status = await db.delete_prj_overview(req.body.prj_name);
  });
  app.get("/healthcheck", async (req, res) => {
    res.status(200).send({ message: "OK" });
  });

  app.use(express.static(buildPath));
  app.get("*", async (req, res) => {
    res.sendFile(path.join(buildPath, "index.html"));
  });
};

export default http_endpoints;
