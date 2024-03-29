from cachetools import LRUCache, cached
from deep_translator import GoogleTranslator

# Crie um cache com um tamanho específico
translation_cache = LRUCache(maxsize=128)

# Função decorada com cache
@cached(cache=translation_cache)
def translate_text_cached(text, language):
    segment_length = 500
    segments = [text[i:i + segment_length] for i in range(0, len(text), segment_length)]
    translations = []

    for segment in segments:
        try:
            translation = GoogleTranslator(source='auto', target=language).translate(segment)
            translations.append(translation)
        except Exception as e:
            print(f"Error during translation: {e}")

    full_translation = " ".join(translations)
    return full_translation
