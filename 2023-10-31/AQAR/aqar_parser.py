import pymongo
from parsel import Selector
from settings import make_request,DATA,URL
from pipeline import connect_to_mongodb
import time
import re
from datetime import datetime

class AqarScraper:

    def fetch_urls(self): 
        url_collection = connect_to_mongodb()
        for doc in url_collection[URL].find():
            url = doc.get("url")
            self.parse(url)
            time.sleep(3)
        print("finished scraping")

    def clean_data(self, data):
        cleaned_data = {}
        for key, value in data.items():
            cleaned_value = str(value) if value is not None else None
            cleaned_value = cleaned_value.strip() if cleaned_value else None
            cleaned_value = cleaned_value.replace(" ", "").replace("\n", "") if cleaned_value is not None else None
            cleaned_data[key] = cleaned_value
        return cleaned_data

    def parse(self, url):
        response = make_request(url)
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
            today_value = today.strftime("%Y-%m-%d")
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
                db=connect_to_mongodb()
                db[DATA].insert_one(cleaned_data)
                print(f"{response.url}")
            except pymongo.errors.DuplicateKeyError:
                print(f"Duplicate key error: Document with URL {response.url} already exists.")

if __name__ == "__main__":
    scraper = AqarScraper()
    scraper.fetch_urls()
    print("Scraping completed.")
