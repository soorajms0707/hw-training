import requests
from parsel import Selector
import csv
import time
import re

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

    def parse(self, selector , text, current_url):
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

                    image_url = product_selector.xpath('//div[@class="MuiBox-root css-1or7vt5"]/li/img/@src').getall()
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
                    # dis = re.search(r'"description":\{"ar":"(.*?)"\}', text)
                    # dis_value = dis.group(1) if dis else None
                    phone=self.get_phone_number()

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
                        "Amenities":Amenities,
                        "phone":phone,
                        # "dis":dis_value
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
    

    def get_phone_number(url):
        url = 'https://uae.dubizzle.com/en/property-for-sale/svc/api/v1/graphql'
        headers={
        "authority":"uae.dubizzle.com", 
        "accept": "application/json",
        "accept-language": "en",
        "cache-control": "must-revalidate, max-age=0, no-cache, no-store",
        "content-type": "application/json;charset=UTF-8",
        "cookie": "ias=0; sid=pow7523mn59wbm9duy4wkgpyy1punwu5; visid_incap_2413658=3Hl98yR8Si+/G7fbE87AxsvMLGUAAAAAQUIPAAAAAABwEmd7jS4Dy0oI1DtIBdLY; _gcl_au=1.1.1737827172.1697434833; _gid=GA1.2.1337590042.1697434835; _fbp=fb.1.1697434835546.1862383121; moe_uuid=0c658813-a1ad-4dbd-8397-3e1c5d1b4b64; USER_DATA=%7B%22attributes%22%3A%5B%5D%2C%22subscribedToOldSdk%22%3Afalse%2C%22deviceUuid%22%3A%220c658813-a1ad-4dbd-8397-3e1c5d1b4b64%22%2C%22deviceAdded%22%3Atrue%7D; OPT_IN_SHOWN_TIME=1697434838589; SOFT_ASK_STATUS=%7B%22actualValue%22%3A%22dismissed%22%2C%22MOE_DATA_TYPE%22%3A%22string%22%7D; _cc_id=bca8b54e1513c7017e1ffd985437b8d4; panoramaId=0821b788f56312b8d249143ca7d916d53938ccc73216aa214c32f5819a97dd9e; panoramaIdType=panoIndiv; panoramaId_expiry=1698039792420; default_site=12; _pbjs_userid_consent_data=3524755945110770; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%221258197886.1697434835%22%7D; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22YhnXQqs0yjCzNvQTTNW6%22%7D; nlbi_2413658=7FN6WNMW83UOcdqPT83W0gAAAABU9kxPuKfJDGstTfq5Sk+v; csrftoken=Vm4UOZ5nsyWc0UouQIluPZ1jAhs9cefsAZm5arcPHf2s2gPbDdAcPoCAdkxHUIl9; incap_ses_50_2413658=7WDlWDs/PQdYnY+/+KKxAMldLWUAAAAAx54TSt1WYKBZz94vOIXRVg==; SETUP_TIME=1697535794093; incap_ses_48_2413658=+tmXZBqxUTo1xAh19IeqAKNkL2UAAAAAydHBUqAR5GEacA54I2bFoQ==; UniqueLead=$23-24176884$24-24165840$23-24153380$24-24255717$24-24209136$24-24278526; reese84=3:JoGivx9Ye58CHbWidLwBhA==:robZ1PHbE8B3LiohQ8qXPrHIrAFQiZs+6Uk/E4FYR/vKkTvmUrCu1Kb6R9j3FdBqZe++wVubroRR1Mm1HbGztTmreO/YrGlsB1mbpjisZ+GNXhZ0z5NMv5udrv965tlLNWBzPkhMk40AGBChCTZIx7m6kwyWxjV9x2L1Iip2FL8Osltmq2RIZiYG0njA7A/VtEe4mYmG3yXVm4/3N9kQaM/B0of98mGdAGyQnSoipJ9ZynuNq8z+uSCIiTtHCWG/VwA25tK4KG36v6vZgiWTzbtxIJwR4O7cm0Eke72OrJqDGvTajdrFVuaMo854j5zJF7Q+7He1Qu+wdvB+iE3ThImAQfQygOZzWBWvNURjZSt3lsu2d6RUNgZnFQJJKZVucn3HcKnt9iIOWXVvC7z6kLnf7E4sY8r4xM+qX4QqXHsM7ZuFgtULb4xiLyhn9pM7bmngK7IqkE/NOl/lT7mZzg==:NEkNlfk65Yf6x8hwe4yQvfOMsMErbldv4GSmoiTAeYg=; nlbi_2413658_2147483392=5FY8Q4BrtHhbSsb4T83W0gAAAACMhiWKpEvIo2Rm47+Pz6nM; _gat_UA-205528691-1=1; __gads=ID=807bb518dd001452:T=1697434987:RT=1697608670:S=ALNI_MY-pGfORpTdGzQyFLPwxQLInGERGw; __gpi=UID=00000c6356c13552:T=1697434987:RT=1697608670:S=ALNI_MYpo5iimrgO3A9_VzKSIWu6yJuDow; _ga=GA1.2.1258197886.1697434835; cto_bundle=Mbyzq19LaSUyRnNHc3c3dlFydjZBVXNHQ0ZiTGhRSjlLbUM3ZGJDc3ZyMTFTZkpIaEJsT2FqMEFiUHdEVHR3bkVUYVA0bVhOZThFZWRXU2hQcWw4SkhiM2xHam52JTJCT3RCUXlERjlnNGFUVE13NXolMkYwZ2M0NVJLQVFrVEJLNFFTZ0NVZkQlMkI5SVhVcVVWS3hpU0dTOHluQ1RBTFlzWG96dE9DNkd2c0xnZGlNWGExeUwzU3RmMWxVZjBsWTRwbFF1Y1dHMTAzdmVhQ1BnJTJGbUxvMXo1QTIyMVQ4djNFTGk5dHcyTEdSVDJRRVA3a2pZR3laUmVrc0ZNeTNRN2Jva2UlMkZ6Z0hOMk5M; _ga_LRML1YM9GH=GS1.1.1697604887.18.1.1697608703.23.0.0",
        "origin":"https://uae.dubizzle.com",
        "referer": "https://uae.dubizzle.com/property-for-rent/residential/apartmentflat/2023/10/18/fully-furnished-near-metro-prime-location-2-736/",
        "sec-ch-ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Linux",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode":"cors",
        "sec-fetch-site":"same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "x-access-token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImQxNmU3ZDMwLWEwYTAtNDgxYy04ZTRiLTZiYTJjZmIxMWM3OCIsImlzcyI6ImR1Yml6emxlLmNvbSIsImF1ZCI6WyJkdWJpenpsZS5jb20iXSwic3ViIjoiZDE2ZTdkMzAtYTBhMC00ODFjLThlNGItNmJhMmNmYjExYzc4IiwiZXhwIjoxNjk3Njk1MDY4LCJpYXQiOjE2OTc2MDg2NjgsImp0aSI6ImM2MTc1ODI3LWRiN2ItNGQxMi1iMzk1LWJkYWQzNzgwNGQ0ZCIsInR5cCI6IkFjY2VzcyBKV1QgVG9rZW4iLCJmbGFncyI6eyJsb2dnZWRfaW4iOmZhbHNlLCJpc19zdGFmZiI6ZmFsc2UsImlzX3N1cGVydXNlciI6ZmFsc2UsImlzX3Byb3BlcnR5X2FnZW50IjpmYWxzZSwiaXNfbGFuZGxvcmQiOmZhbHNlLCJpc19tb3RvcnNfYWdlbnQiOmZhbHNlLCJpc19qb2JzX2FnZW50IjpmYWxzZSwiaXNfbGVhZF9ibG9jayI6ZmFsc2UsImlzX2NoYXRfYmxvY2siOmZhbHNlLCJoYXNfY2FsbF90cmFja2luZyI6ZmFsc2UsImNhbl9yZXBvcnQiOnRydWUsImhpZGVfcHVibGljX3Byb2ZpbGUiOmZhbHNlLCJpc19tb3RvcnNfYWdlbnRfZW1wbG95ZWVfdXNlciI6ZmFsc2V9LCJ1c2VyX2RhdGEiOnsidXNlcl9pZCI6bnVsbCwiZ2VuZGVyIjpudWxsLCJuYXRpb25hbGl0eSI6bnVsbCwiZWR1Y2F0aW9uIjpudWxsLCJyb2xlIjpudWxsLCJkb2IiOm51bGwsImFnZSI6bnVsbCwiZmlyc3RfbmFtZSI6IiIsImxhc3RfbmFtZSI6IiIsImVtYWlsIjoiIiwicGhvbmUiOiIiLCJ2ZXJpZmljYXRpb25fc3RhdHVzIjoibm90X2FwcGxpZWQiLCJ2ZXJpZmljYXRpb25fc3RhcnRfZGF0ZSI6bnVsbH19.Zkk8DHFho7mN5-CRUGRr2bRvTZ9FqAdDKlQO9v5HxRvEMDbPAkow0QHxZmidJ8Rr9h-UBIoYUL5S9krEf8zf6KYZmkPXk_tH9u_baDUfoVqS_EDvMgM8vswbPQnZZ1Ks0wF3oSjl2H4Pha3ii0tGi62Y9OJiTdLyebQ8qXVjkj5GI98Nqv-qKow9URsVhTOIgVwwQvlRwezsBcLdUpWRO0ZXB6VqHJdU6g5gQFvHgnoHo_BhVT-2P0YDFqwDlNAIODFZBYn5A3ACLSjIqaMghaKXMxK9tl9c0Hus3Yq95EAtT09l1qg8kUGYfzxbP42i5-027F-nyfzGT67qLHRIK4eK7yWPePxcU8Kia4q_0QUh3Ww6YMhrs2qMoJcgVCB7C_ltYiON4VVsUs1GArNoU6GFmtukVqBqO7lb42BJE2ezeNfCicQnWixqc0HL3HFod0cWNgCcnOAP-pg6idiwcTJ5Hivvj4ho9vAxLbHa05YeDXPbjAnQZC21Kn_JZv6tnjU9y-Dr6e1_7IDhwzVBoDZuC83sSs1Tv8_P_oyyBQDpxfIO-8HYcgHY3tY05wo6syzoqn6-381T8nYyl7M0zQjNCzgtwfCYJ2wPvnVW5zE3_vmZyEyKXPJ7k16rcwwWZO053GftG8iiPFq0O6civ2KwphW7gdtAg9LFln61o1U",
    

        }
        query = {
            "query": "{ listing(listingId: 24278526, categoryId: 24) { cta(userId: 0, siteId: 4, language: \"en\", includeContact: [\"chat\",\"phone_number\"]) } }"
        }

        response = requests.post(url,headers=headers, json=query)
        print(response)
        print(response.status_code)

        
    
        if response.status_code == 200:
        
            data = response.json()
            phone_number = data.get("data", {}).get("listing", {}).get("cta", {}).get("phone_number", {}).get("phone_number")
        
            if phone_number:
                return phone_number
            else:
                return "Phone number not found"
    


if __name__ == "__main__":
    scraper = Dubizzle()
    scraper.start()
