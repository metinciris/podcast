import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import json
import os
import threading
import time
from gtts import gTTS
import tempfile
from playsound import playsound

DEFAULT_JSON = "customWords.json"

class CustomWordsEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Custom Words Editor")
        self.geometry("900x540")
        self.resizable(False, False)
        self.config(bg="#ecf0f1")
        self.json_filename = DEFAULT_JSON
        self.custom_words = {}
        self.save_label = None
        self.create_widgets()
        self.open_json_file(initial=True)

    def create_widgets(self):
        tk.Button(self, text="JSON Seç", font=("Arial", 18, "bold"), bg="#888", fg="white", command=self.change_json_file).place(x=30, y=20, width=180, height=48)
        self.json_label = tk.Label(self, text="", font=("Arial", 16, "bold"), bg="#ecf0f1", anchor="w")
        self.json_label.place(x=230, y=25, width=420, height=38)

        self.save_label = tk.Label(self, text="", font=("Arial", 15, "bold"), fg="green", bg="#ecf0f1", anchor="e")
        self.save_label.place(x=670, y=25, width=200, height=38)

        self.listbox = tk.Listbox(self, font=("Arial", 21), activestyle='none', selectbackground="#60a5fa")
        self.listbox.place(x=30, y=90, width=500, height=400)
        self.listbox.bind("<Double-1>", lambda e: self.edit_entry())

        sb = tk.Scrollbar(self)
        sb.place(x=530, y=90, height=400)
        self.listbox.config(yscrollcommand=sb.set)
        sb.config(command=self.listbox.yview)

        tk.Label(self, text="Kelime", font=("Arial", 16), bg="#ecf0f1").place(x=570, y=110)
        self.word_entry = tk.Entry(self, font=("Arial", 21))
        self.word_entry.place(x=570, y=145, width=300, height=42)
        tk.Label(self, text="Okunuş", font=("Arial", 16), bg="#ecf0f1").place(x=570, y=210)
        self.pron_entry = tk.Entry(self, font=("Arial", 21))
        self.pron_entry.place(x=570, y=245, width=300, height=42)

        tk.Button(self, text="Ekle", font=("Arial", 17, "bold"), bg="#38bdf8", fg="white", command=self.add_entry).place(x=570, y=320, width=90, height=48)
        tk.Button(self, text="Düzenle", font=("Arial", 17, "bold"), bg="#38bdf8", fg="white", command=self.edit_entry).place(x=675, y=320, width=90, height=48)
        tk.Button(self, text="Sil", font=("Arial", 17, "bold"), bg="#ef4444", fg="white", command=self.delete_entry).place(x=780, y=320, width=90, height=48)
        tk.Button(self, text="Yenile", font=("Arial", 17, "bold"), bg="#a3e635", fg="black", command=self.refresh).place(x=570, y=400, width=195, height=48)
        tk.Button(self, text="Oku", font=("Arial", 17, "bold"), bg="#6366f1", fg="white", command=self.speak_selected).place(x=775, y=400, width=95, height=48)
        tk.Label(self, text="Çift tıkla: Düzenle", fg="#64748b", bg="#ecf0f1", font=("Arial", 14)).place(x=30, y=500)

    def open_json_file(self, initial=False):
        if initial:
            filename = DEFAULT_JSON if os.path.exists(DEFAULT_JSON) else filedialog.askopenfilename(title="Bir JSON dosyası seçin", filetypes=[("JSON Dosyası", "*.json")])
        else:
            filename = filedialog.askopenfilename(title="Bir JSON dosyası seçin", filetypes=[("JSON Dosyası", "*.json")])
            if not filename:
                return
        if filename:
            self.json_filename = filename
            self.json_label.config(text=self.json_filename)
            self.load_json_file()
            self.update_word_list()

    def change_json_file(self):
        self.open_json_file(initial=False)

    def load_json_file(self):
        if not os.path.exists(self.json_filename):
            with open(self.json_filename, "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
        with open(self.json_filename, "r", encoding="utf-8") as f:
            try:
                self.custom_words = json.load(f)
            except Exception:
                self.custom_words = {}

    def save_json_file(self):
        with open(self.json_filename, "w", encoding="utf-8") as f:
            json.dump(self.custom_words, f, ensure_ascii=False, indent=2)
        self.show_saved_label()

    def show_saved_label(self):
        self.save_label.config(text="Kayıt edildi!")
        def hide():
            time.sleep(1.2)
            self.save_label.config(text="")
        threading.Thread(target=hide, daemon=True).start()

    def update_word_list(self):
        self.listbox.delete(0, tk.END)
        for word, pron in self.custom_words.items():
            self.listbox.insert(tk.END, f"{word}  →  {pron}")

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
        new_word = simpledialog.askstring("Kelimeyi Düzenle", "Kelime:", initialvalue=word, parent=self)
        if not new_word:
            return
        new_pron = simpledialog.askstring("Okunuşu Düzenle", "Okunuş:", initialvalue=pron, parent=self)
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

    def speak_selected(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Seçim yok", "Okumak için bir kelime seçin.")
            return
        selected = self.listbox.get(selection[0])
        word, pron = selected.split("→")
        text = word.strip()
        threading.Thread(target=self.gtts_speak, args=(text,), daemon=True).start()

    def gtts_speak(self, text):
        try:
            tts = gTTS(text=text, lang="tr")
            with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
                tts.save(fp.name)
                playsound(fp.name)
        except Exception as e:
            messagebox.showerror("TTS hatası", f"Sesli okuma başarısız!\n\n{e}")

if __name__ == "__main__":
    app = CustomWordsEditor()
    app.mainloop()
