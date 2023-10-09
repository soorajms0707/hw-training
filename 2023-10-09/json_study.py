# python bult-in package
# store and exchanging data 
# data representation format 
# valid data types in json :-

# 1. strings     "hello"
# 2. numbers     12  2.3  -34  1.5e10
# 3. boolean     True  False
# 4. arrays      ["hi","hello"]  ("hii","hello")
# 5. objects     {"model": "BMW"}
# 6. null        empty values

# rules to follow in json
#1. json files have .json extension
#2. to represent data in json as key and value pairs
#                    {"key":"value"}
# value-->json data types
# use comma to separate multiple datas


import json


# json functions:-

# json.loads-->load string
x =  '{"name": "John", "age": 30, "address": {"city": "alappy", "state": "kerala", "country": "india"}, "skills": ["html", "css", "bootstrap"]}'
y = json.loads(x)

# the result is a Python dictionary:
# print(y.get("age"))

# print(y.get("agetwo",25))
# print(y.get("agetwo",y.get("age")))
# print(y["a"]["state"])
# print(y["skills"][0])
datas={
    "name":"surya",
    "age":23,
    "address":{
        "city":"alappuzha",
        "state":"kerala",
        "country":"india"
    },
    "married": True
}
updatess={
    "city":"kollam"
}
datas["address"].update(updatess)
json_strings = json.dumps(datas,indent=4)
# print(json_strings)

# json.dumps-->dump string

data = {
  "name": "John",
  "age": 30,
  "married": True,
  "divorced": False,
  "children": ("Ann","Billy"),
  "pets": None,
  "cars": [
    {"model": "BMW 230", "mpg": 27.5},
    {"model": "Ford Edge", "mpg": 24.1}
  ]
}
updates = {
    "age": 31,
    "children": ("Ann", "William")
}
data.update(updates)
# json_string = json.dumps(data)
# json_string = json.dumps(data,indent=4)
json_string = json.dumps(data,indent=4, separators=(". " , " = "))
# json_string = json.dumps(data,indent=4,skipkeys=True)
# skipkeys=True
# print(json_string)

# json.load -->load from file

# with open('datas.json', 'r') as file:
#     data = json.load(file)
#     print(data)
   

# json.dump-->write data to the file
data = [  {"name": "surya", "age": 23, "city": "New York"},
    {"name": "Alice", "age": 28, "city": "Seattle"},
    {"name": "Bob", "age": 30, "city": "San Francisco"}
]

with open('datas.json', 'w') as file:
    json.dump(data, file)

