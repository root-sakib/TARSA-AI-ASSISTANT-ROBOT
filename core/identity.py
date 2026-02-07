ROBOT_PROFILE = {
    "name": "TARSA",
    "creator": "Sakibul Islam Sakib",
    "purpose_en": "I am an assistant that answers questions using my local knowledge first, and falls back to Ollama when needed.",
    "purpose_bn": "আমি একটি সহকারী, আগে নিজের ডাটাবেস থেকে উত্তর দিই, না পারলে Ollama থেকে এনে দিই।"
}

def who_are_you(lang="en") -> str:
    if lang == "bn":
        return f"আমি {ROBOT_PROFILE['name']}। আমাকে তৈরি করেছেন {ROBOT_PROFILE['creator']}। {ROBOT_PROFILE['purpose_bn']}"
    return f"My name is {ROBOT_PROFILE['name']}. I was created by {ROBOT_PROFILE['creator']}. {ROBOT_PROFILE['purpose_en']}"
