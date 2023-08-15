import requests

# get data 

# r = requests.get("https://www.mytheresa.com/int/en/men/shoes")
# print(r)

# -----------



# download data 

# r = requests.get("https://img.mytheresa.com/1094/1236/90/jpeg/catalog/product/bf/P00856471.jpg")
# with open("shoe.jpg",'wb') as f:
#     f.write(r.content)

# print (r.status_code)
# print (r.headers)

# -----------------------------

# payload = {'page':2,'count':25}
# r = requests.post('http://httpbin.org/get', params=payload)

# # print(r.text)
# print(r.url)

# ----------------------------

# post data 

# payload = {'username':'sss','password':'testing'}
# r = requests.post('http://httpbin.org/post', data=payload)

# print(r.text)
# print(r.url)


# -------------------------

# patch

# payload = {"title": "new title"}
# r = requests.patch('https://jsonplaceholder.typicode.com/posts/1', data=payload)
# print(r.text)

# -----------------
# put


# payload = {"userId": 1,"id": 1,"title": "new title", "body": "new body"}
# r = requests.put('https://jsonplaceholder.typicode.com/posts/1', data=payload)
# print(r.text)

# ------------

# json


# payload = {'username':'sss','password':'testing'}
# r = requests.post('http://httpbin.org/post', data=payload)

# r_dict = r.json()
# print(r_dict['form'])

# ------------------------------------

# parsel

# import requests
# from parsel import Selector

# url = "https://www.mytheresa.com/int/en/men/shoes"
# response = requests.get(url)
# # print(response.text)
# selector = Selector(text=response.text)

# title = selector.css("title::text").get()

# print("Title:", title)

import json
url="https://support.oneskyapp.com/hc/en-us/articles/208047697-JSON-sample-files"
a=json.load(url)
print(a)






