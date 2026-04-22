"""
utils/helpers.py
─────────────────────────────────────────────────────────────
Utility functions.
Mock data removed — real backend is now used via
utils/transcriber.py and utils/topic_extractor.py
"""

import os


# ── CSS Loader ─────────────────────────────────────────────

def load_css(path: str) -> str:
    """Read and return the contents of a CSS file."""
    base_dir  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_dir, path)
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()


# ── Transcript Statistics ──────────────────────────────────

def get_transcript_stats(transcript: str) -> tuple:
    """
    Derive quick statistics from transcript text.
    Returns (word_count, estimated_duration_string, confidence_string).
    Note: duration is overridden by real Whisper duration in layout.py
    """
    words = len(transcript.split())

    # Rough estimate: ~130 wpm average speaking pace
    minutes = words / 130
    if minutes < 1:
        duration = f"{int(minutes * 60)}s"
    else:
        m = int(minutes)
        s = int((minutes - m) * 60)
        duration = f"{m}m {s:02d}s"

    confidence = "—"  # filled in by topic_extractor

    return words, duration, confidence
