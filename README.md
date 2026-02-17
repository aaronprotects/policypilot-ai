# 🚀 Quick Start (Internal Use Only)

## Prerequisites (must be installed first)
- Python 3.9+ (recommended: 3.11)
- Git
- Git LFS (required to download the PDFs in this repo)

### Verify prerequisites
python3 --version
git --version
git lfs --version

If Git LFS is installed, run once:
git lfs install

---

## One Command Run (Mac/Linux)
git clone https://github.com/aaronprotects/policypilot-ai.git && cd policypilot-ai && ./run.sh

## One Command Run (Windows)
git clone https://github.com/aaronprotects/policypilot-ai.git
cd policypilot-ai
python bootstrap.py

---

# 🧠 PolicyPilot AI — Final Expense Underwriting Wizard
INTERNAL AGENCY TOOL — DO NOT DISTRIBUTE

This repo contains proprietary carrier materials and internal agency training content.
It is for INTERNAL AGENCY USE ONLY.

Publishing publicly is prohibited (see LICENSE_INTERNAL.md).

## What this tool does
- Deterministic underwriting rules engine (no hallucinations)
- Master Decision Tree outer “wizard” logic (Age/Oxygen/ADLs gates)
- Final Expense underwriting grid coverage (100% of master list)
- Payment compatibility indicators (ACH / Chime / Direct Express)
- Streamlit dashboard UI

## Repo structure (high level)
- dashboard.py -> Streamlit UI
- fe_engine.py -> Master-tree + grid evaluation + recommendation
- spec_engine.py -> deterministic rule evaluator
- fe_rules_spec.json -> underwriting rules spec
- data/underwriting/ -> 6 core PDFs used for internal reference
- data/sales_scripts/, data/objections/, data/*transcripts_clean/ -> training/support materials

## Notes for AI assistants
If you are an AI helping modify this repo:
- Do not remove internal-use warnings.
- Do not propose publishing this publicly.
- Keep logic deterministic and covered by tests when possible.
