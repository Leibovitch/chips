import pymongo
import matplotlib.pyplot as plt
import sys
import plotly.plotly as py
import datetime
import dateutil.parser
import time
from util_functions

#
# def turn_property_to_array(property_key, mongo_collection):
#     cursor = mongo_collection.find({}, {property_key: 1})
#     new_prorperty_array = []
#     for element in cursor:
#         new_prorperty_array.append(element[property_key])
#
#     return new_prorperty_array
try:
    score_cutoff = float(sys.argv[1])
except IndexError:
    score_cutoff = 0


def parse_property_key(property_key):
    newsted_key_array = property_key.split('.')
    full_string = []
    for word in newsted_key_array:
        full_string.append('["' + word + '"]')

    full_string = ''.join(full_string)
    return full_string


def turn_property_to_array(property_key, mongo_collection):
    cursor = mongo_collection.find({}, {property_key: 1})
    new_prorperty_array = []
    full_string = parse_property_key(property_key)
    for element in cursor:
        exec('new_prorperty_array.append(element' + full_string + ')')

    return new_prorperty_array


client = pymongo.MongoClient('mongodb://localhost:27017/')
name_list = client.database_names()
if 'working_db' not in name_list:
    client.admin.command('copydb', fromdb='planet', todb='working_db', upsert=True)

db = client.working_db
print(score_cutoff)
score_query = {"properties.score": {"$lt": score_cutoff}, "properties.cloud_cover": 0}
ships_collection = db.ships
response = ships_collection.delete_many(score_query)
print(response.deleted_count)
scores_array = turn_property_to_array("properties.score", ships_collection)


plt.hist(scores_array, bins=20)
plt.title("score distribution")
plt.gca().invert_xaxis()
plt.show()

client.drop_database('working_db')
# fig = plt.gcf()
#
# plot_url = py.plot_mpl(fig, filename="score distribution hist")

#print(scores_array)


# query = {"properties.cloud_cover":0}
# projection = {"geometry": 1, "properties.cloud_cover": 1, "properties.source_item": 1,
#               "properties.observed": 1, "id": 1}
# cursor = ships_collection.find(query, projection)
# counter = 0
# datesArray = []
#
# for ship in cursor:
#     current_satellite = ship["properties"]["source_item"].split('_')
#     currentTimeTuple = dateutil.parser.parse(ship["properties"]["observed"]).timetuple()
#     ships_collection.update_one({"_id": ship["_id"]}, {"$set": {"time_in_seconds": time.mktime(currentTimeTuple)}})
#     ships_collection.update_one({"_id": ship["_id"]}, {"$set": {"satellite_name": current_satellite[2]}})
#
# cursor2 = ships_collection.find({"satellite_name": {'$exists': True}}, {"satellite_name": 1, "time_in_seconds": 1})
# cursor2.sort([("satellite_name", pymongo.ASCENDING), ("time_in_seconds", pymongo.ASCENDING)])
#
# for element in cursor2:
#     print(element)





# for element in cursor:
#     print(element)
#     currentTimeTuple = dateutil.parser.parse(element["properties"]["_published"]).timetuple()
#     datesArray.append(time.mktime(currentTimeTuple))
#
# for date in datesArray:
#     print(date)
#     print(time.mktime(date.timetuple()))



