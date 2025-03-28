#!/usr/bin/env python3
"""
aurora_interactive.py
An interactive command-line interface for Aurora.
This script initializes required modules and then enters an interactive loop to process user queries.
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

    logger.info("Enter your query (type 'exit' or 'quit' to end):")
    while True:
        try:
            user_input = input("Aurora> ")
            if user_input.strip().lower() in ['exit', 'quit']:
                logger.info("Exiting interactive session.")
                break

            # Process the query via cognitive_engine if the function exists.
            if hasattr(cognitive_engine, 'process_query'):
                try:
                    response = cognitive_engine.process_query(user_input)
                except Exception as e:
                    response = f"Error processing query: {e}"
            else:
                # Fallback behavior: simply echo the input.
                response = f"Echo: {user_input}"

            print(response)
        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt received. Exiting interactive session.")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    logger.info("Aurora Interactive Session Starting...")
    interactive_loop()
