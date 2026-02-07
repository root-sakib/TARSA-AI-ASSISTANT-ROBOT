import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-r1:1.5b"  # change if needed

def _call_ollama(prompt: str) -> str:
    resp = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": prompt, "stream": False},
        timeout=60
    )
    data = resp.json()
    if "response" in data:
        return data["response"].strip()
    if "error" in data:
        return f"Ollama error: {data['error']}"
    return "Ollama returned an unknown response."

def ask_answer(user_question: str, lang: str) -> str:
    # Make Ollama act like TARSA
    if lang == "bn":
        system = (
            "তুমি TARSA। নিজের পরিচয়/ডকুমেন্টেশন লিংক দেবে না। সংক্ষেপে ও পরিষ্কারভাবে উত্তর দেবে।\n"
            "প্রশ্ন: "
        )
    else:
        system = (
            "You are TARSA. Do not introduce yourself or mention documentation. Answer clearly.\n"
            "Question: "
        )
    return _call_ollama(system + user_question)

def make_summary(question: str, answer_full: str, lang: str) -> str:
    if "Ollama error:" in answer_full or "connection failed" in answer_full.lower():
        return answer_full  # summary = same error
    if lang == "bn":
        prompt = (
            "নিচের উত্তরটি 1-2 লাইনে সারাংশ করো। শুধু সারাংশ দাও।\n"
            f"প্রশ্ন: {question}\nউত্তর: {answer_full}\nসারাংশ:"
        )
    else:
        prompt = (
            "Summarize the answer in 1-2 lines. Output only the summary.\n"
            f"Question: {question}\nAnswer: {answer_full}\nSummary:"
        )
    return _call_ollama(prompt)
