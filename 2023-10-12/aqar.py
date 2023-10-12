import requests
from parsel import Selector
import csv


# scraperer = cloudscraper.create_scraper()

class Aqar:
    def __init__(self):
        self.start_url = "https://sa.aqar.fm/%D8%B9%D9%82%D8%A7%D8%B1%D8%A7%D8%AA/1"
        self.page = 2
        self.counter = 0
        self.session = requests.Session()
        self.user_agent = 'Your User-Agent String'

    def start(self):
        
        try:
            headers = {"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                        "accept-Encoding":"gzip, deflate, br",
                        "accept-Language":"en-US,en;q=0.9,ml-IN;q=0.8,ml;q=0.7",
                        "upgrade-Insecure-Requests":"1",
                        "user-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}
            headers = {'User-Agent': self.user_agent}
            response =  requests.get(self.start_url, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes
            print(response.status_code)
            print(response.reason)
            if response.status_code == 200:
                selector = Selector(text=response.text)
                self.parse(selector)



        except requests.exceptions.RequestException as e:
            print(f"Failed to make the initial request: {str(e)}")
            return 


    def parse(self, selector):
        product_url = selector.xpath('//div[@class="listing_LinkedListingCard__5SRvZ"]/@href').getall()
        # print(product_url)
        for url in product_url:
            print(url)
            headers = {'User-Agent': self.user_agent}
            response = requests.get("https://sa.aqar.fm/"+url, headers=headers)
            print(response.status_code)
            print(response.reason)
            if response.status_code == 200:
                product_selector = Selector(text=response.text)
                self.parse_properties(product_selector,response)


        
        next_page_url = f"https://sa.aqar.fm/%D8%B9%D9%82%D8%A7%D8%B1%D8%A7%D8%AA/{self.page}"
        print(next_page_url)
        
        headers = {'User-Agent': self.user_agent}
        response = requests.get(next_page_url, headers=headers)
        self.page += 1

        print("-------------------------------------------------")
        print(response.status_code)
        print(response.reason)
        if response.status_code == 200:
                selector = Selector(text=response.text)
                self.parse(selector)

    def parse_properties(self, selector, response):


        data = {
        "url": response.url,
        "image_url": selector.xpath('//img[@alt="listing images"]/@src').getall(),
        "breadcrumb": [item.strip() for item in selector.xpath('//li[@class="breadcrumb-module_item__ZLYPz"]/a/text()').getall()],
        "title": selector.xpath('//h1[@class="listingView_title__ttwtw"]/text()').get().strip(),
        "price": selector.xpath('//div[@class="listingView_price__2kZQ8"]/text()').get().strip(),
        "description": " ".join([line.strip() for line in selector.xpath('//div[@class="listingView_description__N7Hio"]/text()').getall() if line.strip()]),
}

        
        
        self.save_to_csv(data)
        self.counter += 1



    def save_to_csv(self, data):
        filename = "output_aqar.csv"
        with open(filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            if self.counter == 0:
                writer.writeheader()
            writer.writerow(data)
        print(filename)




if __name__ == "__main__":
    scraper = Aqar()
    scraper.start()