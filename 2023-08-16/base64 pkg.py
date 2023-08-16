import base64


data=b'https://www.python.org/'


encoded=base64.b64encode(data)
print(encoded)


decoded = base64.b64decode(encoded)
print(decoded)