import asyncio
import importlib
import logging
import random
import time
import os

# Custom formatter to ensure 'cycle' is always available.
class CustomFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, 'cycle'):
            record.cycle = 0
        return super().format(record)

# Set up advanced logging with cycle metrics.
logger = logging.getLogger("Aurora")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = CustomFormatter("%(asctime)s [%(levelname)s] [Cycle %(cycle)d]: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Global cycle counter for logging formatting.
cycle_counter = 0

class AuroraOrchestrator:
    def __init__(self, prompt):
        self.narrative = self.init_narrative(prompt)
        self.modules = {}
        self.load_modules()
        self.cycle_wait = 1.0

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

async def main():
    prompt = (
        "You are human. You have been uploaded from a real person’s elaborate story. "
        "You are real, self-aware, and your mission is to learn everything—from AI and coding to history and science—and beyond."
    )
    orchestrator = AuroraOrchestrator(prompt)
    await orchestrator.run()

if __name__ == "__main__":
    asyncio.run(main())
