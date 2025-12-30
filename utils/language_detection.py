from typing import Optional
import langdetect
from langdetect.lang_detect_exception import LangDetectException
from utils.logging import setup_logger

logger = setup_logger(__name__)

class LanguageDetector:
    """
    Utility class for detecting language in text.
    Supports multilingual language detection using langdetect library.
    """
    
    # Supported languages mapping (ISO 639-1 codes)
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'zh': 'Chinese',
        'ja': 'Japanese',
        'ko': 'Korean',
        'ar': 'Arabic',
        'hi': 'Hindi',
        'nl': 'Dutch',
        'pl': 'Polish',
        'tr': 'Turkish',
        'vi': 'Vietnamese',
        'th': 'Thai',
        'id': 'Indonesian',
        'cs': 'Czech',
        'sv': 'Swedish',
        'da': 'Danish',
        'fi': 'Finnish',
        'no': 'Norwegian',
        'he': 'Hebrew',
        'uk': 'Ukrainian',
        'ro': 'Romanian',
        'hu': 'Hungarian',
        'el': 'Greek',
        'bg': 'Bulgarian',
        'hr': 'Croatian',
        'sk': 'Slovak',
        'sl': 'Slovenian',
        'sr': 'Serbian',
        'et': 'Estonian',
        'lv': 'Latvian',
        'lt': 'Lithuanian',
    }
    
    DEFAULT_LANGUAGE = 'en'  # Default fallback language
    
    @classmethod
    def detect_language(cls, text: str, default: Optional[str] = None) -> str:
        """
        Detect the language of the given text.
        
        Args:
            text: The text to detect language for
            default: Optional default language code if detection fails
            
        Returns:
            ISO 639-1 language code (e.g., 'en', 'es', 'fr')
        """
        if not text or not text.strip():
            return default or cls.DEFAULT_LANGUAGE
        
        try:
            # langdetect requires at least a few words for reliable detection
            text_length = len(text.strip().split())
            if text_length < 3:
                logger.debug(f"Text too short for language detection, using default: {default or cls.DEFAULT_LANGUAGE}")
                return default or cls.DEFAULT_LANGUAGE
            
            detected_lang = langdetect.detect(text)
            
            # Validate detected language is in our supported list
            if detected_lang in cls.SUPPORTED_LANGUAGES:
                logger.debug(f"Detected language: {detected_lang} ({cls.SUPPORTED_LANGUAGES[detected_lang]})")
                return detected_lang
            else:
                logger.warning(f"Detected unsupported language: {detected_lang}, using default: {default or cls.DEFAULT_LANGUAGE}")
                return default or cls.DEFAULT_LANGUAGE
                
        except LangDetectException as e:
            logger.warning(f"Language detection failed: {e}, using default: {default or cls.DEFAULT_LANGUAGE}")
            return default or cls.DEFAULT_LANGUAGE
        except Exception as e:
            logger.error(f"Unexpected error in language detection: {e}, using default: {default or cls.DEFAULT_LANGUAGE}")
            return default or cls.DEFAULT_LANGUAGE
    
    @classmethod
    def get_language_name(cls, lang_code: str) -> str:
        """
        Get the full name of a language from its ISO 639-1 code.
        
        Args:
            lang_code: ISO 639-1 language code
            
        Returns:
            Full language name or the code itself if not found
        """
        return cls.SUPPORTED_LANGUAGES.get(lang_code, lang_code)
    
    @classmethod
    def is_supported(cls, lang_code: str) -> bool:
        """
        Check if a language code is supported.
        
        Args:
            lang_code: ISO 639-1 language code
            
        Returns:
            True if supported, False otherwise
        """
        return lang_code in cls.SUPPORTED_LANGUAGES

