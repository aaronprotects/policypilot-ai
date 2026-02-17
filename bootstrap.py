import os
import subprocess
import sys
from pathlib import Path

def run(cmd):
    print(">>", cmd)
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        sys.exit(result.returncode)

print("== PolicyPilot AI (Internal Bootstrap) ==")

# 1) Python version check
if sys.version_info < (3, 9):
    print("ERROR: Python 3.9+ required.")
    print("Download from https://python.org")
    sys.exit(1)

# 2) Create venv if needed
venv_path = Path(".venv")
if not venv_path.exists():
    run(f"{sys.executable} -m venv .venv")

# 3) Activate venv
if os.name == "nt":
    activate = ".venv\\Scripts\\activate"
else:
    activate = "source .venv/bin/activate"

# 4) Install deps
if os.name == "nt":
    run(".venv\\Scripts\\python -m pip install --upgrade pip setuptools wheel")
    run(".venv\\Scripts\\pip install -r requirements.txt")
else:
    run("bash -c 'source .venv/bin/activate && pip install --upgrade pip setuptools wheel'")
    run("bash -c 'source .venv/bin/activate && pip install -r requirements.txt'")

# 5) Run tests
if os.name == "nt":
    run(".venv\\Scripts\\python test_spec_engine.py")
    run(".venv\\Scripts\\python coverage_report.py")
    run(".venv\\Scripts\\python test_payment_rules.py")
else:
    run("bash -c 'source .venv/bin/activate && python test_spec_engine.py'")
    run("bash -c 'source .venv/bin/activate && python coverage_report.py'")
    run("bash -c 'source .venv/bin/activate && python test_payment_rules.py'")

print("== Launching Streamlit ==")

# 6) Launch dashboard
if os.name == "nt":
    run(".venv\\Scripts\\streamlit run dashboard.py")
else:
    run("bash -c 'source .venv/bin/activate && streamlit run dashboard.py'")
