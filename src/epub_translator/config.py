"""
Configuration module for EPUB Translator
Contains constants, default values, and configuration options
"""

# Default API configuration
DEFAULT_API_BASE = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-3.5-turbo"

# Supported models
SUPPORTED_MODELS = [
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-turbo",
    "gpt-4o",
    "gpt-4o-mini",
]

# Language mappings
LANGUAGE_NAMES = {
    'zh': 'Chinese',
    'en': 'English',
    'ja': 'Japanese',
    'ko': 'Korean',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'ru': 'Russian',
    'ar': 'Arabic',
    'he': 'Hebrew',
    'fa': 'Persian',
    'th': 'Thai',
}

# Language codes for source language selection (includes 'auto')
SOURCE_LANGUAGES = ['auto', 'en', 'ja', 'ko', 'zh', 'es', 'fr', 'de', 'ru']

# Language codes for target language selection
TARGET_LANGUAGES = ['zh', 'en', 'ja', 'ko', 'es', 'fr', 'de', 'ru', 'ar']

# Font families for different languages
LANGUAGE_FONTS = {
    'zh': "'Noto Sans SC', 'Microsoft YaHei', SimSun, sans-serif",
    'ja': "'Noto Sans JP', 'Yu Gothic', 'MS Gothic', sans-serif",
    'ko': "'Noto Sans KR', 'Malgun Gothic', sans-serif",
    'ar': "'Noto Sans Arabic', 'Arial', sans-serif",
    'he': "'Noto Sans Hebrew', 'Arial', sans-serif",
    'th': "'Noto Sans Thai', 'Leelawadee', sans-serif",
    'default': "'Noto Sans', Arial, sans-serif"
}

# RTL (Right-to-Left) languages
RTL_LANGUAGES = ['ar', 'he', 'fa']

# Translation parameters
DEFAULT_TEMPERATURE = 0.3
DEFAULT_MAX_TOKENS = 2000
