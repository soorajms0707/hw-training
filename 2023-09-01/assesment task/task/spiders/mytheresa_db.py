import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mytheresa"]
collection = db["products"]



# data = {
#     "breadcrumb": [
#         "Men",
#         "Designers",
#         "Manolo Blahnik",
#         "Shoes",
#         "Boots",
#         "Chelsea boots"
#     ],
#     "image_url": "https://img.mytheresa.com/1094/1236/90/jpeg/catalog/product/21/P00831255.jpg",
#     "brand": "Manolo Blahnik",
#     "product_name": "hellooo",
#     "listing_price": "€ 755",
#     "offer_price": 456,
#     "discount": 78,
#     "product_id_text": "P00831255",
#     "sizes": [
#         "UK_ 6 / EU 40",
#         "UK_ 7 / EU 41",
#         "UK_ 7.5 / EU 41.5",
#         "UK_ 8 / EU 42",
#         "UK_ 8.5 / EU 42.5",
#         "UK_ 9 / EU 43",
#         "UK_ 9.5 / EU 43.5",
#         "UK_ 10 / EU 44",
#         "UK_ 10.5 / EU 44.5",
#         "UK_ 11 / EU 45",
#         "UK_ 12 / EU 46",
#         "UK_ 13 / EU 47"
#     ],
#     "description": "Team your cold-weather looks with the Delsa Suede Chelsea boot from Manolo Blahnik. The Italian-crafted pair is made from smooth suede and will look good paired with chinos, jeans, and pants.",
#     "other_images": []
# }

# response=collection.insert_one(dict(data))
# print(response)





# query = {"product_name":"hellooo"}
# results = collection.find(query)


# for document in results:
#     print(document)

# filter_query = {"product_name":"hellooo"}
# update_data = {"$set": {"listing_price": "€ 855"}}
# result = collection.update_one(filter_query, update_data)
# print("Modified documents:", result.modified_count)



delete_query = {"product_name":"hellooo"}
result = collection.delete_one(delete_query)
print("Deleted document count:", result.deleted_count)
