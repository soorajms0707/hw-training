import requests
from parsel import Selector
import csv
import re
import time
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["AQAR"]
collection = db["properties"]

class AqarScraper:
    def __init__(self):
        self.start_url = "https://sa.aqar.fm/%D8%B9%D9%82%D8%A7%D8%B1%D8%A7%D8%AA/1"
        self.page = 2
        self.counter = 0
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-Encoding": "gzip, deflate, br",
            "accept-Language": "en-US,en;q=0.9,ml-IN;q=0.8,ml;q=0.7",
            "upgrade-Insecure-Requests": "1",
            "user-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }

    def start(self):
        response = self.make_request(self.start_url)
        if response.status_code == 200:
            selector = Selector(text=response.text)
            self.parse(selector, response.text)

    def make_request(self, url, max_retries=5, retry_delay=3):
        for _ in range(max_retries):
            try:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                if response.status_code == 200:
                    return response
            except requests.exceptions.RequestException as e:
                print(f"Failed to make a request: {str(e)}")
            print(f"Retrying request to {url}...")
            time.sleep(retry_delay)
        return None

    def get_next_page_url(self):
        next_page_url = f"https://sa.aqar.fm/%D8%B9%D9%82%D8%A7%D8%B1%D8%A7%D8%AA/{self.page}"
        self.page += 1
        response = self.make_request(next_page_url)
        selector = Selector(text=response.text)
        self.parse(selector, response.text)

    def clean_data(self, data):
        cleaned_data = {}
        for key, value in data.items():
            if isinstance(value, list):
                cleaned_data[key] = [item.strip() if isinstance(item, str) else item for item in value]
            elif isinstance(value, str):
                cleaned_data[key] = value.strip()
            else:
                cleaned_data[key] = value
        return cleaned_data

    def parse(self, selector, text):
        while True:
            product_url = selector.xpath('//div[@class="listing_LinkedListingCard__5SRvZ"]/@href').getall()
            if not product_url:
                print("No more data to scrape. Exiting.")
                break 

            for url in product_url:
                print(url)
                response = requests.get("https://sa.aqar.fm/" + url, headers=self.headers)

                if response.status_code == 200:
                    product_selector = Selector(text=response.text)
                    description = product_selector.xpath('//div[@class="listingView_description__N7Hio"]/text()').getall()
                    image_url = product_selector.xpath('//img[@alt="listing images"]/@src').getall()
                    breadcrumb = [item.strip() for item in product_selector.xpath('//li[@class="breadcrumb-module_item__ZLYPz"]/a/text()').getall()]
                    title = product_selector.xpath('//h1[@class="listingView_title__ttwtw"]/text()').get()
                    price_currency = product_selector.xpath('//div[@class="listingView_price__2kZQ8"]/text()').get()
                    parts = price_currency.split()
                    price = parts[0]
                    currency = parts[1]
                    broker = product_selector.xpath('//div[@class="ProfileCard-module_name__AoEWG"]/a/span/text()').get()
                    rooms = re.search(r'"rooms":(\d+)', text)
                    rooms_value = rooms.group(1) if rooms else None
                    bathrooms = re.search(r'"wc":(\d+)', text)
                    bathrooms_value = bathrooms.group(1) if bathrooms else None
                    ad_license_match = re.search(r'"ad_license_number":"(\d+)"', text)
                    ad_license_number_value = ad_license_match.group(1) if ad_license_match else None

                    data = {
                        "url": response.url,
                        "Image_url": image_url,
                        "Breadcrumb": breadcrumb,
                        "Title": title,
                        "Price": price,
                        "Currency": currency,
                        "Rooms": rooms_value,
                        "Bathrooms": bathrooms_value,
                        "Broker": broker,
                        "Licence Number": ad_license_number_value,
                        "Description": description,
                    }
                    cleaned_data = self.clean_data(data)
                    self.save_data(cleaned_data)
                    self.save_to_mongodb(cleaned_data)
            self.get_next_page_url()

    def save_to_mongodb(self, data):
        response=collection.insert_one(dict(data))
        print(response)

    def save_data(self, data):
        filename = "output_aqar.csv"
        with open(filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            if self.counter == 0:
                writer.writeheader()
            writer.writerow(data)
        print(f"Saved cleaned data to {filename}")
        self.counter += 1

if __name__ == "__main__":
    scraper = AqarScraper()
    scraper.start()
