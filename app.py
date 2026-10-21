"""
Plant Identification System — Streamlit UI (app.py)
Bento-grid design, beginner-friendly, responsive.

All ML logic lives in plant_backend.py (READ-ONLY).
This file only calls identify_plant() and renders results.
"""

import sys
import traceback

import streamlit as st
from PIL import Image

# ── Page config must be the very first Streamlit call ────────────────────────
st.set_page_config(
    page_title="Plant Identification System",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═════════════════════════════════════════════════════════════════════════════
#  CSS — one clearly labelled block, never split across the file
# ═════════════════════════════════════════════════════════════════════════════
BENTO_CSS = """
<style>
/* ─── Google Font ─────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ─── CSS Custom Properties (design tokens) ──────────────────────────────── */
:root {
    --green-deep:    #1e4d1e;
    --green-mid:     #3d7a3a;
    --green-light:   #6aaf65;
    --green-pale:    #c8e6c4;
    --cream:         #f5f5ed;
    --warm-white:    #fdfdf8;
    --warm-tan:      #e8e0d0;
    --neutral-100:   #f0ede7;
    --neutral-200:   #ddd9d0;
    --neutral-800:   #2c2c28;
    --shadow-sm:     0 2px 8px rgba(30,77,30,.10);
    --shadow-md:     0 6px 20px rgba(30,77,30,.14);
    --shadow-lg:     0 12px 32px rgba(30,77,30,.18);
    --radius:        20px;
    --gap:           14px;
    --transition:    all .22s cubic-bezier(.4,0,.2,1);
}

/* ─── Global reset & base ─────────────────────────────────────────────────── */
html, body, [class*="st-"] {
    font-family: 'Inter', sans-serif !important;
    color: var(--neutral-800);
}
body { background: var(--cream); }

/* Hide default Streamlit chrome we don't need */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 1.6rem 2rem 3rem !important;
    max-width: 1280px;
}

/* ─── Bento card base ─────────────────────────────────────────────────────── */
.bento-card {
    background: var(--warm-white);
    border-radius: var(--radius);
    padding: 1.4rem 1.5rem;
    box-shadow: var(--shadow-sm);
    border: 1px solid rgba(200,230,196,.55);
    transition: var(--transition);
    height: 100%;
}
.bento-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
}

/* ─── Hero card ───────────────────────────────────────────────────────────── */
.bento-hero {
    background: linear-gradient(135deg, #1e4d1e 0%, #3d7a3a 60%, #6aaf65 100%);
    border-radius: 20px;
    padding: 2.4rem 2.2rem;
    color: #fff;
    box-shadow: 0 12px 32px rgba(30,77,30,.18);
    position: relative;
    overflow: hidden;
}
.bento-hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    border-radius: 50%;
    background: rgba(255,255,255,.06);
    pointer-events: none;
}
.bento-hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: -40px;
    width: 160px; height: 160px;
    border-radius: 50%;
    background: rgba(255,255,255,.04);
    pointer-events: none;
}
.hero-title {
    font-size: 2.1rem;
    font-weight: 800;
    letter-spacing: -.03em;
    margin: 0 0 .5rem;
    line-height: 1.15;
}
.hero-subtitle {
    font-size: .98rem;
    font-weight: 400;
    opacity: .88;
    line-height: 1.6;
    max-width: 480px;
    margin: 0;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,.18);
    border: 1px solid rgba(255,255,255,.30);
    border-radius: 999px;
    padding: .22rem .75rem;
    font-size: .76rem;
    font-weight: 600;
    letter-spacing: .05em;
    text-transform: uppercase;
    margin-bottom: .9rem;
}

/* ─── Section headings inside cards ──────────────────────────────────────── */
.card-label {
    font-size: .7rem;
    font-weight: 700;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: #3d7a3a;
    margin-bottom: .55rem;
}
.card-title {
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: .3rem;
    color: #1e4d1e;
}
.card-body {
    font-size: .9rem;
    line-height: 1.65;
    color: #444;
}

/* ─── Plant name result ───────────────────────────────────────────────────── */
.plant-name-big {
    font-size: 2rem;
    font-weight: 800;
    color: #1e4d1e;
    letter-spacing: -.02em;
    line-height: 1.1;
    margin-bottom: .2rem;
}
.confidence-pct {
    font-size: 1.6rem;
    font-weight: 700;
    color: #3d7a3a;
}

/* ─── Info chip (scientific name, family) ────────────────────────────────── */
.info-chip-value {
    font-size: 1.05rem;
    font-weight: 600;
    color: #1e4d1e;
    margin-top: .15rem;
}
.info-chip-na {
    font-size: .92rem;
    color: #999;
    font-style: italic;
}

/* ─── Alternative prediction row ─────────────────────────────────────────── */
.alt-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: .38rem 0;
    border-bottom: 1px solid #ddd9d0;
    font-size: .88rem;
}
.alt-row:last-child { border-bottom: none; }
.alt-name { font-weight: 500; color: #2c2c28; }
.alt-pct  { font-weight: 600; color: #3d7a3a; font-size: .85rem; }

/* ─── Uses / tags ─────────────────────────────────────────────────────────── */
.tag-list { display: flex; flex-wrap: wrap; gap: 7px; margin-top: .5rem; }
.tag {
    background: #c8e6c4;
    color: #1e4d1e;
    border-radius: 999px;
    padding: .22rem .75rem;
    font-size: .78rem;
    font-weight: 600;
    border: 1px solid rgba(61,122,58,.18);
}

/* ─── Tips card ───────────────────────────────────────────────────────────── */
.tip-item {
    display: flex;
    align-items: flex-start;
    gap: .5rem;
    font-size: .86rem;
    margin-bottom: .45rem;
    color: #555;
    line-height: 1.5;
}
.tip-icon { font-size: 1rem; flex-shrink: 0; margin-top: .08rem; }

/* ─── Disclaimer card ────────────────────────────────────────────────────── */
.bento-disclaimer {
    background: linear-gradient(135deg, #fffbea 0%, #fef3c7 100%);
    border: 1px solid #f6d860;
    border-radius: 20px;
    padding: 1.1rem 1.3rem;
}
.disclaimer-text {
    font-size: .82rem;
    color: #7a5f10;
    line-height: 1.6;
}

/* ─── Empty-state placeholder ────────────────────────────────────────────── */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 1.5rem .5rem;
    color: #b0b8ab;
}
.empty-icon { font-size: 2.4rem; margin-bottom: .5rem; }
.empty-text { font-size: .85rem; line-height: 1.5; }

/* ─── Streamlit widget overrides ─────────────────────────────────────────── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #3d7a3a, #1e4d1e) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 14px !important;
    padding: .78rem 1.5rem !important;
    font-size: 1.02rem !important;
    font-weight: 700 !important;
    letter-spacing: .01em !important;
    cursor: pointer !important;
    transition: all .22s cubic-bezier(.4,0,.2,1) !important;
    box-shadow: 0 4px 16px rgba(61,122,58,.35) !important;
}
.stButton > button:hover {
    box-shadow: 0 8px 24px rgba(61,122,58,.50) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* File uploader drop zone */
[data-testid="stFileUploader"] > section {
    border: 2px dashed #c8e6c4 !important;
    border-radius: 14px !important;
    background: rgba(200,230,196,.12) !important;
    transition: all .22s cubic-bezier(.4,0,.2,1) !important;
}
[data-testid="stFileUploader"] > section:hover {
    border-color: #3d7a3a !important;
    background: rgba(200,230,196,.22) !important;
}

/* Progress bar colour */
.stProgress > div > div { background: #3d7a3a !important; }

/* Expander */
details > summary {
    font-size: .82rem !important;
    color: #3d7a3a !important;
}

/* ─── Responsive: stack all columns on narrow screens ─────────────────────── */
@media (max-width: 768px) {
    .block-container { padding: .8rem 1rem 2rem !important; }
    .hero-title { font-size: 1.5rem; }
    .plant-name-big { font-size: 1.4rem; }
    .confidence-pct { font-size: 1.2rem; }
}
</style>
"""


# ═════════════════════════════════════════════════════════════════════════════
#  Backend loader — cached so the model loads only once per Streamlit session
# ═════════════════════════════════════════════════════════════════════════════
@st.cache_resource(show_spinner=False)
def _load_backend():
    """
    Import the backend module once and return the identify_plant callable.
    st.cache_resource keeps the module (and its lru_cache) alive across reruns,
    so the Keras model is not reloaded on every user interaction.
    """
    import plant_backend  # noqa: PLC0415
    return plant_backend.identify_plant


# ═════════════════════════════════════════════════════════════════════════════
#  Helper renderers
# ═════════════════════════════════════════════════════════════════════════════

def _safe(value, fallback="Not available"):
    """Return value if it is a non-empty string, else fallback."""
    if isinstance(value, list):
        value = ", ".join(str(v) for v in value) if value else None
    if value and str(value).strip():
        return str(value).strip()
    return fallback


def _pct(conf: float) -> str:
    return f"{conf * 100:.1f}%"


def _render_hero():
    st.markdown(
        """
        <div class="bento-hero">
            <div class="hero-badge">🌿 AI Plant Identification</div>
            <p class="hero-title">Plant Identification<br>System</p>
            <p class="hero-subtitle">
                Upload a clear photo of a plant leaf and our AI model will identify the species,
                show you the confidence score, and share useful information about the plant —
                all in seconds.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_tips():
    st.markdown(
        """
        <div class="bento-card">
            <div class="card-label">📷 Tips for better results</div>
            <div class="tip-item"><span class="tip-icon">🍃</span>
                <span>Use a <strong>single, clear leaf</strong> as the main subject.</span>
            </div>
            <div class="tip-item"><span class="tip-icon">☀️</span>
                <span>Shoot in <strong>natural daylight</strong> — avoid harsh shadows.</span>
            </div>
            <div class="tip-item"><span class="tip-icon">🎨</span>
                <span>A <strong>plain background</strong> (white paper, grass) improves accuracy.</span>
            </div>
            <div class="tip-item"><span class="tip-icon">📐</span>
                <span>Fill the frame and keep the <strong>leaf flat</strong> and in focus.</span>
            </div>
            <div class="tip-item"><span class="tip-icon">❌</span>
                <span>Avoid very blurry, dark, or extreme close-up shots.</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_disclaimer():
    st.markdown(
        """
        <div class="bento-disclaimer">
            <div class="card-label" style="color:#a07800;">⚠️ Important disclaimer</div>
            <p class="disclaimer-text">
                Results are <strong>model estimates</strong> based on image patterns and are
                <em>not guaranteed to be correct</em>. Do <strong>not</strong> use them to make
                decisions about consuming, treating with, or cultivating plants without first
                verifying the identification with a qualified expert or authoritative reference.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_empty_result_tiles():
    """Placeholder tiles shown before any image is uploaded."""
    st.markdown(
        """
        <div class="bento-card" style="min-height:140px;">
            <div class="card-label">🔍 Identification result</div>
            <div class="empty-state">
                <div class="empty-icon">🌱</div>
                <div class="empty-text">Upload an image and click<br><strong>Identify Plant</strong> to see results here.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_empty_meta_tiles():
    """Placeholder tiles for the metadata section before identification."""
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(
            """<div class="bento-card" style="min-height:90px;">
                <div class="card-label">🔬 Scientific name</div>
                <div class="info-chip-na">Awaiting identification…</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with col_b:
        st.markdown(
            """<div class="bento-card" style="min-height:90px;">
                <div class="card-label">🌳 Family</div>
                <div class="info-chip-na">Awaiting identification…</div>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown(
        """<div class="bento-card" style="margin-top:14px; min-height:90px;">
            <div class="card-label">📖 Description</div>
            <div class="info-chip-na">Awaiting identification…</div>
        </div>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """<div class="bento-card" style="margin-top:14px; min-height:90px;">
            <div class="card-label">💊 Uses</div>
            <div class="info-chip-na">Awaiting identification…</div>
        </div>""",
        unsafe_allow_html=True,
    )


def _render_result_tiles(result: dict):
    """Render all result bento tiles from a successful identify_plant() call."""

    # ── Top tile: plant name + confidence ────────────────────────────────────
    conf = result["confidence"]
    plant = result["plant"]
    conf_color = (
        "#2e7d32" if conf >= 0.75
        else "#f57f17" if conf >= 0.50
        else "#c62828"
    )
    st.markdown(
        f"""
        <div class="bento-card">
            <div class="card-label">🔍 Identification result</div>
            <div class="plant-name-big">{plant}</div>
            <div style="color:{conf_color}; font-size:1.55rem; font-weight:700; margin:.2rem 0 .8rem;">
                {_pct(conf)} confidence
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Native Streamlit progress bar looks cleaner than a custom HTML bar
    st.progress(float(conf))

    # ── Warning (always visible if set) ──────────────────────────────────────
    if result.get("warning"):
        st.warning(f"⚠️ {result['warning']}")

    # ── Metadata tiles ───────────────────────────────────────────────────────
    meta = result.get("metadata") or {}

    col_a, col_b = st.columns(2)
    with col_a:
        sci = _safe(meta.get("scientific_name"))
        val_class = "info-chip-value" if sci != "Not available" else "info-chip-na"
        st.markdown(
            f"""<div class="bento-card" style="min-height:90px;">
                <div class="card-label">🔬 Scientific name</div>
                <div class="{val_class}">{sci}</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with col_b:
        fam = _safe(meta.get("family"))
        val_class = "info-chip-value" if fam != "Not available" else "info-chip-na"
        st.markdown(
            f"""<div class="bento-card" style="min-height:90px;">
                <div class="card-label">🌳 Family</div>
                <div class="{val_class}">{fam}</div>
            </div>""",
            unsafe_allow_html=True,
        )

    # ── Description ──────────────────────────────────────────────────────────
    desc = _safe(meta.get("description"))
    st.markdown(
        f"""<div class="bento-card" style="margin-top:14px;">
            <div class="card-label">📖 Description</div>
            <div class="card-body">{desc}</div>
        </div>""",
        unsafe_allow_html=True,
    )

    # ── Uses ─────────────────────────────────────────────────────────────────
    raw_uses = meta.get("uses")
    if isinstance(raw_uses, list) and raw_uses:
        tags_html = "".join(f'<span class="tag">{u}</span>' for u in raw_uses)
        uses_html = f'<div class="tag-list">{tags_html}</div>'
    else:
        uses_str = _safe(raw_uses)
        uses_html = (
            f'<div class="card-body">{uses_str}</div>'
            if uses_str != "Not available"
            else '<div class="info-chip-na">Not available</div>'
        )

    st.markdown(
        f"""<div class="bento-card" style="margin-top:14px;">
            <div class="card-label">💊 Uses</div>
            {uses_html}
        </div>""",
        unsafe_allow_html=True,
    )

    # ── Top alternatives tile ─────────────────────────────────────────────────
    top = result.get("top_predictions", [])
    if len(top) > 1:
        rows_html = ""
        for i, p in enumerate(top[1:], start=2):
            rows_html += (
                f'<div class="alt-row">'
                f'<span class="alt-name">#{i} &nbsp; {p["plant"]}</span>'
                f'<span class="alt-pct">{_pct(p["confidence"])}</span>'
                f'</div>'
            )
        st.markdown(
            f"""<div class="bento-card" style="margin-top:14px;">
                <div class="card-label">📊 Other top predictions</div>
                {rows_html}
            </div>""",
            unsafe_allow_html=True,
        )


# ═════════════════════════════════════════════════════════════════════════════
#  Main app
# ═════════════════════════════════════════════════════════════════════════════

def main():
    # Inject all custom CSS
    st.markdown(BENTO_CSS, unsafe_allow_html=True)

    # ── Row 1: Hero (full width) ──────────────────────────────────────────────
    _render_hero()
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # ── Row 2: Left column (upload + tips + disclaimer) |
    #           Right column (preview + button + results) ────────────────────
    left_col, right_col = st.columns([1, 1.35], gap="medium")

    with left_col:
        # Upload tile
        with st.container(border=True):
            st.markdown('<div class="card-label">📂 Upload a leaf image</div>', unsafe_allow_html=True)
            uploaded_file = st.file_uploader(
                label="Drop your image here or browse",
                type=["jpg", "jpeg", "png"],
                label_visibility="collapsed",
                key="plant_uploader",
            )

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

        # Tips tile
        _render_tips()

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

        # Disclaimer tile
        _render_disclaimer()

    with right_col:
        # ── Preview tile ─────────────────────────────────────────────────────
        with st.container(border=True):
            st.markdown('<div class="card-label">🖼️ Image preview</div>', unsafe_allow_html=True)

            if uploaded_file is not None:
                try:
                    pil_img = Image.open(uploaded_file)
                    pil_img.verify()       # detect corrupt files early
                    uploaded_file.seek(0)  # reset stream after verify()
                    pil_img = Image.open(uploaded_file)
                    st.image(pil_img, use_container_width=True)
                except Exception as corrupt_err:
                    st.error(
                        "🚫 The uploaded file could not be read as an image. "
                        "Please try a different JPG or PNG file."
                    )
                    with st.expander("Technical details"):
                        st.code(str(corrupt_err))
                    uploaded_file = None   # prevent identify button from running
            else:
                st.markdown(
                    """<div class="empty-state" style="padding:2rem 0;">
                        <div class="empty-icon">🌿</div>
                        <div class="empty-text">Your image will appear here<br>once you upload it.</div>
                    </div>""",
                    unsafe_allow_html=True,
                )

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

        # ── Identify button ──────────────────────────────────────────────────
        identify_clicked = st.button(
            "🔍  Identify Plant",
            disabled=(uploaded_file is None),
            use_container_width=True,
        )

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

        # ── Result tiles ──────────────────────────────────────────────────────
        if not identify_clicked:
            # Empty state — grid still looks complete before first identification
            _render_empty_result_tiles()
            _render_empty_meta_tiles()

        else:
            # Load backend (cached after first call)
            with st.spinner("Loading model assets…"):
                try:
                    identify_plant_fn = _load_backend()
                except FileNotFoundError as fnf:
                    st.error(
                        "🚫 A required project file is missing. "
                        "Make sure plant_model.keras, class_names.json, and "
                        "data/plant_info.json are in the project folder."
                    )
                    with st.expander("Technical details"):
                        st.code(str(fnf))
                    st.stop()
                except Exception:
                    st.error(
                        "🚫 The model could not be loaded. "
                        "Please check your environment and try again."
                    )
                    with st.expander("Technical details"):
                        st.code(traceback.format_exc())
                    st.stop()

            # Run inference
            uploaded_file.seek(0)
            with st.spinner("Identifying plant… this may take a moment ⏳"):
                try:
                    result = identify_plant_fn(uploaded_file, top_k=5)
                except Exception:
                    st.error(
                        "🚫 Something went wrong during identification. "
                        "The image may be in an unsupported format or the model "
                        "encountered an unexpected error."
                    )
                    with st.expander("Technical details"):
                        st.code(traceback.format_exc())
                    st.stop()

            # Render results
            _render_result_tiles(result)


# ─── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
