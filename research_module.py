#!/usr/bin/env python3
"""
Research Module for Aurora AI
-----------------------------
This module performs live research using:
  - Google Custom Search API for search results.
  - OpenAI GPT API for generating concise research topics and summarizing the results.

For testing purposes, the API credentials are provided as defaults.
In production, remove these defaults and load them from secure environment variables.

Default Credentials (testing only):
  GOOGLE_API_KEY: "AIzaSyDkgGTBEARi2p183v1craE4ohVydrJ0vjQ"
  CUSTOM_SEARCH_ENGINE_ID: "67834a4cc93244872"
  OPENAI_API_KEY: "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"
"""

import os
import requests
import logging
import json

# Set up detailed logging.
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("Aurora.Research")

# Load credentials from environment variables or use defaults for testing.
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyDkgGTBEARi2p183v1craE4ohVydrJ0vjQ")
CUSTOM_SEARCH_ENGINE_ID = os.environ.get("CUSTOM_SEARCH_ENGINE_ID", "67834a4cc93244872")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "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")

# Check that credentials are present.
if not GOOGLE_API_KEY:
    logger.error("Google API key not provided.")
if not CUSTOM_SEARCH_ENGINE_ID:
    logger.error("Custom Search Engine ID not provided.")
if not OPENAI_API_KEY:
    logger.error("OpenAI API key not provided.")

def generate_topic(context):
    """
    Generate a concise research topic using the OpenAI GPT API.
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
            {"role": "user", "content": f"Based on this context, generate a short research topic (3-5 words): {context}"}
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
    Search for the given topic using the Google Custom Search API.
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
    Analyze the research text using the OpenAI GPT API to produce a concise summary.
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
    # Define context for topic generation.
    context = "Latest advancements in computational research, artificial intelligence, and science."
    
    topic = generate_topic(context)
    research_result = research(topic)
    analysis = analyze_research(research_result)
    
    # Assemble the output in JSON format.
    output = {
        topic: {
            "research": research_result,
            "analysis": analysis
        }
    }
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
