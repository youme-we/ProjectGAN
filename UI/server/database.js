import { MongoClient } from "mongodb";

export default class DB {
  constructor(db, collection) {
    const uri = "mongodb://localhost:27017/";
    this.client = new MongoClient(uri);
    this.client.connect();
    this.prjs_db_data = this.__get_collection__(collection);
  }

  __get_collection__(collection) {
    const database = this.client.db("ProjectGAN");
    const Projects = database.collection(collection);
    return Projects;
  }
  get_prj(prj_ID, req, res) {
    const prj_db_data = this.prjs_db_data.findOne({ ID: prj_ID });
    this.prjs_db_data.updateOne(
      { _id: prj_db_data._id },
      { $set: { sessionID: req.sessionID } }
    );
  }

  create_prj(ID, req) {
    const prj_db_data = this.prjs_db_data;
    const user_obj = {
      ID,
      sessionID: req.sessionID, //this is done so that the server saves the sessionID in the datbase
    };

    prj_db_data.insertOne(user_obj); //saves created Project to the DB
    req.session.authenticated = true; //this is done so that the browser saves the sessionID
  }
}
