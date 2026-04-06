from flask import Flask, request, jsonify
from pymongo import MongoClient, ReadPreference
from pymongo.write_concern import WriteConcern

MONGO_URI = "mongodb+srv://shurd2_db_user:RpEkdmcLeopyCGwc@cluster0.79zebxx.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "ev_db"
COLLECTION_NAME = "vehicles"

app = Flask(__name__)

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.route("/insert-fast", methods=["POST"])
def insert_fast():
    doc = request.get_json()
    fast_collection = collection.with_options(write_concern=WriteConcern(w=1))

    result = fast_collection.insert_one(doc)
    return jsonify({"inserted_id": str(result.inserted_id)}), 201


@app.route("/insert-safe", methods=["POST"])
def insert_safe():
    doc = request.get_json()
    safe_collection = collection.with_options(write_concern=WriteConcern(w="majority"))

    result = safe_collection.insert_one(doc)
    return jsonify({"inserted_id": str(result.inserted_id)}), 201


@app.route("/count-tesla-primary", methods=["GET"])
def count_tesla_primary():
    primary_collection = collection.with_options(read_preference=ReadPreference.PRIMARY)

    count = primary_collection.count_documents({"make": "TESLA"})
    return jsonify({"count": count}), 200


@app.route("/count-bmw-secondary", methods=["GET"])
def count_bmw_secondary():
    secondary_pref_collection = collection.with_options(read_preference=ReadPreference.SECONDARY_PREFERRED)

    count = secondary_pref_collection.count_documents({"make": "BMW"})
    return jsonify({"count": count}), 200


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API is running"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
