# EPUB Translator - Usage Guide

Complete guide for using the EPUB Translator application.

## Table of Contents

1. [Quick Start](#quick-start)
2. [GUI Usage](#gui-usage)
3. [Programmatic Usage](#programmatic-usage)
4. [Advanced Configuration](#advanced-configuration)
5. [Troubleshooting](#troubleshooting)

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/KimmyXYC/EPUB-Translator.git
cd EPUB-Translator

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage - GUI

```bash
# Start the GUI application
python epub_translator.py
```

### Basic Usage - Command Line

```bash
# Set your API key as environment variable
export OPENAI_API_KEY='sk-your-key-here'

# Run the example script
python example_usage.py
```

## GUI Usage

### Step-by-Step Guide

#### 1. Launch the Application

```bash
python epub_translator.py
```

The main window will appear with several sections.

#### 2. Configure API Settings

**Option A: Using OpenAI**
- API Key: Enter your OpenAI API key (get from https://platform.openai.com/api-keys)
- API Base URL: Leave as default `https://api.openai.com/v1`

**Option B: Using Azure OpenAI**
- API Key: Enter your Azure OpenAI key
- API Base URL: Change to your Azure endpoint, e.g., `https://YOUR-RESOURCE.openai.azure.com/`

**Option C: Using Local/Custom API**
- API Key: Your local API key (if required)
- API Base URL: Your local endpoint, e.g., `http://localhost:8000/v1`

#### 3. Select Languages

**Source Language Options:**
- `auto`: Automatic detection (recommended if unsure)
- `en`: English
- `ja`: Japanese
- `zh`: Chinese
- `ko`: Korean
- And more...

**Target Language Options:**
- Choose the language you want to translate to
- Common choices: `zh` (Chinese), `en` (English), `ja` (Japanese)

#### 4. Select Files

**Input File:**
1. Click the "Browse..." button next to "Input EPUB"
2. Navigate to your EPUB file
3. Select it and click "Open"

**Output File:**
- The output location is automatically suggested
- To change it, click "Browse..." next to "Output EPUB"
- Choose location and filename

#### 5. Translate

1. Click the "Translate" button
2. Watch the progress bar for status
3. Wait for the completion message
4. Find your translated EPUB at the output location

## Programmatic Usage

### Basic Example

```python
from epub_translator import EPUBTranslator

# Initialize translator
translator = EPUBTranslator(
    api_key="your-api-key-here",
    api_base="https://api.openai.com/v1"
)

# Configure languages
translator.source_lang = "en"  # English source
translator.target_lang = "zh"  # Chinese target

# Translate
success = translator.translate_epub(
    input_path="input.epub",
    output_path="output.epub"
)

if success:
    print("Translation completed!")
else:
    print("Translation failed!")
```

### With Progress Tracking

```python
from epub_translator import EPUBTranslator

def progress_callback():
    """Called after each text segment is translated"""
    print(".", end="", flush=True)

def total_callback(total):
    """Called once with total number of documents"""
    print(f"Translating {total} documents...")

translator = EPUBTranslator(api_key="your-key")
translator.target_lang = "zh"

success = translator.translate_epub(
    input_path="book.epub",
    output_path="book_zh.epub",
    progress_callback=progress_callback,
    total_callback=total_callback
)
```

### Using Environment Variables

```python
import os
from epub_translator import EPUBTranslator

# Read API key from environment
api_key = os.environ.get('OPENAI_API_KEY')

if not api_key:
    raise ValueError("Please set OPENAI_API_KEY environment variable")

translator = EPUBTranslator(api_key=api_key)
# ... rest of your code
```

## Advanced Configuration

### Custom API Endpoints

```python
# Using LocalAI
translator = EPUBTranslator(
    api_key="not-needed",  # LocalAI might not need a key
    api_base="http://localhost:8080/v1"
)

# Using Azure OpenAI
translator = EPUBTranslator(
    api_key="your-azure-key",
    api_base="https://YOUR-RESOURCE.openai.azure.com/"
)
```

### Language-Specific Features

The translator automatically adjusts formatting based on the target language:

#### Text Direction
- **Left-to-Right (LTR)**: English, Chinese, Japanese, Korean, most European languages
- **Right-to-Left (RTL)**: Arabic, Hebrew, Persian

```python
# RTL example - Arabic translation
translator.target_lang = "ar"  # Automatically sets RTL
```

#### Font Selection

The application automatically selects appropriate fonts:

| Language | Default Fonts |
|----------|---------------|
| Chinese (zh) | Noto Sans SC, Microsoft YaHei, SimSun |
| Japanese (ja) | Noto Sans JP, Yu Gothic, MS Gothic |
| Korean (ko) | Noto Sans KR, Malgun Gothic |
| Arabic (ar) | Noto Sans Arabic, Arial |
| Thai (th) | Noto Sans Thai, Leelawadee |
| Others | Noto Sans, Arial |

### Batch Translation

```python
import os
from epub_translator import EPUBTranslator

def translate_directory(input_dir, output_dir, target_lang="zh"):
    """Translate all EPUB files in a directory"""
    
    translator = EPUBTranslator(
        api_key=os.environ.get('OPENAI_API_KEY')
    )
    translator.target_lang = target_lang
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each EPUB file
    for filename in os.listdir(input_dir):
        if filename.endswith('.epub'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(
                output_dir, 
                filename.replace('.epub', f'_{target_lang}.epub')
            )
            
            print(f"Translating {filename}...")
            success = translator.translate_epub(input_path, output_path)
            
            if success:
                print(f"✅ {filename} completed")
            else:
                print(f"❌ {filename} failed")

# Usage
translate_directory("input_books", "translated_books", "zh")
```

## Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError: No module named 'tkinter'"

**Problem**: tkinter is not installed (required for GUI)

**Solutions**:
- Ubuntu/Debian: `sudo apt-get install python3-tk`
- Fedora: `sudo dnf install python3-tkinter`
- macOS: tkinter comes with Python
- Windows: tkinter comes with Python

**Alternative**: Use programmatic API (see `example_usage.py`)

#### 2. "Translation failed: Argument must be bytes or unicode"

**Problem**: Issue with EPUB structure or TOC

**Solution**: This should be fixed in the current version. If it persists:
- Try recreating your EPUB
- Check if the EPUB is valid with an EPUB validator
- Report the issue with the specific EPUB file

#### 3. "API key error" or "Invalid authentication"

**Problem**: API key is incorrect or has issues

**Solutions**:
- Verify your API key is correct
- Check if your API key has sufficient quota
- Ensure the API base URL is correct
- For custom APIs, verify they're running and accessible

#### 4. Translation takes very long

**Problem**: Large EPUB files have many text segments

**Solutions**:
- Be patient - translation requires API calls for each segment
- Check your internet connection
- Consider using a faster API endpoint
- Monitor your API quota/rate limits

#### 5. Translated text appears garbled

**Problem**: Font or encoding issues

**Solutions**:
- Ensure your EPUB reader supports the target language
- Try a different EPUB reader
- Check if the original EPUB had proper encoding

### Getting Help

If you encounter issues:

1. Check the console output for detailed error messages
2. Verify your EPUB file is valid
3. Test with the provided test EPUB (`python create_test_epub.py`)
4. Create an issue on GitHub with:
   - Error message
   - Steps to reproduce
   - System information (OS, Python version)
   - Sample EPUB file (if possible)

## Performance Tips

1. **API Selection**: Faster APIs provide quicker translations
2. **Segment Size**: Smaller paragraphs translate faster but use more API calls
3. **Network**: Stable, fast internet connection is crucial
4. **Rate Limits**: Be aware of your API's rate limits

## Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Environment Variables**: Use environment variables for sensitive data
3. **Input Validation**: Only translate EPUB files from trusted sources
4. **API Base URL**: Verify custom API endpoints before use

## Best Practices

1. **Backup Original**: Always keep a copy of the original EPUB
2. **Test First**: Test on a small EPUB before processing large files
3. **Verify Output**: Check a few pages of the translated EPUB
4. **Quota Management**: Monitor your API usage and costs
5. **Error Handling**: Implement proper error handling in automation scripts

## Examples

See the following files for more examples:
- `example_usage.py` - Basic programmatic usage
- `test_translator.py` - Test suite with various examples
- `create_test_epub.py` - Create test EPUB files

## Additional Resources

- [ebooklib Documentation](https://github.com/aerkalov/ebooklib)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [EPUB Specification](http://idpf.org/epub)
