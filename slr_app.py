"""
SLR·Studio — Systematic Literature Review Platform
Developed by Bahas Kebijakan
PRISMA 2020 Compliant
"""

import streamlit as st
import pandas as pd
import json
import re
import io
from datetime import datetime

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SLR·Studio · Bahas Kebijakan",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CUSTOM CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=DM+Sans:wght@300;400;500;600&display=swap');

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp { background-color: #0d1117; }

[data-testid="stSidebar"] {
    background-color: #161b22 !important;
    border-right: 1px solid #2a3147;
}
[data-testid="stSidebar"] .stMarkdown p {
    color: #8b949e;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.82rem;
}

.stMarkdown, .stText, p { color: #e6edf3 !important; font-family: 'DM Sans', sans-serif; }
h1 { font-family: 'DM Sans', sans-serif !important; font-size: 1.4rem !important; color: #e6edf3 !important; }
h2 { font-family: 'DM Sans', sans-serif !important; font-size: 1.1rem !important; color: #e6edf3 !important; }
h3 { font-family: 'DM Sans', sans-serif !important; font-size: 0.9rem !important; color: #8b949e !important; }

[data-testid="metric-container"] {
    background: #161b22;
    border: 1px solid #2a3147;
    border-radius: 8px;
    padding: 0.75rem 1rem !important;
}
[data-testid="metric-container"] label {
    color: #565f73 !important;
    font-size: 0.68rem !important;
    font-family: 'IBM Plex Mono', monospace !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #e6edf3 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 1.5rem !important;
}

[data-testid="stDataFrame"] { border: 1px solid #2a3147; border-radius: 8px; }

.stButton > button {
    background: #1c2333;
    border: 1px solid #374166;
    color: #e6edf3;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.8rem;
    border-radius: 5px;
    padding: 0.4rem 1rem;
    transition: all 0.15s;
}
.stButton > button:hover { background: #f0a500; color: #0d1117; border-color: #f0a500; }

.stSelectbox [data-baseweb="select"] { background: #1c2333; border: 1px solid #2a3147; }
.stSelectbox label { color: #565f73 !important; font-size: 0.68rem !important; font-family: 'IBM Plex Mono', monospace !important; text-transform: uppercase; }

.stTextInput input, .stTextArea textarea {
    background: #1c2333 !important;
    border: 1px solid #2a3147 !important;
    color: #e6edf3 !important;
    font-family: 'DM Sans', sans-serif;
}
.stTextInput label, .stTextArea label {
    color: #565f73 !important;
    font-size: 0.68rem !important;
    font-family: 'IBM Plex Mono', monospace !important;
    text-transform: uppercase;
}

[data-testid="stFileUploader"] { background: #1c2333; border: 1.5px dashed #374166; border-radius: 8px; }

.stRadio label { color: #8b949e !important; font-size: 0.82rem !important; }
.stRadio [data-testid="stMarkdownContainer"] p { color: #8b949e !important; }

.streamlit-expanderHeader { background: #161b22 !important; border: 1px solid #2a3147 !important; border-radius: 6px !important; color: #e6edf3 !important; }

.stTabs [data-baseweb="tab-list"] { background: #161b22; border-bottom: 1px solid #2a3147; }
.stTabs [data-baseweb="tab"] { background: transparent; color: #565f73; font-family: 'DM Sans', sans-serif; font-size: 0.8rem; border-bottom: 2px solid transparent; }
.stTabs [aria-selected="true"] { color: #ffd166 !important; border-bottom-color: #f0a500 !important; background: transparent !important; }

.stProgress > div > div { background: linear-gradient(90deg, #f0a500, #ffd166); }
.stAlert { border-radius: 6px; font-family: 'DM Sans', sans-serif; font-size: 0.82rem; }
hr { border-color: #2a3147 !important; }

.brand-logo { font-family: 'IBM Plex Mono', monospace; font-size: 0.8rem; font-weight: 600; color: #f0a500; letter-spacing: 0.08em; text-transform: uppercase; border: 1px solid #f0a500; padding: 4px 10px; border-radius: 3px; display: inline-block; margin-bottom: 0.5rem; }
.brand-sub { font-family: 'DM Sans', sans-serif; font-size: 0.72rem; color: #565f73; margin-top: 0.2rem; }
.brand-dev { font-size: 0.68rem; color: #565f73; font-family: 'IBM Plex Mono', monospace; margin-top: 0.4rem; }
.brand-dev span { color: #ffd166; font-weight: 600; }

.tag-include { background: rgba(63,185,80,0.15); color: #3fb950; border: 1px solid rgba(63,185,80,0.3); padding: 2px 8px; border-radius: 3px; font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; text-transform: uppercase; display:inline-block; }
.tag-exclude { background: rgba(248,81,73,0.12); color: #f85149; border: 1px solid rgba(248,81,73,0.25); padding: 2px 8px; border-radius: 3px; font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; text-transform: uppercase; display:inline-block; }
.tag-maybe { background: rgba(240,165,0,0.12); color: #ffd166; border: 1px solid rgba(240,165,0,0.25); padding: 2px 8px; border-radius: 3px; font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; text-transform: uppercase; display:inline-block; }
.tag-pending { background: rgba(139,148,158,0.1); color: #565f73; border: 1px solid #2a3147; padding: 2px 8px; border-radius: 3px; font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; text-transform: uppercase; display:inline-block; }
.tag-high { background: rgba(63,185,80,0.15); color: #3fb950; border: 1px solid rgba(63,185,80,0.3); padding: 2px 8px; border-radius: 3px; font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; display:inline-block; }
.tag-med { background: rgba(240,165,0,0.12); color: #ffd166; border: 1px solid rgba(240,165,0,0.25); padding: 2px 8px; border-radius: 3px; font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; display:inline-block; }
.tag-low { background: rgba(248,81,73,0.12); color: #f85149; border: 1px solid rgba(248,81,73,0.25); padding: 2px 8px; border-radius: 3px; font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; display:inline-block; }
.tag-type { background: rgba(88,166,255,0.1); color: #58a6ff; border: 1px solid rgba(88,166,255,0.2); padding: 2px 6px; border-radius: 3px; font-family: 'IBM Plex Mono', monospace; font-size: 0.6rem; display:inline-block; }

.paper-card { background: #161b22; border: 1px solid #2a3147; border-radius: 8px; padding: 1rem 1.25rem; margin-bottom: 0.75rem; }
.paper-title { font-size: 0.9rem; color: #e6edf3; font-weight: 500; margin-bottom: 0.2rem; font-family: 'DM Sans', sans-serif; }
.paper-meta { font-size: 0.65rem; color: #565f73; font-family: 'IBM Plex Mono', monospace; margin-bottom: 0.5rem; }
.paper-abstract { font-size: 0.8rem; color: #8b949e; line-height: 1.7; font-family: 'DM Sans', sans-serif; }
.hl { background: rgba(240,165,0,0.25); color: #ffd166; border-radius: 2px; padding: 0 2px; }

.section-label { font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; text-transform: uppercase; letter-spacing: 0.1em; color: #565f73; margin-bottom: 0.5rem; padding-bottom: 0.35rem; border-bottom: 1px solid #2a3147; }

.footer-brand { text-align: center; padding: 1rem; font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; color: #374166; border-top: 1px solid #2a3147; margin-top: 2rem; }
.footer-brand span { color: #ffd166; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PARSERS
# ══════════════════════════════════════════════════════════════════════════════

def _make_record(i, doc_type, title, authors, year, journal, abstract, doi, url, keywords, volume, local_file):
    """Return a standardised paper dict."""
    return {
        "id": f"P{str(i+1).zfill(3)}",
        "doc_type": doc_type,
        "title": title.strip(),
        "authors": authors,
        "year": year,
        "journal": journal,
        "abstract": abstract.strip(),
        "doi": doi,
        "url": url,
        "keywords": keywords,
        "volume": volume,
        "local_file": local_file,
        "title_decision": None,
        "abstract_decision": None,
        "exclusion_reason": "",
        "study_location": "",
        "methodology": "",
        "dataset": "",
        "policy_implication": "",
        "key_findings": "",
        "qa_obj": 0, "qa_method": 0, "qa_data": 0, "qa_bias": 0, "qa_rel": 0,
    }


def parse_ris(content):
    """Parse RIS — handles Mendeley, Zotero, EndNote exports incl. RPRT, ICOMM, HEAR types."""
    records_raw = []
    current = {}
    last_tag = None

    for line in content.splitlines():
        if line.startswith("ER  -"):
            if current:
                records_raw.append(current)
                current = {}
                last_tag = None
            continue

        m = re.match(r'^([A-Z0-9]{2})\s{2}-\s*(.*)', line)
        if m:
            tag, value = m.group(1), m.group(2).strip()
            last_tag = tag
        elif line.startswith("  ") and last_tag and current:
            # Multi-line continuation
            val = line.strip()
            if last_tag in ("N2", "AB", "N1", "T1"):
                current[last_tag] = current.get(last_tag, "") + " " + val
            continue
        else:
            continue

        if tag == "TY":
            current["TY"] = value
        elif tag in ("T1", "TI"):
            current.setdefault("T1", value)
        elif tag in ("A1", "AU"):
            current.setdefault("authors", []).append(value)
        elif tag in ("Y1", "PY"):
            m2 = re.match(r'(\d{4})', value)
            if m2:
                current["year"] = int(m2.group(1))
        elif tag in ("JF", "JO", "J1", "T2"):
            current.setdefault("JF", value)
        elif tag in ("N2", "AB"):
            current["N2"] = current.get("N2", "") + value
        elif tag == "N1":
            current["N1"] = current.get("N1", "") + value
        elif tag == "DO":
            current["DO"] = value
        elif tag in ("UR", "LK"):
            current.setdefault("UR", value)
        elif tag == "KW":
            current.setdefault("KW", []).append(value)
        elif tag in ("PB",):
            current.setdefault("PB", value)
        elif tag == "CY":
            current.setdefault("CY", value)
        elif tag == "VL":
            current["VL"] = value
        elif tag == "L1":
            current["L1"] = value.replace("file:///", "")

    if current:
        records_raw.append(current)

    out = []
    type_fallback = {"RPRT": "Report", "ICOMM": "Web/Communication",
                     "HEAR": "Hearing", "CONF": "Conference", "BOOK": "Book", "CHAP": "Book Chapter"}

    for i, r in enumerate(records_raw):
        title = r.get("T1", "").strip()
        if not title:
            continue
        doc_type = r.get("TY", "JOUR")
        authors  = "; ".join(r.get("authors", []))
        year     = r.get("year", "")
        journal  = r.get("JF") or r.get("PB") or r.get("CY") or type_fallback.get(doc_type, "")
        abstract = (r.get("N2") or r.get("N1") or "").strip()
        doi      = r.get("DO", "")
        url      = r.get("UR", "")
        keywords = "; ".join(r.get("KW", []))
        volume   = r.get("VL", "")
        local    = r.get("L1", "")
        out.append(_make_record(i, doc_type, title, authors, year, journal, abstract, doi, url, keywords, volume, local))

    return out, f"✓ Parsed {len(out)} records from RIS"


def parse_bib(content):
    """Parse BibTeX from Scopus, Dimensions, Zotero."""
    entries = re.findall(r'@\w+\s*\{[^@]+', content, re.DOTALL)
    out = []
    type_map = {"article": "JOUR", "inproceedings": "CONF", "proceedings": "CONF",
                "book": "BOOK", "techreport": "RPRT", "misc": "MISC", "incollection": "CHAP"}

    def get_field(entry, name):
        # Try braces
        m = re.search(rf'\b{name}\s*=\s*\{{((?:[^{{}}]|\{{[^{{}}]*\}})*)\}}', entry, re.IGNORECASE | re.DOTALL)
        if m:
            return re.sub(r'\{([^{}]*)\}', r'\1', m.group(1)).strip()
        # Try quotes
        m = re.search(rf'\b{name}\s*=\s*"([^"]*)"', entry, re.IGNORECASE | re.DOTALL)
        if m:
            return m.group(1).strip()
        return ""

    for i, entry in enumerate(entries):
        type_m = re.match(r'@(\w+)\s*\{', entry)
        if not type_m:
            continue
        doc_type = type_map.get(type_m.group(1).lower(), type_m.group(1).upper())
        title = get_field(entry, "title")
        if not title:
            continue
        author   = get_field(entry, "author")
        year_s   = get_field(entry, "year")
        year     = int(year_s) if year_s.isdigit() else year_s
        journal  = get_field(entry, "journal") or get_field(entry, "booktitle") or get_field(entry, "publisher") or ""
        abstract = get_field(entry, "abstract")
        doi      = get_field(entry, "doi")
        url      = get_field(entry, "url")
        keywords = get_field(entry, "keywords") or get_field(entry, "keyword")
        volume   = get_field(entry, "volume")
        out.append(_make_record(i, doc_type, title, author, year, journal, abstract, doi, url, keywords, volume, ""))

    return out, f"✓ Parsed {len(out)} records from BibTeX"


def parse_csv(content):
    """Parse CSV from Web of Science or Scopus. Auto-detects column headers."""
    try:
        df = pd.read_csv(io.StringIO(content), dtype=str).fillna("")
    except Exception as e:
        return [], f"❌ CSV parse error: {e}"

    cols = list(df.columns)

    def find(aliases):
        for a in aliases:
            if a in cols:
                return a
        return None

    col_map = {
        "title":    find(["TI","Title","Article Title","title","PT"]),
        "authors":  find(["AU","Authors","Author Names","AF","authors"]),
        "year":     find(["PY","Year","Publication Year","year"]),
        "journal":  find(["SO","Source Title","Journal","journal","JI"]),
        "abstract": find(["AB","Abstract","abstract"]),
        "doi":      find(["DI","DOI","doi"]),
        "keywords": find(["DE","Author Keywords","Keywords","ID","keywords"]),
    }

    out = []
    for i, row in df.iterrows():
        title = row.get(col_map["title"] or "__", "").strip()
        if not title:
            continue
        year_s = row.get(col_map["year"] or "__", "")
        try:
            year = int(str(year_s).strip())
        except Exception:
            year = year_s
        out.append(_make_record(
            i, "JOUR", title,
            row.get(col_map["authors"] or "__", ""),
            year,
            row.get(col_map["journal"] or "__", ""),
            row.get(col_map["abstract"] or "__", ""),
            row.get(col_map["doi"] or "__", ""),
            "", row.get(col_map["keywords"] or "__", ""), "", ""
        ))
    return out, f"✓ Parsed {len(out)} records from CSV"


def parse_file(uploaded_file):
    name = uploaded_file.name.lower()
    try:
        raw = uploaded_file.read().decode("utf-8", errors="replace")
    except Exception as e:
        return [], f"❌ Cannot read file: {e}"

    if name.endswith(".ris"):
        return parse_ris(raw)
    elif name.endswith(".bib"):
        return parse_bib(raw)
    elif name.endswith(".csv"):
        return parse_csv(raw)
    elif name.endswith(".txt"):
        # WoS tab-separated
        if raw.count("\t") > 10:
            return parse_csv(raw.replace("\t", ","))
        else:
            return parse_ris(raw)
    else:
        return [], "❌ Unsupported format. Use .ris .bib .csv .txt"


# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════

if "papers" not in st.session_state:
    st.session_state.papers = []
if "keywords" not in st.session_state:
    st.session_state.keywords = ["hydrogen", "workforce", "skills", "green jobs", "energy transition"]
if "current_tab" not in st.session_state:
    st.session_state.current_tab = 0
if "import_log" not in st.session_state:
    st.session_state.import_log = []
if "dup_results" not in st.session_state:
    st.session_state.dup_results = []


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def update_paper(paper_id, field, value):
    for p in st.session_state.papers:
        if p["id"] == paper_id:
            p[field] = value
            break

def papers_included_title():
    return [p for p in st.session_state.papers if p.get("title_decision") == "include"]

def papers_included_abstract():
    return [p for p in st.session_state.papers if p.get("abstract_decision") == "include"]

def papers_with_extraction():
    return [p for p in papers_included_abstract() if p.get("key_findings")]

def quality_score(p):
    return sum(p.get(k, 0) for k in ["qa_obj", "qa_method", "qa_data", "qa_bias", "qa_rel"])

def quality_label(score):
    if score >= 8:   return "High Quality",   "tag-high"
    elif score >= 5: return "Medium Quality", "tag-med"
    else:            return "Low Quality",    "tag-low"

def highlight_text(text, keywords):
    if not text: return str(text)
    result = str(text)
    for kw in keywords:
        if kw.strip():
            result = re.compile(re.escape(kw.strip()), re.IGNORECASE).sub(
                f'<span class="hl">{kw}</span>', result)
    return result

DOC_TYPE_LABELS = {
    "JOUR": "Journal Article", "RPRT": "Report",
    "ICOMM": "Web/Comm.", "HEAR": "Hearing",
    "CONF": "Conference", "BOOK": "Book",
    "CHAP": "Book Chapter", "MISC": "Misc",
}

NO_DATA_HTML = """
<div style="background:#161b22;border:1.5px dashed #374166;border-radius:10px;padding:3rem 2rem;text-align:center;margin:1rem 0;">
    <div style="font-size:2.2rem;margin-bottom:0.75rem;">📂</div>
    <div style="color:#e6edf3;font-size:1rem;margin-bottom:0.4rem;font-family:'DM Sans',sans-serif;">No data loaded yet</div>
    <div style="color:#565f73;font-size:0.72rem;font-family:'IBM Plex Mono',monospace;">Go to Import (Tab 01) and upload your .ris / .bib / .csv file</div>
</div>
"""

EXCL_REASONS = [
    "— select reason —", "not empirical", "not relevant topic",
    "review article", "wrong population", "wrong study design",
    "grey literature excluded", "language not supported", "duplicate",
]


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

papers = st.session_state.papers
n_total = len(papers)

with st.sidebar:
    st.markdown("""
    <div class="brand-logo">SLR·Studio</div>
    <div class="brand-sub">Systematic Literature Review</div>
    <div class="brand-dev">developed by <span>Bahas Kebijakan</span></div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    n_ti  = len(papers_included_title())
    n_ab  = len(papers_included_abstract())
    n_ex  = len(papers_with_extraction())

    st.markdown('<div class="section-label">Workflow</div>', unsafe_allow_html=True)

    NAV = [
        ("01", "📥 Import",            f"{n_total} records" if n_total else "no data"),
        ("02", "⊛ Deduplicate",         ""),
        ("03", "▤ Title Screen",        f"{len([p for p in papers if not p.get('title_decision')])} pending"),
        ("04", "◫ Abstract Screen",     f"{len([p for p in papers_included_title() if not p.get('abstract_decision')])} pending"),
        ("05", "⬡ Full Text",           f"{n_ti} papers"),
        ("06", "◈ Data Extraction",     f"{n_ab} eligible"),
        ("07", "✦ Quality Assessment",  f"{n_ex} ready"),
        ("08", "⬡ Evidence Synthesis",  ""),
        ("09", "⊞ PRISMA Diagram",      ""),
        ("10", "↓ Export",              ""),
    ]

    for i, (step, label, count) in enumerate(NAV):
        lbl = f"{label}  {count}" if count else label
        if st.button(lbl, key=f"nav_{i}", use_container_width=True):
            st.session_state.current_tab = i
            st.rerun()

    st.markdown("---")
    prog = n_ab / n_total if n_total else 0
    st.progress(prog)
    st.markdown(
        f'<div style="font-family:IBM Plex Mono,monospace;font-size:0.62rem;color:#565f73;margin-top:0.3rem;">'
        f'{n_ab}/{n_total} papers included</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div style="font-family:IBM Plex Mono,monospace;font-size:0.58rem;color:#374166;text-align:center;">PRISMA 2020 Compliant<br/>© Bahas Kebijakan</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════

tab = st.session_state.current_tab
papers = st.session_state.papers


# ─────────────────────────────────────────────────────────────────────────────
# TAB 0 — IMPORT
# ─────────────────────────────────────────────────────────────────────────────
if tab == 0:
    st.markdown("# Data Import")
    st.markdown('<div style="font-family:IBM Plex Mono,monospace;font-size:0.7rem;color:#565f73;margin-bottom:1.5rem;">module 01 — import & standardise records from reference managers</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total Records", n_total)
    with c2: st.metric("Sources Loaded", len(st.session_state.import_log))
    with c3: st.metric("Journal Articles", len([p for p in papers if p.get("doc_type") == "JOUR"]))
    with c4: st.metric("Reports / Other", len([p for p in papers if p.get("doc_type") not in ("JOUR","")]))

    st.markdown("---")
    col_l, col_r = st.columns([1.3, 1])

    with col_l:
        st.markdown('<div class="section-label">Upload Reference File</div>', unsafe_allow_html=True)
        source_db = st.selectbox("Source database", [
            "Mendeley (.ris)", "Zotero (.ris / .bib)", "Scopus (.bib / .csv)",
            "Web of Science (.txt / .csv)", "Dimensions (.bib)", "EndNote (.ris)",
        ])
        uploaded = st.file_uploader("Drop file here", type=["ris","bib","csv","txt"],
                                     label_visibility="collapsed")

        if uploaded:
            st.markdown(f'<div style="color:#3fb950;font-family:IBM Plex Mono,monospace;font-size:0.75rem;">📄 {uploaded.name} &nbsp;({uploaded.size/1024:.1f} KB)</div>', unsafe_allow_html=True)
            b1, b2 = st.columns(2)
            with b1:
                if st.button("⬆ Add to Library", use_container_width=True):
                    with st.spinner("Parsing…"):
                        new_records, msg = parse_file(uploaded)
                    if new_records:
                        offset = len(st.session_state.papers)
                        for j, r in enumerate(new_records):
                            r["id"] = f"P{str(offset+j+1).zfill(3)}"
                        st.session_state.papers.extend(new_records)
                        st.session_state.import_log.append({
                            "file": uploaded.name, "source": source_db,
                            "records": len(new_records),
                            "timestamp": datetime.now().strftime("%H:%M:%S")
                        })
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
            with b2:
                if st.button("🔄 Replace All", use_container_width=True):
                    with st.spinner("Parsing…"):
                        new_records, msg = parse_file(uploaded)
                    if new_records:
                        st.session_state.papers = new_records
                        st.session_state.import_log = [{"file": uploaded.name, "source": source_db, "records": len(new_records), "timestamp": datetime.now().strftime("%H:%M:%S")}]
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
        else:
            st.markdown("""
            <div style="background:#1c2333;border:1.5px dashed #374166;border-radius:8px;padding:2rem;text-align:center;margin-top:0.5rem;">
                <div style="font-size:1.8rem;margin-bottom:0.5rem;">📂</div>
                <div style="color:#8b949e;font-size:0.85rem;margin-bottom:0.3rem;">Drop file here or click Browse</div>
                <div style="color:#374166;font-size:0.68rem;font-family:IBM Plex Mono,monospace;">.ris &nbsp;·&nbsp; .bib &nbsp;·&nbsp; .csv &nbsp;·&nbsp; .txt</div>
            </div>
            """, unsafe_allow_html=True)

        if papers:
            st.markdown("")
            if st.button("🗑 Clear All Records", use_container_width=True):
                st.session_state.papers = []
                st.session_state.import_log = []
                st.rerun()

    with col_r:
        st.markdown('<div class="section-label">Import Log</div>', unsafe_allow_html=True)
        if st.session_state.import_log:
            st.dataframe(pd.DataFrame(st.session_state.import_log), use_container_width=True, hide_index=True)
        else:
            st.caption("No imports yet.")

        st.markdown('<div class="section-label" style="margin-top:1.2rem;">Supported Formats</div>', unsafe_allow_html=True)
        st.markdown("""
| Format | Source | Coverage |
|--------|--------|----------|
| `.ris` | Mendeley, Zotero, EndNote | Full incl. RPRT, ICOMM, abstract, notes |
| `.bib` | Scopus, Dimensions, Zotero | Full — nested braces handled |
| `.csv` | Web of Science, Scopus | Auto-detects column headers |
| `.txt` | Web of Science | Tab-separated or ISI format |
        """)

        st.markdown('<div class="section-label" style="margin-top:1.2rem;">Highlight Keywords</div>', unsafe_allow_html=True)
        new_kw = st.text_input("Add keyword", placeholder="e.g. hydrogen, workforce…")
        if st.button("+ Add", use_container_width=True):
            if new_kw.strip() and new_kw.strip() not in st.session_state.keywords:
                st.session_state.keywords.append(new_kw.strip())
                st.rerun()
        if st.session_state.keywords:
            st.markdown("  ·  ".join([f"`{k}`" for k in st.session_state.keywords]))
            rm = st.selectbox("Remove", ["— keep all —"] + st.session_state.keywords)
            if rm != "— keep all —":
                st.session_state.keywords.remove(rm)
                st.rerun()

    if papers:
        st.markdown("---")
        st.markdown('<div class="section-label">Imported Records Preview</div>', unsafe_allow_html=True)
        type_counts = {}
        for p in papers:
            t = DOC_TYPE_LABELS.get(p.get("doc_type",""), p.get("doc_type","?"))
            type_counts[t] = type_counts.get(t, 0) + 1
        st.markdown("**Document types:** " + "  ·  ".join([f"`{k}` ({v})" for k,v in sorted(type_counts.items(), key=lambda x:-x[1])]))

        prev = pd.DataFrame([{
            "ID": p["id"],
            "Type": DOC_TYPE_LABELS.get(p.get("doc_type",""), p.get("doc_type","")),
            "Title": p["title"][:70]+"…" if len(p.get("title",""))>70 else p.get("title",""),
            "Authors": p.get("authors","")[:40]+"…" if len(p.get("authors",""))>40 else p.get("authors",""),
            "Year": p.get("year",""),
            "Source": p.get("journal","")[:35]+"…" if len(p.get("journal",""))>35 else p.get("journal",""),
            "DOI": "✓" if p.get("doi") else "—",
            "Abstract": "✓" if p.get("abstract") else "—",
        } for p in papers])
        st.dataframe(prev, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — DEDUPLICATION
# ─────────────────────────────────────────────────────────────────────────────
elif tab == 1:
    st.markdown("# Deduplication")
    st.markdown('<div style="font-family:IBM Plex Mono,monospace;font-size:0.7rem;color:#565f73;margin-bottom:1.5rem;">module 02 — remove duplicate records across databases</div>', unsafe_allow_html=True)

    if not papers:
        st.markdown(NO_DATA_HTML, unsafe_allow_html=True)
        st.stop()

    def find_duplicates(records, doi_match, title_sim, threshold):
        from difflib import SequenceMatcher
        dups = []
        seen_doi, seen_title = {}, {}
        for p in records:
            found = False
            if doi_match and p.get("doi"):
                doi = p["doi"].strip().lower()
                if doi in seen_doi:
                    dups.append({"Method":"DOI match","Keep":seen_doi[doi],"Remove":p["id"],"Score":"1.00"})
                    found = True
                else:
                    seen_doi[doi] = p["id"]
            if not found and title_sim and p.get("title"):
                tn = re.sub(r'[^\w\s]','', p["title"].lower().strip())
                for pt, pid in seen_title.items():
                    r = SequenceMatcher(None, tn, pt).ratio()
                    if r >= threshold:
                        dups.append({"Method":f"Title sim. ({r:.2f})","Keep":pid,"Remove":p["id"],"Score":f"{r:.2f}"})
                        found = True
                        break
                if not found:
                    seen_title[tn] = p["id"]
        return dups

    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Records Before", len(papers))

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown('<div class="section-label">Settings</div>', unsafe_allow_html=True)
        doi_m  = st.checkbox("DOI exact match", value=True)
        title_s = st.checkbox("Title similarity", value=True)
        thresh = st.slider("Threshold", 0.70, 1.00, 0.90, 0.05) if title_s else 0.90
        if st.button("▶ Run Deduplication", use_container_width=True):
            st.session_state.dup_results = find_duplicates(papers, doi_m, title_s, thresh)

    with col_r:
        st.markdown('<div class="section-label">Duplicate Log</div>', unsafe_allow_html=True)
        dups = st.session_state.dup_results
        if dups:
            with c2: st.metric("Duplicates Found", len(dups))
            with c3: st.metric("Unique Records",   len(papers)-len(dups))
            st.dataframe(pd.DataFrame(dups), use_container_width=True, hide_index=True)
            if st.button(f"🗑 Remove {len(dups)} duplicate(s)", use_container_width=True):
                ids_rm = {d["Remove"] for d in dups}
                st.session_state.papers = [p for p in papers if p["id"] not in ids_rm]
                st.session_state.dup_results = []
                st.success(f"✓ {len(ids_rm)} duplicate(s) removed.")
                st.rerun()
        else:
            with c2: st.metric("Duplicates Found","—")
            with c3: st.metric("Unique Records", len(papers))
            st.info("Run deduplication to detect duplicates.")


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — TITLE SCREENING
# ─────────────────────────────────────────────────────────────────────────────
elif tab == 2:
    st.markdown("# Title Screening")
    st.markdown('<div style="font-family:IBM Plex Mono,monospace;font-size:0.7rem;color:#565f73;margin-bottom:1.5rem;">module 03 — first-pass relevance screening by title</div>', unsafe_allow_html=True)

    if not papers:
        st.markdown(NO_DATA_HTML, unsafe_allow_html=True)
        st.stop()

    n_inc  = len([p for p in papers if p.get("title_decision")=="include"])
    n_exc  = len([p for p in papers if p.get("title_decision")=="exclude"])
    n_may  = len([p for p in papers if p.get("title_decision")=="maybe"])
    n_pend = len([p for p in papers if not p.get("title_decision")])

    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: st.metric("Total",      len(papers))
    with c2: st.metric("✅ Include",  n_inc)
    with c3: st.metric("❌ Exclude",  n_exc)
    with c4: st.metric("🔶 Maybe",   n_may)
    with c5: st.metric("⏳ Pending",  n_pend)

    fc, sc = st.columns([1,2])
    with fc: show_f = st.selectbox("Show", ["All","Pending only","Included","Excluded","Maybe"])
    with sc: q = st.text_input("Search title", placeholder="Filter…", label_visibility="collapsed")

    st.info("💡 Include / Exclude / Maybe — use 'Maybe' for borderline papers to revisit later.")

    filtered = papers
    if show_f == "Pending only":   filtered = [p for p in papers if not p.get("title_decision")]
    elif show_f == "Included":     filtered = [p for p in papers if p.get("title_decision")=="include"]
    elif show_f == "Excluded":     filtered = [p for p in papers if p.get("title_decision")=="exclude"]
    elif show_f == "Maybe":        filtered = [p for p in papers if p.get("title_decision")=="maybe"]
    if q: filtered = [p for p in filtered if q.lower() in p.get("title","").lower()]

    st.caption(f"Showing {len(filtered)} of {len(papers)} records")
    st.markdown("---")

    for p in filtered:
        ci, cd = st.columns([4,2])
        with ci:
            hl = highlight_text(p.get("title",""), st.session_state.keywords)
            badge = DOC_TYPE_LABELS.get(p.get("doc_type",""), p.get("doc_type",""))
            st.markdown(f'<div class="paper-title"><span class="tag-type">{badge}</span>&nbsp; {hl}</div>'
                        f'<div class="paper-meta">{p["id"]} · {p.get("authors","—")[:50]} · {p.get("year","?")} · {p.get("journal","—")[:50]}</div>',
                        unsafe_allow_html=True)
        with cd:
            cur = p.get("title_decision") or "include"
            opts = ["include","exclude","maybe"]
            dec = st.radio("", opts, index=opts.index(cur) if cur in opts else 0,
                           horizontal=True, key=f"td_{p['id']}", label_visibility="collapsed")
            if dec != p.get("title_decision"):
                update_paper(p["id"], "title_decision", dec)
                st.rerun()
        st.divider()


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — ABSTRACT SCREENING
# ─────────────────────────────────────────────────────────────────────────────
elif tab == 3:
    st.markdown("# Abstract Screening")
    st.markdown('<div style="font-family:IBM Plex Mono,monospace;font-size:0.7rem;color:#565f73;margin-bottom:1.5rem;">module 04 — eligibility assessment by abstract</div>', unsafe_allow_html=True)

    ti = papers_included_title()
    if not ti:
        st.warning("No papers passed title screening yet.")
        st.stop()

    n_el  = len(papers_included_abstract())
    n_exc = len([p for p in ti if p.get("abstract_decision")=="exclude"])
    n_pe  = len([p for p in ti if not p.get("abstract_decision")])

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("From Title Screen", len(ti))
    with c2: st.metric("✅ Eligible",        n_el)
    with c3: st.metric("❌ Excluded",         n_exc)
    with c4: st.metric("⏳ Pending",          n_pe)

    show_f = st.selectbox("Show", ["All","Pending only","Included","Excluded"])
    filtered = ti
    if show_f == "Pending only": filtered = [p for p in ti if not p.get("abstract_decision")]
    elif show_f == "Included":   filtered = [p for p in ti if p.get("abstract_decision")=="include"]
    elif show_f == "Excluded":   filtered = [p for p in ti if p.get("abstract_decision")=="exclude"]

    st.markdown("---")

    for p in filtered:
        bc = {"include":"#3fb950","exclude":"#f85149","maybe":"#f0a500"}.get(p.get("abstract_decision"),"#2a3147")
        has_abs = bool(p.get("abstract","").strip())
        abs_text = p.get("abstract","") if has_abs else "_No abstract available for this record._"

        st.markdown(f"""
        <div class="paper-card" style="border-left:3px solid {bc};">
            <div class="paper-title">{highlight_text(p.get('title',''), st.session_state.keywords)}</div>
            <div class="paper-meta">{p['id']} · {p.get('authors','—')[:60]} · {p.get('year','?')} · {p.get('journal','—')}</div>
            <div class="paper-abstract">{highlight_text(abs_text, st.session_state.keywords)}</div>
        </div>
        """, unsafe_allow_html=True)

        cd, cr, ck = st.columns([2,2,2])
        with cd:
            cur = p.get("abstract_decision") or "include"
            opts = ["include","exclude","maybe"]
            dec = st.radio("", opts, index=opts.index(cur) if cur in opts else 0,
                           horizontal=True, key=f"ad_{p['id']}", label_visibility="collapsed")
            if dec != p.get("abstract_decision"):
                update_paper(p["id"], "abstract_decision", dec)
                st.rerun()
        with cr:
            if p.get("abstract_decision") == "exclude":
                cur_r = p.get("exclusion_reason","")
                ri = EXCL_REASONS.index(cur_r) if cur_r in EXCL_REASONS else 0
                reason = st.selectbox("Reason", EXCL_REASONS, index=ri,
                                      key=f"er_{p['id']}", label_visibility="collapsed")
                if reason != "— select reason —" and reason != p.get("exclusion_reason"):
                    update_paper(p["id"], "exclusion_reason", reason)
        with ck:
            if p.get("keywords"):
                kws = [k.strip() for k in re.split(r'[;,]', p["keywords"]) if k.strip()][:5]
                st.markdown(" ".join([f'<span style="font-size:0.62rem;font-family:IBM Plex Mono,monospace;color:#565f73;background:#1c2333;border:1px solid #2a3147;border-radius:3px;padding:1px 6px;">{k}</span>' for k in kws]), unsafe_allow_html=True)
        st.divider()


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — FULL TEXT
# ─────────────────────────────────────────────────────────────────────────────
elif tab == 4:
    st.markdown("# Full Text Library")
    st.markdown('<div style="font-family:IBM Plex Mono,monospace;font-size:0.7rem;color:#565f73;margin-bottom:1.5rem;">module 05 — manage and review full-text documents</div>', unsafe_allow_html=True)

    ab = papers_included_abstract()
    if not ab:
        st.warning("No papers passed abstract screening yet.")
        st.stop()

    st.info(f"📄 {len(ab)} papers eligible for full-text review.")
    pdfs = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True, label_visibility="collapsed")
    if pdfs:
        st.success(f"✓ {len(pdfs)} PDF(s) uploaded this session")

    st.markdown("---")
    ft_df = pd.DataFrame([{
        "ID": p["id"],
        "Title": p["title"][:65]+"…" if len(p.get("title",""))>65 else p.get("title",""),
        "Year": p.get("year",""),
        "Source": p.get("journal","")[:40],
        "DOI": p.get("doi","—"),
        "Mendeley path": "✓" if p.get("local_file") else "—",
    } for p in ab])
    st.dataframe(ft_df, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 — DATA EXTRACTION
# ─────────────────────────────────────────────────────────────────────────────
elif tab == 5:
    st.markdown("# Data Extraction")
    st.markdown('<div style="font-family:IBM Plex Mono,monospace;font-size:0.7rem;color:#565f73;margin-bottom:1.5rem;">module 06 — structured extraction of study characteristics</div>', unsafe_allow_html=True)

    ab = papers_included_abstract()
    if not ab:
        st.warning("No papers passed abstract screening yet.")
        st.stop()

    n_done = len([p for p in ab if p.get("key_findings")])
    c1,c2,c3 = st.columns(3)
    with c1: st.metric("Eligible", len(ab))
    with c2: st.metric("✅ Extracted", n_done)
    with c3: st.metric("⏳ Pending", len(ab)-n_done)

    vt, et = st.tabs(["📋 Table", "✏️ Extract / Edit"])

    with vt:
        rows = [{
            "ID": p["id"], "Year": p.get("year",""),
            "Title": p["title"][:55]+"…" if len(p.get("title",""))>55 else p.get("title",""),
            "Country": p.get("study_location") or "—",
            "Method": p.get("methodology") or "—",
            "Dataset": p.get("dataset") or "—",
            "Key Findings": (p.get("key_findings") or "—")[:80]+"…" if len(p.get("key_findings",""))>80 else (p.get("key_findings") or "—"),
            "Status": "✅" if p.get("key_findings") else "⏳"
        } for p in ab]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    with et:
        opts = [f"{p['id']} — {p['title'][:60]}…" for p in ab]
        sel  = st.selectbox("Select paper", opts)
        p    = ab[opts.index(sel)]

        st.markdown(f'<div class="paper-card"><div class="paper-title">{p.get("title","")}</div>'
                    f'<div class="paper-meta">{p.get("authors","—")[:60]} · {p.get("year","?")} · {p.get("journal","—")}</div>'
                    f'<div class="paper-abstract" style="margin-top:0.5rem;">{p.get("abstract","No abstract.")[:350]}…</div></div>',
                    unsafe_allow_html=True)

        with st.form(f"ex_{p['id']}"):
            c1,c2 = st.columns(2)
            with c1:
                loc   = st.text_input("Study Location / Country", value=p.get("study_location",""))
                meth  = st.text_input("Research Methodology",     value=p.get("methodology",""))
                data  = st.text_input("Dataset / Data Source",    value=p.get("dataset",""))
            with c2:
                pol   = st.text_area("Policy Implications", value=p.get("policy_implication",""), height=100)
                find  = st.text_area("Key Findings",        value=p.get("key_findings",""),       height=100)
            if st.form_submit_button("💾 Save Extraction", use_container_width=True):
                update_paper(p["id"],"study_location", loc)
                update_paper(p["id"],"methodology",    meth)
                update_paper(p["id"],"dataset",        data)
                update_paper(p["id"],"policy_implication", pol)
                update_paper(p["id"],"key_findings",   find)
                st.success(f"✓ Saved {p['id']}")
                st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# TAB 6 — QUALITY ASSESSMENT
# ─────────────────────────────────────────────────────────────────────────────
elif tab == 6:
    st.markdown("# Quality Assessment")
    st.markdown('<div style="font-family:IBM Plex Mono,monospace;font-size:0.7rem;color:#565f73;margin-bottom:1.5rem;">module 07 — appraise methodological quality of included studies</div>', unsafe_allow_html=True)

    ex = papers_with_extraction()
    if not ex:
        st.warning("Complete Data Extraction first.")
        st.stop()

    n_h = len([p for p in ex if quality_score(p)>=8])
    n_m = len([p for p in ex if 5<=quality_score(p)<8])
    n_l = len([p for p in ex if quality_score(p)<5])

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("Assessable",     len(ex))
    with c2: st.metric("🟢 High (≥8)",   n_h)
    with c3: st.metric("🟡 Medium (5-7)",n_m)
    with c4: st.metric("🔴 Low (<5)",    n_l)

    qv, qe = st.tabs(["📊 Quality Matrix", "✏️ Assess Paper"])

    with qv:
        rows = []
        for p in ex:
            qs = quality_score(p)
            ql, _ = quality_label(qs)
            rows.append({"ID": p["id"],
                "Title": p["title"][:50]+"…" if len(p.get("title",""))>50 else p.get("title",""),
                "Obj": p.get("qa_obj",0), "Method": p.get("qa_method",0),
                "Data": p.get("qa_data",0), "Bias": p.get("qa_bias",0), "Relev.": p.get("qa_rel",0),
                "Total /10": qs, "Category": ql})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    with qe:
        opts = [f"{p['id']} — {p['title'][:55]}…" for p in ex]
        sel  = st.selectbox("Select paper", opts)
        p    = ex[opts.index(sel)]
        st.markdown(f'<div class="paper-card"><div class="paper-title">{p.get("title","")}</div>'
                    f'<div class="paper-meta">{p.get("authors","—")[:60]} · {p.get("year","?")} · {p.get("journal","—")}</div></div>',
                    unsafe_allow_html=True)
        CRIT = [("qa_obj","1. Research objective clear"),("qa_method","2. Methodology quality"),
                ("qa_data","3. Data reliability"),("qa_bias","4. Bias risk assessment"),
                ("qa_rel","5. Relevance to research question")]
        with st.form(f"qa_{p['id']}"):
            scores = {}
            for k, lbl in CRIT:
                scores[k] = st.select_slider(lbl, options=[0,1,2], value=p.get(k,0),
                    format_func=lambda x: ["0 — Not met","1 — Partially met","2 — Fully met"][x])
            tot = sum(scores.values())
            ql, _ = quality_label(tot)
            st.markdown(f"**Total: {tot}/10 — {ql}**")
            if st.form_submit_button("💾 Save Assessment", use_container_width=True):
                for k,v in scores.items():
                    update_paper(p["id"], k, v)
                st.success(f"✓ {p['id']} = {tot}/10 ({ql})")
                st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# TAB 7 — SYNTHESIS
# ─────────────────────────────────────────────────────────────────────────────
elif tab == 7:
    st.markdown("# Evidence Synthesis")
    st.markdown('<div style="font-family:IBM Plex Mono,monospace;font-size:0.7rem;color:#565f73;margin-bottom:1.5rem;">module 08 — synthesise findings across included studies</div>', unsafe_allow_html=True)

    ex = [p for p in papers_included_abstract() if p.get("key_findings")]
    if not ex:
        st.warning("Complete Data Extraction first.")
        st.stop()

    ev, mt, gt = st.tabs(["📋 Evidence Table","📊 Method Distribution","🌍 Geographic Distribution"])

    with ev:
        rows = []
        for p in ex:
            qs=quality_score(p); ql,_=quality_label(qs)
            a = p.get("authors","")
            study = (a.split(";")[0].split(",")[0].strip() + f" et al. ({p.get('year','')})" if a else p["id"])
            rows.append({"Study":study,"Year":p.get("year",""),"Source":p.get("journal",""),
                "Country":p.get("study_location","—"),"Method":p.get("methodology","—"),
                "Dataset":p.get("dataset","—"),"Key Findings":p.get("key_findings","—"),
                "Policy":p.get("policy_implication","—"),"Quality":f"{qs}/10 ({ql})"})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    with mt:
        mc = {}
        for p in ex:
            m = (p.get("methodology") or "Unknown").lower()
            if any(x in m for x in ["regression","panel","ols","quantitative"]): cat="Quantitative/Regression"
            elif any(x in m for x in ["meta","systematic","slr"]): cat="Meta-analysis/SLR"
            elif any(x in m for x in ["machine learning","ml","ai","neural","random forest"]): cat="ML/AI"
            elif any(x in m for x in ["quasi","experiment","rct"]): cat="Quasi-experimental"
            elif any(x in m for x in ["qualitative","interview","case"]): cat="Qualitative"
            elif any(x in m for x in ["mixed"]): cat="Mixed Methods"
            elif any(x in m for x in ["review","literature","narrative"]): cat="Literature Review"
            else: cat="Other"
            mc[cat] = mc.get(cat,0)+1
        if mc: st.bar_chart(pd.DataFrame(list(mc.items()),columns=["Method","Count"]).set_index("Method"), color="#f0a500")

    with gt:
        gc = {}
        for p in ex:
            loc = (p.get("study_location") or "Not specified").strip() or "Not specified"
            gc[loc] = gc.get(loc,0)+1
        if gc: st.bar_chart(pd.DataFrame(list(gc.items()),columns=["Location","Count"]).set_index("Location"), color="#58a6ff")


# ─────────────────────────────────────────────────────────────────────────────
# TAB 8 — PRISMA
# ─────────────────────────────────────────────────────────────────────────────
elif tab == 8:
    st.markdown("# PRISMA Flow Diagram")
    st.markdown('<div style="font-family:IBM Plex Mono,monospace;font-size:0.7rem;color:#565f73;margin-bottom:1.5rem;">module 09 — PRISMA 2020</div>', unsafe_allow_html=True)

    if not papers:
        st.markdown(NO_DATA_HTML, unsafe_allow_html=True)
        st.stop()

    n_dup      = len(st.session_state.dup_results)
    n_id       = n_total + n_dup
    n_scr      = n_total
    n_te       = len([p for p in papers if p.get("title_decision")=="exclude"])
    n_tm       = len([p for p in papers if p.get("title_decision")=="maybe"])
    n_ae       = len(papers_included_title())
    n_axe      = len([p for p in papers if p.get("abstract_decision")=="exclude"])
    n_inc      = len(papers_included_abstract())

    st.success("✓ Counts auto-calculated from your screening decisions.")

    cd, ct = st.columns([1,1])

    with cd:
        st.markdown(f"""
        <div style="display:flex;flex-direction:column;align-items:center;gap:4px;padding:1rem 0;font-family:'DM Sans',sans-serif;">
            <div style="background:#1c2333;border:1.5px solid #58a6ff;border-radius:6px;padding:.75rem 1.5rem;text-align:center;min-width:260px;">
                <div style="font-family:IBM Plex Mono,monospace;font-size:.62rem;text-transform:uppercase;letter-spacing:.08em;color:#565f73;margin-bottom:.2rem;">Identification</div>
                <div style="font-family:IBM Plex Mono,monospace;font-size:1.6rem;font-weight:600;color:#e6edf3;">{n_id}</div>
                <div style="font-size:.72rem;color:#8b949e;margin-top:.15rem;">Records identified from databases</div>
            </div>
            <div style="font-size:1.4rem;color:#374166;">↓</div>
            <div style="display:flex;align-items:center;gap:1rem;">
                <div style="background:#1c2333;border:1.5px solid #58a6ff;border-radius:6px;padding:.75rem 1.5rem;text-align:center;min-width:260px;">
                    <div style="font-family:IBM Plex Mono,monospace;font-size:.62rem;text-transform:uppercase;letter-spacing:.08em;color:#565f73;margin-bottom:.2rem;">After Deduplication</div>
                    <div style="font-family:IBM Plex Mono,monospace;font-size:1.6rem;font-weight:600;color:#e6edf3;">{n_scr}</div>
                    <div style="font-size:.72rem;color:#8b949e;">Records after removing duplicates</div>
                </div>
                <div style="width:2rem;height:1px;background:#374166;"></div>
                <div style="background:rgba(248,81,73,.07);border:1px solid rgba(248,81,73,.2);border-radius:6px;padding:.5rem 1rem;font-size:.7rem;color:#f85149;font-family:IBM Plex Mono,monospace;text-align:center;min-width:140px;">{n_dup} duplicate(s)<br/>removed</div>
            </div>
            <div style="font-size:1.4rem;color:#374166;">↓</div>
            <div style="display:flex;align-items:center;gap:1rem;">
                <div style="background:#1c2333;border:1.5px solid #f0a500;border-radius:6px;padding:.75rem 1.5rem;text-align:center;min-width:260px;">
                    <div style="font-family:IBM Plex Mono,monospace;font-size:.62rem;text-transform:uppercase;letter-spacing:.08em;color:#565f73;margin-bottom:.2rem;">Title Screening</div>
                    <div style="font-family:IBM Plex Mono,monospace;font-size:1.6rem;font-weight:600;color:#e6edf3;">{n_scr}</div>
                    <div style="font-size:.72rem;color:#8b949e;">Records screened by title</div>
                </div>
                <div style="width:2rem;height:1px;background:#374166;"></div>
                <div style="background:rgba(248,81,73,.07);border:1px solid rgba(248,81,73,.2);border-radius:6px;padding:.5rem 1rem;font-size:.7rem;color:#f85149;font-family:IBM Plex Mono,monospace;text-align:center;min-width:140px;">{n_te} excluded<br/>{n_tm} maybe</div>
            </div>
            <div style="font-size:1.4rem;color:#374166;">↓</div>
            <div style="display:flex;align-items:center;gap:1rem;">
                <div style="background:#1c2333;border:1.5px solid #bc8cff;border-radius:6px;padding:.75rem 1.5rem;text-align:center;min-width:260px;">
                    <div style="font-family:IBM Plex Mono,monospace;font-size:.62rem;text-transform:uppercase;letter-spacing:.08em;color:#565f73;margin-bottom:.2rem;">Abstract Screening</div>
                    <div style="font-family:IBM Plex Mono,monospace;font-size:1.6rem;font-weight:600;color:#e6edf3;">{n_ae}</div>
                    <div style="font-size:.72rem;color:#8b949e;">Records assessed for eligibility</div>
                </div>
                <div style="width:2rem;height:1px;background:#374166;"></div>
                <div style="background:rgba(248,81,73,.07);border:1px solid rgba(248,81,73,.2);border-radius:6px;padding:.5rem 1rem;font-size:.7rem;color:#f85149;font-family:IBM Plex Mono,monospace;text-align:center;min-width:140px;">{n_axe} excluded<br/>(abstract)</div>
            </div>
            <div style="font-size:1.4rem;color:#374166;">↓</div>
            <div style="background:#1c2333;border:1.5px solid #3fb950;border-radius:6px;padding:.75rem 1.5rem;text-align:center;min-width:260px;">
                <div style="font-family:IBM Plex Mono,monospace;font-size:.62rem;text-transform:uppercase;letter-spacing:.08em;color:#565f73;margin-bottom:.2rem;">Included in Synthesis</div>
                <div style="font-family:IBM Plex Mono,monospace;font-size:1.6rem;font-weight:600;color:#e6edf3;">{n_inc}</div>
                <div style="font-size:.72rem;color:#8b949e;">Studies included in review</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with ct:
        st.markdown('<div class="section-label">Count Table</div>', unsafe_allow_html=True)
        pf = pd.DataFrame([
            {"Stage":"Records identified","n":n_id},
            {"Stage":"Duplicates removed","n":n_dup},
            {"Stage":"After deduplication","n":n_scr},
            {"Stage":"Title screening","n":n_scr},
            {"Stage":"Excluded (title)","n":n_te},
            {"Stage":"Maybe (title)","n":n_tm},
            {"Stage":"Abstract eligibility","n":n_ae},
            {"Stage":"Excluded (abstract)","n":n_axe},
            {"Stage":"Included in synthesis","n":n_inc},
        ])
        st.dataframe(pf, use_container_width=True, hide_index=True)
        st.download_button("📥 PRISMA Table (CSV)", pf.to_csv(index=False), "prisma_counts.csv","text/csv",use_container_width=True)

        reasons = {}
        for p in papers:
            r = p.get("exclusion_reason","")
            if r: reasons[r] = reasons.get(r,0)+1
        if reasons:
            st.markdown('<div class="section-label" style="margin-top:1rem;">Exclusion Reasons</div>', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(list(reasons.items()),columns=["Reason","n"]).sort_values("n",ascending=False),
                         use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 9 — EXPORT
# ─────────────────────────────────────────────────────────────────────────────
elif tab == 9:
    st.markdown("# Export Results")
    st.markdown('<div style="font-family:IBM Plex Mono,monospace;font-size:0.7rem;color:#565f73;margin-bottom:1.5rem;">module 10 — export for publication (Q1/Q2 journal standard)</div>', unsafe_allow_html=True)

    if not papers:
        st.markdown(NO_DATA_HTML, unsafe_allow_html=True)
        st.stop()

    ab = papers_included_abstract()
    ex = papers_with_extraction()

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("Total Records",   len(papers))
    with c2: st.metric("Title Included",  len(papers_included_title()))
    with c3: st.metric("Final Included",  len(ab))
    with c4: st.metric("Data Extracted",  len(ex))

    st.markdown("---")
    cl, cr = st.columns(2)

    with cl:
        st.markdown('<div class="section-label">Data Exports</div>', unsafe_allow_html=True)

        # Screening log
        scr = pd.DataFrame([{"paper_id":p["id"],"doc_type":p.get("doc_type",""),
            "title":p.get("title",""),"authors":p.get("authors",""),"year":p.get("year",""),
            "journal":p.get("journal",""),"doi":p.get("doi",""),
            "title_decision":p.get("title_decision") or "pending",
            "abstract_decision":p.get("abstract_decision") or "pending",
            "exclusion_reason":p.get("exclusion_reason","")} for p in papers])
        st.download_button("📥 Screening Decisions Log (.csv)", scr.to_csv(index=False),
                           "screening_decisions.csv","text/csv",use_container_width=True)

        if ex:
            ext = pd.DataFrame([{"paper_id":p["id"],"title":p.get("title",""),
                "authors":p.get("authors",""),"year":p.get("year",""),"journal":p.get("journal",""),
                "doi":p.get("doi",""),"study_location":p.get("study_location",""),
                "methodology":p.get("methodology",""),"dataset":p.get("dataset",""),
                "policy_implication":p.get("policy_implication",""),"key_findings":p.get("key_findings",""),
                "quality_score":quality_score(p),"quality_category":quality_label(quality_score(p))[0]} for p in ex])
            st.download_button("📥 Extraction Table (.csv)", ext.to_csv(index=False),
                               "extraction_table.csv","text/csv",use_container_width=True)

            qa = pd.DataFrame([{"paper_id":p["id"],"title":p.get("title",""),
                "qa_obj":p.get("qa_obj",0),"qa_method":p.get("qa_method",0),
                "qa_data":p.get("qa_data",0),"qa_bias":p.get("qa_bias",0),
                "qa_rel":p.get("qa_rel",0),"total":quality_score(p),
                "category":quality_label(quality_score(p))[0]} for p in ex])
            st.download_button("📥 Quality Assessment Matrix (.csv)", qa.to_csv(index=False),
                               "quality_assessment.csv","text/csv",use_container_width=True)

        # BibTeX export
        bib = []
        for p in ab:
            et = {"JOUR":"article","RPRT":"techreport","BOOK":"book","CONF":"inproceedings"}.get(p.get("doc_type","JOUR"),"misc")
            bib.append(f"@{et}{{{p['id']},")
            if p.get("author"):   bib.append(f"  author  = {{{p['authors']}}},")
            if p.get("title"):    bib.append(f"  title   = {{{p['title']}}},")
            if p.get("journal"):  bib.append(f"  journal = {{{p['journal']}}},")
            if p.get("year"):     bib.append(f"  year    = {{{p['year']}}},")
            if p.get("doi"):      bib.append(f"  doi     = {{{p['doi']}}},")
            if p.get("url"):      bib.append(f"  url     = {{{p['url']}}},")
            bib.append("}\n")
        st.download_button("📥 Bibliography — Included (.bib)", "\n".join(bib),
                           "included_studies.bib","text/plain",use_container_width=True)

        st.download_button("📥 Full Review Data (.json)",
                           json.dumps(st.session_state.papers, indent=2, default=str),
                           "slr_full_data.json","application/json",use_container_width=True)

    with cr:
        st.markdown('<div class="section-label">Methodology Draft</div>', unsafe_allow_html=True)
        method_text = f"""METHODOLOGY SECTION DRAFT
Generated by SLR·Studio — Bahas Kebijakan
{datetime.now().strftime('%Y-%m-%d %H:%M')}
==========================================================

2. METHODOLOGY

2.1 Search Strategy
A systematic search was conducted in {len(st.session_state.import_log)} database(s):
{", ".join([l.get("source","") for l in st.session_state.import_log]) or "Not recorded"}.
The initial search yielded {n_total + len(st.session_state.dup_results)} records in total.

2.2 Study Selection (PRISMA 2020)
After deduplication ({n_total} unique records), titles were screened.
Papers passing title screening (n={len(papers_included_title())}) were assessed
by abstract. A final {len(ab)} studies met inclusion criteria.

2.3 Data Extraction
Extracted fields: study location, methodology, data source,
key findings, and policy implications.

2.4 Quality Assessment
Five-criterion rubric (0–2 per criterion; max = 10):
  (1) Research objective clarity
  (2) Methodology quality
  (3) Data reliability
  (4) Bias risk assessment
  (5) Relevance to research question
High ≥8 · Medium 5-7 · Low <5

2.5 Evidence Synthesis
Narrative synthesis due to heterogeneity across study designs.

Reference:
Page MJ et al. BMJ 2021;372:n71. doi:10.1136/bmj.n71
==========================================================
Auto-generated. Adapt before submission.
"""
        st.download_button("📥 Methodology Draft (.txt)", method_text,
                           "methodology_draft.txt","text/plain",use_container_width=True)

        st.markdown("---")
        st.markdown('<div class="section-label">Summary</div>', unsafe_allow_html=True)
        st.markdown(f"""
| Stage | n |
|-------|---|
| Total records | {len(papers)} |
| Title included | {len(papers_included_title())} |
| Final included | {len(ab)} |
| Data extracted | {len(ex)} |
| Quality assessed | {len([p for p in ex if quality_score(p)>0])} |
| High quality | {len([p for p in ex if quality_score(p)>=8])} |
| Medium quality | {len([p for p in ex if 5<=quality_score(p)<8])} |
        """)
        st.caption("Bahas Kebijakan (2025). *SLR·Studio* [Software]. bahaskebijakan.id")


# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-brand">
    SLR·Studio &nbsp;·&nbsp; developed by <span>Bahas Kebijakan</span> &nbsp;·&nbsp; PRISMA 2020 Compliant
</div>
""", unsafe_allow_html=True)
