"""
EPUB Translator - Main application module (Backwards compatibility wrapper)
This module now imports from the refactored src/epub_translator package

For new code, please use:
    from src.epub_translator import EPUBTranslator, TranslatorGUI, start_gui
"""

# Import everything from the new package for backwards compatibility
from src.epub_translator import (
    EPUBTranslator,
    TranslatorGUI,
    start_gui,
    HAS_TKINTER,
    DEFAULT_API_BASE,
    DEFAULT_MODEL,
    SUPPORTED_MODELS,
)


def main():
    """Main entry point - starts the GUI"""
    return start_gui()


if __name__ == "__main__":
    import sys
    sys.exit(main())
