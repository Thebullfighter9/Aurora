#!/usr/bin/env python3
"""
Research Module
---------------
This module performs research by calling the Google Custom Search API and
analyzes the results using the OpenAI GPT API.

It no longer uses dummy responses; it makes live API calls (if provided with
valid credentials).

Before running this module, set these environment variables:
  - GOOGLE_API_KEY: Your Google API key for Custom Search
  - CUSTOM_SEARCH_ENGINE_ID: Your Custom Search Engine ID
  - OPENAI_API_KEY: Your OpenAI API key
"""

import os
import requests
import logging
import json

# Set up logging
logger = logging.getLogger("Aurora.Research")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Retrieve API keys from environment variables
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
CUSTOM_SEARCH_ENGINE_ID = os.environ.get("CUSTOM_SEARCH_ENGINE_ID")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def research(topic):
    """
    Uses the Google Custom Search API to search for the given topic
    and returns a snippet from the first result.
    """
    logger.info(f"Researching topic with Google Custom Search: {topic}")
    if not GOOGLE_API_KEY or not CUSTOM_SEARCH_ENGINE_ID:
        error_msg = "Error: Missing Google API credentials."
        logger.error(error_msg)
        return error_msg

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": topic,
        "key": GOOGLE_API_KEY,
        "cx": CUSTOM_SEARCH_ENGINE_ID,
        "num": 1,
    }
    try:
        response = requests.get(url, params=params, timeout=5)
    except Exception as e:
        error_msg = f"Research error for {topic}: {e}"
        logger.error(error_msg)
        return error_msg

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
    logger.info(result_text)
    return result_text

def analyze_research(research_text):
    """
    Uses the OpenAI GPT API to produce a brief summary or key terms from the research text.
    """
    if not OPENAI_API_KEY:
        error_msg = "No valid GPT API key provided."
        logger.error(error_msg)
        return error_msg

    logger.info("Analyzing research with GPT (concise mode)...")
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
                "content": "You are a concise research assistant. Provide a brief summary (1-2 sentences) or list 3-5 key terms for the given research result."
            },
            {
                "role": "user",
                "content": f"Summarize or extract key terms from the following research result:\n\n{research_text}"
            }
        ],
        "temperature": 0.3,
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
    except Exception as e:
        error_msg = f"GPT analysis error: {e}"
        logger.error(error_msg)
        return error_msg

    if response.status_code == 200:
        result_json = response.json()
        analysis = result_json["choices"][0]["message"]["content"].strip()
        logger.info("GPT analysis completed (concise).")
        return analysis
    else:
        error_msg = f"Failed to analyze research with GPT: HTTP {response.status_code} - {response.text}"
        logger.error(error_msg)
        return error_msg

def generate_topic(context):
    """
    Uses the OpenAI GPT API to generate a concise research topic based on the provided context.
    """
    if not OPENAI_API_KEY:
        logger.error("No valid GPT API key provided. Returning default topic 'AI Research'.")
        return "AI Research"

    logger.info("Generating concise research topic with GPT...")
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
                "content": "You are a creative AI that generates concise research topics. Provide a topic in 3-5 words."
            },
            {
                "role": "user",
                "content": f"Based on the following context, generate a short research topic (3-5 words):\n\n{context}"
            }
        ],
        "temperature": 0.3,
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
    except Exception as e:
        logger.error(f"Error generating topic: {e}")
        return "AI Research"

    if response.status_code == 200:
        result_json = response.json()
        topic = result_json["choices"][0]["message"]["content"].strip()
        logger.info(f"Generated concise topic: {topic}")
        return topic
    else:
        logger.error(f"Failed to generate topic: HTTP {response.status_code} - {response.text}")
        return "AI Research"


# For standalone testing
if __name__ == "__main__":
    # Example context for generating a topic.
    context = "Recent breakthroughs in machine learning and neural networks."
    topic = generate_topic(context)
    print("Generated Topic:", topic)
    research_result = research(topic)
    print("Research Result:")
    print(research_result)
    print("\nGPT Analysis:")
    analysis = analyze_research(research_result)
    print(analysis)
