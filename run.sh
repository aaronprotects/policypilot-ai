#!/usr/bin/env bash
set -euo pipefail

echo "== PolicyPilot AI (Internal) =="

# Python check
if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 not found. Install Python 3.9+ first."
  echo "Mac (Homebrew): brew install python"
  echo "Windows: install from https://python.org (or use: python bootstrap.py)"
  exit 1
fi

# Git LFS (PDFs)
if command -v git >/dev/null 2>&1; then
  if command -v git-lfs >/dev/null 2>&1; then
    git lfs install >/dev/null 2>&1 || true
    git lfs pull >/dev/null 2>&1 || true
  else
    echo "WARN: git-lfs not found. PDFs may not download on fresh clones."
    echo "Install Git LFS: https://git-lfs.com/"
  fi
fi

# Create venv
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

# Activate venv
# shellcheck disable=SC1091
source .venv/bin/activate

# Upgrade pip tooling
python -m pip install --upgrade pip setuptools wheel

# Install deps
if [ ! -f "requirements.txt" ]; then
  echo "ERROR: requirements.txt missing"
  exit 1
fi
pip install -r requirements.txt

# Basic check: core PDFs
PDF_COUNT=$(ls -1 data/underwriting/*.pdf 2>/dev/null | wc -l | tr -d ' ')
if [ "$PDF_COUNT" -lt 6 ]; then
  echo "WARN: Expected 6 core PDFs in data/underwriting, found $PDF_COUNT."
  echo "If using Git LFS, run: git lfs pull"
else
  echo "PASS: Core PDFs found ($PDF_COUNT)"
fi

echo "== Launching dashboard =="
exec streamlit run dashboard.py
