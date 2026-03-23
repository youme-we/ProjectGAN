import { MongoClient, ObjectId } from "mongodb";
import { createRequire } from "module";
const require = createRequire(import.meta.url);

export default class DB {
  constructor(db_name, collection_name) {
    const HOST_MONGODB = process.env.HOST_MONGODB || "localhost";
    const PORT_MONGODB = process.env.PORT_MONGODB || 27018;
    const USER_MONGODB = process.env.USER_MONGODB;
    const PASS_MONGODB = process.env.PASS_MONGODB;
    const AUTHSOURCE_MONGODB = process.env.AUTHSOURCE_MONGODB;
    const uri = `mongodb://${USER_MONGODB}:${PASS_MONGODB}@${HOST_MONGODB}:${PORT_MONGODB}/?authSource=${AUTHSOURCE_MONGODB}`;
    const client = new MongoClient(uri);
    client.connect();
    const database = client.db(db_name);
    // TODO:this.db instead of this.project_configs
    this.project_configs = database.collection(collection_name);
  }

  async create_project_config(project_config) {
    try {
      project_config._id = new ObjectId();
      const status = await this.project_configs.insertOne(project_config);
      return { acknowledged: true, insertedId: status.insertedId };
    } catch (error) {
      return {
        acknowledged: false,
        errorCode: error.code,
        keyValue: error.keyValue,
      };
    }
  }
  async read_project_config(prj_name) {
    const project_config = await this.project_configs.findOne(
      {
        name: prj_name,
      },
      { projection: { _id: 0 } }
    );
    return project_config || false;
  }
  async update_project_config(prj_name, fields) {
    const status = await this.project_configs.updateOne({ name: prj_name }, { $set: fields });
    return status;
  }
  async delete_project_config(prj_name) {
    const status = await this.project_configs.deleteOne({ name: prj_name });
    return status;
  }
}
