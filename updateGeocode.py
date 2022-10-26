from pymongo import MongoClient
from pandas import DataFrame
import certifi
import requests as rq


ca = certifi.where()
def get_database():
    CONNECTION_STRING="mongodb+srv://root_rev_emi:dashrev_emi@cluster0.zpxz50t.mongodb.net/test?authSource=admin&replicaSet=atlas-boo7fm-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true"
    #CONNECTION_STRING="mongodb://admin:dashrev_emi@ac-iuy7e8x-shard-00-02.zpxz50t.mongodb.net:27017,ac-iuy7e8x-shard-00-01.zpxz50t.mongodb.net:27017,ac-iuy7e8x-shard-00-00.zpxz50t.mongodb.net:27017/root_revemi?ssl=true&replicaSet=atlas-255sgz-shard-0&authSource=admin&retryWrites=true&w=majority&maxIdleTimeMS=8000"
    client = MongoClient(CONNECTION_STRING, tlsCAFile=ca)

    return client["root_revemi"]

# dbname=get_database()
# collection_name =dbname["user"]
#
# item_details=collection_name.find_one()
# items_df = DataFrame(item_details)
#
# print(items_df)

def getSortedFarmLocationList():
    result = get_database()['user'].aggregate([
        {
            '$group': {
                '_id': 'farm',
                'fieldN': {
                    '$addToSet': '$FARM LOCATION'
                }
            }
        }
    ])

    for fieldN in  result:
        finalresult = fieldN["fieldN"]

    finalresult.sort(key=str.lower)
    return finalresult


def getGeoCode():
    r = rq.get("https://maps.googleapis.com/maps/api/geocode/json?address=189 orchard st, NY&key=AIzaSyB7iE5c1R8Sg-O73sSAXz5DWfdmea8Bg4g")

    data = r.json()
    return data["results"][0]["geometry"]["location"]


print(getGeoCode())






