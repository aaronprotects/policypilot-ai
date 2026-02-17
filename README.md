# 🚀 Quick Start (Internal Use Only)

git clone <repo>
cd life-insurance-copilot
./run.sh

---

# 🧠 Final Expense Master Decision Tree Dashboard
INTERNAL AGENCY TOOL — DO NOT DISTRIBUTE

## 📌 What This Tool Does

This application is a structured Final Expense underwriting decision engine.

It:

• Encodes carrier underwriting grids into a deterministic JSON spec  
• Applies underwriting logic consistently  
• Handles multi-condition stacking  
• Ranks carriers (Primary + Backup)  
• Validates payment compatibility (ACH, Direct Express, Chime, etc.)  
• Displays carrier breakdown + eligibility  
• Supports medication/device expansion  

This is not a quoting tool.  
This is a structured underwriting intelligence system.

---

## 🏗 Architecture

Core Files:

- fe_rules_spec.json → Master underwriting logic
- spec_engine.py → Deterministic rule engine
- fe_engine.py → Carrier ranking logic
- dashboard.py → Streamlit UI
- payment_rules.py → Payment eligibility
- med_rules.py → Medication rules (expandable)

Data Sources:

- data/underwriting/ → Core underwriting PDFs
- data/sales_scripts/ → Scripts & objection frameworks
- data/training_transcripts_clean/ → Sales training transcripts
- data/transcripts_clean/ → Call transcripts

All rules are test-backed.

---

## 🧪 Validation

The system is validated through:

- test_spec_batch*.py
- test_spec_engine.py
- test_payment_rules.py
- coverage_report.py

Grid coverage: 100% of master condition list.

---

## 🛠 Full Setup (Manual)

Mac/Linux:

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run dashboard.py

Windows:

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run dashboard.py

---

## 🔒 IMPORTANT

This repository contains proprietary carrier materials and internal agency content.

It is for INTERNAL AGENCY USE ONLY.

Publishing publicly is prohibited.

---

## 🤖 Using AI With This Repo

This repository is modular and AI-editable.

An AI can:

• Modify underwriting rules  
• Add new conditions  
• Improve ranking logic  
• Extend medication inference  
• Improve UI  
• Build export/report features  

---

Built as an internal underwriting decision intelligence system.
