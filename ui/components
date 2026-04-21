"""
ui/components.py
─────────────────────────────────────────────────────────────
Re-usable HTML/CSS component builders for LectureAI.
All functions return raw HTML strings rendered via
st.markdown(..., unsafe_allow_html=True).
"""

# ── Header ────────────────────────────────────────────────

def render_header() -> str:
    """App title block with badge, gradient title, and subtitle."""
    return """
<div class="lect-header">
  <div class="lect-badge">⚡ AI-Powered</div>
  <div class="lect-title">LectureAI</div>
  <div class="lect-subtitle">
    Upload any lecture audio and watch it transform into
    structured transcripts and intelligent topic summaries — instantly.
  </div>
</div>
"""


# ── Section Label ──────────────────────────────────────────

def section_label(icon: str, text: str) -> str:
    """Small all-caps label with glowing dot, used above card sections."""
    return f"""
<div class="section-label">
  <span class="dot"></span>
  {icon}&nbsp; {text}
</div>
"""


# ── Divider ────────────────────────────────────────────────

def divider() -> str:
    """Subtle horizontal rule with gradient fade."""
    return '<div class="lect-divider"></div>'


# ── File Info Pill ─────────────────────────────────────────

def file_info_pill(filename: str, size_kb: float) -> str:
    """Pill badge displayed after a file is selected."""
    return f"""
<div class="file-info-pill">
  🎵 <strong>{filename}</strong>&nbsp;&nbsp;·&nbsp;&nbsp;{size_kb:.1f} KB
</div>
"""


# ── Transcript Box ─────────────────────────────────────────

def transcript_box(text: str) -> str:
    """Scrollable dark box containing the transcribed text."""
    # Wrap paragraphs for nicer rendering
    paragraphs = "".join(f"<p style='margin-bottom:0.9rem'>{p.strip()}</p>"
                         for p in text.split("\n") if p.strip())
    return f'<div class="transcript-box">{paragraphs}</div>'


# ── Topic Tags ─────────────────────────────────────────────

def topic_tags(primary: str, secondary: list[str]) -> str:
    """
    Render topic pills.
    primary  → highlighted cyan pill (main topic)
    secondary → list of supporting tags
    """
    html = '<div class="topic-tags">'
    html += f'<span class="topic-tag primary">🏷 {primary}</span>'
    for i, tag in enumerate(secondary):
        css_class = "secondary" if i < 2 else "tertiary"
        html += f'<span class="topic-tag {css_class}">{tag}</span>'
    html += "</div>"
    return html


# ── Stats Row ──────────────────────────────────────────────

def stats_row(word_count: int, duration_est: str, confidence: str) -> str:
    """Three-chip row showing quick transcript statistics."""
    chips = [
        ("📝", str(word_count), "Words"),
        ("⏱", duration_est, "Est. Duration"),
        ("🎯", confidence, "Confidence"),
    ]
    inner = "".join(
        f"""
        <div class="stat-chip">
          <div class="stat-value">{icon} {val}</div>
          <div class="stat-label">{label}</div>
        </div>
        """
        for icon, val, label in chips
    )
    return f'<div class="stats-row">{inner}</div>'


# ── Status Indicator ───────────────────────────────────────

def status_ready() -> str:
    """Green pulsing dot — shown when results are ready."""
    return """
<div class="status-row">
  <div class="status-dot"></div>
  <div class="status-text">Results Ready</div>
</div>
"""


# ── Glass Card wrapper ─────────────────────────────────────

def open_card(extra_style: str = "") -> str:
    style = f' style="{extra_style}"' if extra_style else ""
    return f'<div class="glass-card"{style}>'


def close_card() -> str:
    return "</div>"
