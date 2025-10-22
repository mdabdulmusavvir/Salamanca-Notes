# src/speech_to_text.py
# Spanish speech → English text (local, no API keys)
# Whisper does ASR (Spanish), Hugging Face does translation (es→en)

from typing import Literal, Tuple, Optional
from functools import lru_cache

from faster_whisper import WhisperModel
from transformers import pipeline

# ──────────────────────────────────────────────────────────
# Config
# Choose the Whisper size that fits your CPU:
#   "tiny" < "base" < "small" < "medium" < "large-v3"
# On Windows/CPU, "small" is a good balance; "base" is faster.
WHISPER_MODEL_SIZE = "small"
WHISPER_DEVICE = "cpu"       # "cpu" everywhere; set "cuda" if you have GPU
WHISPER_COMPUTE_TYPE = "int8"  # good speed on CPU

# ──────────────────────────────────────────────────────────
# Lazy singletons (load once, reuse)
@lru_cache(maxsize=1)
def _get_whisper() -> WhisperModel:
    return WhisperModel(WHISPER_MODEL_SIZE, device=WHISPER_DEVICE, compute_type=WHISPER_COMPUTE_TYPE)

@lru_cache(maxsize=1)
def _get_translator():
    # Helsinki-NLP/opus-mt-es-en is small, fast and works offline after first download
    return pipeline("translation", model="Helsinki-NLP/opus-mt-es-en")

# ──────────────────────────────────────────────────────────
def transcribe_audio_spanish(audio_path: str, source_lang: Literal["es", "auto"] = "es") -> str:
    """
    Transcribe audio to SPANISH text with Whisper. This is more accurate for Spanish
    than Whisper's direct translate mode, especially with different accents.
    """
    model = _get_whisper()
    segments, info = model.transcribe(
        audio_path,
        task="transcribe",                          # <-- keep it in Spanish first
        language=None if source_lang == "auto" else source_lang,
        beam_size=5,
    )
    text = " ".join(seg.text.strip() for seg in segments)
    return text.strip()

def translate_spanish_to_english(text_es: str) -> str:
    """
    Translate Spanish text to English using a local Hugging Face model.
    """
    translator = _get_translator()
    # Break very long inputs automatically; pipeline handles chunking internally
    out = translator(text_es, clean_up_tokenization_spaces=True)
    if isinstance(out, list) and out:
        return out[0].get("translation_text", "").strip()
    return ""

def transcribe_audio_to_english(
    audio_path: str,
    source_lang: Literal["es", "auto"] = "es",
    return_spanish: bool = False,
) -> str | Tuple[str, str]:
    """
    Main function used by the app.
    1) Transcribes Spanish speech to Spanish text (Whisper)
    2) Translates Spanish → English (Hugging Face)
    Returns English string by default.
    If return_spanish=True, returns (english_text, spanish_text).
    """
    spanish_text = transcribe_audio_spanish(audio_path, source_lang=source_lang)
    english_text = translate_spanish_to_english(spanish_text)

    if return_spanish:
        return english_text, spanish_text
    return english_text

# ──────────────────────────────────────────────────────────
# Optional: direct Whisper translate (kept for debugging)
def transcribe_direct_translate(audio_path: str, source_lang: Literal["es", "auto"] = "es") -> str:
    """
    Use Whisper's built-in translate mode (es→en). Faster, but less accurate with some accents.
    """
    model = _get_whisper()
    segments, info = model.transcribe(
        audio_path,
        task="translate",                           # <-- direct to English
        language=None if source_lang == "auto" else source_lang,
        beam_size=5,
    )
    text = " ".join(seg.text.strip() for seg in segments)
    return text.strip()
