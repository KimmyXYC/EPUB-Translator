"""
EPUB Translator Package
A tool for translating EPUB e-books using LLM APIs
"""

from .translator import EPUBTranslator
from .gui import TranslatorGUI, start_gui, HAS_TKINTER
from .config import (
    DEFAULT_API_BASE,
    DEFAULT_MODEL,
    SUPPORTED_MODELS,
    SOURCE_LANGUAGES,
    TARGET_LANGUAGES,
)
from .prompts import DEFAULT_SYSTEM_PROMPT, get_system_prompt

__version__ = "1.0.0"

__all__ = [
    'EPUBTranslator',
    'TranslatorGUI',
    'start_gui',
    'HAS_TKINTER',
    'DEFAULT_API_BASE',
    'DEFAULT_MODEL',
    'SUPPORTED_MODELS',
    'SOURCE_LANGUAGES',
    'TARGET_LANGUAGES',
    'DEFAULT_SYSTEM_PROMPT',
    'get_system_prompt',
]
