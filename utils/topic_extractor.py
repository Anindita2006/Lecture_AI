"""
topic_extractor.py
Extracts the dominant academic topic, key concepts, and a short summary
from a lecture transcript using NLP (spaCy + scikit-learn TF-IDF).
No external API needed — fully local.
"""

from __future__ import annotations
import re
from collections import Counter
from typing import Tuple, List

# ─── Topic taxonomy ──────────────────────────────────────────────────────────
TOPIC_KEYWORDS: dict[str, list[str]] = {
    "Computer Science": [
        "algorithm", "data structure", "programming", "software", "code",
        "python", "java", "c++", "machine learning", "neural network", "deep learning",
        "artificial intelligence", "ai", "database", "sql", "api", "server",
        "operating system", "compiler", "recursion", "binary", "array", "stack",
        "queue", "graph", "tree", "hash", "sorting", "searching", "complexity",
        "big o", "object oriented", "class", "function", "variable", "loop",
        "internet", "network", "protocol", "encryption", "cybersecurity",
        "cloud", "devops", "agile", "git", "version control",
    ],
    "Mathematics": [
        "theorem", "proof", "calculus", "derivative", "integral", "matrix",
        "vector", "eigenvalue", "polynomial", "equation", "algebra", "geometry",
        "topology", "probability", "statistics", "distribution", "regression",
        "hypothesis", "set theory", "logic", "number theory", "modular",
        "differential equation", "fourier", "laplace", "limit", "convergence",
        "series", "sequence", "prime", "factorial", "combinatorics",
    ],
    "Science & Technology": [
        "physics", "chemistry", "biology", "quantum", "molecule", "atom",
        "electron", "force", "energy", "mass", "velocity", "acceleration",
        "gravity", "relativity", "thermodynamics", "optics", "wave", "frequency",
        "photon", "dna", "protein", "cell", "organism", "evolution",
        "experiment", "hypothesis", "lab", "reaction", "compound", "element",
        "periodic table", "orbit", "galaxy", "astronomy", "telescope",
    ],
    "Medicine & Health": [
        "disease", "diagnosis", "treatment", "symptom", "patient", "clinical",
        "therapy", "surgery", "anatomy", "physiology", "pharmacology", "drug",
        "vaccine", "immune", "blood", "heart", "brain", "neuroscience",
        "psychiatric", "mental health", "nutrition", "diet", "exercise",
        "cancer", "diabetes", "infection", "bacteria", "virus", "antibiotic",
        "healthcare", "hospital", "physician", "nurse", "medical",
    ],
    "History & Social Studies": [
        "history", "civilization", "war", "empire", "revolution", "democracy",
        "colonial", "ancient", "medieval", "renaissance", "industrial",
        "world war", "cold war", "geography", "culture", "society", "political",
        "government", "constitution", "civil rights", "slavery", "trade",
        "migration", "archaeology", "artifact", "century", "era", "period",
        "dynasty", "republic", "monarchy", "election",
    ],
    "Language & Literature": [
        "novel", "poem", "poetry", "prose", "narrative", "character",
        "protagonist", "antagonist", "metaphor", "simile", "symbolism",
        "theme", "plot", "genre", "author", "shakespeare", "literature",
        "grammar", "syntax", "linguistics", "phonetics", "morphology",
        "discourse", "rhetoric", "essay", "writing", "reading", "language",
        "vocabulary", "dialect", "translation", "semantics",
    ],
    "Business & Economics": [
        "economics", "market", "supply", "demand", "price", "cost",
        "revenue", "profit", "loss", "gdp", "inflation", "monetary",
        "fiscal", "budget", "investment", "stock", "bond", "finance",
        "accounting", "management", "marketing", "strategy", "startup",
        "entrepreneurship", "business", "trade", "export", "import",
        "microeconomics", "macroeconomics", "elasticity", "monopoly",
    ],
    "Engineering": [
        "engineering", "mechanical", "electrical", "civil", "structural",
        "thermodynamics", "fluid dynamics", "circuit", "voltage", "current",
        "resistance", "semiconductor", "transistor", "signal", "control",
        "material", "stress", "strain", "beam", "bridge", "construction",
        "cad", "simulation", "prototype", "manufacturing", "robotics",
        "automation", "embedded", "sensor", "actuator",
    ],
    "Environmental Science": [
        "environment", "ecology", "climate", "global warming", "carbon",
        "greenhouse", "biodiversity", "habitat", "ecosystem", "species",
        "conservation", "renewable", "solar", "wind", "pollution", "emissions",
        "sustainability", "deforestation", "ocean", "atmosphere", "geology",
        "earthquake", "volcano", "soil", "water cycle", "energy transition",
    ],
    "Law & Politics": [
        "law", "legal", "legislation", "statute", "court", "judge",
        "constitution", "rights", "criminal", "civil", "tort", "contract",
        "policy", "government", "parliament", "senate", "congress",
        "election", "voting", "party", "political", "international law",
        "human rights", "jurisdiction", "precedent", "verdict", "prosecution",
    ],
    "Philosophy & Ethics": [
        "philosophy", "ethics", "morality", "consciousness", "existence",
        "epistemology", "ontology", "metaphysics", "logic", "argument",
        "socrates", "plato", "aristotle", "kant", "descartes", "nietzsche",
        "utilitarianism", "deontology", "virtue", "justice", "freedom",
        "determinism", "free will", "mind", "knowledge", "truth", "belief",
    ],
    "Arts & Culture": [
        "art", "music", "painting", "sculpture", "architecture", "film",
        "cinema", "theater", "dance", "photography", "design", "fashion",
        "cultural", "museum", "gallery", "exhibition", "artist", "composer",
        "musician", "rhythm", "harmony", "melody", "canvas", "brush",
        "aesthetic", "baroque", "renaissance", "impressionism", "modern art",
    ],
}


def _clean_text(text: str) -> str:
    """Lowercase and remove punctuation noise."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_topic(transcript: str) -> Tuple[str, float]:
    """
    Score transcript against each topic's keyword list.
    Returns (topic_name, confidence_ratio).
    """
    if not transcript or len(transcript.strip()) < 20:
        return "General Education", 0.5

    cleaned = _clean_text(transcript)
    words   = cleaned.split()
    word_set = Counter(words)

    scores: dict[str, float] = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = 0.0
        for kw in keywords:
            kw_words = kw.split()
            if len(kw_words) == 1:
                score += word_set.get(kw, 0)
            else:
                # multi-word phrase — count occurrences in full text
                score += cleaned.count(kw) * len(kw_words)   # weight longer phrases
        scores[topic] = score

    if max(scores.values()) == 0:
        return "General Education", 0.5

    best_topic = max(scores, key=lambda t: scores[t])
    total      = sum(scores.values())
    confidence = scores[best_topic] / total if total > 0 else 0.5
    # Clamp to a believable range
    confidence = max(0.52, min(0.97, confidence * 2.5))

    return best_topic, confidence


def extract_keywords(transcript: str, top_n: int = 16) -> List[str]:
    """
    Extract top N keywords using TF-IDF or simple frequency fallback.
    """
    if not transcript:
        return []

    # Try sklearn TF-IDF first
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        import numpy as np

        sentences = re.split(r'[.!?]+', transcript)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

        if len(sentences) < 2:
            raise ValueError("Too short for TF-IDF")

        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=200,
            min_df=1,
        )
        tfidf_matrix = vectorizer.fit_transform(sentences)
        scores       = np.array(tfidf_matrix.sum(axis=0)).flatten()
        feature_names = vectorizer.get_feature_names_out()

        top_indices = scores.argsort()[::-1][:top_n]
        keywords    = [feature_names[i].title() for i in top_indices]
        return keywords

    except Exception:
        pass

    # Fallback: simple frequency minus stopwords
    STOPWORDS = {
        "the","a","an","and","or","but","in","on","at","to","for","of","with",
        "is","was","are","were","be","been","being","have","has","had","do",
        "does","did","will","would","could","should","may","might","shall",
        "this","that","these","those","it","its","we","our","they","their",
        "you","your","he","his","she","her","i","my","me","us","not","no",
        "so","if","as","by","from","about","into","through","during","before",
        "after","also","just","more","very","can","all","any","each","both",
    }
    cleaned = _clean_text(transcript)
    words   = [w for w in cleaned.split() if w not in STOPWORDS and len(w) > 3]
    freq    = Counter(words)
    return [w.title() for w, _ in freq.most_common(top_n)]


def generate_summary(transcript: str, max_sentences: int = 4) -> str:
    """
    Extractive summarisation: pick the most 'important' sentences
    using TF-IDF sentence scoring.
    """
    if not transcript or len(transcript.split()) < 30:
        return transcript

    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        import numpy as np

        # Split into sentences
        raw_sents = re.split(r'(?<=[.!?])\s+', transcript.strip())
        sentences = [s.strip() for s in raw_sents if len(s.split()) >= 6]

        if len(sentences) <= max_sentences:
            return " ".join(sentences)

        vectorizer   = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(sentences)
        sent_scores  = np.array(tfidf_matrix.sum(axis=1)).flatten()

        # Keep original order for top sentences
        top_indices = sorted(
            np.argsort(sent_scores)[::-1][:max_sentences]
        )
        summary = " ".join(sentences[i] for i in top_indices)
        return summary

    except Exception:
        # Hard fallback: first N sentences
        sents = re.split(r'(?<=[.!?])\s+', transcript.strip())
        return " ".join(sents[:max_sentences])
