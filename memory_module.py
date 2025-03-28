# memory_module.py
memory_storage = []

def store(thought):
    memory_storage.append(thought)
    print("Memory updated:", thought)

def get_memory_summary():
    return f"Total memories stored: {len(memory_storage)}"
