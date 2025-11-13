"""
EPUB Translator - GUI module
Provides graphical user interface for translation
"""
import os

# Try to import tkinter for GUI (optional)
try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk, scrolledtext
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False
    print("Warning: tkinter not available. GUI will not be available.")

from .translator import EPUBTranslator, fetch_available_models
from .config import (
    DEFAULT_API_BASE,
    SUPPORTED_MODELS,
    SOURCE_LANGUAGES,
    TARGET_LANGUAGES,
)
from .prompts import DEFAULT_SYSTEM_PROMPT


class TranslatorGUI:
    """GUI for EPUB Translator"""
    
    def __init__(self, root):
        """Initialize GUI"""
        if not HAS_TKINTER:
            raise ImportError("tkinter is required for GUI functionality")
        
        self.root = root
        self.root.title("EPUB Translator")
        self.root.geometry("700x700")
        
        self.translator = None
        self.input_file = None
        self.output_file = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Main frame with scrollbar
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        current_row = 0
        
        # API Configuration
        ttk.Label(main_frame, text="API Configuration", font=('Arial', 12, 'bold')).grid(
            row=current_row, column=0, columnspan=3, pady=(0, 10), sticky=tk.W
        )
        current_row += 1
        
        ttk.Label(main_frame, text="API Key:").grid(row=current_row, column=0, sticky=tk.W, pady=5)
        self.api_key_entry = ttk.Entry(main_frame, width=50, show="*")
        self.api_key_entry.grid(row=current_row, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        current_row += 1
        
        ttk.Label(main_frame, text="API Base URL:").grid(row=current_row, column=0, sticky=tk.W, pady=5)
        self.api_base_entry = ttk.Entry(main_frame, width=50)
        self.api_base_entry.insert(0, DEFAULT_API_BASE)
        self.api_base_entry.grid(row=current_row, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        current_row += 1
        
        # Model selection
        ttk.Label(main_frame, text="Model:").grid(row=current_row, column=0, sticky=tk.W, pady=5)
        self.model_var = tk.StringVar(value=SUPPORTED_MODELS[0])
        self.model_combo = ttk.Combobox(main_frame, textvariable=self.model_var, width=37)
        self.model_combo['values'] = SUPPORTED_MODELS
        self.model_combo.grid(row=current_row, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Add button to fetch models from API
        self.fetch_models_button = ttk.Button(main_frame, text="Fetch Models", command=self.fetch_models)
        self.fetch_models_button.grid(row=current_row, column=2, sticky=tk.E, pady=5, padx=(5, 0))
        current_row += 1
        
        # Custom prompt section
        ttk.Label(main_frame, text="Translation Prompt", font=('Arial', 12, 'bold')).grid(
            row=current_row, column=0, columnspan=3, pady=(20, 10), sticky=tk.W
        )
        current_row += 1
        
        ttk.Label(main_frame, text="Custom Prompt:").grid(row=current_row, column=0, sticky=tk.NW, pady=5)
        
        # Frame for prompt text and info
        prompt_frame = ttk.Frame(main_frame)
        prompt_frame.grid(row=current_row, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.prompt_text = scrolledtext.ScrolledText(prompt_frame, width=50, height=4, wrap=tk.WORD)
        self.prompt_text.insert(1.0, DEFAULT_SYSTEM_PROMPT)
        self.prompt_text.pack(fill=tk.BOTH, expand=True)
        
        prompt_info = ttk.Label(
            prompt_frame,
            text="Use {target_language} as placeholder for target language",
            font=('Arial', 8),
            foreground='gray'
        )
        prompt_info.pack(anchor=tk.W, pady=(2, 0))
        
        current_row += 1
        
        # Language selection
        ttk.Label(main_frame, text="Translation Settings", font=('Arial', 12, 'bold')).grid(
            row=current_row, column=0, columnspan=3, pady=(20, 10), sticky=tk.W
        )
        current_row += 1
        
        ttk.Label(main_frame, text="Source Language:").grid(row=current_row, column=0, sticky=tk.W, pady=5)
        self.source_lang = tk.StringVar(value="auto")
        source_lang_combo = ttk.Combobox(main_frame, textvariable=self.source_lang, width=20)
        source_lang_combo['values'] = SOURCE_LANGUAGES
        source_lang_combo.grid(row=current_row, column=1, sticky=tk.W, pady=5)
        current_row += 1
        
        ttk.Label(main_frame, text="Target Language:").grid(row=current_row, column=0, sticky=tk.W, pady=5)
        self.target_lang = tk.StringVar(value="zh")
        target_lang_combo = ttk.Combobox(main_frame, textvariable=self.target_lang, width=20)
        target_lang_combo['values'] = TARGET_LANGUAGES
        target_lang_combo.grid(row=current_row, column=1, sticky=tk.W, pady=5)
        current_row += 1
        
        # File selection
        ttk.Label(main_frame, text="File Selection", font=('Arial', 12, 'bold')).grid(
            row=current_row, column=0, columnspan=3, pady=(20, 10), sticky=tk.W
        )
        current_row += 1
        
        ttk.Label(main_frame, text="Input EPUB:").grid(row=current_row, column=0, sticky=tk.W, pady=5)
        self.input_label = ttk.Label(main_frame, text="No file selected", foreground="gray")
        self.input_label.grid(row=current_row, column=1, sticky=tk.W, pady=5)
        ttk.Button(main_frame, text="Browse...", command=self.select_input_file).grid(
            row=current_row, column=2, sticky=tk.E, pady=5
        )
        current_row += 1
        
        ttk.Label(main_frame, text="Output EPUB:").grid(row=current_row, column=0, sticky=tk.W, pady=5)
        self.output_label = ttk.Label(main_frame, text="No file selected", foreground="gray")
        self.output_label.grid(row=current_row, column=1, sticky=tk.W, pady=5)
        ttk.Button(main_frame, text="Browse...", command=self.select_output_file).grid(
            row=current_row, column=2, sticky=tk.E, pady=5
        )
        current_row += 1
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame, variable=self.progress_var, maximum=100, length=600
        )
        self.progress_bar.grid(row=current_row, column=0, columnspan=3, pady=20, sticky=(tk.W, tk.E))
        current_row += 1
        
        self.status_label = ttk.Label(main_frame, text="Ready", foreground="blue")
        self.status_label.grid(row=current_row, column=0, columnspan=3, pady=5)
        current_row += 1
        
        # Translate button
        self.translate_button = ttk.Button(
            main_frame, text="Translate", command=self.start_translation
        )
        self.translate_button.grid(row=current_row, column=0, columnspan=3, pady=20)
        
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
    
    def fetch_models(self):
        """Fetch available models from the API"""
        # Validate API key is entered
        api_key = self.api_key_entry.get()
        if not api_key:
            messagebox.showwarning("Warning", "Please enter your API key first")
            return
        
        # Get API base URL
        api_base = self.api_base_entry.get() or DEFAULT_API_BASE
        
        # Disable button and show loading state
        self.fetch_models_button.config(state='disabled', text="Fetching...")
        self.root.update_idletasks()
        
        # Fetch models in a separate thread to keep GUI responsive
        import threading
        
        def fetch_and_update():
            try:
                models = fetch_available_models(api_key, api_base)
                
                # Update UI from main thread
                self.root.after(0, self.update_models_list, models)
            except Exception as e:
                self.root.after(0, self.fetch_models_error, str(e))
        
        thread = threading.Thread(target=fetch_and_update)
        thread.daemon = True
        thread.start()
    
    def update_models_list(self, models):
        """Update the models combobox with fetched models"""
        # Re-enable button
        self.fetch_models_button.config(state='normal', text="Fetch Models")
        
        if models:
            # Update combobox with fetched models
            self.model_combo['values'] = models
            
            # Try to keep current selection if it exists in new list
            current_model = self.model_var.get()
            if current_model not in models and models:
                # Set to first model if current selection is not in the list
                self.model_var.set(models[0])
            
            messagebox.showinfo("Success", f"Successfully fetched {len(models)} models from API")
        else:
            # Fall back to hardcoded models
            self.model_combo['values'] = SUPPORTED_MODELS
            messagebox.showwarning(
                "Warning", 
                "Failed to fetch models from API. Using default model list.\n"
                "Please check your API key and base URL."
            )
    
    def fetch_models_error(self, error_msg):
        """Handle errors when fetching models"""
        self.fetch_models_button.config(state='normal', text="Fetch Models")
        messagebox.showerror("Error", f"Failed to fetch models: {error_msg}")
    
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
        
        # Get custom prompt
        custom_prompt = self.prompt_text.get(1.0, tk.END).strip()
        if custom_prompt == DEFAULT_SYSTEM_PROMPT.strip():
            custom_prompt = None  # Use default
        
        # Initialize translator
        try:
            self.translator = EPUBTranslator(
                api_key=self.api_key_entry.get(),
                api_base=self.api_base_entry.get(),
                model=self.model_var.get(),
                custom_prompt=custom_prompt
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


def start_gui():
    """Start the GUI application"""
    if not HAS_TKINTER:
        print("Error: tkinter is not available. Cannot start GUI.")
        print("Please install tkinter or use the programmatic API.")
        print("See example_usage.py for non-GUI usage.")
        return 1
    
    root = tk.Tk()
    app = TranslatorGUI(root)
    root.mainloop()
    return 0
