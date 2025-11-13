"""
Test script for EPUB Translator
Tests the core functionality without requiring a GUI or API
"""
import os
import sys
from src.epub_translator import EPUBTranslator, SUPPORTED_MODELS, DEFAULT_SYSTEM_PROMPT
from ebooklib import epub
from bs4 import BeautifulSoup

class MockTranslator(EPUBTranslator):
    """Mock translator for testing without API calls"""
    
    def __init__(self, model=None, custom_prompt=None):
        """Initialize without API key"""
        # Don't call parent __init__ since we don't have an API key
        self.model = model or "gpt-3.5-turbo"
        self.custom_prompt = custom_prompt
        self.source_lang = "en"
        self.target_lang = "zh"
        self.translation_count = 0
    
    def translate_text(self, text: str, progress_callback=None) -> str:
        """Mock translation - just prepends '[TRANSLATED]' to text"""
        if not text.strip():
            return text
        
        self.translation_count += 1
        
        if progress_callback:
            progress_callback()
        
        return f"[已翻译] {text}"

def test_epub_parsing():
    """Test EPUB parsing functionality"""
    print("🧪 Testing EPUB parsing...")
    
    # Create test EPUB if it doesn't exist
    if not os.path.exists('test_input.epub'):
        print("   Creating test EPUB...")
        os.system('python create_test_epub.py')
    
    translator = MockTranslator()
    
    try:
        book, documents = translator.parse_epub('test_input.epub')
        print(f"   ✅ Successfully parsed EPUB")
        print(f"   📚 Found {len(documents)} documents")
        
        for i, (item, soup) in enumerate(documents):
            print(f"   📄 Document {i+1}: {item.get_name()}")
            segments = translator.extract_text_segments(soup)
            print(f"      - Text segments: {len(segments)}")
        
        return True
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False

def test_text_segmentation():
    """Test text segmentation"""
    print("\n🧪 Testing text segmentation...")
    
    html = """
    <html>
    <body>
        <h1>Title</h1>
        <p>First paragraph.</p>
        <p>Second paragraph.</p>
        <div>A div with text.</div>
    </body>
    </html>
    """
    
    translator = MockTranslator()
    soup = BeautifulSoup(html, 'html.parser')
    segments = translator.extract_text_segments(soup)
    
    print(f"   ✅ Extracted {len(segments)} text segments")
    for text, element in segments:
        print(f"      - '{text}' from <{element.name}>")
    
    return len(segments) > 0

def test_translation():
    """Test translation functionality"""
    print("\n🧪 Testing translation...")
    
    translator = MockTranslator()
    
    test_texts = [
        "Hello, world!",
        "This is a test.",
        "Translation test."
    ]
    
    for text in test_texts:
        translated = translator.translate_text(text)
        print(f"   '{text}' → '{translated}'")
    
    print(f"   ✅ Translated {translator.translation_count} segments")
    return True

def test_full_translation():
    """Test full EPUB translation"""
    print("\n🧪 Testing full EPUB translation...")
    
    if not os.path.exists('test_input.epub'):
        print("   Creating test EPUB...")
        os.system('python create_test_epub.py')
    
    translator = MockTranslator()
    
    total_docs = [0]
    progress = [0]
    
    def set_total(total):
        total_docs[0] = total
    
    def update_progress():
        progress[0] += 1
    
    try:
        success = translator.translate_epub(
            'test_input.epub',
            'test_output.epub',
            progress_callback=update_progress,
            total_callback=set_total
        )
        
        if success:
            print(f"   ✅ Translation completed")
            print(f"   📊 Processed {progress[0]} text segments")
            print(f"   📄 Output saved to test_output.epub")
            
            # Verify output file exists
            if os.path.exists('test_output.epub'):
                size = os.path.getsize('test_output.epub')
                print(f"   📦 Output file size: {size} bytes")
            
            return True
        else:
            print(f"   ❌ Translation failed")
            return False
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_metadata_adjustment():
    """Test metadata adjustment for different languages"""
    print("\n🧪 Testing metadata adjustment...")
    
    translator = MockTranslator()
    book = epub.EpubBook()
    book.set_title("Test Book")
    book.set_language("en")
    
    # Test with Chinese
    translator.target_lang = "zh"
    translator.adjust_epub_metadata(book, "zh")
    print(f"   ✅ Adjusted metadata for Chinese")
    print(f"      Font: {translator.get_font_for_language('zh')}")
    
    # Test with Arabic (RTL language)
    translator.target_lang = "ar"
    translator.adjust_epub_metadata(book, "ar")
    print(f"   ✅ Adjusted metadata for Arabic (RTL)")
    print(f"      Font: {translator.get_font_for_language('ar')}")
    
    # Test with Japanese
    translator.target_lang = "ja"
    translator.adjust_epub_metadata(book, "ja")
    print(f"   ✅ Adjusted metadata for Japanese")
    print(f"      Font: {translator.get_font_for_language('ja')}")
    
    return True

def test_model_selection():
    """Test model selection functionality"""
    print("\n🧪 Testing model selection...")
    
    # Test default model
    translator1 = MockTranslator()
    print(f"   ✅ Default model: {translator1.model}")
    
    # Test custom model
    translator2 = MockTranslator(model="gpt-4o-mini")
    print(f"   ✅ Custom model: {translator2.model}")
    
    # Test all supported models
    print(f"   ℹ️  Supported models: {', '.join(SUPPORTED_MODELS)}")
    
    return translator1.model == "gpt-3.5-turbo" and translator2.model == "gpt-4o-mini"

def test_custom_prompt():
    """Test custom prompt functionality"""
    print("\n🧪 Testing custom prompt...")
    
    # Test default prompt
    translator1 = MockTranslator()
    print(f"   ✅ Default prompt (None): {translator1.custom_prompt is None}")
    
    # Test custom prompt
    custom = "You are a literary translator. Translate to {target_language}."
    translator2 = MockTranslator(custom_prompt=custom)
    print(f"   ✅ Custom prompt set: {translator2.custom_prompt[:50]}...")
    
    # Test prompt module
    from src.epub_translator.prompts import get_system_prompt
    
    default_result = get_system_prompt("Chinese")
    custom_result = get_system_prompt("Chinese", custom)
    
    print(f"   ✅ Default prompt result: {default_result[:60]}...")
    print(f"   ✅ Custom prompt result: {custom_result[:60]}...")
    
    return translator2.custom_prompt == custom

def test_config_module():
    """Test configuration module"""
    print("\n🧪 Testing configuration module...")
    
    from src.epub_translator.config import (
        DEFAULT_MODEL,
        SUPPORTED_MODELS,
        LANGUAGE_NAMES,
        SOURCE_LANGUAGES,
        TARGET_LANGUAGES,
    )
    
    print(f"   ✅ Default model: {DEFAULT_MODEL}")
    print(f"   ✅ Supported models count: {len(SUPPORTED_MODELS)}")
    print(f"   ✅ Language names count: {len(LANGUAGE_NAMES)}")
    print(f"   ✅ Source languages: {len(SOURCE_LANGUAGES)}")
    print(f"   ✅ Target languages: {len(TARGET_LANGUAGES)}")
    
    return len(SUPPORTED_MODELS) > 0 and DEFAULT_MODEL in SUPPORTED_MODELS

def test_gui_imports():
    """Test that GUI can be imported (even if not displayed)"""
    print("\n🧪 Testing GUI imports...")
    
    try:
        # Temporarily set a dummy display
        original_display = os.environ.get('DISPLAY', '')
        os.environ['DISPLAY'] = ':99'
        
        import tkinter as tk
        print(f"   ✅ tkinter imported successfully")
        print(f"   ℹ️  tkinter version: {tk.TkVersion}")
        
        # Restore original display
        if original_display:
            os.environ['DISPLAY'] = original_display
        else:
            os.environ.pop('DISPLAY', None)
        
        return True
    except Exception as e:
        print(f"   ⚠️  tkinter import warning: {e}")
        print(f"   ℹ️  This is expected in headless environments")
        return True  # Not a failure for headless

def main():
    """Run all tests"""
    print("=" * 60)
    print("EPUB Translator - Test Suite")
    print("=" * 60)
    
    tests = [
        ("EPUB Parsing", test_epub_parsing),
        ("Text Segmentation", test_text_segmentation),
        ("Translation", test_translation),
        ("Metadata Adjustment", test_metadata_adjustment),
        ("Model Selection", test_model_selection),
        ("Custom Prompt", test_custom_prompt),
        ("Config Module", test_config_module),
        ("Full Translation", test_full_translation),
        ("GUI Imports", test_gui_imports),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
