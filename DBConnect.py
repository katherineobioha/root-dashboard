from pymongo import MongoClient
import certifi
from pandas import DataFrame
import json
import googleAPI as gmaps




ca = certifi.where()
def getFarmLocation():
    CONNECTION_STRING = "mongodb+srv://root_rev_emi:dashrev_emi@cluster0.zpxz50t.mongodb.net/test?authSource=admin&replicaSet=atlas-boo7fm-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true"
    # CONNECTION_STRING="mongodb://admin:dashrev_emi@ac-iuy7e8x-shard-00-02.zpxz50t.mongodb.net:27017,ac-iuy7e8x-shard-00-01.zpxz50t.mongodb.net:27017,ac-iuy7e8x-shard-00-00.zpxz50t.mongodb.net:27017/root_revemi?ssl=true&replicaSet=atlas-255sgz-shard-0&authSource=admin&retryWrites=true&w=majority&maxIdleTimeMS=8000"
    client = MongoClient(CONNECTION_STRING, tlsCAFile=ca)

    result = client['root_revemi']['user'].aggregate([
    {
        '$match': {
            'FARM LOCATION': {
                '$in': [
                    'Udu', 'Uvwie'
                ]
            }
        }
    }, {
        '$project': {
            'NAME': 1,
            '_id': 0,
            'LOCATION': 1,
            'FARM LOCATION': 1
        }
    }
    ])

    items=[]
    for i in result:
        items.append(i)
    #items=DataFrame(result)
   # z=json.dumps(items[0])
    return items

def getFarmsByLocation(location):
    CONNECTION_STRING = "mongodb+srv://root_rev_emi:dashrev_emi@cluster0.zpxz50t.mongodb.net/test?authSource=admin&replicaSet=atlas-boo7fm-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true"
    # CONNECTION_STRING="mongodb://admin:dashrev_emi@ac-iuy7e8x-shard-00-02.zpxz50t.mongodb.net:27017,ac-iuy7e8x-shard-00-01.zpxz50t.mongodb.net:27017,ac-iuy7e8x-shard-00-00.zpxz50t.mongodb.net:27017/root_revemi?ssl=true&replicaSet=atlas-255sgz-shard-0&authSource=admin&retryWrites=true&w=majority&maxIdleTimeMS=8000"
    client = MongoClient(CONNECTION_STRING, tlsCAFile=ca)

    result = client['root_revemi']['user'].aggregate([
    {
        '$match': {
            'FARM LOCATION': {
                '$in': [
                    location
                ]
            }
        }
    }, {
        '$project': {
            'NAME': 1,
            '_id': 0,
            'SEX': 1,
            'LGA': 1,
            'PHONE NO': 1,
            'PRODUCT TYPE': 1,
            'AGE': 1,
            'FARM SIZE': 1
        }
    }
])

    items=[]
    for i in result:
        items.append(i)
    # items=DataFrame(result)

    return items
#print(getFarmLocation())


def addFarmerToDB(farmer):
    print(farmer)
    CONNECTION_STRING = "mongodb+srv://root_rev_emi:dashrev_emi@cluster0.zpxz50t.mongodb.net/test?authSource=admin&replicaSet=atlas-boo7fm-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true"
    # CONNECTION_STRING="mongodb://admin:dashrev_emi@ac-iuy7e8x-shard-00-02.zpxz50t.mongodb.net:27017,ac-iuy7e8x-shard-00-01.zpxz50t.mongodb.net:27017,ac-iuy7e8x-shard-00-00.zpxz50t.mongodb.net:27017/root_revemi?ssl=true&replicaSet=atlas-255sgz-shard-0&authSource=admin&retryWrites=true&w=majority&maxIdleTimeMS=8000"
    client = MongoClient(CONNECTION_STRING, tlsCAFile=ca)

    result = client['root_revemi']['user']
    print("here")
    y=gmaps.getgeocode(farmer["FARM LOCATION"])
    print(y[0]["geometry"]["location"])
    farmer.update({"LOCATION": {"lat": y[0]["geometry"]["location"]["lat"],
                                "lng": y[0]["geometry"]["location"]["lng"]}})
    print(farmer)

    # print(y)
    x = result.insert_one(farmer)
    print(x.inserted_id)

