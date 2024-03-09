import requests

url = "http://localhost:6000"
response = requests.get(url)

print(f"RESPONSE: {response.text}")