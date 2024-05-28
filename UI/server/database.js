import { MongoClient } from "mongodb";

export default class DB {
  constructor(db_name, collection_name) {
    //make data in the collection with the given collection_name excessable
    const uri = "mongodb://localhost:27017/";
    const client = new MongoClient(uri);
    client.connect();
    const database = client.db(db_name);
    this.projects = database.collection(collection_name);
  }

  async check_prj_existence(ID) {
    const prj = await this.projects.findOne({ ID });
    return prj.ID
  }

  async create_prj(ID) {
    await this.projects.insertOne({ ID }); //saves created Project to the DB
  }
}
