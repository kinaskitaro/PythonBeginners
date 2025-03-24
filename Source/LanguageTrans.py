import tkinter as tk
from tkinter import ttk, scrolledtext
from googletrans import Translator, LANGUAGES
import ttkbootstrap as ttk
import asyncio  # Import asyncio for handling async calls

class LanguageTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Language Translator")
        self.root.geometry("800x700")  # Increased height from 600 to 700
        self.translator = Translator()
        
        # Style configuration
        style = ttk.Style("darkly")
        
        # Main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Language selection
        lang_frame = ttk.Frame(main_frame)
        lang_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Source language
        self.source_lang = ttk.Combobox(
            lang_frame, 
            values=[lang.capitalize() for lang in LANGUAGES.values()],  # Capitalize first character
            width=20
        )
        self.source_lang.set('English')  # Updated to match capitalization
        self.source_lang.pack(side=tk.LEFT, padx=10)
        
        # Swap button
        ttk.Button(lang_frame, text="⇄", width=3, command=self.swap_languages).pack(side=tk.LEFT, padx=10)
        
        # Target language
        self.target_lang = ttk.Combobox(
            lang_frame, 
            values=[lang.capitalize() for lang in LANGUAGES.values()],  # Capitalize first character
            width=20
        )
        self.target_lang.set('Spanish')  # Updated to match capitalization
        self.target_lang.pack(side=tk.LEFT, padx=10)
        
        # Text areas
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        # Source text
        self.source_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=10)
        self.source_text.pack(fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Target text
        self.target_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=10)
        self.target_text.pack(fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Translate button
        self.translate_btn = ttk.Button(main_frame, text="Translate", command=self.translate, style='primary.TButton')
        self.translate_btn.pack(pady=10)

    def translate(self):
        async def perform_translation():
            src_lang = [k for k, v in LANGUAGES.items() if v == self.source_lang.get()][0]
            tgt_lang = [k for k, v in LANGUAGES.items() if v == self.target_lang.get()][0]
            
            try:
                translation = await self.translator.translate(
                    self.source_text.get(1.0, tk.END),
                    src=src_lang,
                    dest=tgt_lang
                )
                self.target_text.delete(1.0, tk.END)
                self.target_text.insert(1.0, translation.text)
            except Exception as e:
                self.target_text.delete(1.0, tk.END)
                self.target_text.insert(1.0, "Error: Could not translate text")

        # Run the async function
        asyncio.run(perform_translation())

    def swap_languages(self):
        src = self.source_lang.get()
        tgt = self.target_lang.get()
        self.source_lang.set(tgt)
        self.target_lang.set(src)
        
        src_text = self.source_text.get(1.0, tk.END)
        tgt_text = self.target_text.get(1.0, tk.END)
        self.source_text.delete(1.0, tk.END)
        self.target_text.delete(1.0, tk.END)
        self.source_text.insert(1.0, tgt_text)
        self.target_text.insert(1.0, src_text)

if __name__ == "__main__":
    root = ttk.Window()
    app = LanguageTranslator(root)
    root.mainloop()
