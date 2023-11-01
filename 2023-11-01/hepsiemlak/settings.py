import requests
import time
import random
# import pymongo


MONGO_URL= "mongodb://localhost:27017/"
MONGODB="hepsiemlak"
URL="hepsi_urls"
DATA="hepsi_data"


proxies = [
    #  'http://5.188.168.19:8443',
    'http://95.0.206.222:8080',
    # 'http://212.154.82.52:9090',
    'http://85.99.109.165:8080',
    
]

# headers = {
#     "authority": "www.hepsiemlak.com",
#     "method": "GET",
#     "path": "/api/realty-list/antalya-satilik?page=1&fillIntentUrls=true",
#     "scheme": "https",
#     "Accept": "application.json, text/plain, */*",
#     "Accept-Encoding": "gzip,deflate,br",
#     "Accept-Language": "tr",
#     "Desktop2019": "1",
#     "Referer": "https://www.hepsiemlak.com/",
#     "Sec-Ch-Ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
#     "Sec-Ch-Ua-Mobile": "?0",
#     "Sec-Ch-Ua-Platform": '"Linux"',
#     "Sec-Fetch-Dest": "empty",
#     "Sec-Fetch-Mode": "cors",
#     "Sec-Fetch-Site": "same-origin",
#     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
# }
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate,",
    "accept-language": "en-GB,en;q=0.9",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
}

def make_request(url, max_retries=10, retry_delay=3):

        for _ in range(max_retries):
            print("1")
            try:
                proxy = random.choice(proxies)
                response = requests.get(url, headers=headers, proxies={'http': proxy, 'https': proxy})
                print(url)
                response.raise_for_status()
                if response.status_code == 200:
                    print(response)
                    return response
            except requests.exceptions.RequestException as e:
                print(f"Failed to make a request: {str(e)}")
            print(f"Retrying request to {url} with a different proxy...")
            time.sleep(retry_delay)
        return None
