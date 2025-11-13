# Quick Start Guide

Get started with EPUB Translator in 5 minutes!

## 1. Install (1 minute)

```bash
# Clone the repository
git clone https://github.com/KimmyXYC/EPUB-Translator.git
cd EPUB-Translator

# Install dependencies
pip install -r requirements.txt
```

## 2. Get API Key (2 minutes)

Visit [OpenAI API Keys](https://platform.openai.com/api-keys) and create a new key.

Or use any OpenAI-compatible API service.

## 3. Run the Application (1 minute)

### Option A: GUI Mode (Recommended)

```bash
python epub_translator.py
```

Then:
1. Enter your API key
2. Select your EPUB file
3. Choose target language
4. Click "Translate"

### Option B: Command Line Mode

```bash
# Set your API key
export OPENAI_API_KEY='sk-your-key-here'

# Run example script
python example_usage.py
```

## 4. Enjoy Your Translated Book! (1 minute)

Find your translated EPUB in the output location you selected!

---

## Example Translation

**Japanese to Chinese:**
```bash
python epub_translator.py
# In GUI:
# - API Key: [your-key]
# - Source: ja (Japanese)
# - Target: zh (Chinese)
# - Input: japanese_book.epub
# - Output: japanese_book_translated.epub
# Click Translate!
```

---

## Need Help?

- **Common Issues**: See [USAGE_GUIDE.md](USAGE_GUIDE.md#troubleshooting)
- **GUI Help**: See [GUI_DESCRIPTION.md](GUI_DESCRIPTION.md)
- **Examples**: See [example_usage.py](example_usage.py)

---

## Features You'll Love

✅ **Easy to Use**: Simple GUI, no coding required
✅ **Smart**: Preserves all images and formatting
✅ **Flexible**: Works with many languages
✅ **Safe**: All your data stays private

---

## What You Can Translate

- ✅ Fiction novels
- ✅ Non-fiction books
- ✅ Textbooks
- ✅ Technical documentation
- ✅ Any EPUB format book!

---

## Tips for Best Results

1. **Start Small**: Test with a short book first
2. **Check Quota**: Ensure you have enough API credits
3. **Be Patient**: Large books take time (20-60 minutes typical)
4. **Verify Output**: Always check a few pages of the result

---

## That's It!

You're ready to translate books! 📚

For more advanced features, see [USAGE_GUIDE.md](USAGE_GUIDE.md)
