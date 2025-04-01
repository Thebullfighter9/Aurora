#!/usr/bin/env python3
"""
Research Module for Aurora AI
-----------------------------
This module performs the following tasks:
  1. Generates a concise research topic using the OpenAI GPT API.
  2. Uses the Google Custom Search API to search for that topic.
  3. Analyzes the research result using the OpenAI GPT API.

Before running, set the following environment variables:
  - GOOGLE_API_KEY: Your Google API key.
  - CUSTOM_SEARCH_ENGINE_ID: Your Custom Search Engine ID.
  - OPENAI_API_KEY: Your OpenAI API key.

Example usage:
    export GOOGLE_API_KEY="your_google_api_key_here"
    export CUSTOM_SEARCH_ENGINE_ID="your_custom_search_engine_id_here"
    export OPENAI_API_KEY="sk-your_valid_openai_key_here"
    python3 research_module.py
"""

import os
import requests
import logging

# Set up logging for full debug information.
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("Aurora.Research")

# Retrieve API keys from environment variables.
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
CUSTOM_SEARCH_ENGINE_ID = os.environ.get("CUSTOM_SEARCH_ENGINE_ID")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Verify that all required credentials are provided.
if not GOOGLE_API_KEY:
    logger.error("Google API key not provided in environment variable GOOGLE_API_KEY.")
if not CUSTOM_SEARCH_ENGINE_ID:
    logger.error("Custom Search Engine ID not provided in environment variable CUSTOM_SEARCH_ENGINE_ID.")
if not OPENAI_API_KEY:
    logger.error("OpenAI API key not provided in environment variable OPENAI_API_KEY.")


def generate_topic(context):
    """
    Generate a concise research topic using OpenAI GPT.
    """
    if not OPENAI_API_KEY:
        logger.error("No valid OpenAI API key provided for topic generation.")
        return "AI Research"
    
    logger.info("Generating concise research topic with GPT...")
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a creative AI that generates concise research topics."},
            {"role": "user", "content": f"Based on the following context, generate a short research topic (3-5 words): {context}"}
        ],
        "temperature": 0.3
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        logger.debug(f"GPT API Response status code: {response.status_code}")
        if response.status_code == 200:
            result_json = response.json()
            topic = result_json["choices"][0]["message"]["content"].strip()
            logger.info(f"Generated Topic: {topic}")
            return topic
        else:
            error_message = f"Failed to generate topic: HTTP {response.status_code} - {response.text}"
            logger.error(error_message)
            return "AI Research"
    except Exception as e:
        logger.error(f"Exception during topic generation: {e}")
        return "AI Research"


def research(topic):
    """
    Uses the Google Custom Search API to perform a search for the topic.
    """
    if not GOOGLE_API_KEY or not CUSTOM_SEARCH_ENGINE_ID:
        error_message = "Error: Missing Google API credentials."
        logger.error(error_message)
        return error_message
    
    logger.info(f"Researching topic with Google Custom Search: {topic}")
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": topic,
        "key": GOOGLE_API_KEY,
        "cx": CUSTOM_SEARCH_ENGINE_ID,
        "num": 1,
    }
    logger.debug(f"Request parameters: {params}")
    
    try:
        response = requests.get(url, params=params, timeout=5)
        logger.debug(f"Google API Response status code: {response.status_code}")
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
    Uses the OpenAI GPT API to analyze research text.
    """
    if not OPENAI_API_KEY:
        logger.error("No valid OpenAI API key provided for research analysis.")
        return "No valid GPT API key provided."
    
    logger.info("Analyzing research with GPT (concise mode)...")
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a concise research assistant. Provide a brief summary or list key terms."},
            {"role": "user", "content": f"Summarize the following research result in 1-2 sentences or list 3-5 key terms:\n\n{research_text}"}
        ],
        "temperature": 0.3
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
            error_message = f"Failed to analyze research with GPT: HTTP {response.status_code} - {response.text}"
            logger.error(error_message)
            return error_message
    except Exception as e:
        logger.error(f"GPT analysis error: {e}")
        return f"GPT analysis error: {e}"


def main():
    # Example context for topic generation.
    context = "Latest advancements in computational research and AI."
    topic = generate_topic(context)
    research_result = research(topic)
    analysis = analyze_research(research_result)
    
    print("Generated Topic:", topic)
    print("\nResearch Result:\n", research_result)
    print("\nGPT Analysis:\n", analysis)


if __name__ == "__main__":
    main()
