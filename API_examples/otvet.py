import requests

dost = requests.get("http://6231f063.ngrok.io/api/vse_zadach").json()
print(dost)

