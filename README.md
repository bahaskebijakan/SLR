# SLR·Studio — Systematic Literature Review Platform
**Developed by Bahas Kebijakan** · PRISMA 2020 Compliant

---

## 🚀 Quick Start (Local)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run slr_app.py
```

App will open at **http://localhost:8501**

---

## ☁️ Deploy to Streamlit Community Cloud (Free)

1. Push files to a **GitHub repository**:
   - `slr_app.py`
   - `requirements.txt`

2. Go to **https://share.streamlit.io**

3. Click **"New app"** → connect your GitHub repo

4. Set:
   - **Main file:** `slr_app.py`
   - **Branch:** `main`

5. Click **Deploy** — done! Your app gets a public URL like:
   `https://your-username-slr-app.streamlit.app`

---

## 📦 Files

| File | Description |
|------|-------------|
| `slr_app.py` | Main Streamlit application |
| `requirements.txt` | Python dependencies |

---

## 📋 Workflow Modules

| # | Module | Description |
|---|--------|-------------|
| 01 | Data Import | Import .bib, .ris, .csv, .txt from Scopus, WoS, etc. |
| 02 | Deduplication | DOI match + title similarity deduplication |
| 03 | Title Screening | Include / Exclude / Maybe decisions |
| 04 | Abstract Screening | Abstract review with keyword highlighting + exclusion reasons |
| 05 | Full Text Library | PDF upload and preview |
| 06 | Data Extraction | Structured extraction with custom fields |
| 07 | Quality Assessment | 5-criterion quality rubric (0–10 score) |
| 08 | Evidence Synthesis | Evidence table + method/geo distribution + narrative |
| 09 | PRISMA Diagram | Auto-generated PRISMA 2020 flow diagram |
| 10 | Export | CSV, BIB, JSON, methodology draft |

---

## 📚 Citation

> Bahas Kebijakan (2025). *SLR·Studio: Systematic Literature Review Platform* [Software].

---

*PRISMA 2020: Page MJ, et al. BMJ 2021;372:n71. doi: 10.1136/bmj.n71*
