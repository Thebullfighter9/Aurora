#!/usr/bin/env python3
"""
aurora_interactive.py
An interactive command-line interface for Aurora.
This script initializes required modules and then enters an interactive loop
to process user commands and queries.
"""

import sys
import logging
import importlib
import time

# Import your modules
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
  help                      - Show this help message.
  status                    - Show system status.
  modules                   - List loaded modules.
  memory                    - Display memory module status.
  query <your query>        - Process a query through the cognitive engine.
  reload                    - Reload all modules.
  reset                     - Reset personality and clear temporary data.
  run                       - Enter continuous run mode (if supported).
  exit or quit              - Exit the interactive session.
  
Any other input is forwarded to the cognitive engine as a query.
"""
    print(help_text)


def show_status():
    print("System Status:")
    print("  Cognitive Engine available:", hasattr(cognitive_engine, "process_query"))
    print("  Learning Module loaded:", hasattr(learning_module, "__name__"))
    print("  Memory Module loaded:", hasattr(memory_module, "__name__"))
    print("  Code Generator loaded:", hasattr(code_generator, "__name__"))
    print("  Research Module loaded:", hasattr(research_module, "__name__"))
    print("  Personality Module loaded:", hasattr(personality_module, "__name__"))
    print("  Current personality: Aurora feels very curious today.")


def list_modules():
    modules = {
        "cognitive_engine": cognitive_engine,
        "learning_module": learning_module,
        "memory_module": memory_module,
        "code_generator": code_generator,
        "research_module": research_module,
        "personality_module": personality_module
    }
    print("Loaded modules and some attributes:")
    for name, mod in modules.items():
        attrs = [attr for attr in dir(mod) if not attr.startswith('__')]
        print(f"  {name}: {', '.join(attrs[:5])} ...")


def show_memory():
    if hasattr(memory_module, "get_memory"):
        memories = memory_module.get_memory()
        print("Stored Memories:")
        for m in memories:
            print(" -", m)
    else:
        print("Memory module is loaded. (No detailed memory view available.)")


def process_query(query):
    if hasattr(cognitive_engine, 'process_query'):
        try:
            response = cognitive_engine.process_query(query)
            return response
        except Exception as e:
            return f"Error processing query: {e}"
    else:
        return f"Echo: {query}"


def reload_modules():
    modules = [cognitive_engine, learning_module, memory_module,
               code_generator, research_module, personality_module]
    for mod in modules:
        try:
            importlib.reload(mod)
            logger.info(f"Reloaded module: {mod.__name__}")
        except Exception as e:
            logger.error(f"Failed to reload {mod.__name__}: {e}")


def reset_system():
    print("Resetting system...")
    if hasattr(personality_module, "reset"):
        personality_module.reset()
    if hasattr(memory_module, "clear_memory"):
        memory_module.clear_memory()
    print("System reset complete.")


def run_continuous():
    # Try to use a continuous run loop from cognitive_engine, if available.
    if hasattr(cognitive_engine, "run_cycle"):
        print("Entering continuous run mode. Press Ctrl+C to exit.")
        try:
            while True:
                result = cognitive_engine.run_cycle()
                # Optionally, print out the result of each cycle.
                print(f"Cycle result: {result}")
                time.sleep(0.5)  # Adjust sleep time as needed.
        except KeyboardInterrupt:
            print("Continuous run mode terminated.")
    else:
        print("Continuous run mode is not available in cognitive_engine.")


def interactive_loop():
    logger.info("Starting interactive session...")

    # Initialize cognitive engine if an initialization function is provided.
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

            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()

            if command in ['exit', 'quit']:
                logger.info("Exiting interactive session.")
                break
            elif command == "help":
                print_help()
            elif command == "status":
                show_status()
            elif command == "modules":
                list_modules()
            elif command == "memory":
                show_memory()
            elif command == "query":
                if len(parts) > 1:
                    response = process_query(parts[1])
                    print(response)
                else:
                    print("Usage: query <your query>")
            elif command == "reload":
                reload_modules()
            elif command == "reset":
                reset_system()
            elif command == "run":
                run_continuous()
            else:
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
