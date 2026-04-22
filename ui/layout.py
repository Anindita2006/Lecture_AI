"""
ui/layout.py
─────────────────────────────────────────────────────────────
Layout with real backend connected.
- No options dropdowns
- Results persist via session_state
- 2-column layout kept
- Scroll fixed: results render in-place, not re-expanded
"""

import os
import time
import tempfile
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
    get_transcript_stats,
    load_css,
)

from utils.transcriber import transcribe_audio
from utils.topic_extractor import extract_topic, extract_keywords, generate_summary


# ── Inject CSS ─────────────────────────────────────────────

def inject_styles() -> None:
    css = load_css("frontend/style.css")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


# ── Header ─────────────────────────────────────────────────

def render_page_header() -> None:
    st.markdown(render_header(), unsafe_allow_html=True)


# ── Top Section (Upload only, no options) ──────────────────

def render_top_section():
    uploaded = None

    st.markdown(section_label("🎙", "Upload Audio"), unsafe_allow_html=True)

    uploaded = st.file_uploader(
        label="Drop your audio file here",
        type=["mp3", "wav", "webm", "m4a", "ogg", "flac"],
        label_visibility="collapsed",
    )

    if uploaded:
        size_kb = len(uploaded.getvalue()) / 1024
        st.markdown(
            file_info_pill(uploaded.name, size_kb),
            unsafe_allow_html=True,
        )

    return uploaded


# ── Process Button ─────────────────────────────────────────

def render_process_button(uploaded):
    clicked = st.button("⚡ Process Lecture", use_container_width=True)

    if clicked and not uploaded:
        st.warning("Upload a file first!")
        return False

    return clicked and uploaded is not None


# ── Processing: runs real backend ──────────────────────────

def _run_processing(uploaded) -> dict:
    """Save upload to temp file, run Whisper + NLP, return result dict."""

    suffix = os.path.splitext(uploaded.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded.getvalue())
        tmp_path = tmp.name

    steps = [
        (0.15, "🔊 Decoding audio..."),
        (0.40, "🧠 Running Whisper transcription..."),
        (0.65, "🔍 Extracting topics..."),
        (0.85, "✍️ Generating summary..."),
        (1.00, "✅ Finalizing..."),
    ]

    bar         = st.progress(0.0)
    placeholder = st.empty()

    # Run transcription while showing early steps
    placeholder.markdown("<p style='color:#cbd5f5; font-size:0.85rem;'>🔊 Decoding audio...</p>", unsafe_allow_html=True)
    bar.progress(0.15)
    time.sleep(0.3)

    placeholder.markdown("<p style='color:#cbd5f5; font-size:0.85rem;'>🧠 Running Whisper transcription...</p>", unsafe_allow_html=True)
    bar.progress(0.40)

    transcript, detected_lang, duration = transcribe_audio(tmp_path, model_size="base")

    placeholder.markdown("<p style='color:#cbd5f5; font-size:0.85rem;'>🔍 Extracting topics...</p>", unsafe_allow_html=True)
    bar.progress(0.65)

    primary_topic, confidence = extract_topic(transcript)
    keywords                  = extract_keywords(transcript)

    placeholder.markdown("<p style='color:#cbd5f5; font-size:0.85rem;'>✍️ Generating summary...</p>", unsafe_allow_html=True)
    bar.progress(0.85)

    summary = generate_summary(transcript)

    bar.progress(1.0)
    time.sleep(0.3)
    bar.empty()
    placeholder.empty()

    os.unlink(tmp_path)

    return {
        "transcript":    transcript,
        "primary_topic": primary_topic,
        "confidence":    f"{confidence:.0%}",
        "keywords":      keywords,
        "summary":       summary,
        "duration":      duration,
        "filename":      uploaded.name,
    }


# ── Topic panel (shown in right col after processing) ──────

def _render_topic_panel(result: dict) -> None:
    st.markdown(open_card(), unsafe_allow_html=True)

    # Topic + confidence
    topic_icon = {
        "Science & Technology": "🔬", "Mathematics": "📐",
        "History & Social Studies": "📜", "Language & Literature": "📖",
        "Medicine & Health": "🏥", "Business & Economics": "📊",
        "Philosophy & Ethics": "🤔", "Computer Science": "💻",
        "Engineering": "⚙️", "Environmental Science": "🌱",
        "Law & Politics": "⚖️", "Arts & Culture": "🎨",
        "General Education": "🎓",
    }.get(result["primary_topic"], "🏷️")

    st.markdown(
        topic_tags(
            f"{topic_icon} {result['primary_topic']}",
            result["keywords"][:5],
        ),
        unsafe_allow_html=True,
    )

    st.markdown(f"""
        <div style="margin-top:0.8rem; font-size:0.78rem; color:#64748b;">
          Confidence: <span style="color:#38bdf8">{result['confidence']}</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(close_card(), unsafe_allow_html=True)


# ── Results Section ────────────────────────────────────────

def render_results(uploaded) -> None:
    """Run backend if not cached, then render all results."""

    # Run backend only if result not yet in session state
    if st.session_state.get("result") is None:
        result = _run_processing(uploaded)
        st.session_state["result"] = result
        st.rerun()
        return

    result     = st.session_state["result"]
    transcript = result["transcript"]
    summary    = result["summary"]
    keywords   = result["keywords"]
    duration   = result["duration"]
    filename   = result["filename"]

    word_count, duration_str, _ = get_transcript_stats(transcript)
    # Override duration_str with real Whisper duration if available
    if duration:
        m = int(duration // 60)
        s = int(duration % 60)
        duration_str = f"{m}m {s:02d}s"

    st.markdown(divider(), unsafe_allow_html=True)

    # ── Stats row ──────────────────────────────────────────
    st.markdown(
        stats_row(word_count, duration_str, result["confidence"]),
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Transcript ─────────────────────────────────────────
    st.markdown(section_label("📄", "Full Transcript"), unsafe_allow_html=True)
    st.markdown(
        open_card() + status_ready() + transcript_box(transcript) + close_card(),
        unsafe_allow_html=True,
    )

    st.download_button(
        label="⬇️ Download Transcript",
        data=transcript,
        file_name=f"{os.path.splitext(filename)[0]}_transcript.txt",
        mime="text/plain",
        use_container_width=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Keywords ───────────────────────────────────────────
    if keywords:
        kw_pills = "".join(
            f"<span class='topic-tag secondary'>{kw}</span>" for kw in keywords
        )
        st.markdown(section_label("🔑", "Key Concepts"), unsafe_allow_html=True)
        st.markdown(
            open_card() + f'<div class="topic-tags">{kw_pills}</div>' + close_card(),
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)

    # ── Summary ────────────────────────────────────────────
    if summary:
        st.markdown(section_label("✍️", "AI Summary"), unsafe_allow_html=True)
        st.markdown(
            open_card() + f"<p style='color:#cbd5f5; line-height:1.75; font-size:0.95rem;'>{summary}</p>" + close_card(),
            unsafe_allow_html=True,
        )
