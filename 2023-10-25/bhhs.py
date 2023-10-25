import requests
from parsel import Selector
import time
import pymongo

class BhssCrawler:
    def __init__(self):
        self.page = 1
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
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
        while self.page <= 5050:  # Adjust the page limit as needed
            url = f"https://www.bhhs.com/bin/bhhs/solrAgentSearchServlet?resultSize=10&sortType=1&page={self.page}&_=1698144935550"
            self.page += 1
            response = self.make_request(url)
            if response and response.status_code == 200:
                self.parse_data(response)
        else:
            print(f"Failed to make a request for page {self.page}. Exiting.")

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

    def get_description_from_profile(self, profile_url):
        response = self.make_request(profile_url)
        if response:
            profile_selector = Selector(text=response.text)
            description_list = profile_selector.xpath('//p[@class="collapsed-bio"]/text()').getall()
            description = " ".join(description_list)
            return description
        else:
            print(f"Failed to retrieve the profile page for URL: {profile_url}")
            return None

    def parse_data(self, response):
        product_selector = Selector(text=response.text)
        product_html = product_selector.get()
        agent_details = []

        for agent in product_html["value"]:
            full_name = agent.get("MemberFullName", "")
            first_name = ""
            middle_name = ""
            last_name = ""
            if len(full_name.split()) > 3 or "&" in full_name:
                first_name = full_name
            else:
                name_parts = full_name.split()
                if len(name_parts) == 1:
                    first_name = name_parts[0]
                elif len(name_parts) == 2:
                    first_name = name_parts[0]
                    last_name = name_parts[1]
                else:
                    first_name = name_parts[0]
                    middle_name = name_parts[1]
                    last_name = name_parts[2]

            office_name = str(agent.get("OfficeName", ""))
            title = str(agent.get("JobTitle", ""))
            languages_list = agent.get("MemberLanguages", [])
            languages = languages_list if isinstance(languages_list, list) else [str(languages_list)]
            image_url = str(agent.get("Photo", ""))
            address = str(agent.get("MemberAddress1", ""))
            city = str(agent.get("MemberCity", ""))
            state = str(agent.get("MemberStateOrProvince", ""))
            country = str(agent.get("MemberCountry", ""))
            zipcode = str(agent.get("MemberPostalCode", ""))
            office_phone_numbers = [(agent.get("MemberOfficePhone", ""))]
            agent_phone_numbers = [(agent.get("MemberMobilePhone", ""))]
            email = str(agent.get("MemberEmail", ""))
            website = str(agent.get("SocialMediaWebsiteUrlOrId", ""))
            social = {
                "facebook": str(agent.get("SocialMediaFacebookUrlOrId", "")),
                "linkedin": str(agent.get("SocialMediaLinkedinUrlOrId", "")),
                "other_urls": [
                    str(agent.get("SocialMediaTwitterUrlOrId", "")),
                    str(agent.get("SocialMediaYoutubeUrlOrId", "")),
                    str(agent.get("SocialMediaInstagramUrlOrId", "")),
                    str(agent.get("SocialMediaPinterestUrlOrId", "")),
                    str(agent.get("SocialMediaGoogleplusUrlOrId", "")),
                    str(agent.get("SocialTumblrUrlOrId", ""))
                ]
            }
            social["other_urls"] = [url for url in social["other_urls"] if url]
            profile_url = str(agent.get("BhhsWebsiteUrl", ""))
            description = str(self.get_description_from_profile(profile_url))

            agent_detail = {
                "first_name": first_name,
                "middle_name": middle_name,
                "last_name": last_name,
                "office_name": office_name,
                "title": title,
                "description": description,
                "languages": languages,
                "image_url": image_url,
                "address": address,
                "city": city,
                "state": state,
                "country": country,
                "zipcode": zipcode,
                "office_phone_numbers": office_phone_numbers,
                "agent_phone_numbers": agent_phone_numbers,
                "email": email,
                "website": website,
                "social": social,
                "profile_url": profile_url,
            }
            agent_details.append(agent_detail)

        for agent_detail in agent_details:
            try:
                client = pymongo.MongoClient("mongodb://localhost:27017/")
                db = client["BHHS"]
                collection = db["agent_data"]
                collection.create_index([("profile_url", pymongo.ASCENDING)], unique=True)
                response = collection.insert_one(agent_detail)
                print(response.inserted_id)
            except pymongo.errors.DuplicateKeyError:
                print(f"Duplicate key error: Document with URL {profile_url} already exists.")

if __name__ == "__main__":
    scraper = BhssCrawler()
    scraper.parse_url()
