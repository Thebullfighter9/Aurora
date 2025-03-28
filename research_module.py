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
                    result_text = f"Google research result for {topic}: {snippet}"
                else:
                    result_text = f"Google research result for {topic}: No snippet available."
            else:
                result_text = f"Google research result for {topic}: No results found."
        else:
            result_text = f"Failed to research {topic}: HTTP {response.status_code}"
    except Exception as e:
        result_text = f"Research error for {topic}: {e}"
    logger.info(result_text)
    return result_text

def analyze_research(research_text):
    """
    Uses the OpenAI GPT API to analyze the research text and generate an analysis.
    """
    if not OPENAI_API_KEY:
        return "No valid GPT API key provided."
    
    logger.info("Analyzing research with GPT...")
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}",
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a highly analytical AI that synthesizes and reflects on research."},
                {"role": "user", "content": f"Please analyze and summarize the following research result:\n\n{research_text}"}
            ],
            "temperature": 0.7,
        }
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            result_json = response.json()
            analysis = result_json["choices"][0]["message"]["content"].strip()
            logger.info("GPT analysis completed.")
            return analysis
        else:
            return f"Failed to analyze research with GPT: HTTP {response.status_code}"
    except Exception as e:
        return f"GPT analysis error: {e}"

def generate_topic(context):
    """
    Uses the OpenAI GPT API to generate a unique research topic based on provided context.
    """
    if not OPENAI_API_KEY:
        return "Artificial Intelligence"  # Fallback topic
    logger.info("Generating research topic with GPT...")
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}",
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a creative AI generating diverse research topics. Think broadly and generate a unique, interesting research topic based on the context provided."},
                {"role": "user", "content": f"Based on the following context, generate one unique research topic that an autonomous AI should explore:\n\n{context}"}
            ],
            "temperature": 0.9,
        }
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            result_json = response.json()
            topic = result_json["choices"][0]["message"]["content"].strip()
            logger.info(f"Generated topic: {topic}")
            return topic
        else:
            logger.error(f"Failed to generate topic: HTTP {response.status_code}")
            return "Artificial Intelligence"  # Fallback
    except Exception as e:
        logger.error(f"Error generating topic: {e}")
        return "Artificial Intelligence"  # Fallback

# For standalone testing
if __name__ == "__main__":
    context = "Memory summary: Example memory content summarizing Aurora's experiences."
    generated_topic = generate_topic(context)
    print("Generated Topic:", generated_topic)
    research_result = research(generated_topic)
    print("Research Result:")
    print(research_result)
    print("\nGPT Analysis:")
    analysis = analyze_research(research_result)
    print(analysis)
