import os
from dotenv import load_dotenv
import serpapi

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def search_google_scholar(query, num_results=10):
    params = {
        "engine": "google_scholar",
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": num_results
    }

    results = serpapi.search(params)

    return results