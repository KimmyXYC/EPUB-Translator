"""
Example usage of EPUB Translator without GUI
This demonstrates the core functionality
"""
import os
from epub_translator import EPUBTranslator

def main():
    """Example of using the translator programmatically"""
    
    # Note: You need to set your API key here or use environment variable
    api_key = os.environ.get('OPENAI_API_KEY', 'your-api-key-here')
    
    if api_key == 'your-api-key-here':
        print("⚠️  Please set your OPENAI_API_KEY environment variable or edit this script")
        print("   Example: export OPENAI_API_KEY='sk-...'")
        return
    
    # Initialize translator
    translator = EPUBTranslator(
        api_key=api_key,
        api_base="https://api.openai.com/v1"  # Or use your custom API endpoint
    )
    
    # Set languages
    translator.source_lang = "en"  # Source language
    translator.target_lang = "zh"  # Target language (Chinese)
    
    # Input and output files
    input_file = "test_input.epub"
    output_file = "test_output.epub"
    
    if not os.path.exists(input_file):
        print(f"❌ Input file not found: {input_file}")
        print("   Please create a test EPUB first by running: python create_test_epub.py")
        return
    
    print(f"📚 Starting translation...")
    print(f"   Input: {input_file}")
    print(f"   Output: {output_file}")
    print(f"   From: {translator.source_lang} → To: {translator.target_lang}")
    print()
    
    # Progress tracking
    total_docs = [0]
    progress = [0]
    
    def set_total(total):
        total_docs[0] = total
        print(f"📖 Total documents to translate: {total}")
    
    def update_progress():
        progress[0] += 1
        if total_docs[0] > 0:
            percent = (progress[0] / total_docs[0]) * 100
            print(f"⏳ Progress: {progress[0]}/{total_docs[0]} segments ({percent:.1f}%)")
    
    # Perform translation
    success = translator.translate_epub(
        input_file,
        output_file,
        progress_callback=update_progress,
        total_callback=set_total
    )
    
    if success:
        print()
        print("✅ Translation completed successfully!")
        print(f"📄 Translated file saved to: {output_file}")
    else:
        print()
        print("❌ Translation failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
