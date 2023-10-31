import requests
import time

MONGO_URL= "mongodb://localhost:27017/"
MONGODB="AQAR_sa"
URL="aqar_urls"
DATA="aqar_data"

session = requests.Session()
headers = {
            "user-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
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

def make_request(url, max_retries=5, retry_delay=3):
        for _ in range(max_retries):
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                if response.status_code == 200:
                    return response
            except requests.exceptions.RequestException as e:
                print(f"Failed to make a request: {str(e)}")
            print(f"Retrying request to {url}...")
            time.sleep(retry_delay)
        return None