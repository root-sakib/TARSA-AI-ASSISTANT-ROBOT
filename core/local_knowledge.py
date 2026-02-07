import json

with open("data/persons.json", "r", encoding="utf-8") as f:
    PERSON_DATA = json.load(f)

def find_person(name: str):
    key = name.lower().strip()
    return PERSON_DATA.get(key)
