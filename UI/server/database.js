import { MongoClient, ObjectId } from "mongodb";
import { createRequire } from "module";
const require = createRequire(import.meta.url);
const overview = require('../../overview.json')

export default class DB {
  constructor(db_name, collection_name) {
    //make data in the collection with the given collection_name excessable
    const uri = "mongodb://localhost:27017/";
    const client = new MongoClient(uri);
    client.connect();
    const database = client.db(db_name);
    this.projects = database.collection(collection_name);
  }

  async get_prj(prj_name) {
    return this.projects.findOne({ prj_name });
  }

  async create_prj(prj_name) {
    overview.prj_name = prj_name
    overview._id = new ObjectId()
    await this.projects.insertOne(overview); //saves created Project to the DB
    return overview
  }
}
