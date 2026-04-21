"""
ui/layout.py
─────────────────────────────────────────────────────────────
Premium Layout Upgrade:
• Side-by-side upload + options
• Tab-based results (no long scroll)
• Summary tab added
• Cleaner spacing + modern UX
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
    css = load_css("styles/styles.css")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


# ── Header ─────────────────────────────────────────────────

def render_page_header() -> None:
    st.markdown(render_header(), unsafe_allow_html=True)


# ── Upload + Options (SIDE BY SIDE) ───────────────────────

def render_top_section():
    col1, col2 = st.columns(2)

    # Upload
    with col1:
        st.markdown(section_label("🎙", "Upload Audio"), unsafe_allow_html=True)
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

        st.markdown(close_card(), unsafe_allow_html=True)

    # Options
    with col2:
        st.markdown(section_label("⚙️", "Options"), unsafe_allow_html=True)
        st.markdown(open_card(), unsafe_allow_html=True)

        model_size = st.selectbox("Whisper Model", ["base", "small", "medium"])
        language = st.selectbox("Language", ["Auto", "English", "Telugu"])

        st.markdown(close_card(), unsafe_allow_html=True)

    return uploaded


# ── Process Button ─────────────────────────────────────────

def render_process_button(uploaded):
    st.markdown("<div style='margin-top:0.8rem'>", unsafe_allow_html=True)
    clicked = st.button("⚡ Process Lecture", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if clicked and not uploaded:
        st.warning("Upload file first 😑")
        return False

    return clicked and uploaded is not None


# ── Processing Animation ───────────────────────────────────

def simulate_processing():
    steps = [
        ("🔊 Decoding audio...", 0.3),
        ("🧠 Running AI model...", 0.6),
        ("🔍 Extracting topics...", 0.85),
        ("✅ Finalizing...", 1.0),
    ]

    placeholder = st.empty()
    bar = st.progress(0)

    for text, val in steps:
        placeholder.markdown(f"<p style='color:#cbd5f5'>{text}</p>", unsafe_allow_html=True)
        bar.progress(val)
        time.sleep(0.6)

    placeholder.empty()
    bar.empty()


# ── Results (TABS — NO SCROLL) ─────────────────────────────

def render_results(filename: str):

    simulate_processing()

    transcript = get_mock_transcript()
    primary_topic, secondary_topics = get_mock_topics()
    word_count, duration_est, confidence = get_transcript_stats(transcript)

    st.markdown(divider(), unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📄 Transcript", "🏷 Topics", "🧠 Summary"])

    # ── Transcript ─────────────────────────
    with tab1:
        st.markdown(open_card(), unsafe_allow_html=True)
        st.markdown(status_ready(), unsafe_allow_html=True)
        st.markdown(transcript_box(transcript), unsafe_allow_html=True)
        st.markdown(
            stats_row(word_count, duration_est, confidence),
            unsafe_allow_html=True,
        )
        st.markdown(close_card(), unsafe_allow_html=True)

    # ── Topics ────────────────────────────
    with tab2:
        st.markdown(open_card(), unsafe_allow_html=True)
        st.markdown(topic_tags(primary_topic, secondary_topics), unsafe_allow_html=True)
        st.markdown(close_card(), unsafe_allow_html=True)

    # ── Summary (NEW COOL PART) ───────────
    with tab3:
        st.markdown(open_card(), unsafe_allow_html=True)
        st.markdown(
            "<p style='color:#cbd5f5'>This lecture discusses core concepts in a structured and easy-to-understand way. Key ideas are highlighted with practical examples, making it useful for revision and learning.</p>",
            unsafe_allow_html=True,
        )
        st.markdown(close_card(), unsafe_allow_html=True)

    # ── Download ─────────────────────────
    st.markdown("<div style='margin-top:1rem'>", unsafe_allow_html=True)
    st.download_button(
        label="⬇️ Download Transcript",
        data=transcript,
        file_name=f"{filename.rsplit('.', 1)[0]}_transcript.txt",
        mime="text/plain",
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)
