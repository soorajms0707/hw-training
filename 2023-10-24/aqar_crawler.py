import requests
from parsel import Selector
import time
import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["AQAR"]
collection = db["properties_urls"]

collection.create_index([("url", pymongo.ASCENDING)], unique=True)

class AqarScraper:
    def __init__(self):
        self.start_url = "https://sa.aqar.fm/%D8%B9%D9%82%D8%A7%D8%B1%D8%A7%D8%AA/1"
        self.page = 2
        self.session = requests.Session()
        
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

    def parse_url(self):
        url=self.start_url
        while True:
            response = self.make_request(url)
            if response.status_code == 200:
                selector = Selector(text=response.text)
                product_url = selector.xpath('//div[@class="listing_LinkedListingCard__5SRvZ"]/@href').getall()
                if not product_url:
                    print("No more data to scrape. Exiting.")
                    break
                for url in product_url:
                    full_url = "https://sa.aqar.fm" + url
                    self.save_to_mongodb(full_url)
                    time.sleep(3)
                self.page += 1
                url = f"https://sa.aqar.fm/%D8%B9%D9%82%D8%A7%D8%B1%D8%A7%D8%AA/{self.page}"
            elif response and response.status_code == 403:
                print("Received a 403 Forbidden error. Pausing for a while before retrying...")
                time.sleep(60)
            else:
                print("Failed to make a request. Exiting.")
                break

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

    def save_to_mongodb(self, url):
        data = {"url": url}
        # Try to insert the URL into the collection with a unique constraint
        try:
            response = collection.insert_one(data)
            print(response.inserted_id)
        except pymongo.errors.DuplicateKeyError:
            # Handle the case when the URL is already in the collection
            print(f"URL '{url}' is already in the collection, skipping.")

if __name__ == "__main__":
    scraper = AqarScraper()
    scraper.parse_url()
