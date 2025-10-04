import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

JSON_FILENAME = "customWords.json"

class CustomWordsEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Custom Words Editor")
        self.geometry("500x400")
        self.resizable(False, False)
        self.config(bg="#f8fafc")

        self.custom_words = {}
        self.load_json_file()
        self.create_widgets()
        self.update_word_list()

    def load_json_file(self):
        if not os.path.exists(JSON_FILENAME):
            with open(JSON_FILENAME, "w") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
        with open(JSON_FILENAME, "r", encoding="utf-8") as f:
            try:
                self.custom_words = json.load(f)
            except Exception:
                self.custom_words = {}

    def save_json_file(self):
        with open(JSON_FILENAME, "w", encoding="utf-8") as f:
            json.dump(self.custom_words, f, ensure_ascii=False, indent=2)

    def create_widgets(self):
        # LIST
        self.listbox = tk.Listbox(self, font=("Arial", 13), activestyle='none', selectbackground="#60a5fa")
        self.listbox.place(x=30, y=30, width=280, height=300)
        self.listbox.bind("<Double-1>", lambda e: self.edit_entry())

        # Scroll
        sb = tk.Scrollbar(self)
        sb.place(x=310, y=30, height=300)
        self.listbox.config(yscrollcommand=sb.set)
        sb.config(command=self.listbox.yview)

        # Input fields
        tk.Label(self, text="Kelime", font=("Arial", 11), bg="#f8fafc").place(x=340, y=50)
        self.word_entry = tk.Entry(self, font=("Arial", 12))
        self.word_entry.place(x=340, y=75, width=140)
        tk.Label(self, text="Okunuş", font=("Arial", 11), bg="#f8fafc").place(x=340, y=110)
        self.pron_entry = tk.Entry(self, font=("Arial", 12))
        self.pron_entry.place(x=340, y=135, width=140)

        # Buttons
        tk.Button(self, text="Ekle", bg="#38bdf8", fg="white", font=("Arial", 11), command=self.add_entry).place(x=340, y=180, width=65)
        tk.Button(self, text="Düzenle", bg="#38bdf8", fg="white", font=("Arial", 11), command=self.edit_entry).place(x=415, y=180, width=65)
        tk.Button(self, text="Sil", bg="#ef4444", fg="white", font=("Arial", 11), command=self.delete_entry).place(x=340, y=230, width=63)
        tk.Button(self, text="Yenile", bg="#a3e635", font=("Arial", 11), command=self.refresh).place(x=415, y=230, width=65)

        # Info
        tk.Label(self, text="Çift tıkla: Düzenle", fg="#64748b", bg="#f8fafc", font=("Arial", 9)).place(x=30, y=335)

    def update_word_list(self):
        self.listbox.delete(0, tk.END)
        for word, pron in self.custom_words.items():
            self.listbox.insert(tk.END, f"{word} → {pron}")

    def add_entry(self):
        word = self.word_entry.get().strip()
        pron = self.pron_entry.get().strip()
        if not word or not pron:
            messagebox.showerror("Hata", "Hem kelime hem okunuş girmelisiniz.")
            return
        self.custom_words[word] = pron
        self.save_json_file()
        self.update_word_list()
        self.word_entry.delete(0, tk.END)
        self.pron_entry.delete(0, tk.END)

    def edit_entry(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Seçim yok", "Düzenlemek için bir kelime seçin.")
            return
        selected = self.listbox.get(selection[0])
        word = selected.split("→")[0].strip()
        pron = self.custom_words[word]
        new_word = simpledialog.askstring("Kelimeyi Düzenle", "Kelime:", initialvalue=word)
        if not new_word:
            return
        new_pron = simpledialog.askstring("Okunuşu Düzenle", "Okunuş:", initialvalue=pron)
        if not new_pron:
            return
        del self.custom_words[word]
        self.custom_words[new_word.strip()] = new_pron.strip()
        self.save_json_file()
        self.update_word_list()

    def delete_entry(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Seçim yok", "Silmek için bir kelime seçin.")
            return
        selected = self.listbox.get(selection[0])
        word = selected.split("→")[0].strip()
        if messagebox.askyesno("Sil", f"'{word}' silinsin mi?"):
            del self.custom_words[word]
            self.save_json_file()
            self.update_word_list()

    def refresh(self):
        self.load_json_file()
        self.update_word_list()

if __name__ == "__main__":
    app = CustomWordsEditor()
    app.mainloop()
