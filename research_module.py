#!/usr/bin/env python3
"""
research_module.py – Fully updated research module with real API calls and extended debugging.

This module uses:
  - Google Custom Search JSON API to search for a given topic.
  - OpenAI GPT API (gpt-3.5-turbo) to analyze the research result.
  
Debug logging is enabled to trace all request and response details.
"""

import requests
import logging
import json

# -----------------------------------------------------------------------------
# Logging Configuration
# -----------------------------------------------------------------------------
logger = logging.getLogger("Aurora.Research")
logger.setLevel(logging.DEBUG)
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

# -----------------------------------------------------------------------------
# API Credentials (For demonstration only; do not hard‑code in production!)
# -----------------------------------------------------------------------------
GOOGLE_API_KEY = "AIzaSyDkgGTBEARi2p183v1craE4ohVydrJ0vjQ"  # Replace with your actual Google API key
CUSTOM_SEARCH_ENGINE_ID = "67834a4cc93244872"                # Replace with your actual search engine ID (cx)
OPENAI_API_KEY = "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"  # Replace with your actual OpenAI API key

# -----------------------------------------------------------------------------
# Function: research(topic)
# -----------------------------------------------------------------------------
def research(topic):
    """
    Searches for the given topic using Google Custom Search API.
    Returns a snippet from the first search result.
    """
    logger.debug(f"research() called with topic: {topic}")
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": topic,
        "key": GOOGLE_API_KEY,
        "cx": CUSTOM_SEARCH_ENGINE_ID,
        "num": 1,
    }
    logger.debug(f"Request parameters: {params}")
    try:
        response = requests.get(url, params=params, timeout=10)
        logger.debug(f"Google API Response status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            if items:
                snippet = items[0].get("snippet", "").strip()
                result_text = f"Google result for {topic}: {snippet}" if snippet else f"Google result for {topic}: No snippet available."
            else:
                result_text = f"Google result for {topic}: No results found."
        else:
            result_text = f"Failed to research {topic}: HTTP {response.status_code} - {response.text}"
    except Exception as e:
        result_text = f"Research error for {topic}: {str(e)}"
    logger.info(result_text)
    return result_text

# -----------------------------------------------------------------------------
# Function: analyze_research(research_text)
# -----------------------------------------------------------------------------
def analyze_research(research_text):
    """
    Analyzes the research result using the OpenAI GPT API.
    Returns a concise summary or key terms extracted from the research.
    """
    if not OPENAI_API_KEY:
        return "No valid GPT API key provided."
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
                "content": "You are a concise research assistant. Summarize the following research result in one or two sentences, or provide 3-5 key terms."
            },
            {
                "role": "user",
                "content": f"Summarize this research result:\n\n{research_text}"
            }
        ],
        "temperature": 0.3,
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        logger.debug(f"GPT API Response status code: {response.status_code}")
        if response.status_code == 200:
            result_json = response.json()
            analysis = result_json["choices"][0]["message"]["content"].strip()
            logger.info("GPT analysis completed (concise).")
            return analysis
        else:
            error_info = response.text
            return f"Failed to analyze research with GPT: HTTP {response.status_code} - {error_info}"
    except Exception as e:
        return f"GPT analysis error: {str(e)}"

# -----------------------------------------------------------------------------
# Function: generate_topic(context)
# -----------------------------------------------------------------------------
def generate_topic(context):
    """
    Generates a concise research topic (3-5 words) based on the provided context using the OpenAI GPT API.
    """
    if not OPENAI_API_KEY:
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
                "content": "You are a creative AI that generates concise research topics. Provide a research query of 3-5 words."
            },
            {
                "role": "user",
                "content": f"Generate a research topic based on the following context:\n{context}"
            }
        ],
        "temperature": 0.3,
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            result_json = response.json()
            topic = result_json["choices"][0]["message"]["content"].strip()
            logger.info(f"Generated topic: {topic}")
            return topic
        else:
            logger.error(f"Failed to generate topic: HTTP {response.status_code} - {response.text}")
            return "AI Research"
    except Exception as e:
        logger.error(f"Error generating topic: {str(e)}")
        return "AI Research"

# -----------------------------------------------------------------------------
# Standalone Testing
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    test_context = "Aurora has been learning continuously and storing various research data."
    topic = generate_topic(test_context)
    print("Generated Topic:", topic)
    
    research_result = research(topic)
    print("\nResearch Result:")
    print(research_result)
    
    analysis = analyze_research(research_result)
    print("\nGPT Analysis:")
    print(analysis)
