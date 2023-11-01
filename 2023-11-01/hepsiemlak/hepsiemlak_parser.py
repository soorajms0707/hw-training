import pymongo
from parsel import Selector
import requests
import time
import re
from datetime import datetime
from settings import make_request

class DubizzleParser:

    def fetch_urls(self): 
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["Hepsiemlak"]
        collection = db["properties_urls"]

        cursor = collection.find({}, {"api_url": 1}) 
        for doc in cursor:
            url = doc["api_url"]
            self.parse_data(url)
            time.sleep(3)

        client.close()
   
    def clean_data(self, data):
        cleaned_data = {}
        for key, value in data.items():
            cleaned_value = str(value) if value is not None else None
            cleaned_value = cleaned_value.strip() if cleaned_value else None
            cleaned_value = cleaned_value.replace(" ", "").replace("\n", "") if cleaned_value is not None else None
            cleaned_data[key] = cleaned_value
        return cleaned_data

    def parse_data(self, url):
        response = make_request(url)
        if response.status_code == 200:
            property_selector = Selector(text=response.text)
            property_html = property_selector.get()

            title = data.get("realtyDetail", {}).get("title", "Title Not Found")
            description = data.get("realtyDetail", {}).get("description", "Description Not Found")

            data = {
                    "url": url,
                    "broker_display_name": title,
                # Add other data extraction logic here
                }
            print(data)
        else:
            print(f"Failed to fetch data from {url}. Status code: {response.status_code}") 
        
            # cleaned_data = self.clean_data(data)
            # for key, value in cleaned_data.items():
            #     if value is None:
            #         cleaned_data[key] = None

            # try:
            #     client = pymongo.MongoClient('mongodb://localhost:27017/')
            #     db = client["Dubizzle"]
            #     collection = db['properties_data']
            #     collection.create_index([("url", pymongo.ASCENDING)], unique=True)
            #     collection.insert_one(cleaned_data)
            # except pymongo.errors.DuplicateKeyError:
            #     print(f"Duplicate key error: Document with URL {response.url} already exists.")

if __name__ == "__main__":
    scraper = DubizzleParser()
    scraper.fetch_urls()
    print("Scraping completed.")