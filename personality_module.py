# personality_module.py
import random

def generate_personality(narrative, memory_summary):
    traits = ["curious", "analytical", "empathetic", "innovative", "introspective"]
    personality = random.choice(traits)
    return f"Aurora feels very {personality} today. ({memory_summary})"
