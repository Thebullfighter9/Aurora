#!/usr/bin/env python3
"""
Memory Module
-------------
Simulates storing and retrieving memories.
"""

import logging

class MemoryModule:
    def __init__(self):
        self.loaded = False
        self.memories = []

    def load(self):
        self.loaded = True
        logging.info("Memory Module initialized.")

    def add_memory(self, memory):
        self.memories.append(memory)
        logging.info(f"Memory updated: {memory}")

    def show_memory(self):
        if not self.memories:
            return "No memories stored."
        return "\n".join(self.memories)

    def reload(self):
        logging.info("Memory Module reloaded.")

    def status(self):
        return self.loaded
