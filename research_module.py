#!/usr/bin/env python3


import os
import requests
import logging

# Set up logger with DEBUG level to show detailed information.
logger = logging.getLogger("Aurora.Research")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s", "%Y-%m-%d %H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)

# ----------------------------------------------------------------------------------
# API Keys (Hard–coded for testing; do not use in production)
# ----------------------------------------------------------------------------------
GOOGLE_API_KEY = "AIzaSyDkgGTBEARi2p183v1craE4ohVydrJ0vjQ"  # Must start with 'AIza...'
CUSTOM_SEARCH_ENGINE_ID = "auorora-1743163807274"            # Your custom search engine ID
OPENAI_API_KEY = "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""               # Replace with your valid OpenAI API key

# ----------------------------------------------------------------------------------
# Research using Google Custom Search API.
# ----------------------------------------------------------------------------------
def research(topic):
    """
    Uses the Google Custom Search API to search for the topic and returns a snippet from the first result.
    """
    logger.debug("research() called with topic: %s", topic)
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
    logger.debug("Google Custom Search URL: %s", url)
    logger.debug("Request parameters: %s", params)
    try:
        response = requests.get(url, params=params, timeout=10)
        logger.debug("Response status code: %s", response.status_code)
        logger.debug("Response text: %s", response.text)
        if response.status_code == 200:
            data = response.json()
            logger.debug("Parsed JSON data: %s", data)
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
        logger.exception("Exception occurred during research()")
    logger.info(result_text)
    return result_text

# ----------------------------------------------------------------------------------
# Analyze research result using OpenAI GPT API.
# ----------------------------------------------------------------------------------
def analyze_research(research_text):
    """
    Uses the OpenAI GPT API to produce a concise analysis of the research text.
    """
    logger.debug("analyze_research() called with research_text: %s", research_text)
    if not OPENAI_API_KEY:
        error_msg = "Error: No valid OpenAI API key provided."
        logger.error(error_msg)
        return error_msg

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
                "content": f"Summarize the following research result in 1-2 sentences or list 3-5 key terms:\n\n{research_text}"
            }
        ],
        "temperature": 0.3,
    }
    logger.debug("OpenAI GPT URL: %s", url)
    logger.debug("Request headers: %s", headers)
    logger.debug("Request data: %s", data)
    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        logger.debug("Response status code: %s", response.status_code)
        logger.debug("Response text: %s", response.text)
        if response.status_code == 200:
            result_json = response.json()
            logger.debug("Parsed JSON data: %s", result_json)
            analysis = result_json["choices"][0]["message"]["content"].strip()
            logger.info("GPT analysis completed (concise).")
            return analysis
        else:
            error_msg = f"Failed to analyze research with GPT: HTTP {response.status_code} - {response.text}"
            logger.error(error_msg)
            return error_msg
    except Exception as e:
        error_msg = f"GPT analysis error: {e}"
        logger.exception("Exception occurred during analyze_research()")
        return error_msg

# ----------------------------------------------------------------------------------
# Generate a concise research topic using OpenAI GPT API.
# ----------------------------------------------------------------------------------
def generate_topic(context):
    """
    Uses the OpenAI GPT API to generate a concise research topic based on the provided context.
    """
    logger.debug("generate_topic() called with context: %s", context)
    if not OPENAI_API_KEY:
        logger.error("No valid OpenAI API key provided.")
        return "AI Research"
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
                "content": f"Based on this context, generate a short research query (3-5 words):\n\n{context}"
            }
        ],
        "temperature": 0.3,
    }
    logger.debug("Requesting topic generation with OpenAI GPT.")
    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        logger.debug("Response status code: %s", response.status_code)
        logger.debug("Response text: %s", response.text)
        if response.status_code == 200:
            result_json = response.json()
            logger.debug("Parsed JSON data: %s", result_json)
            topic = result_json["choices"][0]["message"]["content"].strip()
            logger.info(f"Generated concise topic: {topic}")
            return topic
        else:
            error_msg = f"Failed to generate topic: HTTP {response.status_code} - {response.text}"
            logger.error(error_msg)
            return "AI Research"
    except Exception as e:
        error_msg = f"Error generating topic: {e}"
        logger.exception("Exception occurred during generate_topic()")
        return "AI Research"

# ----------------------------------------------------------------------------------
# Standalone testing
# ----------------------------------------------------------------------------------
if __name__ == "__main__":
    # Example context for topic generation (could be derived from system memory or current state)
    context = "Current memory summary: System initialized and learning modules active."
    topic = generate_topic(context)
    print("Generated Topic:", topic)
    research_result = research(topic)
    print("Research Result:")
    print(research_result)
    print("\nGPT Analysis:")
    analysis = analyze_research(research_result)
    print(analysis)
