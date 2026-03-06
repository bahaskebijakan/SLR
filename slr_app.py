"""
SLR·Studio — Systematic Literature Review Platform
Bahas Kebijakan · PRISMA 2020
Design: Editorial Research Journal — stark, refined, authoritative
"""

import streamlit as st
import pandas as pd
import json, re, io
from datetime import datetime

st.set_page_config(
    page_title="SLR·Studio · Bahas Kebijakan",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Space+Grotesk:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

:root {
  --ink:        #1A1A1A;
  --ink2:       #2D2D2D;
  --ink3:       #3D3D3D;
  --steel:      #1E2028;
  --panel:      #22252F;
  --panel2:     #272B36;
  --border:     #353A48;
  --border2:    #414759;
  --mist:       #6E7891;
  --mist2:      #8E96AB;
  --snow:       #F4F2EE;
  --snow2:      #E8E4DD;
  --snow3:      #D4CEC4;
  --accent:     #E8B84B;
  --accent2:    #F0CC78;
  --accent-bg:  rgba(232,184,75,0.08);
  --red:        #D9534F;
  --red-bg:     rgba(217,83,79,0.08);
  --green:      #5DA87A;
  --green-bg:   rgba(93,168,122,0.08);
  --blue:       #5B8DB8;
  --blue-bg:    rgba(91,141,184,0.08);
  --fD: 'Playfair Display', Georgia, serif;
  --fS: 'Space Grotesk', sans-serif;
  --fM: 'Space Mono', monospace;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
#MainMenu, footer, header { visibility: hidden; }

/* ── App shell ── */
.stApp { background: var(--steel); }
.block-container { padding: 0 2rem 3rem !important; max-width: 1440px !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: var(--ink) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div { background: var(--ink) !important; }
[data-testid="stSidebar"] section { padding: 0 !important; }

/* ── Buttons ── */
.stButton > button {
  background: transparent !important;
  border: 1px solid var(--border) !important;
  color: var(--mist2) !important;
  font-family: var(--fM) !important;
  font-size: 0.68rem !important;
  letter-spacing: 0.04em !important;
  border-radius: 3px !important;
  padding: 0.45rem 1rem !important;
  transition: all 0.2s !important;
  text-align: left !important;
}
.stButton > button:hover {
  border-color: var(--accent) !important;
  color: var(--accent) !important;
  background: var(--accent-bg) !important;
}
.stButton > button:focus { box-shadow: none !important; outline: none !important; }

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea {
  background: var(--panel) !important;
  border: 1px solid var(--border) !important;
  color: var(--snow) !important;
  font-family: var(--fS) !important;
  font-size: 0.82rem !important;
  border-radius: 3px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 1px var(--accent-bg) !important;
}
.stTextInput label, .stTextArea label {
  color: var(--mist) !important;
  font-family: var(--fM) !important;
  font-size: 0.6rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.12em !important;
}

/* ── Select ── */
.stSelectbox > div > div > div {
  background: var(--panel) !important;
  border: 1px solid var(--border) !important;
  border-radius: 3px !important;
  color: var(--snow2) !important;
  font-family: var(--fS) !important;
  font-size: 0.8rem !important;
}
.stSelectbox label { color: var(--mist) !important; font-family: var(--fM) !important; font-size: 0.6rem !important; text-transform: uppercase !important; letter-spacing: 0.12em !important; }
[data-baseweb="popover"] { background: var(--panel2) !important; border: 1px solid var(--border2) !important; border-radius: 3px !important; }
[data-baseweb="menu"] { background: var(--panel2) !important; }
[data-baseweb="option"] { background: transparent !important; color: var(--snow2) !important; font-family: var(--fS) !important; font-size: 0.8rem !important; }
[data-baseweb="option"]:hover { background: var(--panel) !important; }

/* ── Radio ── */
.stRadio > div { gap: 0.15rem !important; }
.stRadio label span { color: var(--mist2) !important; font-family: var(--fM) !important; font-size: 0.7rem !important; }

/* ── Checkbox ── */
.stCheckbox label span { color: var(--mist2) !important; font-family: var(--fM) !important; font-size: 0.72rem !important; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
  background: var(--panel) !important;
  border: 1px dashed var(--border2) !important;
  border-radius: 4px !important;
}
[data-testid="stFileUploader"] p {
  color: var(--mist) !important;
  font-family: var(--fM) !important;
  font-size: 0.7rem !important;
}
[data-testid="stFileUploader"] small { color: var(--mist) !important; font-family: var(--fM) !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: transparent !important;
  border-bottom: 1px solid var(--border) !important;
  gap: 0 !important;
  padding: 0 !important;
}
.stTabs [data-baseweb="tab"] {
  font-family: var(--fM) !important;
  font-size: 0.65rem !important;
  color: var(--mist) !important;
  background: transparent !important;
  border-bottom: 2px solid transparent !important;
  padding: 0.65rem 1.2rem !important;
  letter-spacing: 0.06em !important;
  text-transform: uppercase !important;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--snow2) !important; }
.stTabs [aria-selected="true"] {
  color: var(--accent) !important;
  border-bottom-color: var(--accent) !important;
  font-weight: 700 !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] { border: 1px solid var(--border) !important; border-radius: 3px !important; overflow: hidden !important; }
[data-testid="stDataFrame"] table { font-family: var(--fM) !important; font-size: 0.7rem !important; }
[data-testid="stDataFrame"] thead th {
  background: var(--panel2) !important; color: var(--mist) !important;
  font-size: 0.58rem !important; text-transform: uppercase !important; letter-spacing: 0.1em !important;
  border-bottom: 1px solid var(--border2) !important; padding: 0.6rem 0.8rem !important;
}
[data-testid="stDataFrame"] tbody td {
  background: var(--panel) !important; color: var(--snow2) !important;
  border-bottom: 1px solid var(--border) !important; padding: 0.5rem 0.8rem !important;
}
[data-testid="stDataFrame"] tbody tr:hover td { background: var(--panel2) !important; }

/* ── Alerts ── */
.stAlert { border-radius: 3px !important; font-family: var(--fM) !important; font-size: 0.7rem !important; }
.stAlert p { font-family: var(--fM) !important; font-size: 0.7rem !important; }

/* ── Progress bar ── */
.stProgress > div { background: var(--border) !important; height: 2px !important; border-radius: 1px !important; }
.stProgress > div > div { background: var(--accent) !important; }

/* ── Slider ── */
[data-baseweb="slider"] [data-testid="stThumbValue"] {
  font-family: var(--fM) !important; font-size: 0.6rem !important;
  background: var(--panel2) !important; color: var(--accent) !important;
  border: 1px solid var(--border2) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--ink2); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }

hr { border-color: var(--border) !important; margin: 0.75rem 0 !important; }

/* ═══════════════════════════════════════
   CUSTOM LAYOUT COMPONENTS
   ═══════════════════════════════════════ */

/* ── Top nav bar ── */
.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.85rem 0 0.85rem 0;
  border-bottom: 1px solid var(--border);
  margin-bottom: 0;
}
.topbar-brand {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
}
.topbar-logo {
  font-family: var(--fD);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--snow);
  letter-spacing: -0.01em;
}
.topbar-logo em {
  font-style: italic;
  color: var(--accent);
}
.topbar-sep {
  width: 1px; height: 18px;
  background: var(--border2);
  display: inline-block;
}
.topbar-subtitle {
  font-family: var(--fM);
  font-size: 0.6rem;
  color: var(--mist);
  letter-spacing: 0.12em;
  text-transform: uppercase;
}
.topbar-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}
.topbar-stat {
  text-align: right;
}
.topbar-stat-val {
  font-family: var(--fM);
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--snow2);
  display: block;
}
.topbar-stat-key {
  font-family: var(--fM);
  font-size: 0.52rem;
  color: var(--mist);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}
.topbar-stat-val.gold { color: var(--accent); }
.topbar-divider { width: 1px; height: 28px; background: var(--border); }

/* ── Page header ── */
.pg {
  padding: 1.75rem 0 1.5rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 1.75rem;
}
.pg-step {
  font-family: var(--fM);
  font-size: 0.58rem;
  color: var(--accent);
  text-transform: uppercase;
  letter-spacing: 0.2em;
  margin-bottom: 0.5rem;
}
.pg-h1 {
  font-family: var(--fD);
  font-size: 2rem;
  font-weight: 700;
  color: var(--snow);
  line-height: 1.1;
  letter-spacing: -0.02em;
}
.pg-h1 em { font-style: italic; color: var(--accent2); }
.pg-desc {
  font-family: var(--fS);
  font-size: 0.82rem;
  color: var(--mist2);
  margin-top: 0.5rem;
  line-height: 1.6;
  max-width: 620px;
}

/* ── Section header ── */
.sh {
  font-family: var(--fM);
  font-size: 0.58rem;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  color: var(--mist);
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.sh-acc { color: var(--accent); }

/* ── Metric cards ── */
.mc-row {
  display: grid;
  gap: 1px;
  background: var(--border);
  border: 1px solid var(--border);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 1.75rem;
}
.mc-row-4 { grid-template-columns: repeat(4, 1fr); }
.mc-row-5 { grid-template-columns: repeat(5, 1fr); }
.mc-row-3 { grid-template-columns: repeat(3, 1fr); }
.mc {
  background: var(--panel);
  padding: 1rem 1.25rem;
}
.mc-val {
  font-family: var(--fD);
  font-size: 1.9rem;
  font-weight: 700;
  color: var(--snow);
  line-height: 1;
  margin-bottom: 0.3rem;
}
.mc-val.gold { color: var(--accent); }
.mc-val.green { color: var(--green); }
.mc-val.red { color: var(--red); }
.mc-val.blue { color: var(--blue); }
.mc-key {
  font-family: var(--fM);
  font-size: 0.55rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--mist);
}

/* ── Paper card ── */
.pcard {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 1.1rem 1.4rem;
  margin-bottom: 0.5rem;
  transition: border-color 0.15s;
  position: relative;
}
.pcard:hover { border-color: var(--border2); }
.pcard-type {
  font-family: var(--fM);
  font-size: 0.52rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--mist);
  background: var(--panel2);
  border: 1px solid var(--border);
  padding: 2px 7px;
  border-radius: 2px;
  display: inline-block;
  margin-bottom: 0.5rem;
}
.pcard-title {
  font-family: var(--fD);
  font-size: 0.96rem;
  font-weight: 600;
  color: var(--snow);
  line-height: 1.4;
  margin-bottom: 0.3rem;
}
.pcard-meta {
  font-family: var(--fM);
  font-size: 0.6rem;
  color: var(--mist);
  letter-spacing: 0.04em;
  margin-bottom: 0.6rem;
}
.pcard-abstract {
  font-family: var(--fS);
  font-size: 0.8rem;
  color: var(--mist2);
  line-height: 1.75;
  max-height: 120px;
  overflow: hidden;
  position: relative;
}
.pcard-abstract::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 40px;
  background: linear-gradient(transparent, var(--panel));
}
.hl { background: rgba(232,184,75,0.2); color: var(--accent2); border-radius: 2px; padding: 0 2px; }

/* Decision strip */
.pcard-inc { border-left: 3px solid var(--green); }
.pcard-exc { border-left: 3px solid var(--red); }
.pcard-may { border-left: 3px solid var(--accent); }

/* ── Status pills ── */
.pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-family: var(--fM);
  font-size: 0.58rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 3px 9px;
  border-radius: 2px;
}
.pill-inc { background: var(--green-bg); color: var(--green); border: 1px solid rgba(93,168,122,0.3); }
.pill-exc { background: var(--red-bg);   color: var(--red);   border: 1px solid rgba(217,83,79,0.3); }
.pill-may { background: var(--accent-bg); color: var(--accent); border: 1px solid rgba(232,184,75,0.3); }
.pill-pnd { background: var(--panel);    color: var(--mist);  border: 1px solid var(--border); }
.pill-hq  { background: var(--green-bg); color: var(--green); border: 1px solid rgba(93,168,122,0.3); }
.pill-mq  { background: var(--accent-bg); color: var(--accent); border: 1px solid rgba(232,184,75,0.3); }
.pill-lq  { background: var(--red-bg);   color: var(--red);   border: 1px solid rgba(217,83,79,0.3); }

/* ── Sidebar ── */
.sb-logo-wrap { padding: 1.4rem 1.25rem 1rem; border-bottom: 1px solid var(--border); }
.sb-logotype {
  font-family: var(--fD);
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--snow);
  letter-spacing: -0.01em;
}
.sb-logotype em { font-style: italic; color: var(--accent); }
.sb-tagline { font-family: var(--fM); font-size: 0.52rem; color: var(--mist); text-transform: uppercase; letter-spacing: 0.14em; margin-top: 0.2rem; }
.sb-dev { font-family: var(--fM); font-size: 0.52rem; color: var(--border2); margin-top: 0.25rem; letter-spacing: 0.06em; }
.sb-dev b { color: var(--mist); font-weight: 400; }

.sb-nav-section { padding: 0.9rem 1.25rem 0.3rem; font-family: var(--fM); font-size: 0.5rem; text-transform: uppercase; letter-spacing: 0.18em; color: var(--border2); }

.sb-stats { padding: 1rem 1.25rem; border-top: 1px solid var(--border); }
.sb-stat-row { display: flex; justify-content: space-between; align-items: center; padding: 0.22rem 0; }
.sb-stat-key { font-family: var(--fM); font-size: 0.56rem; color: var(--mist); text-transform: uppercase; letter-spacing: 0.08em; }
.sb-stat-val { font-family: var(--fM); font-size: 0.7rem; color: var(--snow2); }
.sb-stat-val.gold { color: var(--accent); }
.sb-prog { height: 1px; background: var(--border); margin: 0.6rem 0 0.3rem; overflow: hidden; }
.sb-prog-fill { height: 100%; background: var(--accent); transition: width 0.4s; }
.sb-pct { font-family: var(--fM); font-size: 0.52rem; color: var(--mist); display: flex; justify-content: space-between; }

/* ── Import items ── */
.import-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 0.6rem 0.9rem;
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 3px;
  margin-bottom: 0.35rem;
}
.import-fn { font-family: var(--fM); font-size: 0.68rem; color: var(--snow2); }
.import-src { font-family: var(--fM); font-size: 0.56rem; color: var(--mist); margin-top: 0.1rem; }
.import-n { font-family: var(--fD); font-size: 1.1rem; font-weight: 600; color: var(--accent); }

/* ── PRISMA boxes ── */
.prisma-flow { display: flex; flex-direction: column; align-items: center; gap: 0; }
.prisma-box {
  background: var(--panel);
  border: 1px solid var(--border2);
  border-radius: 4px;
  padding: 0.85rem 2rem;
  text-align: center;
  min-width: 300px;
  position: relative;
}
.prisma-box.blue-acc  { border-top: 3px solid var(--blue); }
.prisma-box.gold-acc  { border-top: 3px solid var(--accent); }
.prisma-box.purple-acc{ border-top: 3px solid #9B7FCC; }
.prisma-box.green-acc { border-top: 3px solid var(--green); }
.prisma-n   { font-family: var(--fD); font-size: 2rem; font-weight: 700; color: var(--snow); }
.prisma-lbl { font-family: var(--fM); font-size: 0.56rem; text-transform: uppercase; letter-spacing: 0.12em; color: var(--mist); margin-bottom: 0.2rem; }
.prisma-sub { font-family: var(--fS); font-size: 0.72rem; color: var(--mist2); margin-top: 0.1rem; }
.prisma-arrow { font-size: 1.1rem; color: var(--border2); padding: 0.3rem 0; }
.prisma-row { display: flex; align-items: center; gap: 0.75rem; }
.prisma-branch {
  background: var(--red-bg);
  border: 1px solid rgba(217,83,79,0.25);
  border-radius: 3px;
  padding: 0.5rem 0.9rem;
  font-family: var(--fM);
  font-size: 0.62rem;
  color: var(--red);
  text-align: center;
  min-width: 130px;
  line-height: 1.5;
}
.prisma-line { width: 1.5rem; height: 1px; background: var(--border2); flex-shrink: 0; }

/* ── Empty state ── */
.empty-st {
  text-align: center;
  padding: 4rem 2rem;
  border: 1px dashed var(--border);
  border-radius: 4px;
  margin: 1rem 0;
}
.empty-glyph { font-family: var(--fD); font-size: 3rem; color: var(--border2); margin-bottom: 0.75rem; font-style: italic; }
.empty-title { font-family: var(--fD); font-size: 1.1rem; color: var(--mist2); margin-bottom: 0.4rem; }
.empty-sub   { font-family: var(--fM); font-size: 0.62rem; color: var(--border2); text-transform: uppercase; letter-spacing: 0.1em; }

/* ── Keyword tags ── */
.kw-tag { display: inline-block; font-family: var(--fM); font-size: 0.58rem; color: var(--mist); background: var(--panel2); border: 1px solid var(--border); padding: 2px 8px; border-radius: 2px; margin: 2px; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PARSERS (logic unchanged)
# ══════════════════════════════════════════════════════════════

def _rec(i, doc_type, title, authors, year, journal, abstract, doi, url, keywords, volume, local_file):
    return {"id": f"P{str(i+1).zfill(3)}", "doc_type": doc_type, "title": title.strip(),
            "authors": authors, "year": year, "journal": journal, "abstract": abstract.strip(),
            "doi": doi, "url": url, "keywords": keywords, "volume": volume, "local_file": local_file,
            "title_decision": None, "abstract_decision": None, "exclusion_reason": "",
            "study_location": "", "methodology": "", "dataset": "",
            "policy_implication": "", "key_findings": "",
            "qa_obj": 0, "qa_method": 0, "qa_data": 0, "qa_bias": 0, "qa_rel": 0}

def parse_ris(content):
    records_raw, current, last_tag = [], {}, None
    for line in content.splitlines():
        if line.startswith("ER  -"):
            if current: records_raw.append(current)
            current, last_tag = {}, None; continue
        m = re.match(r'^([A-Z0-9]{2})\s{2}-\s*(.*)', line)
        if m:
            tag, value = m.group(1), m.group(2).strip(); last_tag = tag
        elif line.startswith("  ") and last_tag and current:
            if last_tag in ("N2","AB","N1","T1"):
                current[last_tag] = current.get(last_tag,"") + " " + line.strip()
            continue
        else: continue
        if   tag == "TY":             current["TY"] = value
        elif tag in ("T1","TI"):      current.setdefault("T1", value)
        elif tag in ("A1","AU"):      current.setdefault("authors",[]).append(value)
        elif tag in ("Y1","PY"):
            m2 = re.match(r'(\d{4})', value)
            if m2: current["year"] = int(m2.group(1))
        elif tag in ("JF","JO","J1","T2"): current.setdefault("JF", value)
        elif tag in ("N2","AB"):      current["N2"] = current.get("N2","") + value
        elif tag == "N1":             current["N1"] = current.get("N1","") + value
        elif tag == "DO":             current["DO"] = value
        elif tag in ("UR","LK"):      current.setdefault("UR", value)
        elif tag == "KW":             current.setdefault("KW",[]).append(value)
        elif tag == "PB":             current.setdefault("PB", value)
        elif tag == "CY":             current.setdefault("CY", value)
        elif tag == "VL":             current["VL"] = value
        elif tag == "L1":             current["L1"] = value.replace("file:///","")
    if current: records_raw.append(current)
    tf = {"RPRT":"Report","ICOMM":"Web/Comm.","HEAR":"Hearing","CONF":"Conference"}
    out = []
    for i, r in enumerate(records_raw):
        title = r.get("T1","").strip()
        if not title: continue
        dt = r.get("TY","JOUR")
        out.append(_rec(i, dt, title, "; ".join(r.get("authors",[])), r.get("year",""),
            r.get("JF") or r.get("PB") or r.get("CY") or tf.get(dt,""),
            (r.get("N2") or r.get("N1") or "").strip(),
            r.get("DO",""), r.get("UR",""), "; ".join(r.get("KW",[])), r.get("VL",""), r.get("L1","")))
    return out, f"Parsed {len(out)} records"

def parse_bib(content):
    entries = re.findall(r'@\w+\s*\{[^@]+', content, re.DOTALL)
    tm = {"article":"JOUR","inproceedings":"CONF","book":"BOOK","techreport":"RPRT","misc":"MISC","incollection":"CHAP"}
    def gf(entry, name):
        m = re.search(rf'\b{name}\s*=\s*\{{((?:[^{{}}]|\{{[^{{}}]*\}})*)\}}', entry, re.IGNORECASE|re.DOTALL)
        if m: return re.sub(r'\{([^{}]*)\}', r'\1', m.group(1)).strip()
        m = re.search(rf'\b{name}\s*=\s*"([^"]*)"', entry, re.IGNORECASE|re.DOTALL)
        return m.group(1).strip() if m else ""
    out = []
    for i, entry in enumerate(entries):
        tm2 = re.match(r'@(\w+)\s*\{', entry)
        if not tm2: continue
        dt = tm.get(tm2.group(1).lower(), tm2.group(1).upper())
        title = gf(entry,"title")
        if not title: continue
        ys = gf(entry,"year"); year = int(ys) if ys.isdigit() else ys
        out.append(_rec(i, dt, title, gf(entry,"author"), year,
            gf(entry,"journal") or gf(entry,"booktitle") or gf(entry,"publisher"),
            gf(entry,"abstract"), gf(entry,"doi"), gf(entry,"url"),
            gf(entry,"keywords") or gf(entry,"keyword"), gf(entry,"volume"), ""))
    return out, f"Parsed {len(out)} records"

def parse_csv_file(content):
    try: df = pd.read_csv(io.StringIO(content), dtype=str).fillna("")
    except Exception as e: return [], f"CSV error: {e}"
    cols = list(df.columns)
    def fc(als): return next((a for a in als if a in cols), None)
    cm = {"title": fc(["TI","Title","Article Title","title"]),
          "authors": fc(["AU","Authors","AF","authors"]),
          "year": fc(["PY","Year","Publication Year","year"]),
          "journal": fc(["SO","Source Title","Journal","journal"]),
          "abstract": fc(["AB","Abstract","abstract"]),
          "doi": fc(["DI","DOI","doi"]),
          "keywords": fc(["DE","Author Keywords","Keywords","ID","keywords"])}
    out = []
    for i, row in df.iterrows():
        t = row.get(cm["title"] or "__","").strip()
        if not t: continue
        ys = row.get(cm["year"] or "__","")
        try: year = int(str(ys).strip())
        except: year = ys
        out.append(_rec(i,"JOUR",t, row.get(cm["authors"] or "__",""), year,
            row.get(cm["journal"] or "__",""), row.get(cm["abstract"] or "__",""),
            row.get(cm["doi"] or "__",""), "", row.get(cm["keywords"] or "__",""),"",""))
    return out, f"Parsed {len(out)} records"

def parse_file(uf):
    name = uf.name.lower()
    try: raw = uf.read().decode("utf-8", errors="replace")
    except Exception as e: return [], f"Cannot read: {e}"
    if name.endswith(".ris"):   return parse_ris(raw)
    elif name.endswith(".bib"): return parse_bib(raw)
    elif name.endswith(".csv"): return parse_csv_file(raw)
    elif name.endswith(".txt"):
        return parse_csv_file(raw.replace("\t",",")) if raw.count("\t")>10 else parse_ris(raw)
    return [], "Unsupported format — use .ris .bib .csv .txt"


# ══════════════════════════════════════════════════════════════
# STATE
# ══════════════════════════════════════════════════════════════
for k, v in [("papers",[]),("keywords",["hydrogen","workforce","skills","green jobs","energy transition"]),
              ("current_tab",0),("import_log",[]),("dup_results",[])]:
    if k not in st.session_state: st.session_state[k] = v


# ══════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════
def upd(pid, f, v):
    for p in st.session_state.papers:
        if p["id"]==pid: p[f]=v; break

def ti():  return [p for p in st.session_state.papers if p.get("title_decision")=="include"]
def ab():  return [p for p in st.session_state.papers if p.get("abstract_decision")=="include"]
def ex():  return [p for p in ab() if p.get("key_findings")]

def qs(p): return sum(p.get(k,0) for k in ["qa_obj","qa_method","qa_data","qa_bias","qa_rel"])
def ql(s):
    if s>=8:   return "High",   "pill-hq"
    elif s>=5: return "Medium", "pill-mq"
    else:      return "Low",    "pill-lq"

def hltext(text, kws):
    if not text: return str(text)
    r = str(text)
    for kw in kws:
        if kw.strip(): r = re.compile(re.escape(kw.strip()), re.IGNORECASE).sub(f'<span class="hl">{kw}</span>', r)
    return r

DTL = {"JOUR":"Journal","RPRT":"Report","ICOMM":"Web","HEAR":"Hearing","CONF":"Conf.","BOOK":"Book","CHAP":"Chapter","MISC":"Misc."}
EXCL = ["— select —","not empirical","not relevant topic","review article","wrong population","wrong study design","grey literature","language barrier","duplicate"]

def sh(label, accent=""):
    acc_html = f'<span class="sh-acc">{accent}</span>' if accent else ""
    st.markdown(f'<div class="sh">{acc_html}{label}</div>', unsafe_allow_html=True)

def pg(step, title_plain, title_em="", desc=""):
    em_part = f"<em>{title_em}</em>" if title_em else ""
    st.markdown(f"""
    <div class="pg">
      <div class="pg-step">{step}</div>
      <div class="pg-h1">{title_plain}{em_part}</div>
      {"<div class='pg-desc'>"+desc+"</div>" if desc else ""}
    </div>""", unsafe_allow_html=True)

def empty_st(title="No data loaded", sub="Go to Import and upload your reference file"):
    st.markdown(f"""
    <div class="empty-st">
      <div class="empty-glyph">◈</div>
      <div class="empty-title">{title}</div>
      <div class="empty-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

def mc_row(items, cols=4):
    cls = f"mc-row mc-row-{min(cols,5)}"
    inner = "".join([f'<div class="mc"><div class="mc-val {c}">{v}</div><div class="mc-key">{k}</div></div>' for k,v,c in items])
    st.markdown(f'<div class="{cls}">{inner}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
papers = st.session_state.papers
n_total = len(papers)
n_ti, n_ab, n_ex = len(ti()), len(ab()), len(ex())

with st.sidebar:
    st.markdown(f"""
    <div class="sb-logo-wrap">
      <div class="sb-logotype">SLR<em>·</em>Studio</div>
      <div class="sb-tagline">Systematic Literature Review</div>
      <div class="sb-dev">by <b>Bahas Kebijakan</b></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-nav-section">— Workflow</div>', unsafe_allow_html=True)

    NAV = [("01","Import"),("02","Deduplicate"),("03","Title Screen"),("04","Abstract Screen"),
           ("05","Full Text"),("06","Data Extraction"),("07","Quality Assess."),
           ("08","Evidence Synthesis"),("09","PRISMA Diagram"),("10","Export")]
    CNTS = [f"{n_total} records" if n_total else "empty", "",
            f"{len([p for p in papers if not p.get('title_decision')])} pending",
            f"{len([p for p in ti() if not p.get('abstract_decision')])} pending",
            f"{n_ti} papers", f"{n_ab} eligible", f"{n_ex} ready", "", "", ""]

    for i,(step,label) in enumerate(NAV):
        cnt = CNTS[i]
        lbl = f"{step}  {label}  ·  {cnt}" if cnt else f"{step}  {label}"
        if st.button(lbl, key=f"nav_{i}", use_container_width=True):
            st.session_state.current_tab = i; st.rerun()

    pct = int((n_ab/n_total)*100) if n_total else 0
    st.markdown(f"""
    <div class="sb-stats">
      <div class="sb-stat-row"><span class="sb-stat-key">Records</span><span class="sb-stat-val">{n_total}</span></div>
      <div class="sb-stat-row"><span class="sb-stat-key">Title Incl.</span><span class="sb-stat-val">{n_ti}</span></div>
      <div class="sb-stat-row"><span class="sb-stat-key">Final Incl.</span><span class="sb-stat-val gold">{n_ab}</span></div>
      <div class="sb-stat-row"><span class="sb-stat-key">Extracted</span><span class="sb-stat-val">{n_ex}</span></div>
      <div class="sb-prog"><div class="sb-prog-fill" style="width:{pct}%"></div></div>
      <div class="sb-pct"><span>Review Progress</span><span>{pct}%</span></div>
    </div>
    <div style="padding:.4rem 1.25rem .75rem;font-family:'Space Mono',monospace;font-size:.5rem;color:var(--border2);text-transform:uppercase;letter-spacing:.12em;">
      PRISMA 2020 Compliant
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# TOP BAR (inside main area)
# ══════════════════════════════════════════════════════════════
tab = st.session_state.current_tab
papers = st.session_state.papers

st.markdown(f"""
<div class="topbar">
  <div class="topbar-brand">
    <span class="topbar-logo">SLR<em>·</em>Studio</span>
    <span class="topbar-sep"></span>
    <span class="topbar-subtitle">Bahas Kebijakan · PRISMA 2020</span>
  </div>
  <div class="topbar-right">
    <div class="topbar-stat">
      <span class="topbar-stat-val">{n_total}</span>
      <span class="topbar-stat-key">Records</span>
    </div>
    <div class="topbar-divider"></div>
    <div class="topbar-stat">
      <span class="topbar-stat-val">{n_ti}</span>
      <span class="topbar-stat-key">Title Incl.</span>
    </div>
    <div class="topbar-divider"></div>
    <div class="topbar-stat">
      <span class="topbar-stat-val gold">{n_ab}</span>
      <span class="topbar-stat-key">Final Incl.</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE 0 — IMPORT
# ══════════════════════════════════════════════════════════════
if tab == 0:
    pg("Module 01", "Data ", "Import",
       "Import and standardise reference records from Mendeley, Zotero, Scopus, Web of Science, or any PRISMA-compatible export.")

    n_jour = len([p for p in papers if p.get("doc_type")=="JOUR"])
    n_rpt  = len([p for p in papers if p.get("doc_type") not in ("JOUR","")])
    mc_row([("Total Records", n_total, ""),("Journal Articles", n_jour, "blue"),
            ("Reports & Other", n_rpt, ""),("Sources Loaded", len(st.session_state.import_log), "gold")], 4)

    col_l, col_r = st.columns([1.4, 1], gap="large")

    with col_l:
        sh("Upload Reference File", "◈ ")
        src = st.selectbox("Source database", ["Mendeley (.ris)","Zotero (.ris / .bib)",
              "Scopus (.bib / .csv)","Web of Science (.txt / .csv)","Dimensions (.bib)","EndNote (.ris)"])
        uf = st.file_uploader("Drop file — .ris · .bib · .csv · .txt", type=["ris","bib","csv","txt"])

        if uf:
            st.success(f"**{uf.name}** — {uf.size/1024:.1f} KB detected")
            b1, b2 = st.columns(2)
            with b1:
                if st.button("Add to Library", use_container_width=True):
                    with st.spinner("Parsing…"):
                        recs, msg = parse_file(uf)
                    if recs:
                        off = len(st.session_state.papers)
                        for j,r in enumerate(recs): r["id"] = f"P{str(off+j+1).zfill(3)}"
                        st.session_state.papers.extend(recs)
                        st.session_state.import_log.append({"file":uf.name,"source":src,"n":len(recs),"time":datetime.now().strftime("%H:%M")})
                        st.success(f"✓ {msg}"); st.rerun()
                    else: st.error(msg)
            with b2:
                if st.button("Replace All", use_container_width=True):
                    with st.spinner("Parsing…"):
                        recs, msg = parse_file(uf)
                    if recs:
                        st.session_state.papers = recs
                        st.session_state.import_log = [{"file":uf.name,"source":src,"n":len(recs),"time":datetime.now().strftime("%H:%M")}]
                        st.success(f"✓ {msg}"); st.rerun()
                    else: st.error(msg)

        if papers:
            if st.button("Clear All Records", use_container_width=True):
                st.session_state.papers = []; st.session_state.import_log = []; st.rerun()

        if papers:
            st.markdown("&nbsp;", unsafe_allow_html=True)
            sh("Keyword Highlights", "◈ ")
            kw_new = st.text_input("Add keyword", placeholder="e.g. hydrogen, workforce…")
            if st.button("Add", use_container_width=True):
                if kw_new.strip() and kw_new.strip() not in st.session_state.keywords:
                    st.session_state.keywords.append(kw_new.strip()); st.rerun()
            if st.session_state.keywords:
                kw_html = " ".join([f'<span class="kw-tag">{k}</span>' for k in st.session_state.keywords])
                st.markdown(kw_html, unsafe_allow_html=True)
                rm = st.selectbox("Remove keyword", ["— keep all —"] + st.session_state.keywords)
                if rm != "— keep all —":
                    st.session_state.keywords.remove(rm); st.rerun()

    with col_r:
        sh("Import Log", "◈ ")
        if st.session_state.import_log:
            for lg in st.session_state.import_log:
                st.markdown(f"""
                <div class="import-row">
                  <div>
                    <div class="import-fn">{lg['file']}</div>
                    <div class="import-src">{lg['source']} · {lg['time']}</div>
                  </div>
                  <div class="import-n">{lg['n']}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div style="font-family:\'Space Mono\',monospace;font-size:.65rem;color:var(--border2);padding:.5rem 0;">No imports yet — upload a file to begin.</div>', unsafe_allow_html=True)

        st.markdown("&nbsp;", unsafe_allow_html=True)
        sh("Supported Formats", "◈ ")
        st.markdown("""
| Format | Sources |
|--------|---------|
| `.ris` | Mendeley, Zotero, EndNote |
| `.bib` | Scopus, Dimensions, Zotero |
| `.csv` | Web of Science, Scopus |
| `.txt` | Web of Science (ISI / tab-sep.) |
        """)

    if papers:
        st.markdown("&nbsp;", unsafe_allow_html=True)
        sh("Records Preview", "◈ ")
        prev = pd.DataFrame([{
            "ID": p["id"],
            "Type": DTL.get(p.get("doc_type",""), p.get("doc_type","")),
            "Title": p["title"][:72]+"…" if len(p.get("title",""))>72 else p.get("title",""),
            "Authors": p.get("authors","")[:40]+"…" if len(p.get("authors",""))>40 else p.get("authors",""),
            "Year": p.get("year",""),
            "Source": p.get("journal","")[:38]+"…" if len(p.get("journal",""))>38 else p.get("journal",""),
            "DOI": "✓" if p.get("doi") else "—",
            "Abstract": "✓" if p.get("abstract") else "—",
        } for p in papers])
        st.dataframe(prev, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════
# PAGE 1 — DEDUPLICATION
# ══════════════════════════════════════════════════════════════
elif tab == 1:
    pg("Module 02", "De", "duplication",
       "Identify and remove duplicate records by exact DOI match and fuzzy title similarity.")

    if not papers:
        empty_st(); st.stop()

    def find_dups(records, doi_m, title_s, thresh):
        from difflib import SequenceMatcher
        dups, seen_doi, seen_title = [], {}, {}
        for p in records:
            found = False
            if doi_m and p.get("doi"):
                doi = p["doi"].strip().lower()
                if doi in seen_doi:
                    dups.append({"Method":"DOI exact","Keep":seen_doi[doi],"Remove":p["id"],"Score":"1.00"}); found=True
                else: seen_doi[doi] = p["id"]
            if not found and title_s and p.get("title"):
                tn = re.sub(r'[^\w\s]','', p["title"].lower().strip())
                for pt, pid in seen_title.items():
                    r2 = SequenceMatcher(None, tn, pt).ratio()
                    if r2 >= thresh:
                        dups.append({"Method":f"Title ({r2:.2f})","Keep":pid,"Remove":p["id"],"Score":f"{r2:.2f}"}); found=True; break
                if not found: seen_title[tn] = p["id"]
        return dups

    mc_row([("Before Deduplication", n_total, ""),
            ("Duplicates Found", len(st.session_state.dup_results), "red" if st.session_state.dup_results else ""),
            ("Unique Records", n_total - len(st.session_state.dup_results), "green")], 3)

    col_l, col_r = st.columns(2, gap="large")
    with col_l:
        sh("Detection Settings", "◈ ")
        doi_m = st.checkbox("DOI exact match", value=True)
        title_s = st.checkbox("Title similarity matching", value=True)
        thresh = st.slider("Similarity threshold", 0.70, 1.00, 0.90, 0.05) if title_s else 0.90
        if st.button("Run Deduplication", use_container_width=True):
            st.session_state.dup_results = find_dups(papers, doi_m, title_s, thresh)
            st.rerun()

    with col_r:
        sh("Duplicate Log", "◈ ")
        dups = st.session_state.dup_results
        if dups:
            st.dataframe(pd.DataFrame(dups), use_container_width=True, hide_index=True)
            if st.button(f"Remove {len(dups)} duplicate(s)", use_container_width=True):
                ids_rm = {d["Remove"] for d in dups}
                st.session_state.papers = [p for p in papers if p["id"] not in ids_rm]
                st.session_state.dup_results = []
                st.success(f"✓ Removed {len(ids_rm)} records"); st.rerun()
        else:
            st.info("Run deduplication to detect duplicates.")


# ══════════════════════════════════════════════════════════════
# PAGE 2 — TITLE SCREENING
# ══════════════════════════════════════════════════════════════
elif tab == 2:
    pg("Module 03", "Title ", "Screening",
       "First-pass relevance screening. Include, exclude, or flag papers based on title alone.")

    if not papers:
        empty_st(); st.stop()

    n_inc  = len([p for p in papers if p.get("title_decision")=="include"])
    n_exc  = len([p for p in papers if p.get("title_decision")=="exclude"])
    n_may  = len([p for p in papers if p.get("title_decision")=="maybe"])
    n_pend = len([p for p in papers if not p.get("title_decision")])

    mc_row([("Total",n_total,""),("Included",n_inc,"green"),("Excluded",n_exc,"red"),("Maybe",n_may,"gold"),("Pending",n_pend,"")], 5)

    fc, sc = st.columns([1,2], gap="medium")
    with fc:
        show_f = st.selectbox("Filter", ["All","Pending","Included","Excluded","Maybe"])
    with sc:
        q = st.text_input("Search", placeholder="Filter by title keyword…", label_visibility="collapsed")

    filtered = papers
    if show_f == "Pending":   filtered = [p for p in papers if not p.get("title_decision")]
    elif show_f == "Included": filtered = [p for p in papers if p.get("title_decision")=="include"]
    elif show_f == "Excluded": filtered = [p for p in papers if p.get("title_decision")=="exclude"]
    elif show_f == "Maybe":    filtered = [p for p in papers if p.get("title_decision")=="maybe"]
    if q: filtered = [p for p in filtered if q.lower() in p.get("title","").lower()]

    st.caption(f"{len(filtered)} of {len(papers)} records")
    st.markdown("---")

    for p in filtered:
        dec_class = {"include":"pcard-inc","exclude":"pcard-exc","maybe":"pcard-may"}.get(p.get("title_decision",""),"")
        badge = DTL.get(p.get("doc_type",""), p.get("doc_type","?"))
        hl_t = hltext(p.get("title",""), st.session_state.keywords)

        ci, cd = st.columns([4,2])
        with ci:
            st.markdown(f"""
            <div class="pcard {dec_class}">
              <span class="pcard-type">{badge}</span>
              <div class="pcard-title">{hl_t}</div>
              <div class="pcard-meta">{p['id']} · {p.get('authors','—')[:55]} · {p.get('year','?')} · {p.get('journal','—')[:50]}</div>
            </div>""", unsafe_allow_html=True)
        with cd:
            cur = p.get("title_decision") or "include"
            opts = ["include","exclude","maybe"]
            dec = st.radio("", opts, index=opts.index(cur) if cur in opts else 0,
                           horizontal=True, key=f"td_{p['id']}", label_visibility="collapsed")
            if dec != p.get("title_decision"):
                upd(p["id"],"title_decision",dec); st.rerun()
        st.markdown('<hr style="margin:.35rem 0;">', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE 3 — ABSTRACT SCREENING
# ══════════════════════════════════════════════════════════════
elif tab == 3:
    pg("Module 04", "Abstract ", "Screening",
       "Full eligibility assessment. Read abstracts and apply inclusion/exclusion criteria.")

    title_passed = ti()
    if not title_passed:
        empty_st("No papers passed title screening", "Complete Title Screening first"); st.stop()

    n_el  = len(ab())
    n_exc = len([p for p in title_passed if p.get("abstract_decision")=="exclude"])
    n_pe  = len([p for p in title_passed if not p.get("abstract_decision")])

    mc_row([("From Title Screen",len(title_passed),""),("Eligible",n_el,"green"),
            ("Excluded",n_exc,"red"),("Pending",n_pe,"")], 4)

    show_f = st.selectbox("Filter", ["All","Pending","Included","Excluded"])
    filtered = title_passed
    if show_f == "Pending":  filtered = [p for p in title_passed if not p.get("abstract_decision")]
    elif show_f == "Included": filtered = [p for p in title_passed if p.get("abstract_decision")=="include"]
    elif show_f == "Excluded": filtered = [p for p in title_passed if p.get("abstract_decision")=="exclude"]

    st.markdown("---")

    for p in filtered:
        dec_class = {"include":"pcard-inc","exclude":"pcard-exc","maybe":"pcard-may"}.get(p.get("abstract_decision",""),"")
        abs_text = p.get("abstract","") or "_No abstract available for this record._"
        hl_t = hltext(p.get("title",""), st.session_state.keywords)
        hl_a = hltext(abs_text, st.session_state.keywords)
        badge = DTL.get(p.get("doc_type",""), p.get("doc_type","?"))

        st.markdown(f"""
        <div class="pcard {dec_class}">
          <span class="pcard-type">{badge}</span>
          <div class="pcard-title">{hl_t}</div>
          <div class="pcard-meta">{p['id']} · {p.get('authors','—')[:60]} · {p.get('year','?')} · {p.get('journal','—')}</div>
          <div class="pcard-abstract">{hl_a}</div>
        </div>""", unsafe_allow_html=True)

        cd, cr, ck = st.columns([2,2,2])
        with cd:
            cur = p.get("abstract_decision") or "include"
            opts = ["include","exclude","maybe"]
            dec = st.radio("", opts, index=opts.index(cur) if cur in opts else 0,
                           horizontal=True, key=f"ad_{p['id']}", label_visibility="collapsed")
            if dec != p.get("abstract_decision"):
                upd(p["id"],"abstract_decision",dec); st.rerun()
        with cr:
            if p.get("abstract_decision") == "exclude":
                cur_r = p.get("exclusion_reason","")
                ri = EXCL.index(cur_r) if cur_r in EXCL else 0
                reason = st.selectbox("Reason", EXCL, index=ri, key=f"er_{p['id']}", label_visibility="collapsed")
                if reason != "— select —" and reason != p.get("exclusion_reason"):
                    upd(p["id"],"exclusion_reason",reason)
        with ck:
            if p.get("keywords"):
                kws = [k.strip() for k in re.split(r'[;,]', p["keywords"]) if k.strip()][:5]
                st.markdown(" ".join([f'<span class="kw-tag">{k}</span>' for k in kws]), unsafe_allow_html=True)
        st.markdown('<hr style="margin:.4rem 0;">', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE 4 — FULL TEXT
# ══════════════════════════════════════════════════════════════
elif tab == 4:
    pg("Module 05", "Full Text ", "Library",
       "Manage and annotate full-text documents for included papers.")

    abs_inc = ab()
    if not abs_inc:
        empty_st("No papers passed abstract screening", "Complete Abstract Screening first"); st.stop()

    mc_row([("Eligible Papers", len(abs_inc),"gold"),("With Mendeley Path",len([p for p in abs_inc if p.get("local_file")]),"green"),("Awaiting Upload",len([p for p in abs_inc if not p.get("local_file")]),"")], 3)

    col_l, col_r = st.columns(2, gap="large")
    with col_l:
        sh("Upload PDFs", "◈ ")
        pdfs = st.file_uploader("Upload PDF files (multiple allowed)", type=["pdf"], accept_multiple_files=True)
        if pdfs:
            st.success(f"✓ {len(pdfs)} PDF(s) uploaded this session")
        else:
            st.caption("PDFs are not stored between sessions. Re-upload each time.")
    with col_r:
        sh("Eligible Papers List", "◈ ")

    st.markdown("&nbsp;", unsafe_allow_html=True)
    ft = pd.DataFrame([{"ID":p["id"],"Title":p["title"][:65]+"…" if len(p.get("title",""))>65 else p.get("title",""),
        "Year":p.get("year",""),"Source":p.get("journal","")[:40],"DOI":p.get("doi","—"),
        "Path":"✓" if p.get("local_file") else "—"} for p in abs_inc])
    st.dataframe(ft, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════
# PAGE 5 — DATA EXTRACTION
# ══════════════════════════════════════════════════════════════
elif tab == 5:
    pg("Module 06", "Data ", "Extraction",
       "Structured extraction of study characteristics: location, methodology, dataset, findings, and policy implications.")

    abs_inc = ab()
    if not abs_inc:
        empty_st("No papers passed abstract screening", "Complete Abstract Screening first"); st.stop()

    n_done = len([p for p in abs_inc if p.get("key_findings")])
    mc_row([("Eligible",len(abs_inc),""),("Extracted",n_done,"green"),("Pending",len(abs_inc)-n_done,"")], 3)

    vt, et = st.tabs(["TABLE VIEW","EXTRACT / EDIT"])

    with vt:
        rows = [{"ID":p["id"],"Year":p.get("year",""),
            "Title":p["title"][:55]+"…" if len(p.get("title",""))>55 else p.get("title",""),
            "Country":p.get("study_location") or "—","Method":p.get("methodology") or "—",
            "Dataset":p.get("dataset") or "—",
            "Key Findings":(p.get("key_findings") or "—")[:80]+"…" if len(p.get("key_findings",""))>80 else (p.get("key_findings") or "—"),
            "Status":"✓" if p.get("key_findings") else "·"} for p in abs_inc]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    with et:
        opts = [f"{p['id']}  —  {p['title'][:60]}…" for p in abs_inc]
        sel = st.selectbox("Select paper to extract", opts)
        p = abs_inc[opts.index(sel)]
        badge = DTL.get(p.get("doc_type",""), p.get("doc_type","?"))
        st.markdown(f"""
        <div class="pcard">
          <span class="pcard-type">{badge}</span>
          <div class="pcard-title">{p.get('title','')}</div>
          <div class="pcard-meta">{p.get('authors','—')[:70]} · {p.get('year','?')} · {p.get('journal','—')}</div>
          <div class="pcard-abstract" style="max-height:80px;">{p.get('abstract','No abstract available.')[:350]}…</div>
        </div>""", unsafe_allow_html=True)

        with st.form(f"ex_{p['id']}"):
            c1,c2 = st.columns(2)
            with c1:
                loc  = st.text_input("Study Location / Country", value=p.get("study_location",""))
                meth = st.text_input("Research Methodology",     value=p.get("methodology",""))
                data = st.text_input("Dataset / Data Source",    value=p.get("dataset",""))
            with c2:
                pol  = st.text_area("Policy Implications", value=p.get("policy_implication",""), height=90)
                find = st.text_area("Key Findings",        value=p.get("key_findings",""),       height=90)
            if st.form_submit_button("Save Extraction", use_container_width=True):
                for f2,v in [("study_location",loc),("methodology",meth),("dataset",data),("policy_implication",pol),("key_findings",find)]:
                    upd(p["id"],f2,v)
                st.success(f"✓ Saved {p['id']}"); st.rerun()


# ══════════════════════════════════════════════════════════════
# PAGE 6 — QUALITY ASSESSMENT
# ══════════════════════════════════════════════════════════════
elif tab == 6:
    pg("Module 07", "Quality ", "Assessment",
       "Appraise methodological quality using a five-criterion rubric (max score 10).")

    ex_papers = ex()
    if not ex_papers:
        empty_st("No extracted papers yet", "Complete Data Extraction first"); st.stop()

    n_h = len([p for p in ex_papers if qs(p)>=8])
    n_m = len([p for p in ex_papers if 5<=qs(p)<8])
    n_l = len([p for p in ex_papers if qs(p)<5])
    mc_row([("Assessable",len(ex_papers),""),("High Quality ≥8",n_h,"green"),("Medium 5–7",n_m,"gold"),("Low <5",n_l,"red")], 4)

    qv, qe = st.tabs(["QUALITY MATRIX","ASSESS PAPER"])

    with qv:
        rows = []
        for p in ex_papers:
            s = qs(p); lbl, _ = ql(s)
            rows.append({"ID":p["id"],"Title":p["title"][:50]+"…" if len(p.get("title",""))>50 else p.get("title",""),
                "Obj":p.get("qa_obj",0),"Method":p.get("qa_method",0),"Data":p.get("qa_data",0),
                "Bias":p.get("qa_bias",0),"Relev.":p.get("qa_rel",0),"Total/10":s,"Category":lbl})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    with qe:
        opts = [f"{p['id']}  —  {p['title'][:55]}…" for p in ex_papers]
        sel = st.selectbox("Select paper", opts)
        p = ex_papers[opts.index(sel)]
        s = qs(p); lbl, pill_cls = ql(s)
        st.markdown(f"""
        <div class="pcard">
          <div class="pcard-title">{p.get('title','')}</div>
          <div class="pcard-meta">{p.get('authors','—')[:70]} · {p.get('year','?')} · {p.get('journal','—')}</div>
          <div style="margin-top:.5rem;"><span class="pill {pill_cls}">{lbl}</span>&nbsp;
          <span style="font-family:'Space Mono',monospace;font-size:.7rem;color:var(--snow2);">{s}/10</span></div>
        </div>""", unsafe_allow_html=True)

        CRIT = [("qa_obj","Research objective clarity"),("qa_method","Methodology quality"),
                ("qa_data","Data reliability"),("qa_bias","Bias risk assessment"),("qa_rel","Relevance to research question")]
        with st.form(f"qa_{p['id']}"):
            scores = {}
            for k, lbl2 in CRIT:
                scores[k] = st.select_slider(lbl2, options=[0,1,2], value=p.get(k,0),
                    format_func=lambda x: ["0 — Not met","1 — Partial","2 — Fully met"][x])
            tot = sum(scores.values()); ql_lbl, _ = ql(tot)
            st.markdown(f"**Score: {tot}/10 — {ql_lbl}**")
            if st.form_submit_button("Save Assessment", use_container_width=True):
                for k,v in scores.items(): upd(p["id"],k,v)
                st.success(f"✓ Saved — {p['id']} = {tot}/10"); st.rerun()


# ══════════════════════════════════════════════════════════════
# PAGE 7 — SYNTHESIS
# ══════════════════════════════════════════════════════════════
elif tab == 7:
    pg("Module 08", "Evidence ", "Synthesis",
       "Synthesise findings across included studies. Evidence table, methodology distribution, and geographic breakdown.")

    ex_papers = [p for p in ab() if p.get("key_findings")]
    if not ex_papers:
        empty_st("No extracted papers yet", "Complete Data Extraction first"); st.stop()

    ev, mt, gt = st.tabs(["EVIDENCE TABLE","METHOD DISTRIBUTION","GEOGRAPHIC DISTRIBUTION"])

    with ev:
        rows = []
        for p in ex_papers:
            s=qs(p); lbl,_=ql(s)
            a = p.get("authors","")
            study = (a.split(";")[0].split(",")[0].strip() + f" et al. ({p.get('year','')})" if a else p["id"])
            rows.append({"Study":study,"Year":p.get("year",""),"Source":p.get("journal",""),
                "Country":p.get("study_location","—"),"Method":p.get("methodology","—"),
                "Dataset":p.get("dataset","—"),
                "Key Findings":(p.get("key_findings","—"))[:80]+"…" if len(p.get("key_findings",""))>80 else p.get("key_findings","—"),
                "Policy":(p.get("policy_implication","—"))[:60]+"…" if len(p.get("policy_implication",""))>60 else p.get("policy_implication","—"),
                "Quality":f"{s}/10 ({lbl})"})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    with mt:
        mc2 = {}
        for p in ex_papers:
            m = (p.get("methodology") or "Unknown").lower()
            if any(x in m for x in ["regression","panel","ols","quantitative"]): cat="Quantitative"
            elif any(x in m for x in ["meta","systematic","slr"]): cat="Meta-analysis / SLR"
            elif any(x in m for x in ["machine learning","ml","ai","neural"]): cat="ML / AI"
            elif any(x in m for x in ["quasi","experiment","rct"]): cat="Quasi-experimental"
            elif any(x in m for x in ["qualitative","interview","case"]): cat="Qualitative"
            elif any(x in m for x in ["mixed"]): cat="Mixed Methods"
            elif any(x in m for x in ["review","literature","narrative"]): cat="Literature Review"
            else: cat="Other / Not specified"
            mc2[cat] = mc2.get(cat,0)+1
        if mc2: st.bar_chart(pd.DataFrame(list(mc2.items()),columns=["Method","Count"]).set_index("Method"))
        else: st.info("Fill in methodology field in Data Extraction to see distribution.")

    with gt:
        gc = {}
        for p in ex_papers:
            loc = (p.get("study_location") or "Not specified").strip() or "Not specified"
            gc[loc] = gc.get(loc,0)+1
        if gc: st.bar_chart(pd.DataFrame(list(gc.items()),columns=["Location","Count"]).set_index("Location"))


# ══════════════════════════════════════════════════════════════
# PAGE 8 — PRISMA
# ══════════════════════════════════════════════════════════════
elif tab == 8:
    pg("Module 09", "PRISMA ", "Flow Diagram",
       "Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA 2020). All counts auto-calculated.")

    if not papers:
        empty_st(); st.stop()

    n_dup  = len(st.session_state.dup_results)
    n_id   = n_total + n_dup
    n_scr  = n_total
    n_te   = len([p for p in papers if p.get("title_decision")=="exclude"])
    n_tm   = len([p for p in papers if p.get("title_decision")=="maybe"])
    n_ae   = len(ti())
    n_axe  = len([p for p in papers if p.get("abstract_decision")=="exclude"])
    n_inc  = len(ab())

    cd, ct = st.columns([1.1, 1], gap="large")

    with cd:
        sh("Flow Diagram", "◈ ")
        st.markdown(f"""
        <div class="prisma-flow">
          <div class="prisma-box blue-acc">
            <div class="prisma-lbl">Identification</div>
            <div class="prisma-n">{n_id}</div>
            <div class="prisma-sub">Records identified from databases</div>
          </div>
          <div class="prisma-arrow">↓</div>

          <div class="prisma-row">
            <div class="prisma-box blue-acc">
              <div class="prisma-lbl">After Deduplication</div>
              <div class="prisma-n">{n_scr}</div>
              <div class="prisma-sub">Unique records screened</div>
            </div>
            <div class="prisma-line"></div>
            <div class="prisma-branch">{n_dup} duplicate(s)<br/>removed</div>
          </div>
          <div class="prisma-arrow">↓</div>

          <div class="prisma-row">
            <div class="prisma-box gold-acc">
              <div class="prisma-lbl">Title Screening</div>
              <div class="prisma-n">{n_scr}</div>
              <div class="prisma-sub">Screened by title</div>
            </div>
            <div class="prisma-line"></div>
            <div class="prisma-branch">{n_te} excluded<br/>{n_tm} maybe</div>
          </div>
          <div class="prisma-arrow">↓</div>

          <div class="prisma-row">
            <div class="prisma-box purple-acc">
              <div class="prisma-lbl">Abstract Screening</div>
              <div class="prisma-n">{n_ae}</div>
              <div class="prisma-sub">Assessed for eligibility</div>
            </div>
            <div class="prisma-line"></div>
            <div class="prisma-branch">{n_axe} excluded<br/>(abstract)</div>
          </div>
          <div class="prisma-arrow">↓</div>

          <div class="prisma-box green-acc">
            <div class="prisma-lbl">Included in Synthesis</div>
            <div class="prisma-n">{n_inc}</div>
            <div class="prisma-sub">Studies included in review</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with ct:
        sh("Count Table", "◈ ")
        pf = pd.DataFrame([
            {"Stage":"Records identified","n":n_id},
            {"Stage":"Duplicates removed","n":n_dup},
            {"Stage":"After deduplication","n":n_scr},
            {"Stage":"Title excluded","n":n_te},
            {"Stage":"Title maybe","n":n_tm},
            {"Stage":"Abstract eligible","n":n_ae},
            {"Stage":"Abstract excluded","n":n_axe},
            {"Stage":"Included in synthesis","n":n_inc},
        ])
        st.dataframe(pf, use_container_width=True, hide_index=True)
        st.download_button("Download PRISMA Table", pf.to_csv(index=False), "prisma.csv","text/csv",use_container_width=True)

        reasons = {}
        for p in papers:
            r = p.get("exclusion_reason","")
            if r: reasons[r] = reasons.get(r,0)+1
        if reasons:
            st.markdown("&nbsp;", unsafe_allow_html=True)
            sh("Exclusion Reasons", "◈ ")
            st.dataframe(pd.DataFrame(list(reasons.items()),columns=["Reason","n"]).sort_values("n",ascending=False),
                         use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════
# PAGE 9 — EXPORT
# ══════════════════════════════════════════════════════════════
elif tab == 9:
    pg("Module 10", "Export ", "Results",
       "Export all review data for publication. PRISMA-compliant audit trail included.")

    if not papers:
        empty_st(); st.stop()

    abs_inc = ab()
    ex_papers = ex()

    mc_row([("Total Records",len(papers),""),("Title Included",len(ti()),""),
            ("Final Included",len(abs_inc),"gold"),("Data Extracted",len(ex_papers),"green")], 4)

    cl, cr = st.columns(2, gap="large")

    with cl:
        sh("Data Exports", "◈ ")

        scr = pd.DataFrame([{"id":p["id"],"doc_type":p.get("doc_type",""),
            "title":p.get("title",""),"authors":p.get("authors",""),"year":p.get("year",""),
            "journal":p.get("journal",""),"doi":p.get("doi",""),
            "title_decision":p.get("title_decision") or "pending",
            "abstract_decision":p.get("abstract_decision") or "pending",
            "exclusion_reason":p.get("exclusion_reason","")} for p in papers])
        st.download_button("Screening Decisions (.csv)", scr.to_csv(index=False),"screening.csv","text/csv",use_container_width=True)

        if ex_papers:
            ext = pd.DataFrame([{"id":p["id"],"title":p.get("title",""),"authors":p.get("authors",""),
                "year":p.get("year",""),"journal":p.get("journal",""),"doi":p.get("doi",""),
                "study_location":p.get("study_location",""),"methodology":p.get("methodology",""),
                "dataset":p.get("dataset",""),"policy_implication":p.get("policy_implication",""),
                "key_findings":p.get("key_findings",""),"quality":qs(p),"category":ql(qs(p))[0]} for p in ex_papers])
            st.download_button("Extraction Table (.csv)", ext.to_csv(index=False),"extraction.csv","text/csv",use_container_width=True)

            qa = pd.DataFrame([{"id":p["id"],"title":p.get("title",""),"qa_obj":p.get("qa_obj",0),
                "qa_method":p.get("qa_method",0),"qa_data":p.get("qa_data",0),"qa_bias":p.get("qa_bias",0),
                "qa_rel":p.get("qa_rel",0),"total":qs(p),"category":ql(qs(p))[0]} for p in ex_papers])
            st.download_button("Quality Matrix (.csv)", qa.to_csv(index=False),"quality.csv","text/csv",use_container_width=True)

        bib = []
        for p in abs_inc:
            et = {"JOUR":"article","RPRT":"techreport","BOOK":"book","CONF":"inproceedings"}.get(p.get("doc_type","JOUR"),"misc")
            bib += [f"@{et}{{{p['id']},",f"  title   = {{{p.get('title','')}}}," if p.get("title") else "",
                    f"  author  = {{{p.get('authors','')}}}," if p.get("authors") else "",
                    f"  journal = {{{p.get('journal','')}}}," if p.get("journal") else "",
                    f"  year    = {{{p.get('year','')}}}," if p.get("year") else "",
                    f"  doi     = {{{p.get('doi','')}}}," if p.get("doi") else "","}\n"]
        st.download_button("Bibliography (.bib)", "\n".join(bib),"included.bib","text/plain",use_container_width=True)
        st.download_button("Full Review Data (.json)", json.dumps(st.session_state.papers,indent=2,default=str),"full_data.json","application/json",use_container_width=True)

    with cr:
        sh("Methodology Section Draft", "◈ ")
        method_text = f"""METHODOLOGY SECTION DRAFT
Generated by SLR·Studio — Bahas Kebijakan
{datetime.now().strftime('%Y-%m-%d %H:%M')}
==========================================================

2. METHODOLOGY

2.1 Search Strategy
Systematic search in {len(st.session_state.import_log)} database(s):
{", ".join([l.get("source","") for l in st.session_state.import_log]) or "Not recorded"}.
Initial search: {n_total + len(st.session_state.dup_results)} records.

2.2 Study Selection (PRISMA 2020)
After deduplication ({n_total} unique records), titles were screened.
Title-passed (n={len(ti())}), abstract-assessed (n={len(ab())}).
Final included: {len(abs_inc)} studies.

2.3 Data Extraction
Fields: study location, methodology, data source,
key findings, policy implications.

2.4 Quality Assessment
Five-criterion rubric (0–2 each; max 10):
(1) Research objective clarity
(2) Methodology quality
(3) Data reliability
(4) Bias risk assessment
(5) Relevance to research question
High ≥8 · Medium 5–7 · Low <5

2.5 Evidence Synthesis
Narrative synthesis (heterogeneity across designs).

Reference: Page MJ et al. BMJ 2021;372:n71.
==========================================================
Auto-generated — adapt before submission.
"""
        st.download_button("Methodology Draft (.txt)", method_text,"methodology.txt","text/plain",use_container_width=True)

        st.markdown("&nbsp;", unsafe_allow_html=True)
        sh("Review Summary", "◈ ")
        sum_df = pd.DataFrame([
            {"Stage":"Total records","n":len(papers)},
            {"Stage":"Title included","n":len(ti())},
            {"Stage":"Final included","n":len(abs_inc)},
            {"Stage":"Data extracted","n":len(ex_papers)},
            {"Stage":"High quality (≥8)","n":len([p for p in ex_papers if qs(p)>=8])},
            {"Stage":"Medium quality","n":len([p for p in ex_papers if 5<=qs(p)<8])},
        ])
        st.dataframe(sum_df, use_container_width=True, hide_index=True)
        st.caption("Bahas Kebijakan (2025). SLR·Studio. bahaskebijakan.id")
