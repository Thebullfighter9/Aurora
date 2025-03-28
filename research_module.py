# research_module.py
import os
import requests
import logging

logger = logging.getLogger("Aurora.Research")

# Retrieve API keys from environment variables
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
CUSTOM_SEARCH_ENGINE_ID = os.environ.get("CUSTOM_SEARCH_ENGINE_ID")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def research(topic):
    """
    Uses Google Custom Search API to search for the topic and returns a snippet from the first result.
    """
    logger.info(f"Researching topic with Google Custom Search: {topic}")
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": topic,
            "key": GOOGLE_API_KEY,
            "cx": CUSTOM_SEARCH_ENGINE_ID,
            "num": 1,
        }
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            if items:
                snippet = items[0].get("snippet", "").strip()
                if snippet:
                    result_text = f"Google result for {topic}: {snippet}"
                else:
                    result_text = f"Google result for {topic}: No snippet available."
            else:
                result_text = f"Google result for {topic}: No results found."
        else:
            result_text = f"Failed to research {topic}: HTTP {response.status_code}"
    except Exception as e:
        result_text = f"Research error for {topic}: {e}"
    logger.info(result_text)
    return result_text

def analyze_research(research_text):
    """
    Uses the OpenAI GPT API to produce a brief, concise summary of the research text.
    """
    if not OPENAI_API_KEY:
        return "No valid GPT API key provided."
    
    logger.info("Analyzing research with GPT (concise mode)...")
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}",
        }
        # Adjust prompt to request a short summary in 1-2 sentences or key terms.
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a concise research assistant. Provide only a brief summary or key terms."
                },
                {
                    "role": "user",
                    "content": f"Summarize the following research result in one or two sentences, or list 3-5 key terms:\n\n{research_text}"
                }
            ],
            "temperature": 0.3,  # lower temperature for more deterministic output
        }
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            result_json = response.json()
            analysis = result_json["choices"][0]["message"]["content"].strip()
            logger.info("GPT analysis completed (concise).")
            return analysis
        else:
            return f"Failed to analyze research with GPT: HTTP {response.status_code}"
    except Exception as e:
        return f"GPT analysis error: {e}"

def generate_topic(context):
    """
    Uses the OpenAI GPT API to generate a concise research topic based on provided context.
    The prompt instructs GPT to output a short query (3-5 words).
    """
    if not OPENAI_API_KEY:
        return "AI Research"
    logger.info("Generating concise research topic with GPT...")
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}",
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a creative AI that generates concise research queries. Provide only 3-5 words as a research query."
                },
                {
                    "role": "user",
                    "content": f"Based on this context, generate a short research query (3-5 words) that an autonomous AI might use:\n\n{context}"
                }
            ],
            "temperature": 0.3,  # deterministic output
        }
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            result_json = response.json()
            topic = result_json["choices"][0]["message"]["content"].strip()
            logger.info(f"Generated concise topic: {topic}")
            return topic
        else:
            logger.error(f"Failed to generate topic: HTTP {response.status_code}")
            return "AI Research"
    except Exception as e:
        logger.error(f"Error generating topic: {e}")
        return "AI Research"

# For standalone testing
if __name__ == "__main__":
    context = "Memory summary: Example summary from Aurora's current memory."
    generated_topic = generate_topic(context)
    print("Generated Topic:", generated_topic)
    research_result = research(generated_topic)
    print("Research Result:")
    print(research_result)
    print("\nGPT Analysis:")
    analysis = analyze_research(research_result)
    print(analysis)
