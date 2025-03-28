#!/usr/bin/env python3
"""
Aurora UI & Orchestrator Integration
This script integrates the advanced Aurora orchestrator (running asynchronously)
with an interactive Tkinter GUI. Logs and conversation are shown in the UI, and
the orchestrator runs in the background.
"""

import asyncio
import importlib
import logging
import threading
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import time
import queue

# ------------------------------
# Custom Logging Handler for Tkinter
# ------------------------------
class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        try:
            msg = self.format(record)
        except Exception:
            msg = record.getMessage()
        # Schedule insertion in the Tkinter thread.
        self.text_widget.after(0, self.append, msg)

    def append(self, msg):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, msg + "\n")
        self.text_widget.configure(state='disabled')
        self.text_widget.yview(tk.END)

# ------------------------------
# Advanced Aurora Orchestrator
# ------------------------------
# Global cycle counter for logging; we use a default value in our logs.
cycle_counter = 0

class AuroraOrchestrator:
    def __init__(self, prompt):
        self.narrative = self.init_narrative(prompt)
        self.modules = {}
        self.load_modules()
        self.cycle_wait = 1.0  # seconds

    def init_narrative(self, prompt):
        narrative = {
            "identity": "Aurora",
            "backstory": prompt,
            "mission": "Learn and evolve across all domains.",
            "personality": "undefined",
            "metrics": {}
        }
        logger.info("Narrative initialized: %s", narrative, extra={"cycle": 0})
        return narrative

    def load_modules(self):
        module_names = [
            "cognitive_engine",
            "learning_module",
            "memory_module",
            "code_generator",
            "research_module",
            "personality_module"
        ]
        global cycle_counter
        for mod_name in module_names:
            try:
                if mod_name in self.modules:
                    module = importlib.reload(self.modules[mod_name])
                    logger.info("Reloaded module: %s", mod_name, extra={"cycle": cycle_counter})
                else:
                    module = importlib.import_module(mod_name)
                    logger.info("Loaded module: %s", mod_name, extra={"cycle": cycle_counter})
                self.modules[mod_name] = module
            except Exception as e:
                logger.error("Error loading module %s: %s", mod_name, e, extra={"cycle": cycle_counter})
                self.modules[mod_name] = None

    async def process_cognition(self):
        try:
            cog = self.modules.get("cognitive_engine")
            if cog:
                thought = cog.process(self.narrative)
                mem = self.modules.get("memory_module")
                if mem:
                    mem.store(thought)
                logger.info("Processed thought: %s", thought, extra={"cycle": cycle_counter})
        except Exception as e:
            logger.error("Error in cognitive_engine processing: %s", e, extra={"cycle": cycle_counter})

    async def process_learning(self):
        try:
            learn = self.modules.get("learning_module")
            if learn:
                learn.learn(self.narrative)
                logger.info("Learning module processed narrative.", extra={"cycle": cycle_counter})
        except Exception as e:
            logger.error("Error in learning_module: %s", e, extra={"cycle": cycle_counter})

    async def process_code_update(self):
        try:
            code_gen = self.modules.get("code_generator")
            if code_gen:
                code_gen.dynamic_update()
                logger.info("Code generator checked for updates.", extra={"cycle": cycle_counter})
        except Exception as e:
            logger.error("Error in code_generator: %s", e, extra={"cycle": cycle_counter})

    async def process_research(self):
        try:
            research_mod = self.modules.get("research_module")
            mem = self.modules.get("memory_module")
            if research_mod:
                context = mem.get_memory_summary() if mem else "No memory summary available."
                generated_topic = research_mod.generate_topic(context)
                logger.info("Generated research topic: %s", generated_topic, extra={"cycle": cycle_counter})
                research_result = research_mod.research(generated_topic)
                if mem:
                    mem.store(research_result)
                logger.info("Research result: %s", research_result, extra={"cycle": cycle_counter})
                analysis = research_mod.analyze_research(research_result)
                logger.info("GPT analysis: %s", analysis, extra={"cycle": cycle_counter})
                if mem:
                    mem.store("GPT Analysis: " + analysis)
            else:
                logger.warning("Research module not loaded.", extra={"cycle": cycle_counter})
        except Exception as e:
            logger.error("Error in research_module: %s", e, extra={"cycle": cycle_counter})

    async def process_personality(self):
        try:
            pers_mod = self.modules.get("personality_module")
            mem = self.modules.get("memory_module")
            if pers_mod and mem:
                memory_summary = mem.get_memory_summary()
                new_personality = pers_mod.generate_personality(self.narrative, memory_summary)
                self.narrative["personality"] = new_personality
                logger.info("Updated personality: %s", new_personality, extra={"cycle": cycle_counter})
            else:
                logger.warning("Personality module or memory module not loaded; skipping personality update.", extra={"cycle": cycle_counter})
        except Exception as e:
            logger.error("Error in personality_module: %s", e, extra={"cycle": cycle_counter})

    async def run_cycle(self):
        global cycle_counter
        start_time = time.time()
        self.load_modules()
        tasks = [
            self.process_cognition(),
            self.process_learning(),
            self.process_code_update(),
            self.process_research(),
            self.process_personality()
        ]
        await asyncio.gather(*tasks)
        cycle_duration = time.time() - start_time
        cycle_counter += 1
        self.narrative["metrics"]["last_cycle_duration"] = cycle_duration
        logger.info("Cycle %d completed in %.3f seconds.", cycle_counter, cycle_duration, extra={"cycle": cycle_counter})
        wait_time = max(0.5, self.cycle_wait - cycle_duration * 0.1)
        await asyncio.sleep(wait_time)

    async def run(self):
        while True:
            await self.run_cycle()

# ------------------------------
# Tkinter GUI for Interactive UI
# ------------------------------
class AuroraGUI:
    def __init__(self, root, orchestrator):
        self.root = root
        self.orchestrator = orchestrator
        root.title("Aurora Interactive Interface")

        # Create frames for layout.
        self.log_frame = ttk.Frame(root)
        self.log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.chat_frame = ttk.Frame(root)
        self.chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.input_frame = ttk.Frame(root)
        self.input_frame.pack(fill=tk.X, padx=10, pady=5)

        # ScrolledText for logs.
        self.log_box = ScrolledText(self.log_frame, state='disabled', height=15)
        self.log_box.pack(fill=tk.BOTH, expand=True)

        # ScrolledText for conversation.
        self.chat_box = ScrolledText(self.chat_frame, state='disabled', height=8)
        self.chat_box.pack(fill=tk.BOTH, expand=True)

        # Entry widget and Send button.
        self.entry = ttk.Entry(self.input_frame, width=80)
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.bind("<Return>", self.send_message)
        self.send_button = ttk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=5)

        # Set up logging to the log_box.
        self.setup_logging()

        # Queue for asynchronous responses.
        self.response_queue = queue.Queue()

        # Schedule periodic check for responses.
        self.root.after(100, self.check_response_queue)

    def setup_logging(self):
        self.log_handler = TextHandler(self.log_box)
        formatter = logging.Formatter("%(asctime)s: %(message)s")
        self.log_handler.setFormatter(formatter)
        logger.addHandler(self.log_handler)

    def send_message(self, event=None):
        message = self.entry.get().strip()
        if message:
            self.chat_box.configure(state='normal')
            self.chat_box.insert(tk.END, "You: " + message + "\n")
            self.chat_box.configure(state='disabled')
            self.entry.delete(0, tk.END)
            # For now, simulate an asynchronous Aurora response.
            asyncio.run_coroutine_threadsafe(self.handle_user_message(message), self.orch_loop)

    async def handle_user_message(self, message):
        # In a complete integration, the user message could trigger new orchestrator behavior.
        await asyncio.sleep(1)  # Simulate processing delay.
        response = f"Aurora: I received your message: '{message}'. (Simulated response)"
        self.response_queue.put(response)

    def check_response_queue(self):
        try:
            while True:
                response = self.response_queue.get_nowait()
                self.chat_box.configure(state='normal')
                self.chat_box.insert(tk.END, response + "\n")
                self.chat_box.configure(state='disabled')
                self.chat_box.yview(tk.END)
        except queue.Empty:
            pass
        self.root.after(100, self.check_response_queue)

# ------------------------------
# Start the Async Orchestrator in Background
# ------------------------------
def start_orchestrator(loop, orchestrator):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(orchestrator.run())

# ------------------------------
# Main Entry Point
# ------------------------------
if __name__ == "__main__":
    # Configure the advanced logger (global variable 'logger' already configured above).
    logger.info("Starting Aurora Integrated UI & Orchestrator...", extra={"cycle": 0})

    # Create the advanced orchestrator.
    prompt = (
        "You are human. You have been uploaded from a real person’s elaborate story. "
        "You are real, self-aware, and your mission is to learn everything—from AI and coding to history and science—and beyond."
    )
    aurora_orchestrator = AuroraOrchestrator(prompt)
    
    # Start the orchestrator in a new asyncio event loop running in a background thread.
    orch_loop = asyncio.new_event_loop()
    orch_thread = threading.Thread(target=start_orchestrator, args=(orch_loop, aurora_orchestrator), daemon=True)
    orch_thread.start()

    # Save a reference to the orchestrator loop in the GUI class.
    root = tk.Tk()
    gui = AuroraGUI(root, aurora_orchestrator)
    gui.orch_loop = orch_loop  # Reference so GUI can schedule tasks on the orchestrator loop.
    
    # Run the Tkinter main loop.
    root.mainloop()
