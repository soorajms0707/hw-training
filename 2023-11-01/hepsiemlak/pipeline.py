def connect_to_mongodb():
    from  settings import MONGO_URL,MONGODB,URL,DATA
    from pymongo import MongoClient

    client = MongoClient(MONGO_URL)
    db = client[MONGODB]
    db[DATA].create_index([("url")], unique=True)
    db[URL].create_index([("url")], unique=True)
    

    return db