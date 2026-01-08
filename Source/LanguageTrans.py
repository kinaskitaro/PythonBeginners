import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from googletrans import Translator, LANGUAGES
from threading import Thread
from datetime import datetime

try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False

COLORS = {
    "bg": "#2C3E50",
    "panel": "#34495E",
    "text": "#ECF0F1",
    "secondary": "#BDC3C7",
    "primary": "#3498DB",
    "primary_hover": "#2980B9",
    "success": "#27AE60",
    "warning": "#F39C12",
    "danger": "#E74C3C",
    "input_bg": "#ECF0F1",
    "input_text": "#2C3E50"
}

class LanguageTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title("🌐 Modern Language Translator")
        self.root.geometry("650x750")
        self.root.minsize(550, 650)
        self.root.configure(bg=COLORS["bg"])
        
        self.translator = Translator()
        self.translation_history = []
        
        self.lang_dict = {v.capitalize(): k for k, v in LANGUAGES.items()}
        self.lang_names = list(self.lang_dict.keys())
        self.lang_names.sort()
        
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg=COLORS["bg"], padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(main_frame, text="🌐 Modern Language Translator", 
                             font=('Helvetica', 18, 'bold'), 
                             bg=COLORS["bg"], fg="#F39C12")
        title_label.pack(pady=(0, 15))
        
        lang_frame = tk.Frame(main_frame, bg=COLORS["panel"])
        lang_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(lang_frame, text="From:", font=('Helvetica', 10, 'bold'),
                bg=COLORS["panel"], fg=COLORS["text"]).pack(side=tk.LEFT, padx=(15, 5))
        
        self.source_lang = ttk.Combobox(lang_frame, values=['Auto-Detect'] + self.lang_names, 
                                      width=22, state='readonly')
        self.source_lang.set('Auto-Detect')
        self.source_lang.pack(side=tk.LEFT, padx=5, pady=10)
        
        swap_btn = tk.Button(lang_frame, text="⇄", width=4,
                           bg=COLORS["primary"], fg="white",
                           activebackground=COLORS["primary_hover"],
                           cursor="hand2", relief=tk.FLAT,
                           command=self.swap_languages)
        swap_btn.pack(side=tk.LEFT, padx=10)
        
        tk.Label(lang_frame, text="To:", font=('Helvetica', 10, 'bold'),
                bg=COLORS["panel"], fg=COLORS["text"]).pack(side=tk.LEFT, padx=(0, 5))
        
        self.target_lang = ttk.Combobox(lang_frame, values=self.lang_names, 
                                      width=22, state='readonly')
        self.target_lang.set('Spanish')
        self.target_lang.pack(side=tk.LEFT, padx=5, pady=10)
        
        tk.Label(main_frame, text="📝 Source Text", font=('Helvetica', 11, 'bold'),
                bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor=tk.W, pady=(5, 5))
        
        input_header = tk.Frame(main_frame, bg=COLORS["panel"])
        input_header.pack(fill=tk.X, pady=(3, 8))
        
        self.char_count_label = tk.Label(input_header, text="Characters: 0", 
                                     font=('Helvetica', 9),
                                     bg=COLORS["panel"], fg=COLORS["secondary"])
        self.char_count_label.pack(side=tk.LEFT, padx=10, pady=8)
        
        clear_btn = tk.Button(input_header, text="Clear", width=8,
                           bg=COLORS["danger"], fg="white",
                           activebackground="#C0392B",
                           cursor="hand2", relief=tk.FLAT,
                           command=lambda: self.clear_text(self.source_text))
        clear_btn.pack(side=tk.RIGHT, padx=3, pady=5)
        
        copy_btn = tk.Button(input_header, text="Copy", width=8,
                           bg=COLORS["primary"], fg="white",
                           activebackground=COLORS["primary_hover"],
                           cursor="hand2", relief=tk.FLAT,
                           command=lambda: self.copy_text(self.source_text))
        copy_btn.pack(side=tk.RIGHT, padx=3, pady=5)
        
        self.source_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=10, 
                                              font=('Helvetica', 11),
                                              bg=COLORS["input_bg"], fg=COLORS["input_text"])
        self.source_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.source_text.bind('<KeyRelease>', self.update_char_count)
        
        button_frame = tk.Frame(main_frame, bg=COLORS["bg"])
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.translate_btn = tk.Button(button_frame, text="🚀 Translate", width=15,
                                   bg=COLORS["success"], fg="white",
                                   activebackground="#229954",
                                   cursor="hand2", relief=tk.FLAT,
                                   font=('Helvetica', 11, 'bold'),
                                   command=self.translate_threaded)
        self.translate_btn.pack(side=tk.LEFT, padx=5)
        
        history_btn = tk.Button(button_frame, text="📜 History", width=12,
                             bg=COLORS["primary"], fg="white",
                             activebackground=COLORS["primary_hover"],
                             cursor="hand2", relief=tk.FLAT,
                             command=self.show_history)
        history_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Label(main_frame, text="🌍 Translation Result", font=('Helvetica', 11, 'bold'),
                bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor=tk.W)
        
        output_header = tk.Frame(main_frame, bg=COLORS["panel"])
        output_header.pack(fill=tk.X, pady=(3, 8))
        
        clear_btn2 = tk.Button(output_header, text="Clear", width=8,
                             bg=COLORS["danger"], fg="white",
                             activebackground="#C0392B",
                             cursor="hand2", relief=tk.FLAT,
                             command=lambda: self.clear_text(self.target_text))
        clear_btn2.pack(side=tk.RIGHT, padx=3, pady=5)
        
        copy_btn2 = tk.Button(output_header, text="Copy", width=8,
                            bg=COLORS["primary"], fg="white",
                            activebackground=COLORS["primary_hover"],
                            cursor="hand2", relief=tk.FLAT,
                            command=lambda: self.copy_text(self.target_text))
        copy_btn2.pack(side=tk.RIGHT, padx=3, pady=5)
        
        self.target_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=10, 
                                              font=('Helvetica', 11),
                                              bg=COLORS["input_bg"], fg=COLORS["input_text"])
        self.target_text.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        self.status_var = tk.StringVar()
        self.status_var.set("✓ Ready to translate")
        self.status_label = tk.Label(main_frame, textvariable=self.status_var, 
                                   font=('Helvetica', 9),
                                   bg=COLORS["bg"], fg=COLORS["secondary"])
        self.status_label.pack(side=tk.BOTTOM, pady=5)

    def update_char_count(self, event=None):
        text = self.source_text.get(1.0, tk.END).strip()
        self.char_count_label.config(text=f"Characters: {len(text)}")

    def translate_threaded(self):
        text_to_translate = self.source_text.get(1.0, tk.END).strip()
        
        if not text_to_translate:
            self.show_error("⚠️ Please enter text to translate")
            return
        
        self.translate_btn.config(state='disabled', text='⏳ Translating...')
        self.status_var.set("🔄 Translating...")
        Thread(target=self.translate, daemon=True).start()

    def translate(self):
        src_lang_name = self.source_lang.get()
        tgt_lang_name = self.target_lang.get()
        
        if src_lang_name == 'Auto-Detect':
            src_lang = 'auto'
        else:
            src_lang = self.lang_dict.get(src_lang_name, 'en')
        
        tgt_lang = self.lang_dict.get(tgt_lang_name, 'es')
        text_to_translate = self.source_text.get(1.0, tk.END).strip()
        
        try:
            translator = Translator()
            translation = translator.translate(text_to_translate, src=src_lang, dest=tgt_lang)
            
            result_text = getattr(translation, 'text', str(translation))
            
            self.root.after(0, lambda: self.display_translation(result_text))
            
            if src_lang == 'auto':
                detected_lang = getattr(translation, 'src', 'unknown')
                detected_name = LANGUAGES.get(detected_lang, 'Unknown').capitalize()
                self.root.after(0, lambda: self.status_var.set(f"✓ Detected: {detected_name} → {tgt_lang_name}"))
            else:
                self.root.after(0, lambda: self.status_var.set(f"✓ {src_lang_name} → {tgt_lang_name}"))
            
            self.translation_history.append({
                'source': text_to_translate,
                'target': result_text,
                'from': src_lang_name,
                'to': tgt_lang_name,
                'timestamp': datetime.now().strftime("%H:%M:%S")
            })
            
        except Exception as e:
            error_msg = f"❌ Translation error: {str(e)}"
            self.root.after(0, lambda msg=error_msg: self.translate_error(msg))

    def display_translation(self, text):
        self.target_text.delete(1.0, tk.END)
        self.target_text.insert(1.0, text)
        self.translate_btn.config(state='normal', text='🚀 Translate')

    def translate_error(self, message):
        self.target_text.delete(1.0, tk.END)
        self.target_text.insert(1.0, message)
        self.status_var.set("⚠️ Error occurred")
        self.translate_btn.config(state='normal', text='🚀 Translate')

    def show_error(self, message):
        self.status_var.set(message)
        self.target_text.delete(1.0, tk.END)
        self.target_text.insert(1.0, message)

    def swap_languages(self):
        src = self.source_lang.get()
        tgt = self.target_lang.get()
        
        if src == 'Auto-Detect':
            messagebox.showinfo("ℹ️ Info", "Cannot swap when Auto-Detect is selected")
            return
        
        self.source_lang.set(tgt)
        self.target_lang.set(src)
        
        src_text = self.source_text.get(1.0, tk.END)
        tgt_text = self.target_text.get(1.0, tk.END)
        self.source_text.delete(1.0, tk.END)
        self.target_text.delete(1.0, tk.END)
        self.source_text.insert(1.0, tgt_text)
        self.target_text.insert(1.0, src_text)

    def clear_text(self, text_widget):
        text_widget.delete(1.0, tk.END)
        if text_widget == self.source_text:
            self.char_count_label.config(text="Characters: 0")
        self.status_var.set("✓ Text cleared")

    def copy_text(self, text_widget):
        text = text_widget.get(1.0, tk.END).strip()
        if text:
            if HAS_PYPERCLIP:
                try:
                    import pyperclip as pc
                    pc.copy(text)
                    self.status_var.set("✓ Text copied to clipboard")
                except:
                    text_widget.clipboard_clear()
                    text_widget.clipboard_append(text)
                    self.status_var.set("✓ Text copied to clipboard")
            else:
                text_widget.clipboard_clear()
                text_widget.clipboard_append(text)
                self.status_var.set("✓ Text copied to clipboard")
        else:
            self.status_var.set("⚠️ No text to copy")

    def show_history(self):
        if not self.translation_history:
            messagebox.showinfo("📜 History", "No translation history available")
            return
        
        history_window = tk.Toplevel(self.root)
        history_window.title("Translation History 📜")
        history_window.geometry("700x500")
        history_window.configure(bg=COLORS["bg"])
        
        text_area = scrolledtext.ScrolledText(history_window, wrap=tk.WORD, 
                                           font=('Consolas', 9),
                                           bg=COLORS["input_bg"], fg=COLORS["input_text"])
        text_area.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        for i, item in enumerate(reversed(self.translation_history[-15:]), 1):
            text_area.insert(tk.END, f"\n{'='*60}\n")
            text_area.insert(tk.END, f"📌 Entry #{i} - {item.get('timestamp', 'N/A')}\n")
            text_area.insert(tk.END, f"{'-'*60}\n")
            text_area.insert(tk.END, f"🔤 {item['from']} → {item['to']}\n\n")
            text_area.insert(tk.END, f"📥 Source:\n{item['source']}\n\n")
            text_area.insert(tk.END, f"📤 Target:\n{item['target']}\n")
        
        text_area.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = LanguageTranslator(root)
    root.mainloop()
