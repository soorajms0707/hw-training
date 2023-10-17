import requests
from parsel import Selector
import csv
import time

class Dubizzle:
    def __init__(self):
        self.start_urls = [
            "https://uae.dubizzle.com/property-for-rent/residential/",
            "https://uae.dubizzle.com/property-for-sale/residential/"
        ]
        self.entries_per_url = 100
        self.page = 2
        self.line = 0
        self.session = requests.Session()
        self.current_url_index = 0  # Track the current URL index
        self.data_count = 0  # Track the number of data entries collected
        self.processed_urls = set() 
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-Encoding": "gzip, deflate, br",
            "accept-Language": "en-US,en;q=0.9,ml-IN;q=0.8,ml;q=0.7",
            "upgrade-Insecure-Requests": "1",
            "user-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        

    def start(self):
        self.data_count = 0

        while self.current_url_index <len(self.start_urls):
            current_url = self.start_urls[self.current_url_index]
            self.parse_url(current_url)
        print("No more urls. Scraping completed")

    def parse_url(self, current_url):
        self.data_count = 0

        while self.data_count < self.entries_per_url:
            if self.data_count >= self.entries_per_url:
                break  # Stop scraping when the limit is reached
            response = self.make_request(current_url)
            if response is not None:
                selector = Selector(text=response.text)
                self.parse(selector, response.text, current_url)
                self.data_count += 1
            else:
                break

        if self.data_count < self.entries_per_url:
            print("No more data to scrape from the current URL. Switching to the next URL.")
        else:
            self.data_count = 0  # Reset data_count when switching to the next URL

    def make_request(self, url, max_retries=5, retry_delay=3):

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

    def get_next_page_url(self, current_url):

        next_page_url = f"{current_url}?page={self.page}"
        self.page += 1
        response = self.make_request(next_page_url)
        if response is not None:
            selector = Selector(text=response.text)
            self.parse(selector, response.text, current_url)

    def parse(self, selector, text, current_url):
        while self.data_count < self.entries_per_url:
            product_url = selector.xpath('//a[@class="sc-15l4r6f-1 sc-15l4r6f-2 eabKDt kPUoSI"]/@href').getall()

            for url in product_url:
                if url in self.processed_urls:
                    print(url,"already scraped url")
                
                if self.data_count >=self.entries_per_url:
                    break
                self.processed_urls.add(url)
                print(url)
                response = self.make_request("https://uae.dubizzle.com/" + url)

                if response is not None and response.status_code == 200:
                    product_selector = Selector(text=response.text)

                    image_url = product_selector.xpath('//img[@alt="listing images"]/@src').getall()
                    breadcrumb = product_selector.xpath('//span[@class="MuiTypography-root MuiTypography-subtitle2 css-12lvvp"]/text()').getall()
                    currency = product_selector.xpath('//p[@class="MuiTypography-root MuiTypography-body1 css-ui2w6t"]/text()').get()
                    rooms = product_selector.xpath('//p[@class="MuiTypography-root MuiTypography-body1 css-kl0fiy"]/text()').get()
                    bathrooms = product_selector.xpath('//p[@class="MuiTypography-root MuiTypography-body1 css-kl0fiy"]/text()').getall()
                    price = product_selector.xpath('//p[@class="MuiTypography-root MuiTypography-body1 css-jt41tg"]/text()').get()
                    currency = product_selector.xpath('//p[@class="MuiTypography-root MuiTypography-body1 css-ui2w6t"]/text()').get()
                    rooms  = product_selector.xpath('//p[@data-testid="bed_space"]/text()').get()
                    bathrooms = product_selector.xpath('//p[@data-testid="bath"]/text()').get()
                    sqft = product_selector.xpath('//p[@data-testid="sqft"]/text()').get()
                    location = product_selector.xpath('//p[@data-testid="location-information"]/text()').get()
                    type = product_selector.xpath('//div[@data-testid="Type"]/text()').get()
                    Purpose = product_selector.xpath('//div[@data-testid="Purpose"]/text()').get()
                    Property_Age = product_selector.xpath('//div[@data-testid="Property Age"]/text()').get()
                    Furnishing = product_selector.xpath('//div[@data-testid="Furnishing"]/text()').get()
                    Updated = product_selector.xpath('//div[@data-testid="Updated"]/text()').get()
                    agent_name= product_selector.xpath('//h6[@data-testid="agent-name"]/text()').get()
                    agent = product_selector.xpath('//p[@class="MuiTypography-root MuiTypography-body1 css-1eeyhet"]/text()').get()
                    Permit_Number = product_selector.xpath('//div[@data-testid="Permit Number"]/text()').get()
                    Reference = product_selector.xpath('//div[@data-testid="Reference ID"]/text()').get()
                    Amenities = product_selector.xpath('//span[@class="MuiTypography-root MuiTypography-medium css-1lu8jlx"]/text()').getall()

                    data = {

                        "url": response.url,
                        "Image_url": image_url,
                        "Breadcrumb": breadcrumb,
                        "price":price,
                        "currency":currency,
                        "bed rooms":rooms,
                        "bathroom":bathrooms,
                        "sqft":sqft,
                        "location":location,
                        "type":type,
                        "Purpose":Purpose,
                        "Property_Age":Property_Age,
                        "Furnishing":Furnishing,
                        "Updated":Updated,
                        "agent-name":agent_name,
                        "agent":agent,
                        "Permit Number":Permit_Number,
                        "Reference ID":Reference,
                        "Amenities":Amenities
                    }

                    self.save_data(data)
                    self.data_count += 1

            if self.data_count < self.entries_per_url:
                self.get_next_page_url(current_url)
            else:
                print(f"Switching to the next URL after collecting {self.entries_per_url} data entries.")
                self.page = 2  # Reset page number
                self.current_url_index += 1
                break
        self.start

    def save_data(self, data):
        filename = "output_dubizzle.csv"

        with open(filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            if self.line == 0:
                writer.writeheader()
            writer.writerow(data)
        print(filename)
        self.line += 1
        # self.data_count += 1

if __name__ == "__main__":
    scraper = Dubizzle()
    scraper.start()
