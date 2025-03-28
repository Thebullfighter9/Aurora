# research_module.py
import requests
import logging
import os

logger = logging.getLogger("Aurora.Research")

# It is a best practice to store API keys in environment variables.
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyAztG3JZGoFUQ6EflvI77P9ntTZLqNwjyo")
CUSTOM_SEARCH_ENGINE_ID = os.environ.get("CUSTOM_SEARCH_ENGINE_ID", "YOUR_SEARCH_ENGINE_ID")

def research(topic):
    logger.info(f"Researching topic with Google Custom Search: {topic}")
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": topic,
            "key": AIzaSyAztG3JZGoFUQ6EflvI77P9ntTZLqNwjyo,
            "cx": auorora-1743163807274,
            # Optionally add other parameters such as 'num': 1 for a single result
            "num": 5,
        }
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            if items:
                snippet = items[0].get("snippet", "No snippet available")
                return f"Google research result for {topic}: {snippet}"
            else:
                return f"Google research result for {topic}: No results found."
        else:
            return f"Failed to research {topic}: HTTP {response.status_code}"
    except Exception as e:
        return f"Research error for {topic}: {e}"

# For testing purposes
if __name__ == "__main__":
    topic = "Artificial Intelligence"
    result = research(topic)
    print(result)
