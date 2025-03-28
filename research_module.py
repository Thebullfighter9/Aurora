# research_module.py
import requests
import logging

logger = logging.getLogger("Aurora.Research")

def research(topic):
    logger.info(f"Researching topic: {topic}")
    try:
        response = requests.get("https://api.duckduckgo.com/", params={
            "q": topic,
            "format": "json",
            "no_redirect": 1,
            "no_html": 1
        }, timeout=5)
        if response.status_code == 200:
            data = response.json()
            abstract = data.get("Abstract", "No abstract available.")
            return f"Research result for {topic}: {abstract}"
        else:
            return f"Failed to research {topic}: HTTP {response.status_code}"
    except Exception as e:
        return f"Research error for {topic}: {e}"
