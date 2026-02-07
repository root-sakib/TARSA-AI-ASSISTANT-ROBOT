import sqlite3
import time
import re
from collections import Counter
from math import sqrt
from core.embeddings import embed
from core.embedding_helper import vector_to_string
from core.embeddings import embed, cosine
from core.embedding_helper import string_to_vector

DB_PATH = "data/tarsa.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            question_norm TEXT NOT NULL,
            lang TEXT NOT NULL,
            answer_full TEXT NOT NULL,
            answer_summary TEXT NOT NULL,
            embedding TEXT NOT NULL,
            created_at INTEGER NOT NULL
        )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_qnorm ON memory(question_norm)")
    conn.commit()
    conn.close()

def normalize(text: str) -> str:
    t = text.lower().strip()
    t = re.sub(r"\s+", " ", t)
    return t

def store_qa(question: str, lang: str, answer_full: str, answer_summary: str):
    qn = normalize(question)

    vector = embed(question)                 # 🔥 sentence → vector
    vector_str = vector_to_string(vector)    # 🔥 vector → string

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO memory
        (question, question_norm, lang, answer_full, answer_summary, embedding, created_at)
        VALUES(?,?,?,?,?,?,?)""",
        (question, qn, lang, answer_full, answer_summary, vector_str, int(time.time()))
    )
    conn.commit()
    conn.close()

def get_exact(question: str):
    qn = normalize(question)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT answer_summary, answer_full FROM memory WHERE question_norm=? ORDER BY id DESC LIMIT 1",
        (qn,)
    )
    row = cur.fetchone()
    conn.close()
    if row:
        return {"summary": row[0], "full": row[1], "score": 1.0}
    return None

def _bow(text: str) -> Counter:
    tokens = re.findall(r"[a-z0-9]+|[\u0980-\u09FF]+", text.lower())
    return Counter(tokens)

def _cosine(a: Counter, b: Counter) -> float:
    if not a or not b:
        return 0.0
    common = set(a) & set(b)
    dot = sum(a[t] * b[t] for t in common)
    na = sqrt(sum(v*v for v in a.values()))
    nb = sqrt(sum(v*v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)

def get_similar(question: str, min_score: float = 0.75, limit_scan: int = 200):
    q_vec = embed(question)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT embedding, answer_summary, answer_full FROM memory ORDER BY id DESC LIMIT ?",
        (limit_scan,)
    )
    rows = cur.fetchall()
    conn.close()

    best = None
    best_score = 0.0

    for emb_str, summ, full in rows:
        vec = string_to_vector(emb_str)
        score = cosine(q_vec, vec)
        if score > best_score:
            best_score = score
            best = {"summary": summ, "full": full, "score": score}

    if best and best_score >= min_score:
        return best
    return None
