import tkinter as tk
from core.ai_engine import ask_ai


class TARSAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TARSA Assistant")
        self.root.geometry("500x600")

        self.is_on = False

        self.toggle_btn = tk.Button(
            root, text="OFF", bg="red",
            command=self.toggle
        )
        self.toggle_btn.pack(pady=10)

        self.chat_box = tk.Text(root, state="disabled")
        self.chat_box.pack(expand=True, fill="both", padx=10)

        self.entry = tk.Entry(root)
        self.entry.pack(fill="x", padx=10, pady=10)
        self.entry.bind("<Return>", self.send)

    def toggle(self):
        self.is_on = not self.is_on
        if self.is_on:
            self.toggle_btn.config(text="ON", bg="green")
        else:
            self.toggle_btn.config(text="OFF", bg="red")

    def send(self, event):
        if not self.is_on:
            return

        question = self.entry.get()
        self.entry.delete(0, tk.END)

        answer = ask_ai(question)

        self.chat_box.config(state="normal")
        self.chat_box.insert(tk.END, "You: " + question + "\n")
        self.chat_box.insert(tk.END, "AI: " + answer + "\n\n")
        self.chat_box.config(state="disabled")
