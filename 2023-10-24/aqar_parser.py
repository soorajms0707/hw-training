import pymongo
from parsel import Selector
import requests
import time
import re
from datetime import datetime
import random

class AqarScraper:
    def __init__(self):
        self.session = requests.Session()
        # self.user_agents = [
        #     "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
        #     "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        #     "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36,gzip(gfe)",
        #     "Mozilla/5.0 (Linux; Android 13; SM-S901U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        #     "Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        #     "Mozilla/5.0 (Linux; Android 12; moto g pure) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        #     "Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        #     "Mozilla/5.0 (iPhone12,1; U; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/15E148 Safari/602.1",
        #     "Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; RM-1152) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.15254",
        #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
        # ]
        self.headers = {
            "user-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
            }
        # self.scraped_data_count = 0

    def get_random_user_agent(self):
        return random.choice(self.user_agents)

    def fetch_urls(self): 
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["AQAR"]
        collection = db["properties"]

        # Fetch all documents in the collection
        cursor = collection.find({}, {"url": 1})  # Only retrieve the "url" field
        for doc in cursor:
            url = doc["url"]
            self.parse(url)
            time.sleep(3)

        client.close()

    def make_request(self, url, max_retries=5, retry_delay=3):
        # if self.scraped_data_count >= 100:
        # Print the user-agent before changing
            # print(f"Changing user-agent to: {self.get_random_user_agent()}")
        
        # Change user agent after processing 100 URLs
            # self.headers["User-Agent"] = self.get_random_user_agent()
            # self.scraped_data_count = 0
        # Print the user-agent after changing
            # print(f"Changed user-agent to: {self.headers['User-Agent']}")

        for _ in range(max_retries):
            try:
                response = self.session.get(url, headers=self.headers)
                response.raise_for_status()
                if response.status_code == 200:
                    return response
            except requests.exceptions.RequestException as e:
                print(f"Failed to make a request: {str(e)}")
            print(f"Retrying request to {url}...")
            time.sleep(retry_delay)
        return None

    def clean_data(self, data):
        cleaned_data = {}
        for key, value in data.items():
            cleaned_value = str(value) if value is not None else None
            cleaned_value = cleaned_value.strip() if cleaned_value else None
            cleaned_value = cleaned_value.replace(" ", "").replace("\n", "") if cleaned_value is not None else None
            cleaned_data[key] = cleaned_value
        return cleaned_data

    def parse(self, url):
        # print(url)
        response = self.make_request(url)
        if response:
            product_selector = Selector(text=response.text)
            product_html = product_selector.get()

            broker_display_name = product_selector.xpath('//div[@class="ProfileCard-module_name__AoEWG"]/a/span/text()').get()
            if broker_display_name:
                broker = broker_display_name.upper()
            else:
                broker = None
            category_url1 = url.rfind("/")
            category_url = url[:category_url1 + 1]
            title = product_selector.xpath('//h1[@class="listingView_title__ttwtw"]/text()').get()
            description = product_selector.xpath('//div[@class="listingView_description__N7Hio"]/text()').getall()
            lng, lat = None, None
            
            lat_match = re.search(r'"lat":([0-9.]+)', product_html)
            lng_match = re.search(r'"lng":([0-9.]+)', product_html)
            if lat_match and lng_match:
                lat = lat_match.group(1) if lat_match else None
                lng = lng_match.group(1) if lng_match else None

            price_currency = product_selector.xpath('//div[@class="listingView_price__2kZQ8"]/text()').get()
            if price_currency:
                parts = price_currency.split()
                price = parts[0] if parts else None
                currency = parts[1] if len(parts) > 1 else None
                price_per = parts[2] if len(parts) > 2 else None
            else:
                price = currency = price_per = None

            rooms = re.search(r'"rooms":(\d+)', product_html)
            rooms_value = rooms.group(1) if rooms else None
            bathrooms = re.search(r'"wc":(\d+)', product_html)
            bathrooms_value = bathrooms.group(1) if bathrooms else None
            furnished_match = re.search(r'"furnished":(\d+)', product_html)
            furnished_value = int(furnished_match.group(1)) if furnished_match else None

            area_match = re.search(r'"area":(\d+)', str(product_html))
            area_value = int(area_match.group(1)) if area_match else None
            if area_value is not None:
                area_value = str(area_value) + " m²"
            image_urls = product_selector.xpath('//img[@alt="listing images"]/@src').getall()
            image_count = len(image_urls)
            verified_match = re.search(r'"iam_verified":(true|false)', product_html)
            verified_value = verified_match.group(1) if verified_match else None

            breadcrumb = [item.strip() for item in product_selector.xpath('//li[@class="breadcrumb-module_item__ZLYPz"]/a/text()').getall()]
            if len(breadcrumb) > 1:
                category = breadcrumb[1]
            else:
                category = None

            today = datetime.today()
            today_value = today.strftime("%Y-%m-d")
            published_date = product_selector.xpath('//div[@class="listingView_advertiserDetails__MSxmX"]/div/text()').get()
            if published_date:
                date = published_date.split()
                published_at = date[2]
            else:
                published_at = None

            data = {
                "url": response.url,
                "broker_display_name": broker_display_name,
                "broker": broker,
                "category": category,
                "category_url": category_url,
                "title": title,
                "description": description,
                "longitude": lng,
                "latitude": lat,
                "price": price,
                "currency": currency,
                "price_per": price_per,
                "bedrooms": rooms_value,
                "bathrooms": bathrooms_value,
                "furnished": furnished_value,
                "scraped_ts": today_value,
                "details": area_value,
                "number_of_photos": image_count,
                "date": today_value,
                "published_at": published_at,
                "verified": verified_value,
            }

            cleaned_data = self.clean_data(data)
            for key, value in cleaned_data.items():
                if value is None:
                    cleaned_data[key] = None

            try:
                client = pymongo.MongoClient('mongodb://localhost:27017/')
                db = client["AQAR"]
                collection = db['property_data']
                collection.create_index([("url", pymongo.ASCENDING)], unique=True)
                collection.insert_one(cleaned_data)
            except pymongo.errors.DuplicateKeyError:
                print(f"Duplicate key error: Document with URL {response.url} already exists.")
        # self.scraped_data_count += 1

if __name__ == "__main__":
    scraper = AqarScraper()
    scraper.fetch_urls()
    print("Scraping completed.")
