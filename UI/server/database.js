import { MongoClient, ObjectId } from "mongodb";
import { createRequire } from "module";
const require = createRequire(import.meta.url);

export default class DB {
  constructor(db_name, collection_name) {
    const HOST_MONGODB = process.env.HOST_MONGODB || "localhost";
    const PORT_MONGODB = process.env.PORT_MONGODB || 27018;
    const USER_MONGODB = process.env.USER_MONGODB;
    const PASS_MONGODB = process.env.PASS_MONGODB;
    const uri = `mongodb://${USER_MONGODB}:${PASS_MONGODB}@${HOST_MONGODB}:${PORT_MONGODB}/?authSource=admin`;
    const client = new MongoClient(uri);
    client.connect();
    const database = client.db(db_name);
    // TODO:this.db instead of this.prj_overviews
    this.prj_overviews = database.collection(collection_name);
  }

  async create_prj_overview(prj_overview) {
    try {
      prj_overview._id = new ObjectId();
      const status = await this.prj_overviews.insertOne(prj_overview);
      return { acknowledged: true, insertedId: status.insertedId };
    } catch (error) {
      return {
        acknowledged: false,
        errorCode: error.code,
        keyValue: error.keyValue,
      };
    }
  }
  async read_prj_overview(prj_name) {
    const prj_overview = await this.prj_overviews.findOne(
      {
        "prj_info.name": prj_name,
      },
      { projection: { _id: 0 } }
    );
    return prj_overview;
  }
  async update_prj_overview(prj_name, fields) {
    const status = await this.prj_overviews.updateOne(
      { "prj_info.name": prj_name },
      { $set: fields }
    );
    console.log(status);
    return status;
  }
  async delete_prj_overview(prj_name) {
    const status = await this.prj_overviews.deleteOne({ name: prj_name });
    return status;
  }
}
