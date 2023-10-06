# sudo docker ps
# sudo docker ps -a
# sudo docker run --name my-mongo -p 27017:27017 -d mongo            detached mode
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
#     "name": "sooraj m s",
#     "email": "sooraj@example.com",
#     "age": 30
# },
#     {
#     "name": "sooraj v s"  ,
#     "email": "soorajms@.com",
#     "age": 30
# },
# {
#     "name": "vishnu",
#     "email": "vishnu@example.com",
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
# update = {"$set": {"age": 20}}
# result = collection.update_one(query, update)


# query = {"name": "sooraj"}
# update = {"$set": {"age": 24}}
# result = collection.update_many(query, update)



# count

# query = {"name": "sooraj"}
# count = collection.count_documents(query)
# print(count)


# #  Retrieves distinct values


# distinct_categories = collection.distinct("age")
# print(distinct_categories)

# # range (operator)
# operator:-
# $lt:-less than
# $lte:-less than and equal to
# $gt:-greater than 
# $gte:-greater than and equal to
# $and
# $or




# query1 = {"age": {"$lt": 20}}
# results1 = collection.find(query1)

# query2 = {"age": {"$gte": 20, "$lte": 29}}
# results2 = collection.find(query2)

# query3 = {"$or": [{"age": {"$gte": 30}}, {"name": "rahul"}]}
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



# aggregate
# $last
# $first
# $min
# $max
# $sum

# pipeline = [
#     {"$group": {"_id": None, "avg_age": {"$sum": "$age"}}}
# ]

# result = collection.aggregate(pipeline)

# for doc in result:
#     print("Age:", doc["avg_age"])



# # delete

# query = {"name": "rahul"}
# result = collection.delete_one(query)

# query = {"name": "sooraj"}
# result = collection.delete_many(query)



# indexed

# collection.create_index([("email", pymongo.ASCENDING)], unique=True)



# details = {
#     "name": "rahul",
#     "email": "rahul@example.com",
#     "age": 30
# }

# try:
#     # Attempt to insert the document defined in the "details" dictionary into the collection
#     result = collection.insert_one(details)
    
#     # Print the ID of the inserted document if the insertion is successful
#     print("Document inserted with ID:", result.inserted_id)

# except pymongo.errors.DuplicateKeyError:
#     # Handle the case where a document with the same "email" field already exists
#     print("Data with the same email already exists.")

# except pymongo.errors.PyMongoError as e:
#     # Handle any other MongoDB-related errors that may occur during the insertion
#     print("An error occurred:", e)





# Define a filter query to match documents with names containing "sooraj"
filter_query = {"name": {"$regex": "sooraj"}}  # "i" for case-insensitive match

# Delete documents that match the filter query
result = collection.find(filter_query)

# Print the number of documents deleted
if result:
    for document in result:
        print(document)
else:
    print("Document not found.")

