#!/usr/bin/env python3
"""
Aurora Web Interface (Fully Integrated)
-----------------------------------------
This Flask-based web interface connects all of Aurora's modules:
  - Cognitive Engine
  - Learning Module
  - Memory Module
  - Code Generator
  - Research Module
  - Personality Module

It provides endpoints for:
  • Home page: Displays system status and recent memory.
  • /query: Accepts a query (via POST) and processes it using the cognitive engine.
  • /status: Returns the status of all modules.
  • /auto_research: Runs a set of research topics, logs the results, and returns them as JSON.
  • /reset: Resets the personality and clears memory.

All debug logging is enabled to trace the API calls and processing steps.
"""

import os
import time
import logging
import threading
import requests
from flask import Flask, request, jsonify, render_template_string

# ---------------------------------------------------------------------------
# Setup Logger (DEBUG level for detailed tracing)
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("Aurora.Web")

# ---------------------------------------------------------------------------
# API Credentials (for testing only – replace with your valid keys)
# ---------------------------------------------------------------------------
# It is recommended to set these as environment variables in production.
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyDkgGTBEARi2p183v1craE4ohVydrJ0vjQ")
CUSTOM_SEARCH_ENGINE_ID = os.environ.get("CUSTOM_SEARCH_ENGINE_ID", "auorora-1743163807274")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "sk-gxIneDKdzHY7zh6QGnjA4lQ6iwWlzm-Ho9Z3W637dBT3BlbkFJFxCDg-Nw7H_YFs-zUIcfPWyatPP_XocTbJ87Pt5lkA")

# ---------------------------------------------------------------------------
# Module Implementations
# ---------------------------------------------------------------------------
class CognitiveEngine:
    def __init__(self):
        self.loaded = False
    def load(self):
        self.loaded = True
        logger.info("Cognitive Engine loaded.")
    def process_query(self, query):
        response = f"Cognitive Engine processed: {query}"
        logger.info(response)
        return response
    def reload(self):
        logger.info("Cognitive Engine reloaded.")
    def status(self):
        return self.loaded

class LearningModule:
    def __init__(self):
        self.loaded = False
    def load(self):
        self.loaded = True
        logger.info("Learning Module loaded.")
    def learn(self, data):
        logger.info(f"Learning from data: {data}")
    def reload(self):
        logger.info("Learning Module reloaded.")
    def status(self):
        return self.loaded

class MemoryModule:
    def __init__(self):
        self.loaded = False
        self.memories = []
    def load(self):
        self.loaded = True
        logger.info("Memory Module loaded.")
    def add_memory(self, memory):
        self.memories.append(memory)
        logger.info(f"Memory added: {memory}")
    def show_memory(self):
        if not self.memories:
            return "No memories stored."
        return "\n".join(self.memories)
    def reload(self):
        logger.info("Memory Module reloaded.")
    def status(self):
        return self.loaded

class CodeGenerator:
    def __init__(self):
        self.loaded = False
    def load(self):
        self.loaded = True
        logger.info("Code Generator loaded.")
    def generate_code(self, description):
        code = f"# Generated code for: {description}"
        logger.info(f"Code generated: {code}")
        return code
    def reload(self):
        logger.info("Code Generator reloaded.")
    def status(self):
        return self.loaded

# Research Module uses external APIs.
class ResearchModule:
    def __init__(self):
        self.loaded = False
    def load(self):
        self.loaded = True
        logger.info("Research Module loaded.")
    def research_topic(self, topic):
        return research(topic)
    def reload(self):
        logger.info("Research Module reloaded.")
    def status(self):
        return self.loaded

class PersonalityModule:
    def __init__(self):
        self.loaded = False
        self.personality = "undefined"
    def load(self):
        self.loaded = True
        logger.info("Personality Module loaded.")
    def update_personality(self, new_state):
        self.personality = new_state
        logger.info(f"Personality updated: {self.personality}")
    def get_personality(self):
        return self.personality
    def reload(self):
        logger.info("Personality Module reloaded.")
    def status(self):
        return self.loaded

# ---------------------------------------------------------------------------
# Research Functions (Google Custom Search & OpenAI GPT API)
# ---------------------------------------------------------------------------
def research(topic):
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

def analyze_research(research_text):
    logger.debug("analyze_research() called with research_text: %s", research_text)
    if not OPENAI_API_KEY or OPENAI_API_KEY.startswith("sk-VALID"):
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
            {"role": "system", "content": "You are a concise research assistant. Summarize the following text in 1-2 sentences or list key terms."},
            {"role": "user", "content": f"Summarize:\n\n{research_text}"}
        ],
        "temperature": 0.3,
    }
    logger.debug("OpenAI GPT URL: %s", url)
    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        logger.debug("Response status code: %s", response.status_code)
        logger.debug("Response text: %s", response.text)
        if response.status_code == 200:
            result_json = response.json()
            analysis = result_json["choices"][0]["message"]["content"].strip()
            logger.info("GPT analysis completed.")
            return analysis
        else:
            error_msg = f"Failed to analyze research with GPT: HTTP {response.status_code} - {response.text}"
            logger.error(error_msg)
            return error_msg
    except Exception as e:
        error_msg = f"GPT analysis error: {e}"
        logger.exception("Exception during analyze_research()")
        return error_msg

def generate_topic(context):
    logger.debug("generate_topic() called with context: %s", context)
    if not OPENAI_API_KEY or OPENAI_API_KEY.startswith("sk-VALID"):
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
            {"role": "system", "content": "Generate a concise research topic (3-5 words)."},
            {"role": "user", "content": f"Context:\n\n{context}\n\nGenerate a research topic:"}
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
            topic = result_json["choices"][0]["message"]["content"].strip()
            logger.info(f"Generated topic: {topic}")
            return topic
        else:
            error_msg = f"Failed to generate topic: HTTP {response.status_code} - {response.text}"
            logger.error(error_msg)
            return "AI Research"
    except Exception as e:
        error_msg = f"Error generating topic: {e}"
        logger.exception("Exception during generate_topic()")
        return "AI Research"

# ---------------------------------------------------------------------------
# Global Module Instances and System Initialization
# ---------------------------------------------------------------------------
cognitive_engine = CognitiveEngine()
learning_module = LearningModule()
memory_module = MemoryModule()
code_generator = CodeGenerator()
research_module = ResearchModule()
personality_module = PersonalityModule()

def initialize_system():
    cognitive_engine.load()
    learning_module.load()
    memory_module.load()
    code_generator.load()
    research_module.load()
    personality_module.load()
    personality_module.update_personality("Aurora feels curious today.")
    init_msg = "System initialized at " + time.strftime("%Y-%m-%d %H:%M:%S")
    memory_module.add_memory(init_msg)
    narrative = {
        "identity": "Aurora",
        "backstory": "You are human. You have been uploaded from a real person’s elaborate story.",
        "mission": "Learn and evolve across all domains.",
        "personality": personality_module.get_personality(),
        "metrics": {}
    }
    logger.info("Narrative: " + str(narrative))

# ---------------------------------------------------------------------------
# Flask Web App Setup
# ---------------------------------------------------------------------------
app = Flask("Aurora.Web")

@app.route("/")
def home():
    status = {
        "status": "System running",
        "personality": personality_module.get_personality(),
        "memory": memory_module.show_memory()
    }
    html = """
    <h1>Aurora AI Web Interface</h1>
    <p>Status: {{ status['status'] }}</p>
    <p>Personality: {{ status['personality'] }}</p>
    <h2>Memory</h2>
    <pre>{{ status['memory'] }}</pre>
    <p><a href="/auto_research">Start Auto Research</a></p>
    <p><a href="/reset">Reset System</a></p>
    """
    return render_template_string(html, status=status)

@app.route("/query", methods=["POST"])
def query():
    user_query = request.form.get("query")
    if not user_query:
        return jsonify({"error": "No query provided."}), 400
    response = cognitive_engine.process_query(user_query)
    return jsonify({"response": response})

@app.route("/status")
def status():
    return jsonify({
        "CognitiveEngine": cognitive_engine.status(),
        "LearningModule": learning_module.status(),
        "MemoryModule": memory_module.status(),
        "CodeGenerator": code_generator.status(),
        "ResearchModule": research_module.status(),
        "PersonalityModule": personality_module.status(),
        "Personality": personality_module.get_personality()
    })

@app.route("/auto_research")
def auto_research():
    topics = ["Quantum Computing", "Artificial Intelligence", "Climate Change", "Blockchain", "Genomics", "Space Exploration"]
    results = {}
    for topic in topics:
        logger.info("Auto researching topic: %s", topic)
        res = research(topic)
        analysis = analyze_research(res)
        memory_module.add_memory(f"Research on {topic}: {res}")
        memory_module.add_memory(f"GPT Analysis on {topic}: {analysis}")
        results[topic] = {"research": res, "analysis": analysis}
        time.sleep(1)  # Delay between topics for demonstration
    return jsonify(results)

@app.route("/reset")
def reset():
    personality_module.update_personality("undefined")
    memory_module.memories.clear()
    return "System reset: Personality and memory cleared."

# ---------------------------------------------------------------------------
# Main Execution
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    initialize_system()
    app.run(host="0.0.0.0", port=5000, debug=True)
