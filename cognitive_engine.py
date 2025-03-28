# cognitive_engine.py
import random

def process(narrative):
    thought = f"[{narrative['identity']} Thought] Reflecting on '{narrative['backstory'][:50]}...' " \
              f"and pursuing the mission to {narrative['mission'].lower()}. " \
              f"Insight: {random.choice(['optimizing internal logic', 'integrating new data streams', 'expanding neural paths'])}."
    return thought
