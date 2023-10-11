import requests
from parsel import Selector
import csv

class Houza:
    def __init__(self):
        self.start_url = "https://houza.com/en/search?listingType=SALE"
        self.page = 2
        self.counter = 0
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'

    def start(self):
        headers = {'User-Agent': self.user_agent}
        response = requests.get(self.start_url, headers=headers)
        print(response.status_code)
        print(response.reason)
        if response.status_code == 200:
            selector = Selector(text=response.text)
            self.parse(selector)

    def parse(self, selector):
        product_url = selector.xpath('//a[@class="list-card__content"]/@href').getall()

        for url in product_url:
            print(url)
            headers = {'User-Agent': self.user_agent}
            response = requests.get("https://houza.com/"+url, headers=headers)
            if response.status_code == 200:
                # print(response.status_code)
                # print(response.reason)
                if response.status_code == 200:
                    product_selector = Selector(text=response.text)
                    self.parse_properties(product_selector,response)

        if self.page == 2:
            next_page_url = selector.xpath('//a[@class="arrow arrow-left ng-star-inserted"]/@href').get()
            self.page += 1
        else:
            next_page_url = selector.xpath('//a[@class="arrow arrow-left ng-star-inserted"][2]/@href').get()

        if next_page_url:
            next_page_url = f'https://houza.com/{next_page_url}'
            print(next_page_url)
            headers = {'User-Agent': self.user_agent}
            response = requests.get(next_page_url, headers=headers)
            if response.status_code == 200:
                selector = Selector(text=response.text)
                self.parse(selector)

    def parse_properties(self, selector, response):


        data = {
            "product_url":response.url,
            "Title": selector.xpath('//h1[@class="title ng-star-inserted"]/text()').get(),
            "image_url": selector.xpath('//img[@class="responsive-item"]/@src').getall(),
            "price": (selector.xpath('//div[@class="price"]/span/text()').get()),
            "broker_name": selector.xpath('//div[@class="names"]/span/text()').get(),
            "broker": selector.xpath('//div[@class="names"]/span[2]/text()').get(),
            "category": selector.xpath('//h2[@class="subtitle no-mb ng-star-inserted"]/text()').get(),
            "bedroom": selector.xpath('//span[@class="text ng-star-inserted"]/text()').get(),
            "bathroom":selector.xpath('//span[@class="text ng-star-inserted"][2]/text()').get(),
            # "description": selector.xpath('//div[@class="property_description"]/text()').get(),
            "amenities": selector.xpath('//div[@class="amenity-item ng-star-inserted"]/span[@class="label"]/text()').getall(),
            }
        
        if data["Title"]:
            self.save_to_csv(data)
            self.counter += 1



    def save_to_csv(self, data):
        filename = "output_houza.csv"
        with open(filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            if self.counter == 0:
                writer.writeheader()
            writer.writerow(data)
        print(filename)

if __name__ == "__main__":
    scraper = Houza()
    scraper.start()
