"""
app.py  —  LectureAI Entry Point
─────────────────────────────────────────────────────────────
Run with:  streamlit run app.py
─────────────────────────────────────────────────────────────
Architecture overview
  app.py          ← page config + main orchestration loop
  ui/layout.py    ← section renderers (header, upload, results)
  ui/components.py← raw HTML/CSS component builders
  styles/styles.css← all custom CSS
  utils/helpers.py← mock data + utility functions
"""

import streamlit as st

from ui.layout import (
    inject_styles,
    render_page_header,
    render_upload_section,
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

# ── Inject Premium CSS ─────────────────────────────────────

inject_styles()

# ── Session State ──────────────────────────────────────────

if "processed" not in st.session_state:
    st.session_state["processed"]      = False
if "last_filename" not in st.session_state:
    st.session_state["last_filename"]  = ""

# ── Page Layout ────────────────────────────────────────────

render_page_header()

uploaded = render_upload_section()

# Reset results if a new file is uploaded
if uploaded and uploaded.name != st.session_state["last_filename"]:
    st.session_state["processed"]     = False
    st.session_state["last_filename"] = uploaded.name

process_clicked = render_process_button(uploaded)

# Trigger processing
if process_clicked:
    st.session_state["processed"] = True

# Render results when ready
if st.session_state["processed"] and uploaded:
    render_results(uploaded.name)
