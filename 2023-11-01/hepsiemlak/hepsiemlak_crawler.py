import time
import pymongo
from settings import make_request,URL
from pipeline import connect_to_mongodb

class HepsiemlakCrawler:
    def __init__(self):
        self.base_urls = [
            "https://www.hepsiemlak.com/api/realty-list/antalya-satilik",
            "https://www.hepsiemlak.com/api/realty-list/antalya-kiralik",
            "https://www.hepsiemlak.com/api/realty-list/antalya-sezonluk-kiralik",    
        ]
        self.entries_per_url = 1000
        self.page = 1
        self.line = 0
        self.current_url_index = 0 
        self.data_count = 0  

    def start(self):
        self.data_count = 0
        while self.current_url_index < len(self.base_urls):
            current_url =  self.base_urls[self.current_url_index]
            url=f"{current_url}?page={self.page}&fillIntentUrls=true"
            self.parse_url(current_url,url)
        print("No more URLs. Scraping completed")

    def parse_url(self,current_url, url):
        self.data_count = 0

        while self.data_count < self.entries_per_url:
            if self.data_count >= self.entries_per_url:
                break  
            response = make_request(url)
            if response is not None:
                self.parse_property(response, current_url)
                self.data_count += 1
            else:
                break

        if self.data_count < self.entries_per_url:
            print("No more data to scrape from the current URL. Switching to the next URL.")
        else:
            self.data_count = 0 

    def get_next_page_url(self, current_url):
        self.page += 1
        next_page_url = f"{current_url}?page={self.page}&fillIntentUrls=true"
        response = make_request(next_page_url)
        if response is not None:
            self.parse_property(response,current_url)

    def parse_property(self, response, current_url):
        while self.data_count < self.entries_per_url:
            time.sleep(3)
            response_json = response.json()
            if 'realtyList' in response_json:
                realty_list = response_json['realtyList']
                for property_data in realty_list:
                    if self.data_count >= self.entries_per_url:
                         break
                    detail_url = property_data.get("detailUrl")
                    if detail_url:
                        print(detail_url)
                        last_part = detail_url.rsplit('/', 1)[-1]
                        api_url = f"https://www.hepsiemlak.com/api/realties/{last_part}"
                        print(api_url)
                        full_url=f"https://www.hepsiemlak.com/{detail_url}"
                        data = {
                                "api_url": api_url,
                                "url":full_url
                        }
                        try:
                            db=connect_to_mongodb()
                            db[URL].insert_one(data)
                            print(f"{full_url}")
                        except pymongo.errors.DuplicateKeyError:
                            print(f"URL '{full_url}' is already in the collection, skipping.")
                        self.data_count += 1
                        time.sleep(2)
                if self.data_count < self.entries_per_url:
                    self.get_next_page_url(current_url)
                else:
                    print(f"Switching to the next URL after collecting {self.entries_per_url} data entries.")
                    self.page = 1  # Reset page number
                    self.current_url_index += 1
                    break
            self.start

if __name__ == "__main__":
    scraper = HepsiemlakCrawler()
    scraper.start()