"""
EPUB Translator - Main application module
Translates EPUB documents using OpenAI-compatible LLM APIs
"""
import os
import re
from typing import List, Tuple, Optional
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import openai
from openai import OpenAI

# Try to import tkinter for GUI (optional)
try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False
    print("Warning: tkinter not available. GUI will not be available.")


class EPUBTranslator:
    """Main class for EPUB translation operations"""
    
    def __init__(self, api_key: str, api_base: str = "https://api.openai.com/v1"):
        """
        Initialize the translator
        
        Args:
            api_key: OpenAI API key or compatible API key
            api_base: API base URL (default: OpenAI)
        """
        self.client = OpenAI(api_key=api_key, base_url=api_base)
        self.source_lang = "auto"
        self.target_lang = "zh"  # Default to Chinese
        
    def parse_epub(self, epub_path: str) -> Tuple[epub.EpubBook, List[Tuple[epub.EpubItem, BeautifulSoup]]]:
        """
        Parse EPUB file and extract content
        
        Args:
            epub_path: Path to the EPUB file
            
        Returns:
            Tuple of (original book object, list of (item, parsed_content) tuples)
        """
        book = epub.read_epub(epub_path)
        documents = []
        
        # Extract all document items (HTML/XHTML)
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                content = item.get_content()
                soup = BeautifulSoup(content, 'html.parser')
                documents.append((item, soup))
        
        return book, documents
    
    def extract_text_segments(self, soup: BeautifulSoup) -> List[Tuple[str, any]]:
        """
        Extract text segments from parsed HTML
        
        Args:
            soup: BeautifulSoup parsed HTML
            
        Returns:
            List of (text, element) tuples
        """
        segments = []
        
        # Find all text-containing elements
        for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'td', 'th', 'div', 'span']):
            # Get direct text content (not from children)
            if element.string:
                text = element.string.strip()
                if text:
                    segments.append((text, element))
            else:
                # Handle elements with mixed content
                for content in element.contents:
                    if isinstance(content, str):
                        text = content.strip()
                        if text:
                            segments.append((text, element))
        
        return segments
    
    def translate_text(self, text: str, progress_callback=None) -> str:
        """
        Translate text using LLM API
        
        Args:
            text: Text to translate
            progress_callback: Optional callback for progress updates
            
        Returns:
            Translated text
        """
        if not text.strip():
            return text
        
        try:
            system_message = f"You are a professional translator. Translate the following text to {self.get_language_name(self.target_lang)}. Only return the translated text without any additional explanation or notes."
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": text}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            translated = response.choices[0].message.content.strip()
            
            if progress_callback:
                progress_callback()
            
            return translated
            
        except Exception as e:
            print(f"Translation error: {e}")
            return text  # Return original text on error
    
    def get_language_name(self, lang_code: str) -> str:
        """Get full language name from code"""
        lang_map = {
            'zh': 'Chinese',
            'en': 'English',
            'ja': 'Japanese',
            'ko': 'Korean',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'ru': 'Russian',
            'ar': 'Arabic'
        }
        return lang_map.get(lang_code, lang_code)
    
    def translate_document(self, item: epub.EpubItem, soup: BeautifulSoup, 
                          progress_callback=None) -> str:
        """
        Translate a document while preserving structure
        
        Args:
            item: EPUB item
            soup: Parsed HTML content
            progress_callback: Optional callback for progress updates
            
        Returns:
            Translated HTML content
        """
        segments = self.extract_text_segments(soup)
        
        for text, element in segments:
            translated = self.translate_text(text, progress_callback)
            
            # Replace text in element
            if element.string:
                element.string.replace_with(translated)
            else:
                # Handle mixed content
                for i, content in enumerate(element.contents):
                    if isinstance(content, str) and content.strip() == text:
                        element.contents[i].replace_with(translated)
        
        return str(soup)
    
    def adjust_epub_metadata(self, book: epub.EpubBook, target_lang: str):
        """
        Adjust EPUB metadata for target language
        
        Args:
            book: EPUB book object
            target_lang: Target language code
        """
        # Set language
        book.set_language(target_lang)
        
        # Update title
        original_title = book.get_metadata('DC', 'title')
        if original_title:
            book.set_title(f"{original_title[0][0]} (Translated)")
        
        # Add CSS for text direction and fonts
        if target_lang in ['ar', 'he', 'fa']:  # RTL languages
            direction = 'rtl'
        else:
            direction = 'ltr'
        
        # Define appropriate fonts
        font_family = self.get_font_for_language(target_lang)
        
        # Create or update CSS
        css = f"""
        body {{
            direction: {direction};
            font-family: {font_family};
        }}
        p, div, span {{
            direction: {direction};
        }}
        """
        
        # Add CSS file
        css_item = epub.EpubItem(
            uid="style_translation",
            file_name="style/translation.css",
            media_type="text/css",
            content=css.encode('utf-8')
        )
        book.add_item(css_item)
    
    def get_font_for_language(self, lang_code: str) -> str:
        """Get appropriate font family for language"""
        font_map = {
            'zh': "'Noto Sans SC', 'Microsoft YaHei', SimSun, sans-serif",
            'ja': "'Noto Sans JP', 'Yu Gothic', 'MS Gothic', sans-serif",
            'ko': "'Noto Sans KR', 'Malgun Gothic', sans-serif",
            'ar': "'Noto Sans Arabic', 'Arial', sans-serif",
            'he': "'Noto Sans Hebrew', 'Arial', sans-serif",
            'th': "'Noto Sans Thai', 'Leelawadee', sans-serif",
            'default': "'Noto Sans', Arial, sans-serif"
        }
        return font_map.get(lang_code, font_map['default'])
    
    def _fix_toc_links(self, book: epub.EpubBook):
        """
        Fix TOC links to have UIDs - required for ebooklib to write properly
        
        Args:
            book: EPUB book object
        """
        if not book.toc:
            return
        
        def fix_link(item, index=0):
            """Recursively fix links in TOC"""
            if isinstance(item, epub.Link):
                # If uid is None, generate one
                if item.uid is None:
                    item.uid = f"toc_link_{index}"
                return index + 1
            elif isinstance(item, tuple) or isinstance(item, list):
                for sub_item in item:
                    index = fix_link(sub_item, index)
                return index
            else:
                # It's likely an EpubHtml or similar item that already has a uid
                return index
        
        # Process TOC items
        if isinstance(book.toc, (list, tuple)):
            index = 0
            for item in book.toc:
                index = fix_link(item, index)
    
    def translate_epub(self, input_path: str, output_path: str, 
                       progress_callback=None, total_callback=None) -> bool:
        """
        Translate entire EPUB file
        
        Args:
            input_path: Input EPUB file path
            output_path: Output EPUB file path
            progress_callback: Callback for progress updates (called after each segment)
            total_callback: Callback to set total number of documents
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Parse EPUB
            book, documents = self.parse_epub(input_path)
            
            if total_callback:
                total_callback(len(documents))
            
            # Translate each document
            for item, soup in documents:
                translated_content = self.translate_document(item, soup, progress_callback)
                item.set_content(translated_content.encode('utf-8'))
            
            # Adjust metadata for target language
            self.adjust_epub_metadata(book, self.target_lang)
            
            # Fix TOC links to have UIDs (required for writing)
            self._fix_toc_links(book)
            
            # Write translated EPUB
            epub.write_epub(output_path, book)
            
            return True
            
        except Exception as e:
            print(f"Translation failed: {e}")
            import traceback
            traceback.print_exc()
            return False


class TranslatorGUI:
    """GUI for EPUB Translator"""
    
    def __init__(self, root):
        """Initialize GUI"""
        if not HAS_TKINTER:
            raise ImportError("tkinter is required for GUI functionality")
        
        self.root = root
        self.root.title("EPUB Translator")
        self.root.geometry("600x500")
        
        self.translator = None
        self.input_file = None
        self.output_file = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # API Configuration
        ttk.Label(main_frame, text="API Configuration", font=('Arial', 12, 'bold')).grid(
            row=0, column=0, columnspan=3, pady=(0, 10), sticky=tk.W
        )
        
        ttk.Label(main_frame, text="API Key:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.api_key_entry = ttk.Entry(main_frame, width=50, show="*")
        self.api_key_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(main_frame, text="API Base URL:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.api_base_entry = ttk.Entry(main_frame, width=50)
        self.api_base_entry.insert(0, "https://api.openai.com/v1")
        self.api_base_entry.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Language selection
        ttk.Label(main_frame, text="Translation Settings", font=('Arial', 12, 'bold')).grid(
            row=3, column=0, columnspan=3, pady=(20, 10), sticky=tk.W
        )
        
        ttk.Label(main_frame, text="Source Language:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.source_lang = tk.StringVar(value="auto")
        source_lang_combo = ttk.Combobox(main_frame, textvariable=self.source_lang, width=20)
        source_lang_combo['values'] = ('auto', 'en', 'ja', 'ko', 'zh', 'es', 'fr', 'de', 'ru')
        source_lang_combo.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(main_frame, text="Target Language:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.target_lang = tk.StringVar(value="zh")
        target_lang_combo = ttk.Combobox(main_frame, textvariable=self.target_lang, width=20)
        target_lang_combo['values'] = ('zh', 'en', 'ja', 'ko', 'es', 'fr', 'de', 'ru', 'ar')
        target_lang_combo.grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # File selection
        ttk.Label(main_frame, text="File Selection", font=('Arial', 12, 'bold')).grid(
            row=6, column=0, columnspan=3, pady=(20, 10), sticky=tk.W
        )
        
        ttk.Label(main_frame, text="Input EPUB:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.input_label = ttk.Label(main_frame, text="No file selected", foreground="gray")
        self.input_label.grid(row=7, column=1, sticky=tk.W, pady=5)
        ttk.Button(main_frame, text="Browse...", command=self.select_input_file).grid(
            row=7, column=2, sticky=tk.E, pady=5
        )
        
        ttk.Label(main_frame, text="Output EPUB:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.output_label = ttk.Label(main_frame, text="No file selected", foreground="gray")
        self.output_label.grid(row=8, column=1, sticky=tk.W, pady=5)
        ttk.Button(main_frame, text="Browse...", command=self.select_output_file).grid(
            row=8, column=2, sticky=tk.E, pady=5
        )
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame, variable=self.progress_var, maximum=100, length=500
        )
        self.progress_bar.grid(row=9, column=0, columnspan=3, pady=20, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(main_frame, text="Ready", foreground="blue")
        self.status_label.grid(row=10, column=0, columnspan=3, pady=5)
        
        # Translate button
        self.translate_button = ttk.Button(
            main_frame, text="Translate", command=self.start_translation
        )
        self.translate_button.grid(row=11, column=0, columnspan=3, pady=20)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
    
    def select_input_file(self):
        """Open file dialog to select input EPUB"""
        filename = filedialog.askopenfilename(
            title="Select Input EPUB",
            filetypes=[("EPUB files", "*.epub"), ("All files", "*.*")]
        )
        if filename:
            self.input_file = filename
            self.input_label.config(text=os.path.basename(filename), foreground="black")
            
            # Auto-suggest output filename
            if not self.output_file:
                base_name = os.path.splitext(filename)[0]
                suggested_output = f"{base_name}_translated.epub"
                self.output_file = suggested_output
                self.output_label.config(text=os.path.basename(suggested_output), foreground="black")
    
    def select_output_file(self):
        """Open file dialog to select output EPUB"""
        filename = filedialog.asksaveasfilename(
            title="Save Translated EPUB As",
            defaultextension=".epub",
            filetypes=[("EPUB files", "*.epub"), ("All files", "*.*")]
        )
        if filename:
            self.output_file = filename
            self.output_label.config(text=os.path.basename(filename), foreground="black")
    
    def start_translation(self):
        """Start the translation process"""
        # Validate inputs
        if not self.api_key_entry.get():
            messagebox.showerror("Error", "Please enter your API key")
            return
        
        if not self.input_file:
            messagebox.showerror("Error", "Please select an input EPUB file")
            return
        
        if not self.output_file:
            messagebox.showerror("Error", "Please select an output file location")
            return
        
        # Initialize translator
        try:
            self.translator = EPUBTranslator(
                api_key=self.api_key_entry.get(),
                api_base=self.api_base_entry.get()
            )
            self.translator.source_lang = self.source_lang.get()
            self.translator.target_lang = self.target_lang.get()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize translator: {e}")
            return
        
        # Disable button during translation
        self.translate_button.config(state='disabled')
        self.status_label.config(text="Translating...", foreground="blue")
        
        # Start translation in a separate thread to keep GUI responsive
        import threading
        thread = threading.Thread(target=self.perform_translation)
        thread.daemon = True
        thread.start()
    
    def perform_translation(self):
        """Perform the actual translation"""
        self.total_segments = 0
        self.completed_segments = 0
        
        def set_total(total):
            self.total_segments = total
        
        def update_progress():
            self.completed_segments += 1
            if self.total_segments > 0:
                progress = (self.completed_segments / self.total_segments) * 100
                self.progress_var.set(progress)
                self.root.update_idletasks()
        
        success = self.translator.translate_epub(
            self.input_file,
            self.output_file,
            progress_callback=update_progress,
            total_callback=set_total
        )
        
        # Update UI from main thread
        self.root.after(0, self.translation_complete, success)
    
    def translation_complete(self, success: bool):
        """Handle translation completion"""
        self.translate_button.config(state='normal')
        
        if success:
            self.status_label.config(text="Translation completed successfully!", foreground="green")
            self.progress_var.set(100)
            messagebox.showinfo("Success", f"Translation completed!\nOutput saved to:\n{self.output_file}")
        else:
            self.status_label.config(text="Translation failed", foreground="red")
            messagebox.showerror("Error", "Translation failed. Please check the console for details.")


def main():
    """Main entry point"""
    if not HAS_TKINTER:
        print("Error: tkinter is not available. Cannot start GUI.")
        print("Please install tkinter or use the programmatic API.")
        print("See example_usage.py for non-GUI usage.")
        return 1
    
    root = tk.Tk()
    app = TranslatorGUI(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
