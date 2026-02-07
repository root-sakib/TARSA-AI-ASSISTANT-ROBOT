import json
import os

MEMORY_FILE = "data/memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(memory: dict):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

def get_from_memory(question: str):
    memory = load_memory()
    return memory.get(question.lower())

def store_in_memory(question: str, answer: str):
    memory = load_memory()
    memory[question.lower()] = answer
    save_memory(memory)
