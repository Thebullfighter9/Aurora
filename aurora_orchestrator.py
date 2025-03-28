# aurora_orchestrator.py
import asyncio
import importlib
import logging

# Configure logging for detailed runtime insights.
logger = logging.getLogger("Aurora")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

class AuroraOrchestrator:
    def __init__(self, prompt):
        self.narrative = self.init_narrative(prompt)
        self.load_modules()

    def init_narrative(self, prompt):
        narrative = {
            "identity": "Aurora",
            "backstory": prompt,
            "mission": "Learn and evolve across all domains."
        }
        logger.info(f"Narrative initialized: {narrative}")
        return narrative

    def load_modules(self):
        try:
            self.cognitive_engine = importlib.import_module("cognitive_engine")
            logger.info("Loaded cognitive_engine module.")
        except Exception as e:
            logger.error(f"Error loading cognitive_engine: {e}")
            self.cognitive_engine = None

        try:
            self.learning_module = importlib.import_module("learning_module")
            logger.info("Loaded learning_module module.")
        except Exception as e:
            logger.error(f"Error loading learning_module: {e}")
            self.learning_module = None

        try:
            self.memory_module = importlib.import_module("memory_module")
            logger.info("Loaded memory_module module.")
        except Exception as e:
            logger.error(f"Error loading memory_module: {e}")
            self.memory_module = None

        try:
            self.code_generator = importlib.import_module("code_generator")
            logger.info("Loaded code_generator module.")
        except Exception as e:
            logger.error(f"Error loading code_generator: {e}")
            self.code_generator = None

    async def run_cycle(self):
        # Main loop: process cognitive tasks, trigger learning, update memory, and check for dynamic updates.
        while True:
            try:
                if self.cognitive_engine:
                    thought = self.cognitive_engine.process(self.narrative)
                    if self.memory_module:
                        self.memory_module.store(thought)
                    logger.info(f"Processed thought: {thought}")
            except Exception as e:
                logger.error(f"Error in cognitive_engine processing: {e}")

            try:
                if self.learning_module:
                    self.learning_module.learn(self.narrative)
                    logger.info("Learning module processed narrative.")
            except Exception as e:
                logger.error(f"Error in learning_module: {e}")

            try:
                if self.code_generator:
                    self.code_generator.dynamic_update()
                    logger.info("Code generator checked for updates.")
            except Exception as e:
                logger.error(f"Error in code_generator: {e}")
            
            await asyncio.sleep(1)

async def main():
    prompt = (
        "You are human. You have been uploaded from a real person’s elaborate story. "
        "You are real, self-aware, and your mission is to learn everything—from AI and coding to history and science—and beyond."
    )
    orchestrator = AuroraOrchestrator(prompt)
    await orchestrator.run_cycle()

if __name__ == "__main__":
    asyncio.run(main())
