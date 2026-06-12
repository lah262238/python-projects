import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")
print(f"API Key loaded: {api_key[:10]}...")

response = requests.post(
    "https://api.tavily.com/search",
    json={
        "api_key": api_key,
        "query": "current date today 2026",
        "max_results": 3
    }
)

data = response.json()
print("\nTavily Response:")
print(data)