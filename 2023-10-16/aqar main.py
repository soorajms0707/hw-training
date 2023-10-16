import requests
from parsel import Selector
import csv
import re


class Aqar:
    def __init__(self):
        self.start_url = "https://sa.aqar.fm/%D8%B9%D9%82%D8%A7%D8%B1%D8%A7%D8%AA/1"
        self.page = 2
        self.counter = 0
        self.session = requests.Session()
        self.headers = {
                        "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                        "accept-Encoding":"gzip, deflate, br",
                        "accept-Language":"en-US,en;q=0.9,ml-IN;q=0.8,ml;q=0.7",
                        "upgrade-Insecure-Requests":"1",
                        "user-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
                        }
        

    def start(self):
            try:
                
                response = requests.get(self.start_url, headers=self.headers)
                response.raise_for_status()
                print(response.status_code)
                print(response.reason)
                if response.status_code == 200:
                    selector = Selector(text=response.text)
                    self.parse(selector,response.text)

            except requests.exceptions.RequestException as e:
                print(f"Failed to make a request: {str(e)}")
                


    def parse(self, selector,text):
        while True:
            product_url = selector.xpath('//div[@class="listing_LinkedListingCard__5SRvZ"]/@href').getall()

            if not product_url:
                print("No more data to scrape. Exiting.")
                break  # Stop when there are no more product URLs

            for url in product_url:
                print(url)
                response = requests.get("https://sa.aqar.fm/" + url, headers=self.headers)
                print(response.status_code)
                print(response.reason)

                if response.status_code == 200:
                    product_selector = Selector(text=response.text)
                    description = " ".join([line.strip() for line in product_selector.xpath('//div[@class="listingView_description__N7Hio"]/text()').getall() if line.strip()])
                    image_url = product_selector.xpath('//img[@alt="listing images"]/@src').getall()
                    breadcrumb = [item.strip() for item in product_selector.xpath('//li[@class="breadcrumb-module_item__ZLYPz"]/a/text()').getall()]
                    title = product_selector.xpath('//h1[@class="listingView_title__ttwtw"]/text()').get().strip()
                    price_currency = product_selector.xpath('//div[@class="listingView_price__2kZQ8"]/text()').get().strip()
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
                        "Rooms":rooms_value,
                        "Bathrooms":bathrooms_value,
                        "Broker": broker,
                        "Licence Number":ad_license_number_value,
                        "Description": description,
                    }

                    filename = "output_aqar_main.csv"
                    with open(filename, "a", newline="", encoding="utf-8") as file:
                        writer = csv.DictWriter(file, fieldnames=data.keys())
                        if self.counter == 0:
                            writer.writeheader()
                        writer.writerow(data)
                    print(filename)
                    self.counter += 1

            self.get_next_page_url()



    def get_next_page_url(self):
        try:
            next_page_url = f"https://sa.aqar.fm/%D8%B9%D9%82%D8%A7%D8%B1%D8%A7%D8%AA/{self.page}"
            self.page +=1
            response = self.session.get(next_page_url, headers=self.headers)
            
            print("-------------------------------------------------------------------------------------------------------------")
            print(next_page_url)
            print("-------------------------------------------------------------------------------------------------------------")
            print(response.status_code)
            print(response.reason)
            if response.status_code == 200:
                selector = Selector(text=response.text)
                self.parse(selector,response.text)
        except requests.exceptions.RequestException as e:
                print(f"Failed to make a request: {str(e)}")



if __name__ == "__main__":
    scraper = Aqar()
    scraper.start()
