# zxc

# # Username and password (replace with your actual values)
# username = "sooraj"
# password = "123"

# # Escape the username and password
# escaped_username = quote_plus(username)
# escaped_password = quote_plus(password)

# # Connection string
# # connection_string = f"mongodb+srv://{escaped_username}:{escaped_password}@cluster0.t6e6og9.mongodb.net/test?retryWrites=true&w=majority"
# address= "mongodb://localhost:27017"

# # Connect to the MongoDB server
# client = pymongo.MongoClient(address)

# # Select the database
# db = client["xample"]

# # Select or create a collection
# collection = db["mycollection"]

# # Data to be inserted
# data = {
#     "name": "Jffff",
#     "age": 3085,
#     "email": "n@example.com"
# }

# # Insert the data into the collection
# inserted_data = collection.insert_one(data)

# # Print the inserted document's ID
# print("Inserted document ID:", inserted_data.inserted_id)




import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["company"]
collection = db["employee"]


# # Data to be inserted
data = {
    "name": "sooraj",
    "age": 3085,
    "email": "n@example.com"
}

result = collection.insert_one(data)

query = {"name": "sooraj"}
results = collection.find(query)

for document in results:
    print(document)


filter_query = {"name": "sooraj"}
update_data = {"$set": {"age": 31}}
result = collection.update_one(filter_query, update_data)
print("Modified documents:", result.modified_count)

# delete_query = {"name": "sooraj"}
# result = collection.delete_one(delete_query)
# print("Deleted document count:", result.deleted_count)

