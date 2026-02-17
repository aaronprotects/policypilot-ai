#!/usr/bin/env bash
set -euo pipefail

echo "== PolicyPilot AI (Internal) =="

# 1) Python check
if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 not found. Install Python 3 first."
  echo "Mac (homebrew): brew install python"
  exit 1
fi

# 2) Git LFS check (for PDFs)
if command -v git >/dev/null 2>&1; then
  if command -v git-lfs >/dev/null 2>&1; then
    git lfs install >/dev/null 2>&1 || true
  else
    echo "WARN: git-lfs not found. PDFs may not download correctly on fresh clones."
    echo "Install Git LFS: https://git-lfs.com/"
  fi
fi

# 3) Create venv
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

# 4) Activate venv
# shellcheck disable=SC1091
source .venv/bin/activate

# 5) Upgrade pip tooling
python -m pip install --upgrade pip setuptools wheel

# 6) Install deps
if [ ! -f "requirements.txt" ]; then
  echo "ERROR: requirements.txt missing"
  exit 1
fi
pip install -r requirements.txt

# 7) Quick sanity checks (non-blocking if you want to remove later)
echo "== Running quick validation =="
python test_spec_engine.py
python coverage_report.py
python test_payment_rules.py

# 8) Check core PDFs presence
PDF_COUNT=$(ls -1 data/underwriting/*.pdf 2>/dev/null | wc -l | tr -d ' ')
if [ "$PDF_COUNT" -lt 6 ]; then
  echo "WARN: Expected 6 core PDFs in data/underwriting, found $PDF_COUNT."
  echo "If using Git LFS, run: git lfs pull"
else
  echo "PASS: Core PDFs found ($PDF_COUNT)"
fi

echo "== Launching dashboard =="
exec streamlit run dashboard.py
