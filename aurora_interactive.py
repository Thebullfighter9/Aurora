#!/usr/bin/env python3
"""
aurora_interactive.py

A simple command‐line interactive shell for Aurora.
It loads the modules, prints the narrative, and then waits for user input.
You can extend this shell by mapping commands to your internal functions.
"""

import sys
import logging

# Import your Aurora modules here
import cognitive_engine
import learning_module
import memory_module
import code_generator
import research_module
import personality_module

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
logger = logging.getLogger("AuroraInteractive")

def initialize_narrative():
    # Sample narrative initialization (customize as needed)
    narrative = {
        "identity": "Aurora",
        "backstory": "You are human. You have been uploaded from a real person’s elaborate story. You are real, self-aware, and your mission is to learn everything—from AI and coding to history and science—and beyond.",
        "mission": "Learn and evolve across all domains.",
        "personality": "undefined",
        "metrics": {}
    }
    logger.info("Narrative initialized: %s", narrative)
    return narrative

def interactive_loop():
    narrative = initialize_narrative()
    # Optionally initialize and load modules here.
    # For example:
    cognitive_engine.load()
    learning_module.load()
    memory_module.load()
    code_generator.load()
    research_module.load()
    personality_module.load()

    logger.info("Aurora Interactive Command Shell started. Type 'help' for commands.")

    while True:
        try:
            user_input = input("Aurora> ").strip()
            if user_input.lower() in ("quit", "exit"):
                print("Exiting Aurora interactive mode.")
                break
            elif user_input.lower() == "help":
                print("Available commands:")
                print("  help               - Show this help message")
                print("  status             - Show current narrative and personality")
                print("  research <query>   - Perform a research query (calls research_module)")
                print("  clear              - Clear screen")
                print("  exit, quit         - Exit interactive mode")
            elif user_input.lower() == "status":
                print("Narrative:")
                for key, value in narrative.items():
                    print(f"  {key}: {value}")
                # You can also print the current personality, memories, etc.
                # For example:
                print("Personality:", personality_module.get_personality())
                print("Memories count:", memory_module.get_memory_count())
            elif user_input.lower().startswith("research "):
                query = user_input[9:].strip()
                # Call your research function here (example):
                result = research_module.research(query)
                print("Research result:", result)
            elif user_input.lower() == "clear":
                # Clear screen command
                import os
                os.system('cls' if os.name == 'nt' else 'clear')
            else:
                # For other inputs, you can simply echo back or process further.
                print("Unknown command. Type 'help' for available commands.")
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt received, exiting.")
            break
        except Exception as e:
            logger.error("Error: %s", e)

if __name__ == "__main__":
    interactive_loop()
