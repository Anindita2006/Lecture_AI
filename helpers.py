"""
utils/helpers.py
─────────────────────────────────────────────────────────────
Utility functions and mock/placeholder data.
Replace the mock functions with real backend calls later.
"""

import os


# ── CSS Loader ─────────────────────────────────────────────

def load_css(path: str) -> str:
    """Read and return the contents of a CSS file."""
    # Resolve relative to this file's location → project root
    base_dir  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_dir, path)
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()


# ── Mock Transcript ────────────────────────────────────────

def get_mock_transcript() -> str:
    """
    Placeholder transcript text.
    ── REPLACE with: backend.transcribe(audio_bytes) ──
    """
    return (
        "Welcome to today's lecture on the fundamentals of quantum mechanics. "
        "We will begin by exploring the wave-particle duality of light and matter, "
        "which forms the bedrock of our modern understanding of physics at the subatomic scale.\n"

        "In 1905, Albert Einstein proposed that light is quantised into discrete packets of energy "
        "called photons. This insight, combined with Max Planck's earlier work on blackbody radiation, "
        "gave birth to the quantum theory. What is remarkable is that a single photon, when passed "
        "through a double-slit apparatus, creates an interference pattern — behaviour associated with "
        "waves — even though it is detected as a single particle on the screen.\n"

        "This duality is not a paradox but rather a fundamental feature of nature. The Heisenberg "
        "Uncertainty Principle tells us that we cannot simultaneously know the exact position and "
        "exact momentum of a particle. The more precisely we measure one quantity, the more "
        "uncertain the other becomes. This is not a limitation of our instruments — it is woven "
        "into the fabric of reality itself.\n"

        "Schrödinger's wave equation, published in 1926, provides a mathematical framework for "
        "calculating the probability distribution of a particle's position. The wave function ψ "
        "encodes all measurable information about a quantum system. When a measurement is made, "
        "the wave function 'collapses' to a definite state — a process that remains one of the "
        "most debated topics in the philosophy of physics.\n"

        "Applications of quantum mechanics are everywhere in modern technology: semiconductors, "
        "lasers, MRI machines, and the emerging field of quantum computing all rely on quantum "
        "principles. As we move deeper into this course, we will examine these applications and "
        "build the mathematical tools needed to describe quantum systems rigorously."
    )


# ── Mock Topics ────────────────────────────────────────────

def get_mock_topics() -> tuple[str, list[str]]:
    """
    Placeholder topic extraction.
    ── REPLACE with: backend.extract_topics(transcript) ──
    Returns (primary_topic, [secondary_topics]).
    """
    primary = "Quantum Mechanics"
    secondary = [
        "Wave-Particle Duality",
        "Heisenberg Uncertainty",
        "Schrödinger Equation",
        "Quantum Computing",
        "Physics",
        "Subatomic Science",
    ]
    return primary, secondary


# ── Transcript Statistics ──────────────────────────────────

def get_transcript_stats(transcript: str) -> tuple[int, str, str]:
    """
    Derive quick statistics from transcript text.
    Returns (word_count, estimated_duration_string, confidence_string).
    """
    words = len(transcript.split())

    # Rough estimate: average speaking pace ~130 wpm
    minutes = words / 130
    if minutes < 1:
        duration = f"{int(minutes * 60)}s"
    else:
        m = int(minutes)
        s = int((minutes - m) * 60)
        duration = f"{m}m {s:02d}s"

    # Mock confidence level
    confidence = "97.4%"

    return words, duration, confidence
