import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st

from ui.layout import (
    inject_styles,
    render_page_header,
    render_top_section,
    render_process_button,
    render_results,
)

# ── Page Configuration ─────────────────────────────────────

st.set_page_config(
    page_title="LectureAI — Transcription & Topic Extraction",
    page_icon="🎙",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Inject CSS ─────────────────────────────────────────────

inject_styles()

# ── Session State ──────────────────────────────────────────

if "processed" not in st.session_state:
    st.session_state["processed"] = False

if "last_filename" not in st.session_state:
    st.session_state["last_filename"] = ""

# ── Page Layout ────────────────────────────────────────────

render_page_header()

# 🔥 FIXED HERE (new function returns 3 values)
uploaded, model_size, language = render_top_section()

# Reset results if new file uploaded
if uploaded and uploaded.name != st.session_state["last_filename"]:
    st.session_state["processed"] = False
    st.session_state["last_filename"] = uploaded.name

process_clicked = render_process_button(uploaded)

if process_clicked:
    st.session_state["processed"] = True

if st.session_state["processed"] and uploaded:
    render_results(uploaded.name)
