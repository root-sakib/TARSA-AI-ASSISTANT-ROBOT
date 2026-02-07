from core.lang import detect_lang
from core.identity import who_are_you
from core.user_profile import who_is_user, get_user_field
from core.memory_db import (
    init_db,
    get_exact,
    get_similar,
    store_qa
)
from core.ollama_client import ask_answer, make_summary

# 🔥 database initialize (একবারই হবে)
init_db()


def generate_response(user_input: str) -> str:
    """
    TARSA brain:
    1. USER self questions (my / me)
    2. Robot identity
    3. User identity (do you know me)
    4. Exact memory
    5. Similar memory
    6. Ollama fallback
    7. Learn & store
    """

    text = user_input.strip()
    text_lower = text.lower()
    lang = detect_lang(text)

    # ==================================================
    # 1️⃣ USER self questions (VERY IMPORTANT)
    # ==================================================
    if "my name" in text_lower:
        name = get_user_field("name")
        if name:
            return f"Your name is {name}."

    if "my education" in text_lower:
        edu = get_user_field("education")
        if edu:
            return f"Your education is: {edu}."

    if (
        "my current study" in text_lower
        or "what am i studying" in text_lower
        or "what am i studying now" in text_lower
    ):
        study = get_user_field("current_study")
        if study:
            return f"You are currently studying {study}."

    # ==================================================
    # 2️⃣ Robot identity
    # ==================================================
    if "who are you" in text_lower or "tumi ke" in text_lower or "apni ke" in text_lower:
        return who_are_you(lang)

    # ==================================================
    # 3️⃣ User identity (general)
    # ==================================================
    if (
        "do you know me" in text_lower
        or "who am i" in text_lower
        or "amake chino" in text_lower
        or "ami ke" in text_lower
    ):
        return who_is_user(lang)

    # ==================================================
    # 4️⃣ Exact memory match (instant)
    # ==================================================
    exact = get_exact(text)
    if exact:
        return exact["summary"]

    # ==================================================
    # 5️⃣ Similar memory (human-like recall)
    # ==================================================
    similar = get_similar(text)
    if similar:
        return similar["summary"]

    # ==================================================
    # 6️⃣ Ollama fallback (last option)
    # ==================================================
    full_answer = ask_answer(text, lang)

    # ==================================================
    # 7️⃣ Learn & store (auto memory)
    # ==================================================
    summary = make_summary(text, full_answer, lang)

    # error হলে save করবে না
    if summary and not summary.lower().startswith("ollama error"):
        store_qa(
            question=text,
            lang=lang,
            answer_full=full_answer,
            answer_summary=summary
        )

    return summary if summary else full_answer
