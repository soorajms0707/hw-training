from settings import make_request,URL
from pipeline import connect_to_mongodb
from parsel import Selector
import time
import pymongo

class AqarScraper:
    def __init__(self):
        self.start_url = "https://sa.aqar.fm/%D8%B9%D9%82%D8%A7%D8%B1%D8%A7%D8%AA/1"
        self.page = 2
        
    def parse_url(self):
        url=self.start_url
        db = connect_to_mongodb()
        while True:
            response = make_request(url)
            if response.status_code == 200:
                selector = Selector(text=response.text)
                product_url = selector.xpath('//div[@class="listing_LinkedListingCard__5SRvZ"]/@href').getall()
                if not product_url:
                    print("No more data to scrape. Exiting.")
                    break
                for url in product_url:
                    full_url = "https://sa.aqar.fm" + url
                    try:
                        db[URL].insert_one({"url": full_url}) 
                        print(f"Saved URL: {full_url}")
                    except pymongo.errors.DuplicateKeyError:
                        print(f"URL '{url}' is already in the collection, skipping.")
                    time.sleep(3)
                self.page += 1
                url = f"https://sa.aqar.fm/%D8%B9%D9%82%D8%A7%D8%B1%D8%A7%D8%AA/{self.page}"
            elif response and response.status_code == 403:
                print("Received a 403 Forbidden error. Pausing for a while before retrying...")
                time.sleep(60)
            else:
                print("Failed to make a request. Exiting.")
                break

if __name__ == "__main__":
    scraper = AqarScraper()
    scraper.parse_url()
