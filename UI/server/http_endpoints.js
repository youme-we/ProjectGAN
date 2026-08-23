import express from "express";
import path from "path";
import { fileURLToPath } from "url";
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const buildPath = path.join(__dirname, "build");

const http_endpoints = (app, db) => {
  app.post("/create_project_config", async (req, res) => {
    const status = await db.create_project_config(req.body.project_config);
    res.send(status);
  });

  app.post("/read_project_config", async (req, res) => {
    const project_config = await db.read_project_config(req.body._id);
    res.send(project_config);
  });

  app.post("/update_project_config", async (req, res) => {
    const status = await db.update_project_config(req.body.prj_name, req.body.fields);
    res.send(status);
  });

  app.post("/delete_project_config", async (req, res) => {
    const status = await db.delete_project_config(req.body.prj_name);
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
