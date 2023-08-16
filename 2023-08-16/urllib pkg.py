# # import urllib
# import urllib.request


# url="https://www.python.org/"
# response=urllib.request.urlopen(url)
# data = response.read()

# print(data)
# print(response)
# print(response.status)
# print(response.headers)



# import urllib.parse


# url="https://www.python.org"
# parsed_url=urllib.parse.urlparse(url)


# print("Scheme:", parsed_url.scheme)
# print("Netloc:", parsed_url.netloc)
# print("Path:", parsed_url.path)
# print("Query:", parsed_url.query)
# print("Fragment:", parsed_url.fragment)


# new_url = urllib.parse.urlunparse(parsed_url)
# print("Reconstructed URL:", new_url)



# import urllib.request
# import urllib.error

# url="https://www.asdcfddyrjuhggjhf"

# try:
#     response = urllib.request.urlopen(url)
# except urllib.error.HTTPError as e:
#     print("HTTP Error:", e.code, e.reason)
# except urllib.error.URLError as e:
#     print("URL Error:", e.reason)