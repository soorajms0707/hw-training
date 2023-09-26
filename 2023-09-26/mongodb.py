# sudo docker ps
# sudo docker run --name my-mongo -p 27017:27017 -d mongo
# sudo docker rm my-mongo
# sudo docker start my-mongo



# -----------------------------------------------------------------------



import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["database1"]
collection = db["details"]

# # to insert (insert_one)

# details = {
#     "name": "rahul",
#     "email": "rahul@example.com",
#     "age": 30
# }

# result = collection.insert_one(details)
# print( result.inserted_id)


# documents = [
#     {
#     "name": "sooraj",
#     "email": "sooraj@example.com",
#     "age": 30
# },
#     {
#     "name": "sooraj",
#     "email": "soorajms@.com",
#     "age": 30
# },
# {
#     "name": "vishnu",
#     "email": vishnu@example.com",
#     "age": 10
# }

# ]
# result = collection.insert_many(documents)

# -----------------------------------


# # get single data 

# query = {"name": "sooraj"}
# result = collection.find_one(query)

# if result:
#     print("Found Document:", result)
    
# else:
#     print("Document not found.")



# query = {"name": "sooraj"}
# result = collection.find(query)

# if result:
#     for document in result:
#         print(document)
# else:
#     print("Document not found.")



# # update 

# query = {"name": "sooraj"}
# update = {"$set": {"age": 18}}
# result = collection.update_one(query, update)


# query = {"name": "sooraj"}
# update = {"$set": {"age": 24}}
# result = collection.update_many(query, update)



# count

# query = {"name": "sooraj"}
# count = collection.count_documents(query)
# print(count)


# #  Retrieves distinct values


# distinct_categories = collection.distinct("name")
# print(distinct_categories)

# # range 

# query1 = {"age": {"$lt": 20}}
# results1 = collection.find(query1)

# query2 = {"age": {"$gte": 20, "$lte": 29}}
# results2 = collection.find(query2)

# query3 = {"$and": [{"age": {"$gte": 30}}, {"name": "John Doe"}]}
# results3 = collection.find(query3)

# print("age less than 20:")
# for doc in results1:
#     print(doc)

# print("\nage between 20 and 29:")
# for doc in results2:
#     print(doc)

# print("\nJohn age greater than or equal to 30:")
# for doc in results3:
#     print(doc)


# # delete

# query = {"name": "sooraj"}
# result = collection.delete_one(query)

# query = {"name": "rahul"}
# result = collection.delete_many(query)


