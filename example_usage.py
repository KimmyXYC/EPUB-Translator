"""
Example usage of EPUB Translator without GUI
This demonstrates the core functionality including model selection and custom prompts
"""
import os
from src.epub_translator import EPUBTranslator, SUPPORTED_MODELS, DEFAULT_SYSTEM_PROMPT, fetch_available_models

def main():
    """Example of using the translator programmatically"""
    
    # Note: You need to set your API key here or use environment variable
    api_key = os.environ.get('OPENAI_API_KEY', 'your-api-key-here')
    
    if api_key == 'your-api-key-here':
        print("⚠️  Please set your OPENAI_API_KEY environment variable or edit this script")
        print("   Example: export OPENAI_API_KEY='sk-...'")
        return
    
    # Example 1: Fetch available models from API
    print("=" * 60)
    print("Example 1: Fetch Available Models from API")
    print("=" * 60)
    
    print("Fetching available models from API...")
    available_models = fetch_available_models(
        api_key=api_key,
        api_base="https://api.openai.com/v1"
    )
    
    if available_models:
        print(f"✅ Found {len(available_models)} models from API:")
        for model in available_models[:10]:  # Show first 10
            print(f"   - {model}")
        if len(available_models) > 10:
            print(f"   ... and {len(available_models) - 10} more")
    else:
        print("⚠️  Failed to fetch models from API, using default list")
        print(f"Default models: {', '.join(SUPPORTED_MODELS)}")
    print()
    
    # Example 2: Basic usage with default settings
    print("=" * 60)
    print("Example 2: Basic Translation with Default Settings")
    print("=" * 60)
    
    translator = EPUBTranslator(
        api_key=api_key,
        api_base="https://api.openai.com/v1"  # Or use your custom API endpoint
    )
    
    # Set languages
    translator.source_lang = "en"  # Source language
    translator.target_lang = "zh"  # Target language (Chinese)
    
    print(f"Model: {translator.model}")
    print(f"From: {translator.source_lang} → To: {translator.target_lang}")
    print()
    
    # Example 3: Using a specific model
    print("=" * 60)
    print("Example 3: Translation with Specific Model")
    print("=" * 60)
    
    print(f"Hardcoded default models: {', '.join(SUPPORTED_MODELS)}")
    
    translator_with_model = EPUBTranslator(
        api_key=api_key,
        api_base="https://api.openai.com/v1",
        model="gpt-4o-mini"  # Use a specific model
    )
    
    translator_with_model.source_lang = "en"
    translator_with_model.target_lang = "zh"
    
    print(f"Model: {translator_with_model.model}")
    print(f"From: {translator_with_model.source_lang} → To: {translator_with_model.target_lang}")
    print()
    
    # Example 4: Using a custom prompt
    print("=" * 60)
    print("Example 4: Translation with Custom Prompt")
    print("=" * 60)
    
    custom_prompt = """You are an expert literary translator specializing in {target_language}.
Translate the following text to {target_language} with careful attention to:
1. Preserving the original tone and style
2. Using natural, fluent language
3. Maintaining cultural context where appropriate
Only return the translated text without explanations."""
    
    translator_with_prompt = EPUBTranslator(
        api_key=api_key,
        api_base="https://api.openai.com/v1",
        model="gpt-3.5-turbo",
        custom_prompt=custom_prompt
    )
    
    translator_with_prompt.source_lang = "en"
    translator_with_prompt.target_lang = "zh"
    
    print(f"Model: {translator_with_prompt.model}")
    print(f"Custom prompt: {custom_prompt[:100]}...")
    print()
    
    # Now select which translator to use for actual translation
    print("=" * 60)
    print("Performing Translation")
    print("=" * 60)
    
    # Use the translator with custom prompt for this example
    active_translator = translator
    
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
    print(f"   Model: {active_translator.model}")
    print(f"   From: {active_translator.source_lang} → To: {active_translator.target_lang}")
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
    success = active_translator.translate_epub(
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
