from pymongo import MongoClient
import certifi
from pandas import DataFrame
import json
import googleAPI as gmaps
import pandas as pd
import numpy as np



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

def getPercentageForFarmers():
    CONNECTION_STRING = "mongodb+srv://root_rev_emi:dashrev_emi@cluster0.zpxz50t.mongodb.net/test?authSource=admin&replicaSet=atlas-boo7fm-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true"
    # CONNECTION_STRING="mongodb://admin:dashrev_emi@ac-iuy7e8x-shard-00-02.zpxz50t.mongodb.net:27017,ac-iuy7e8x-shard-00-01.zpxz50t.mongodb.net:27017,ac-iuy7e8x-shard-00-00.zpxz50t.mongodb.net:27017/root_revemi?ssl=true&replicaSet=atlas-255sgz-shard-0&authSource=admin&retryWrites=true&w=majority&maxIdleTimeMS=8000"
    client = MongoClient(CONNECTION_STRING, tlsCAFile=ca)

    resultTotal = client['root_revemi']['user'].aggregate([
    {
        '$group': {
            '_id': '$SEX',
            'count': {
                '$sum': 1
            }
        }
    }, {
        '$group': {
            '_id': '$SEX',
            'docs': {
                '$push': {
                    'SEX': '$_id',
                    'count': '$count'
                }
            },
            'count': {
                '$sum': '$count'
            }
        }
    }, {
        '$project': {
            '_id': 0,
            'count': 1,
            'data': {
                '$map': {
                    'input': '$docs',
                    'in': {
                        'k': {
                            '$concat': [
                                '', {
                                    '$toString': '$$this.SEX'
                                }
                            ]
                        },
                        'v': {
                            '$multiply': [
                                {
                                    '$divide': [
                                        '$$this.count', '$count'
                                    ]
                                }, 100
                            ]
                        }
                    }
                }
            }
        }
    }, {
        '$project': {
            'count': 1,
            'data': 1
        }
    }
])
    items = []
    for i in resultTotal:
        items.append(i)
    #print(items)

    resultAge = client['root_revemi']['user'].aggregate([
    {
        '$match': {
            'AGE': {
                '$lte': '35'
            }
        }
    }, {
        '$group': {
            '_id': '$SEX',
            'count': {
                '$count': {}
            }
        }
    }, {
        '$group': {
            '_id': '$SEX',
            'sex': {
                '$sum': 1
            },
            'docs': {
                '$push': {
                    'SEX': '$_id',
                    'count': '$count',
                    'y': '$SEX'
                }
            }
        }
    }, {
        '$project': {
            '_id': 0,
            'docs': 1
        }
    }
])
    for i in resultAge:
        items.append(i)
    #print(items)
    return items

def getpercent():
    y= getPercentageForFarmers()
    Total=y[0]["count"]
    Men=None
    #print(y[0]["data"][0]['k'])
    if y[0]["data"][0]['k']=='F':
        Women=y[0]["data"][0]['v']
    else:
        Men = y[0]["data"][0]['v']
    if y[0]["data"][1]['k']=='M':
        Men=y[0]["data"][1]['v']
    else:
        Women = y[0]["data"][1]['v']
    ######################
    if y[1]["docs"][0]['SEX']=='F':
        Women30=y[1]["docs"][0]['count']
    else:
        Men30 = y[1]["docs"][0]['count']
    if y[1]["docs"][1]['SEX']=='M':
        Men30=y[1]["docs"][1]['count']
    else:
        Women30 = y[1]["docs"][1]['count']

    Women30 = (Women30/Total) * 100
    Men30=(Men30/Total)*100
    #print(y[1]["docs"])
    print(Total, Men, Women, Women30, Men30)
    np.ceil(Men)
    data={"Total":np.ceil(Total),
          "Men":np.ceil(Men),
          "Women":np.ceil(Women),
          "Men30":np.ceil(Men30),
          "Women30":np.ceil(Women30),
          }
    return data




