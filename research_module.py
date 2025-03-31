#!/usr/bin/env python3
"""
Research Module (Fully Updated)
--------------------------------
This module performs real API calls using your provided credentials.
It queries Google Custom Search for research data and uses the OpenAI GPT API
to generate concise summaries or key terms.

**WARNING:** Hardcoding API keys is insecure for production use.
"""

import requests
import logging

logger = logging.getLogger("Aurora.Research")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Hardcoded API credentials (for demonstration purposes only)
GOOGLE_API_KEY = "53832af814f74e8afb4e438673f6b962ab979c2b"
CUSTOM_SEARCH_ENGINE_ID = "auorora-1743163807274"
OPENAI_API_KEY = "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"

def research(topic):
    """
    Queries the Google Custom Search API for the specified topic.
    Returns the snippet of the first result or an error message.
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
        response = requests.get(url, params=params, timeout=10)
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
            result_text = f"Failed to research {topic}: HTTP {response.status_code} - {response.text}"
    except Exception as e:
        result_text = f"Research error for {topic}: {e}"
    logger.info(result_text)
    return result_text

def analyze_research(research_text):
    """
    Uses the OpenAI GPT API to produce a brief summary or list key terms
    for the provided research text.
    """
    if not OPENAI_API_KEY:
        msg = "No valid GPT API key provided."
        logger.error(msg)
        return msg

    logger.info("Analyzing research with GPT (concise mode)...")
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
                    "content": "You are a concise research assistant. Provide a brief summary or list 3-5 key terms."
                },
                {
                    "role": "user",
                    "content": f"Summarize the following research result in one or two sentences, or list key terms:\n\n{research_text}"
                }
            ],
            "temperature": 0.3
        }
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            result_json = response.json()
            analysis = result_json["choices"][0]["message"]["content"].strip()
            logger.info("GPT analysis completed (concise).")
            return analysis
        else:
            error_msg = f"Failed to analyze research with GPT: HTTP {response.status_code} - {response.text}"
            logger.error(error_msg)
            return error_msg
    except Exception as e:
        error_msg = f"GPT analysis error: {e}"
        logger.error(error_msg)
        return error_msg

def generate_topic(context):
    """
    Uses the OpenAI GPT API to generate a concise research topic based on the provided context.
    """
    if not OPENAI_API_KEY:
        msg = "AI Research"
        logger.error("No valid GPT API key provided. Defaulting to: " + msg)
        return msg

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
                    "content": "You are a creative AI that generates concise research queries. Provide only 3-5 words."
                },
                {
                    "role": "user",
                    "content": f"Based on this context, generate a short research query (3-5 words):\n\n{context}"
                }
            ],
            "temperature": 0.3
        }
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            result_json = response.json()
            topic = result_json["choices"][0]["message"]["content"].strip()
            logger.info(f"Generated concise topic: {topic}")
            return topic
        else:
            error_msg = f"Failed to generate topic: HTTP {response.status_code} - {response.text}"
            logger.error(error_msg)
            return "AI Research"
    except Exception as e:
        error_msg = f"Error generating topic: {e}"
        logger.error(error_msg)
        return "AI Research"

# For standalone testing
if __name__ == "__main__":
    context = "System memory summary and recent interactions."
    topic = generate_topic(context)
    print("Generated Topic:", topic)
    research_result = research(topic)
    print("Research Result:")
    print(research_result)
    print("\nGPT Analysis:")
    analysis = analyze_research(research_result)
    print(analysis)
