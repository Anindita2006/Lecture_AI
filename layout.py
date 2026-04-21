"""
ui/layout.py
─────────────────────────────────────────────────────────────
High-level layout functions.  Each function renders one
logical "section" of the page using Streamlit primitives
and the HTML components from ui/components.py.
"""

import time
import streamlit as st

from ui.components import (
    render_header,
    section_label,
    divider,
    file_info_pill,
    transcript_box,
    topic_tags,
    stats_row,
    status_ready,
    open_card,
    close_card,
)
from utils.helpers import (
    get_mock_transcript,
    get_mock_topics,
    get_transcript_stats,
    load_css,
)


# ── Inject CSS ─────────────────────────────────────────────

def inject_styles() -> None:
    """Load the external stylesheet into the Streamlit page."""
    css = load_css("styles/styles.css")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


# ── Header Section ─────────────────────────────────────────

def render_page_header() -> None:
    """Display the animated title block."""
    st.markdown(render_header(), unsafe_allow_html=True)


# ── Upload Section ─────────────────────────────────────────

def render_upload_section() -> "st.runtime.uploaded_file_manager.UploadedFile | None":
    """
    Render the file-upload card.
    Returns the uploaded file object, or None.
    """
    st.markdown(section_label("🎙", "Upload Lecture Audio"), unsafe_allow_html=True)
    st.markdown(open_card(), unsafe_allow_html=True)

    uploaded = st.file_uploader(
        label="Drop your audio file here",
        type=["mp3", "wav", "webm"],
        label_visibility="collapsed",
    )

    if uploaded:
        size_kb = len(uploaded.getvalue()) / 1024
        st.markdown(
            file_info_pill(uploaded.name, size_kb),
            unsafe_allow_html=True,
        )

    st.markdown(
        "<p style='font-size:0.78rem;color:#475569;margin-top:0.6rem;text-align:center'>"
        "Supported formats: MP3 · WAV · WEBM&nbsp;&nbsp;·&nbsp;&nbsp;Max 200 MB</p>",
        unsafe_allow_html=True,
    )
    st.markdown(close_card(), unsafe_allow_html=True)
    return uploaded


# ── Process Button ─────────────────────────────────────────

def render_process_button(uploaded) -> bool:
    """
    Show the CTA button.  Returns True if clicked and a file is loaded.
    Displays a warning if no file is uploaded yet.
    """
    st.markdown("<div style='margin-top:1.25rem'>", unsafe_allow_html=True)
    clicked = st.button("⚡  Process Lecture", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if clicked and not uploaded:
        st.warning("⚠️  Please upload an audio file first.")
        return False

    return clicked and uploaded is not None


# ── Simulated Processing ───────────────────────────────────

def simulate_processing() -> None:
    """Fake multi-step progress bar to simulate AI pipeline."""
    steps = [
        ("🔊  Decoding audio stream …",       0.30),
        ("🧠  Running speech-to-text model …", 0.65),
        ("🔍  Extracting topics & themes …",   0.88),
        ("✅  Finalising results …",            1.00),
    ]

    placeholder = st.empty()
    bar          = st.progress(0)

    for label, pct in steps:
        placeholder.markdown(
            f"<p style='color:#94a3b8;font-size:0.88rem;margin:0'>{label}</p>",
            unsafe_allow_html=True,
        )
        bar.progress(pct)
        time.sleep(0.75)

    placeholder.empty()
    bar.empty()


# ── Results Section ────────────────────────────────────────

def render_results(filename: str) -> None:
    """Display transcript + topics after processing."""

    simulate_processing()

    transcript = get_mock_transcript()
    primary_topic, secondary_topics = get_mock_topics()
    word_count, duration_est, confidence = get_transcript_stats(transcript)

    st.markdown(divider(), unsafe_allow_html=True)

    # ── Transcript card ──────────────────────────────────
    st.markdown(
        section_label("📄", "Transcription"),
        unsafe_allow_html=True,
    )
    st.markdown(open_card(), unsafe_allow_html=True)
    st.markdown(status_ready(), unsafe_allow_html=True)
    st.markdown(transcript_box(transcript), unsafe_allow_html=True)
    st.markdown(
        stats_row(word_count, duration_est, confidence),
        unsafe_allow_html=True,
    )
    st.markdown(close_card(), unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1.25rem'>", unsafe_allow_html=True)

    # ── Topics card ──────────────────────────────────────
    st.markdown(
        section_label("🏷", "Extracted Topics"),
        unsafe_allow_html=True,
    )
    st.markdown(open_card(), unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.88rem;color:#94a3b8;margin-bottom:0.6rem'>"
        "AI-identified subjects from the lecture content:</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        topic_tags(primary_topic, secondary_topics),
        unsafe_allow_html=True,
    )
    st.markdown(close_card(), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Download stub ────────────────────────────────────
    st.markdown("<div style='margin-top:1.5rem'>", unsafe_allow_html=True)
    st.download_button(
        label="⬇️  Download Transcript (.txt)",
        data=transcript,
        file_name=f"{filename.rsplit('.', 1)[0]}_transcript.txt",
        mime="text/plain",
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)
