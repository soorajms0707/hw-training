# import requests
# import mongodb

# client = mongodb.MongoClient("mongodb://localhost:27017/")
# db = client["mytheresa_db"]
# collection = db["products"]


# data_to_insert = {
#     "name": "John",
#     "age": 30,
#     "city": "New York"
# }
# insert_result = collection.insert_one(data_to_insert)

# response = requests.post(mongo_api_url, json=data_to_insert)

# if response.status_code == 201:
#     print("Data insertion successful!")
# else:
#     print(f"Failed to insert data. Status code: {response.status_code}")



import pymongo


# Username and password (replace with your actual values)
username = "sooraj"
password = "123"

# Escape the username and password
# escaped_username = quote_plus(username)
# escaped_password = quote_plus(password)

# Connection string
connection_string = f"mongodb+srv://{username}:{password}@cluster0.t6e6og9.mongodb.net/?retryWrites=true&w=majority"

# Connect to the MongoDB server
client = pymongo.MongoClient(connection_string)

# Select the database
db = client["mydatabase"]

# Select or create a collection
collection = db["mycollection"]

# Data to be inserted
data = {
    "name": "sooraj",
    "age": 29,
    "email": "sooraj@gmail.com"
}

# Insert the data into the collection
inserted_data = collection.insert_one(data)

# Print the inserted document's ID
print("Inserted document ID:", inserted_data.inserted_id)
