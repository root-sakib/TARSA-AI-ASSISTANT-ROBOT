import ollama
from core.memory import get_answer, save_answer
from core.utils import clean_text


def ask_ai(question):
    # 1. Check memory first
    cached = get_answer(question)
    if cached:
        return cached

    # 2. Ask DeepSeek if not found
    response = ollama.chat(
        model="deepseek-r1:1.5b",
        messages=[
            {
                "role": "user",
                "content": (
                    "Reply using only plain English letters numbers "
                    "spaces and basic punctuation. "
                    "Do not use symbols.\n\n"
                    + question
                )
            }
        ]
    )

    answer = clean_text(response["message"]["content"])

    # 3. Save for future
    save_answer(question, answer)

    return answer
