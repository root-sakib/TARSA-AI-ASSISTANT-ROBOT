import tkinter as tk
import threading
from core.brain import generate_response

def start_gui():
    root = tk.Tk()
    root.title("TARSA Assistant")
    root.geometry("560x460")

    active = {"status": False}

    chat = tk.Text(root, height=18)
    chat.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    status_lbl = tk.Label(root, text="Status: OFF")
    status_lbl.pack(pady=(0, 6))

    entry = tk.Entry(root, state="disabled")
    entry.pack(fill=tk.X, padx=10)

    def append(msg: str):
        chat.insert(tk.END, msg + "\n")
        chat.see(tk.END)

    def set_on():
        active["status"] = True
        status_lbl.config(text="Status: ON")
        entry.config(state="normal")
        append("AI: Hello! I am TARSA.")
        entry.focus_set()

    def set_off():
        active["status"] = False
        status_lbl.config(text="Status: OFF")
        entry.config(state="disabled")
        append("AI: Goodbye!")

    def _worker(user_text: str):
        # background thread work
        reply = generate_response(user_text)
        root.after(0, lambda: append(f"AI: {reply}"))
        root.after(0, lambda: send_btn.config(state="normal"))
        root.after(0, lambda: status_lbl.config(text="Status: ON"))

    def send():
        if not active["status"]:
            append("AI: TARSA is OFF. Please turn ON first.")
            return

        user_text = entry.get().strip()
        if not user_text:
            return

        entry.delete(0, tk.END)
        append(f"You: {user_text}")

        # show thinking + disable send while working
        status_lbl.config(text="Status: Thinking...")
        send_btn.config(state="disabled")

        t = threading.Thread(target=_worker, args=(user_text,), daemon=True)
        t.start()

    entry.bind("<Return>", lambda event: send())

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=8)

    tk.Button(btn_frame, text="Turn ON", command=set_on).pack(side=tk.LEFT, padx=6)
    send_btn = tk.Button(btn_frame, text="Send", command=send, state="disabled")
    send_btn.pack(side=tk.LEFT, padx=6)
    tk.Button(btn_frame, text="Turn OFF", command=set_off).pack(side=tk.LEFT, padx=6)

    root.mainloop()
