"""
transcriber.py
Handles audio transcription using OpenAI Whisper (runs locally, no API key needed).
"""

import os
import warnings
warnings.filterwarnings("ignore", message=".*FP16 is not supported on CPU.*")


def transcribe_audio(audio_path: str, model_size: str = "base", language: str = None):
    """
    Transcribe an audio file using OpenAI Whisper.

    Args:
        audio_path: Path to the audio file.
        model_size: Whisper model size — 'tiny', 'base', 'small', 'medium', 'large'.
        language: ISO language code (e.g. 'en') or None for auto-detect.

    Returns:
        Tuple of (transcript_text, detected_language, duration_seconds)
    """
    try:
        import whisper
    except ImportError:
        raise ImportError(
            "openai-whisper is not installed. Run: pip install openai-whisper"
        )

    model = whisper.load_model(model_size)

    options = {}
    if language:
        options["language"] = language

    result = model.transcribe(audio_path, **options)

    transcript    = result.get("text", "").strip()
    detected_lang = result.get("language", "unknown")
    duration      = _get_duration(result)

    return transcript, detected_lang, duration


def _get_duration(result: dict) -> float:
    """Extract total duration in seconds from Whisper result segments."""
    segments = result.get("segments", [])
    if segments:
        return segments[-1].get("end", 0.0)
    return 0.0
