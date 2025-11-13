"""
Prompt templates for EPUB Translator
Contains default and customizable prompts for translation
"""

# Default system prompt template
DEFAULT_SYSTEM_PROMPT = (
    "You are a professional translator. "
    "Translate the following text to {target_language}. "
    "Only return the translated text without any additional explanation or notes."
)

def get_system_prompt(target_language: str, custom_prompt: str = None) -> str:
    """
    Get the system prompt for translation
    
    Args:
        target_language: Name of the target language
        custom_prompt: Optional custom prompt to use instead of default
        
    Returns:
        Formatted system prompt
    """
    if custom_prompt:
        # If custom prompt contains {target_language}, format it
        if '{target_language}' in custom_prompt:
            return custom_prompt.format(target_language=target_language)
        return custom_prompt
    
    return DEFAULT_SYSTEM_PROMPT.format(target_language=target_language)
