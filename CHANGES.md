# CHANGELOG - Version 1.0.0

## New Features

### 1. Model Selection
Users can now choose which OpenAI model to use for translation:
- **gpt-3.5-turbo** (Default) - Fast and cost-effective
- **gpt-4** - Highest quality
- **gpt-4-turbo** - Fast GPT-4 variant
- **gpt-4o** - Latest optimized model
- **gpt-4o-mini** - Efficient and affordable

**Usage:**
```python
from src.epub_translator import EPUBTranslator

translator = EPUBTranslator(
    api_key="your-key",
    model="gpt-4o-mini"  # Specify model
)
```

**GUI:** Select model from the "Model" dropdown in API Configuration section.

### 2. Custom Translation Prompts
Users can now customize the translation prompt to achieve specific translation styles:
- Literary translation with style preservation
- Technical translation with accuracy focus
- Casual vs. formal tone
- Cultural adaptation preferences

**Usage:**
```python
custom_prompt = """You are an expert literary translator.
Translate to {target_language} with attention to style and tone.
Only return the translation."""

translator = EPUBTranslator(
    api_key="your-key",
    custom_prompt=custom_prompt
)
```

**GUI:** Edit the prompt in the "Translation Prompt" text area.

### 3. Modular Code Structure
The codebase has been refactored into a maintainable modular structure:

```
src/epub_translator/
├── __init__.py       # Package exports
├── translator.py     # Core translation logic
├── gui.py           # GUI implementation
├── config.py        # Configuration and constants
└── prompts.py       # Prompt templates
```

**Benefits:**
- Easier to understand and modify
- Better separation of concerns
- More testable code
- Easier to extend with new features

## Breaking Changes

**None!** The refactoring maintains full backwards compatibility. Old import style still works:

```python
# Old style - still works
from epub_translator import EPUBTranslator

# New style - recommended
from src.epub_translator import EPUBTranslator
```

## Improvements

### Code Organization
- **translator.py**: Core translation logic separated from UI
- **gui.py**: All GUI code in one place
- **config.py**: Centralized configuration (models, languages, fonts)
- **prompts.py**: Reusable prompt templates

### Testing
- Added tests for model selection
- Added tests for custom prompts
- Added tests for configuration module
- All 9 test suites passing

### Documentation
- Updated README with new features
- Enhanced USAGE_GUIDE with examples
- Added model selection guide
- Added custom prompt examples
- Documented new code structure

## Migration Guide

### For Existing Users
No changes needed! Your existing code will continue to work.

### To Use New Features

**Model Selection:**
```python
# Before
translator = EPUBTranslator(api_key="key")

# After (with model selection)
translator = EPUBTranslator(api_key="key", model="gpt-4o-mini")
```

**Custom Prompts:**
```python
# Before
translator = EPUBTranslator(api_key="key")

# After (with custom prompt)
translator = EPUBTranslator(
    api_key="key",
    custom_prompt="Your custom prompt with {target_language}"
)
```

### For Developers

**Importing:**
```python
# Recommended new imports
from src.epub_translator import (
    EPUBTranslator,
    TranslatorGUI,
    SUPPORTED_MODELS,
    DEFAULT_SYSTEM_PROMPT,
)

# Accessing configuration
from src.epub_translator.config import (
    LANGUAGE_NAMES,
    LANGUAGE_FONTS,
    RTL_LANGUAGES,
)

# Custom prompts
from src.epub_translator.prompts import get_system_prompt
```

## Future Enhancements

Possible future additions:
- [ ] Additional model providers (Anthropic, Cohere, etc.)
- [ ] Batch translation with rate limiting
- [ ] Translation memory/glossary support
- [ ] Multi-threaded translation
- [ ] Progress persistence (resume interrupted translations)
- [ ] Translation quality metrics
- [ ] A/B testing different prompts

## Files Changed

### New Files
- `src/epub_translator/__init__.py` - Package initialization
- `src/epub_translator/translator.py` - Core translator
- `src/epub_translator/gui.py` - GUI implementation
- `src/epub_translator/config.py` - Configuration
- `src/epub_translator/prompts.py` - Prompt templates
- `CHANGES.md` - This file

### Modified Files
- `epub_translator.py` - Now a compatibility wrapper
- `example_usage.py` - Updated with new feature examples
- `test_translator.py` - Added new tests
- `README.md` - Updated feature list and usage
- `USAGE_GUIDE.md` - Added detailed examples

## Acknowledgments

This refactoring improves maintainability and extensibility while maintaining full backwards compatibility. Thanks to all users for feedback that guided these improvements!
