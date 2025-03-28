#!/usr/bin/env python3
"""
aurora_interactive.py
An interactive command-line interface for Aurora.
This script initializes required modules and then enters an interactive loop
to process user commands and queries.
"""

import sys
import logging
import cognitive_engine
import learning_module
import memory_module
import code_generator
import research_module
import personality_module

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s]: %(message)s')
logger = logging.getLogger()

def print_help():
    help_text = """
Available commands:
  help     - Show this help message.
  status   - Show system status.
  exit     - Exit the interactive session.
  
Any other input will be forwarded to the cognitive engine for processing.
"""
    print(help_text)

def show_status():
    # This is a placeholder. You can add more detailed status information.
    print("System Status:")
    print("  Cognitive Engine loaded:", hasattr(cognitive_engine, "process_query"))
    print("  Learning Module loaded:", hasattr(learning_module, "__name__"))
    print("  Memory Module loaded:", hasattr(memory_module, "__name__"))
    print("  Code Generator loaded:", hasattr(code_generator, "__name__"))
    print("  Research Module loaded:", hasattr(research_module, "__name__"))
    print("  Personality Module loaded:", hasattr(personality_module, "__name__"))
    print("  Current personality: Aurora feels very curious today.")
    
def process_query(query):
    # Forward the query to the cognitive_engine if a function exists,
    # otherwise just echo the input.
    if hasattr(cognitive_engine, 'process_query'):
        try:
            return cognitive_engine.process_query(query)
        except Exception as e:
            return f"Error processing query: {e}"
    else:
        return f"Echo: {query}"

def interactive_loop():
    logger.info("Starting interactive session...")
    
    # Optional initialization for cognitive_engine (if available)
    if hasattr(cognitive_engine, 'initialize'):
        try:
            cognitive_engine.initialize()
            logger.info("Cognitive engine initialized successfully.")
        except Exception as e:
            logger.error(f"Error during cognitive engine initialization: {e}")
    else:
        logger.info("No initialization required for cognitive engine.")

    print("Enter your command or query (type 'help' for options):")
    
    while True:
        try:
            user_input = input("Aurora> ").strip()
            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit']:
                logger.info("Exiting interactive session.")
                break

            # Built-in commands
            if user_input.lower() == "help":
                print_help()
                continue
            elif user_input.lower() == "status":
                show_status()
                continue

            # Otherwise, process as a query:
            response = process_query(user_input)
            print(response)
            
        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt received. Exiting interactive session.")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            break

if __name__ == "__main__":
    logger.info("Aurora Interactive Session Starting...")
    interactive_loop()
