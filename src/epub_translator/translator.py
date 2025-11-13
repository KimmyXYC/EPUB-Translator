"""
EPUB Translator - Core translation module
Handles EPUB parsing, translation, and output generation
"""
import os
from typing import List, Tuple, Optional
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from openai import OpenAI

from .config import (
    DEFAULT_API_BASE,
    DEFAULT_MODEL,
    LANGUAGE_NAMES,
    LANGUAGE_FONTS,
    RTL_LANGUAGES,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS,
)
from .prompts import get_system_prompt


class EPUBTranslator:
    """Main class for EPUB translation operations"""
    
    def __init__(
        self,
        api_key: str,
        api_base: str = DEFAULT_API_BASE,
        model: str = DEFAULT_MODEL,
        custom_prompt: str = None
    ):
        """
        Initialize the translator
        
        Args:
            api_key: OpenAI API key or compatible API key
            api_base: API base URL (default: OpenAI)
            model: Model name to use for translation (default: gpt-3.5-turbo)
            custom_prompt: Optional custom system prompt for translation
        """
        self.client = OpenAI(api_key=api_key, base_url=api_base)
        self.model = model
        self.custom_prompt = custom_prompt
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
            target_language_name = self.get_language_name(self.target_lang)
            system_message = get_system_prompt(target_language_name, self.custom_prompt)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": text}
                ],
                temperature=DEFAULT_TEMPERATURE,
                max_tokens=DEFAULT_MAX_TOKENS
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
        return LANGUAGE_NAMES.get(lang_code, lang_code)
    
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
        if target_lang in RTL_LANGUAGES:
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
        return LANGUAGE_FONTS.get(lang_code, LANGUAGE_FONTS['default'])
    
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
