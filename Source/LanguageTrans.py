import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from googletrans import Translator, LANGUAGES
import ttkbootstrap as ttk
from threading import Thread
import asyncio

try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False

class LanguageTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Language Translator")
        self.root.geometry("700x900")
        self.root.minsize(600, 800)
        self.translator = Translator()
        self.translation_history = []
        
        style = ttk.Style("darkly")
        
        self.lang_dict = {v.capitalize(): k for k, v in LANGUAGES.items()}
        self.lang_names = list(self.lang_dict.keys())
        self.lang_names.sort()
        
        main_frame = ttk.Frame(root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="Language Translator", font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=(0, 10))
        
        lang_frame = ttk.Frame(main_frame)
        lang_frame.pack(fill=tk.X, pady=(0, 10))
        
        source_label = ttk.Label(lang_frame, text="From:", font=('Helvetica', 9, 'bold'))
        source_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.source_lang = ttk.Combobox(lang_frame, values=['Auto-Detect'] + self.lang_names, width=20, state='readonly')
        self.source_lang.set('Auto-Detect')
        self.source_lang.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(lang_frame, text="⇄", width=4, command=self.swap_languages, style='secondary.TButton').pack(side=tk.LEFT, padx=10)
        
        target_label = ttk.Label(lang_frame, text="To:", font=('Helvetica', 9, 'bold'))
        target_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.target_lang = ttk.Combobox(lang_frame, values=self.lang_names, width=20, state='readonly')
        self.target_lang.set('Spanish')
        self.target_lang.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(main_frame, text="Source Text", font=('Helvetica', 10, 'bold')).pack(anchor=tk.W, pady=(5, 0))
        
        input_header = ttk.Frame(main_frame)
        input_header.pack(fill=tk.X, pady=(3, 5))
        
        self.char_count_label = ttk.Label(input_header, text="Characters: 0", font=('Helvetica', 8))
        self.char_count_label.pack(side=tk.LEFT)
        
        ttk.Button(input_header, text="Clear", command=lambda: self.clear_text(self.source_text), width=7, style='warning.TButton').pack(side=tk.RIGHT, padx=2)
        ttk.Button(input_header, text="Copy", command=lambda: self.copy_text(self.source_text), width=7, style='info.TButton').pack(side=tk.RIGHT, padx=2)
        
        self.source_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=12, font=('Helvetica', 10))
        self.source_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.source_text.bind('<KeyRelease>', self.update_char_count)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.translate_btn = ttk.Button(button_frame, text="Translate", command=self.translate_threaded, style='primary.TButton')
        self.translate_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="History", command=self.show_history, style='secondary.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Label(main_frame, text="Translation", font=('Helvetica', 10, 'bold')).pack(anchor=tk.W)
        
        output_header = ttk.Frame(main_frame)
        output_header.pack(fill=tk.X, pady=(3, 5))
        
        ttk.Button(output_header, text="Clear", command=lambda: self.clear_text(self.target_text), width=7, style='warning.TButton').pack(side=tk.RIGHT, padx=2)
        ttk.Button(output_header, text="Copy", command=lambda: self.copy_text(self.target_text), width=7, style='info.TButton').pack(side=tk.RIGHT, padx=2)
        
        self.target_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=12, font=('Helvetica', 10))
        self.target_text.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, font=('Helvetica', 8), foreground='gray')
        self.status_label.pack(side=tk.BOTTOM)

    def update_char_count(self, event=None):
        text = self.source_text.get(1.0, tk.END).strip()
        self.char_count_label.config(text=f"Characters: {len(text)}")

    def translate_threaded(self):
        self.translate_btn.config(state='disabled', text='Translating...')
        self.status_var.set("Translating...")
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
        
        if not text_to_translate:
            self.root.after(0, lambda: self.translate_error("Please enter text to translate"))
            return
        
        try:
            translator = Translator()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            translation = loop.run_until_complete(translator.translate(text_to_translate, src=src_lang, dest=tgt_lang))
            loop.close()
            
            result_text = getattr(translation, 'text', str(translation))
            
            self.root.after(0, lambda: self.display_translation(result_text))
            
            if src_lang == 'auto':
                detected_lang = getattr(translation, 'src', 'unknown')
                detected_name = LANGUAGES.get(detected_lang, 'Unknown').capitalize()
                self.root.after(0, lambda: self.status_var.set(f"Detected: {detected_name} → {tgt_lang_name}"))
            else:
                self.root.after(0, lambda: self.status_var.set(f"{src_lang_name} → {tgt_lang_name}"))
            
            self.translation_history.append({
                'source': text_to_translate,
                'target': result_text,
                'from': src_lang_name,
                'to': tgt_lang_name
            })
            
        except Exception as e:
            error_msg = f"Translation failed: {str(e)}"
            self.root.after(0, lambda msg=error_msg: self.translate_error(msg))

    def display_translation(self, text):
        self.target_text.delete(1.0, tk.END)
        self.target_text.insert(1.0, text)
        self.translate_btn.config(state='normal', text='Translate')

    def translate_error(self, message):
        self.target_text.delete(1.0, tk.END)
        self.target_text.insert(1.0, message)
        self.status_var.set("Error occurred")
        self.translate_btn.config(state='normal', text='Translate')

    def swap_languages(self):
        src = self.source_lang.get()
        tgt = self.target_lang.get()
        
        if src == 'Auto-Detect':
            messagebox.showinfo("Info", "Cannot swap with Auto-Detect selected")
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

    def copy_text(self, text_widget):
        text = text_widget.get(1.0, tk.END).strip()
        if text:
            if HAS_PYPERCLIP:
                pyperclip.copy(text)
                self.status_var.set("Text copied to clipboard")
            else:
                text_widget.clipboard_clear()
                text_widget.clipboard_append(text)
                self.status_var.set("Text copied to clipboard")
        else:
            self.status_var.set("No text to copy")

    def show_history(self):
        if not self.translation_history:
            messagebox.showinfo("History", "No translation history available")
            return
        
        history_window = tk.Toplevel(self.root)
        history_window.title("Translation History")
        history_window.geometry("600x400")
        
        text_area = scrolledtext.ScrolledText(history_window, wrap=tk.WORD, font=('Helvetica', 10))
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for i, item in enumerate(self.translation_history[-10:], 1):
            text_area.insert(tk.END, f"\n{'='*50}\n")
            text_area.insert(tk.END, f"{i}. {item['from']} → {item['to']}\n")
            text_area.insert(tk.END, f"{'-'*50}\n")
            text_area.insert(tk.END, f"Source: {item['source'][:100]}...\n")
            text_area.insert(tk.END, f"Target: {item['target'][:100]}...\n")
        
        text_area.config(state='disabled')

if __name__ == "__main__":
    root = ttk.Window()
    app = LanguageTranslator(root)
    root.mainloop()
