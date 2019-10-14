import pymongo as pm
import json, urllib2
from constants import STATIONS_FEED_URL, MONGO_CLIENT_HOST

def getJsonResponse(url):
	req = urllib2.Request(url)
	opener = urllib2.build_opener()
	f = opener.open(req)
	return json.loads(f.read())



data = getJsonResponse(STATIONS_FEED_URL)

#Connecting to Mongodb
mongoClient = pm.MongoClient(MONGO_CLIENT_HOST)
db = mongoClient.mydb

db.Stations_Collection.remove({})

db.Stations_Collection.insert(data['stationBeanList'])

print(db.Stations_Collection.find({}).count())

