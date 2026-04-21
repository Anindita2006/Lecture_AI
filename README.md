# 🎙 LectureAI — Transcription & Topic Extraction System

> A premium, portfolio-grade frontend for AI-powered lecture audio processing.  
> Built with **Streamlit** + custom CSS (dark glassmorphism theme).

---

## ✨ Features

| Feature | Status |
|---|---|
| Audio file upload (MP3 / WAV / WEBM) | ✅ |
| File info display (name + size) | ✅ |
| Multi-step processing animation | ✅ |
| Scrollable transcript output | ✅ |
| Topic/tag badges | ✅ |
| Word count, duration & confidence stats | ✅ |
| Transcript download (.txt) | ✅ |
| Dark glassmorphism UI | ✅ |
| Backend AI integration hooks | 🔌 Ready |

---

## 🚀 Quick Start

```bash
# 1. Clone / unzip the project
cd lecture_ai

# 2. (Optional) create a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the app
streamlit run frontend/app.py
```

Open your browser at **http://localhost:8501**

---

## 📁 Project Structure

```
lecture_ai/
├── requirements.txt
├── README.md
└── frontend/
    ├── app.py                  ← Streamlit entry point
    ├── ui/
    │   ├── __init__.py
    │   ├── layout.py           ← Page section renderers
    │   └── components.py       ← HTML/CSS component builders
    ├── styles/
    │   └── styles.css          ← Full custom dark-theme stylesheet
    └── utils/
        ├── __init__.py
        └── helpers.py          ← Mock data + utility functions
```

---

## 🔌 Integrating Real Backend Logic

All AI calls are isolated in `utils/helpers.py`.  
Replace the two mock functions with real calls:

```python
# utils/helpers.py

def get_mock_transcript() -> str:
    # REPLACE ↓ with your actual transcription call
    return backend.transcribe(audio_bytes)

def get_mock_topics() -> tuple[str, list[str]]:
    # REPLACE ↓ with your actual topic-extraction call
    return backend.extract_topics(transcript_text)
```

No other files need to change.

---

## 🎨 Design System

| Token | Value |
|---|---|
| Background | `#080b12` (void black) |
| Surface | `rgba(255,255,255,0.04)` (glass) |
| Accent Cyan | `#00e5ff` |
| Accent Violet | `#7c3aed` |
| Display font | Syne (Google Fonts) |
| Body font | DM Sans (Google Fonts) |

---

## 📄 License

MIT — free to use, modify, and distribute.
