import pymongo
from bson import ObjectId

clientMongoDB = pymongo.MongoClient("mongodb://mongodb:27017/")

def addResultatMongoDB(resultat):
    db = clientMongoDB["app"]
    collection = db["resultats"]
    collection.insert_one(resultat)

def getResultatsMongoDB():
    db = clientMongoDB["app"]
    collection = db["resultats"]
    return collection.find()

def addMatiereMongoDB(matiere):
    db = clientMongoDB["app"]
    collection = db["matieres"]
    collection.insert_one(matiere)

def getMatieresMongoDB():
    db = clientMongoDB["app"]
    collection = db["matieres"]
    return collection.find()

def getMatiereByIdMongoDB(id):
    db = clientMongoDB["app"]
    collection = db["matieres"]
    return collection.find_one({'_id': ObjectId(id)})