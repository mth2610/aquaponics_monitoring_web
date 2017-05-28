import pymongo
from bson.objectid import ObjectId
client = pymongo.MongoClient()
db = client['smart_aquaponics']

def insert_data(collection,data):
    return db[collection].insert_one(data)

def find_data(collection,conditions=None,**kwargs):
    if conditions == None:
        return (db[collection]).find()
    elif type(conditions) == dict:
        return (db[collection]).find(conditions)
    else:
        raise Exception('conditions have to be a dictornary')

def find_lastest_data(collection,conditions=None,number_of_data=None):
    if conditions == None:
        cursor = db[collection].find({}, {"$sort":{"$natural":-1}})
        return db[collection].find({}, {"$sort":{"$natural":-1}})
    elif type(conditions) == dict:
        cursor = db[collection].find(conditions).sort([("datetime", pymongo.DESCENDING),])
        if number_of_data == None:
            return cursor
        else:
            return cursor.limit(number_of_data)
    else:
        raise Exception('conditions have to be a dictornary')

def update_data(collection,data,conditions=None,**kwargs):
    db[collection].update(
               conditions,
               {'$set' : data}
        )
    return

def extend_data(collection,_id,field,data):
    return db[collection].update(
        { "_id": ObjectId(_id)},
        { "$push": {field: {"$each":data}}}
    )

def get_collection(collection):
    return
