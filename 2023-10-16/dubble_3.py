import requests
from parsel import Selector
import csv
import re
import time

class Dubizzle:
    def __init__(self):
        self.start_urls = [
            "https://uae.dubizzle.com/property-for-rent/residential/",
            "https://uae.dubizzle.com/property-for-sale/residential/"
        ]
        self.entries_per_url = 100
        self.page = 2
        self.line =0
        self.counter = 0
        self.session = requests.Session()
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-Encoding": "gzip, deflate, br",
            "accept-Language": "en-US,en;q=0.9,ml-IN;q=0.8,ml;q=0.7",
            "upgrade-Insecure-Requests": "1",
            "user-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }

    def start(self):
        for start_url in self.start_urls:
            self.page = 2  # Reset the page number for each start URL
            for _ in range(self.entries_per_url):
                response = self.make_request(start_url)
                if response is not None:
                    selector = Selector(text=response.text)
                    self.parse(selector, response.text)
                    self.counter += 1
                    if self.counter >= self.entries_per_url:
                        break

    def make_request(self, url, max_retries=5, retry_delay=3):
        for _ in range(max_retries):
            try:
                response = self.session.get(url, headers=self.headers)
                response.raise_for_status()
                print(response.status_code)
                print(response.reason)
                if response.status_code == 200:
                    return response
            except requests.exceptions.RequestException as e:
                print(f"Failed to make a request: {str(e)}")
            print(f"Retrying request to {url}...")
            time.sleep(retry_delay)
        return None

    def get_next_page_url(self):
        try:
            if "property-for-rent" in self.start_urls:
                next_page_url = f"https://uae.dubizzle.com/property-for-rent/residential/?page={self.page}"
            else:
                next_page_url = f"https://uae.dubizzle.com/property-for-sale/residential/?page={self.page}"

            self.page += 1
        
            response = self.make_request(next_page_url)
            if response is not None:
                selector = Selector(text=response.text)
                self.parse(selector, response.text)
        except requests.exceptions.RequestException as e:
            print(f"Failed to make a request: {str(e)}")
    def parse(self, selector, text):
        while True:
            product_url = selector.xpath('//a[@class="sc-15l4r6f-1 sc-15l4r6f-2 eabKDt kPUoSI"]/@href').getall()
            if not product_url:
                print("No more data to scrape. Exiting.")
                break  # Stop when there are no more product URLs

            for url in product_url:
                print(url)
                response = self.make_request("https://uae.dubizzle.com/" + url)
                if response is not None and response.status_code == 200:
                    product_selector = Selector(text=response.text)
                    image_url = product_selector.xpath('//img[@alt="listing images"]/@src').getall()
                    breadcrumb = product_selector.xpath('//span[@class="MuiTypography-root MuiTypography-subtitle2 css-12lvvp"]/text()').getall()
                    price = product_selector.xpath('//p[@class="MuiTypography-root MuiTypography-body1 css-jt41tg"]/text()').get()
                    currency = product_selector.xpath('//p[@class="MuiTypography-root MuiTypography-body1 css-ui2w6t"]/text()').get()
                    rooms = product_selector.xpath('//p[@class="MuiTypography-root MuiTypography-body1 css-kl0fiy"]/text()').get()
                    bathrooms = product_selector.xpath('//p[@class="MuiTypography-root MuiTypography-body1 css-kl0fiy"]/text()').getall()

                    data = {
                        "url": response.url,
                        "Image_url": image_url,
                        "Breadcrumb": breadcrumb,
                        "price": price,
                        "currency": currency,
                        "bed rooms": rooms,
                        "bathroom": bathrooms,
                    }

                    filename = "output_d.csv"
                    with open(filename, "a", newline="", encoding="utf-8") as file:
                        writer = csv.DictWriter(file, fieldnames=data.keys())
                        if self.line  == 0:
                            writer.writeheader()
                        writer.writerow(data)
                    print(filename)
                    self.line  += 1

            self.get_next_page_url()

if __name__ == "__main__":
    scraper = Dubizzle()
    scraper.start()
