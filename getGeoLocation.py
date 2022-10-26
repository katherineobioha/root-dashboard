from pymongo import MongoClient
import certifi
from pandas import DataFrame
import json



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
            'LOCATION': 1
        }
    }
    ])

    items=[]
    for i in result:
        items.append(i)
    #items=DataFrame(result)
   # z=json.dumps(items[0])
    return items


print(getFarmLocation())

