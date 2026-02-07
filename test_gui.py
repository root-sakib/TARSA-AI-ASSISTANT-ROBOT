import tkinter as tk

root = tk.Tk()                 # GUI window তৈরি
root.title("TARSA Assistant")  # window নাম
root.geometry("400x300")       # window size

label = tk.Label(root, text="Hello, I am TARSA")
label.pack(pady=20)

root.mainloop()                # 🔥 এই লাইন না দিলে GUI খুলবে না
