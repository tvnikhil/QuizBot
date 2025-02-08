import requests

BASE_URL = "http://34.174.9.236:11434/v1"

response = requests.get(f"{BASE_URL}/models")
print(response.status_code, response.json())