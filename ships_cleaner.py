import pymongo
import datetime
import dateutil.parser
import time
import util_functions


client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.newdb
ships_collection = db.ships

query = {"properties.cloud_cover":0}
projection = {"geometry": 1, "properties.cloud_cover": 1, "properties.source_item": 1,
              "properties.observed": 1, "id": 1}
cursor = ships_collection.find(query, projection)
counter = 0
datesArray = []

for ship in cursor:
    current_satellite = ship["properties"]["source_item"].split('_')
    currentTimeTuple = dateutil.parser.parse(ship["properties"]["observed"]).timetuple()
    ships_collection.update_one({"_id": ship["_id"]}, {"$set": {"time_in_seconds": time.mktime(currentTimeTuple)}})
    ships_collection.update_one({"_id": ship["_id"]}, {"$set": {"satellite_name": current_satellite[2]}})

cursor2 = ships_collection.find({"satellite_name": {'$exists': True}}, {"satellite_name": 1, "time_in_seconds": 1})
cursor2.sort([("satellite_name", pymongo.ASCENDING), ("time_in_seconds", pymongo.ASCENDING)])

for element in cursor2:
    print(element)





# for element in cursor:
#     print(element)
#     currentTimeTuple = dateutil.parser.parse(element["properties"]["_published"]).timetuple()
#     datesArray.append(time.mktime(currentTimeTuple))
#
# for date in datesArray:
#     print(date)
#     print(time.mktime(date.timetuple()))



