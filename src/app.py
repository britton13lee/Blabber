from flask import Flask, jsonify, make_response, json, request
from time import time
from uuid import uuid4
import pymongo
from bson.objectid import ObjectId
from prometheus_flask_exporter import PrometheusMetrics
import os

file = os.getenv("SETTINGS_FILE", None)
if file:
  mongo_settings = json.loads(open(file).read())
  if "username" in  mongo_settings and "password" in mongo_settings:
    uri = "mongodb://%s:%s@%s:%s" % (mongo_settings["username"], mongo_settings["password"], mongo_settings["host"], mongo_settings["port"])
    mongoClient = pymongo.MongoClient(uri)
  else:
    uri = "mongodb://%s:%s" % (mongo_settings["host"], mongo_settings["port"])
    mongoClient = pymongo.MongoClient(uri)
else:
  mongoClient = pymongo.MongoClient("mongodb://mongo:27017")

mongoCollection = mongoClient["cs2304"]["blabs"]

app=Flask(__name__)
metrics = PrometheusMetrics(app)

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