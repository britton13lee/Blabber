from flask import Flask, jsonify, make_response, json, request
from time import time
from uuid import uuid4
import pymongo
from bson.objectid import ObjectId
from prometheus_flask_exporter import PrometheusMetrics
import os

mongo_settings = {
    "host": "mongo",
    "port": 27017,
    "username": None,
    "password": None
}

file = os.getenv("SETTINGS_FILE", None)
if file:
  mongo_settings.update(json.load(open(file)))

app=Flask(__name__)
metrics = PrometheusMetrics(app)

mongoClient = pymongo.MongoClient(**mongo_settings)
mongoCollection = mongoClient["cs2304"]["blabs"]



@app.route('/blabs', methods=['GET'])
def get_all_blabs():
  blabs = []
  for aBlab in mongoCollection.find():
    blab = aBlab.copy()
    blab["id"] = str(blab["_id"])
    del blab["_id"]
    blabs.append(blab)
  createdSince = 0
  #Check url params for createdSince and set variable accordingly
  if request.args.get("createdSince"):
    createdSince = int(request.args.get("createdSince"))
  else:
    #If the param is not there, just return all blabs
    return make_response(jsonify(blabs), 200)

  blabsInRange = []
  #Loop through all blabs and return those created after createdSince
  for blab in blabs:
    created = json.loads(json.dumps(blab))["postTime"]
    if created >= createdSince:
      blabsInRange.append(blab)
  return make_response(jsonify(blabsInRange), 200)


@app.route('/blabs', methods = ['POST'])
@metrics.counter('new_blab', 'Total number of blabs created.')
def add_blab():
  #Retrieve author and message from the content of the request
  content = request.json
  author = content["author"]
  message = content["message"]
  postTime = int(time())
  #Create the actual blab, add it to blabs, and return successful
  newBlab = {"postTime": postTime, "author": author, "message": message}
  response = mongoCollection.insert_one(newBlab)
  newBlab = {"postTime": postTime, "author": author, "message": message}
  newBlab["id"] = str(response.inserted_id)
  return make_response(jsonify(newBlab), 201)


@app.route('/blabs/<string:identity>', methods=['DELETE'])
def delete(identity):
  result = mongoCollection.delete_one({"_id": ObjectId(identity)})
  print(result.deleted_count)
  if result.deleted_count > 0:
    return make_response(jsonify({"message": "Blab deleted successfully."}), 200)
  #Otherwise, return unsuccessful
  else:
    return make_response(jsonify({"message": "Blab not found."}), 404)