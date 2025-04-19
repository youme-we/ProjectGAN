import { MongoClient, ObjectId } from "mongodb";
import { createRequire } from "module";
const require = createRequire(import.meta.url);

export default class DB {
  constructor(db_name, collection_name) {
    //make data in the collection with the given collection_name excessable
    const HOST = process.env.DB_HOST || "localhost";
    const uri = `mongodb://${HOST}:27017/`;
    console.log(uri);
    const client = new MongoClient(uri);
    client.connect();
    const database = client.db(db_name);
    this.projects = database.collection(collection_name);
  }

  async get_prj(prj_name) {
    //return this.projects.findOne({ prj_name });
    return require("./overview.json");
  }

  async create_prj(prj_name) {
    const overview = require("./overview.json");
    const prj = overview;
    prj.prj_name = prj_name;
    prj._id = new ObjectId();
    await this.projects.insertOne(prj); //saves created Project to the DB
    return prj;
  }
}
