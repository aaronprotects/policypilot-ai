import json
from pathlib import Path
import streamlit as st
from fe_engine import evaluate_fe, recommend

st.set_page_config(page_title="FE Master Tree Wizard", layout="wide")
st.title("🧠 Final Expense Master Decision Tree Wizard")

SPEC = json.loads(Path("fe_rules_spec.json").read_text(encoding="utf-8"))
COND_SPEC = SPEC.get("conditions", {})

# ----------------------------
# Step 1 — Master Tree Inputs
# ----------------------------
st.sidebar.header("Step 1 — Master Tree Inputs")
age = int(st.sidebar.slider("Age", 18, 90, 60))
smoker = st.sidebar.checkbox("Smoker", value=False)  # reserved for future gating
oxygen = st.sidebar.checkbox("Uses Oxygen", value=False)
adls = st.sidebar.checkbox("Needs help with ADLs / Nursing home", value=False)

master_ctx = {"age": age, "smoker": smoker, "oxygen": oxygen, "adls": adls}

# ----------------------------
# Step 2 — Add Conditions (no search)
# ----------------------------
st.sidebar.header("Step 2 — Add Conditions")

master_list_path = Path("conditions_master_list.json")
if master_list_path.exists():
    master_conditions = json.loads(master_list_path.read_text(encoding="utf-8")).get("conditions", [])
else:
    master_conditions = sorted(COND_SPEC.keys())

def norm_key(label: str) -> str:
    return (
        label.upper()
        .replace("&", "AND")
        .replace("/", "_")
        .replace("'", "")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "_")
        .replace(" ", "_")
    )

label_to_key = {lbl: norm_key(lbl) for lbl in master_conditions}
all_labels = list(label_to_key.keys())

selected_labels = st.sidebar.multiselect("Select conditions", all_labels, default=[])
selected_keys = [label_to_key[lbl] for lbl in selected_labels if label_to_key.get(lbl) in COND_SPEC]

# ----------------------------
# Step 3 — Condition Details
# ----------------------------
st.sidebar.header("Step 3 — Condition Details")

def input_widget(cond_key: str, field: str):
    if field == "years_since_event":
        return st.sidebar.number_input(f"{cond_key}: years_since_event", 0.0, 60.0, 1.0, 0.5, key=f"{cond_key}:{field}")
    if field in ("months_since_event", "months_since"):
        return st.sidebar.number_input(f"{cond_key}: months_since_event", 0.0, 240.0, 3.0, 1.0, key=f"{cond_key}:{field}")
    if field == "age_at_diagnosis":
        return st.sidebar.number_input(f"{cond_key}: age_at_diagnosis", 0, 120, 55, 1, key=f"{cond_key}:{field}")
    if field in ("insulin_use", "is_diabetes_related", "awaiting_trial", "has_cirrhosis", "is_chronic"):
        return st.sidebar.checkbox(f"{cond_key}: {field}", value=False, key=f"{cond_key}:{field}")
    if field == "subtype":
        return st.sidebar.selectbox(f"{cond_key}: subtype", ["unknown", "dialysis", "failure_or_disease"], index=0, key=f"{cond_key}:{field}")
    if field == "cause":
        return st.sidebar.selectbox(f"{cond_key}: cause", ["unknown", "injury", "disease", "diabetes"], index=0, key=f"{cond_key}:{field}")
    return st.sidebar.text_input(f"{cond_key}: {field}", value="", key=f"{cond_key}:{field}")

conditions = []
for cond_key in selected_keys:
    inputs = COND_SPEC.get(cond_key, {}).get("inputs", [])
    ctx = {"age": age}
    for f in inputs:
        ctx[f] = input_widget(cond_key, f)
    conditions.append((cond_key, ctx))

# Optional debug (you can remove later)
with st.expander("DEBUG: Selected condition keys + contexts"):
    st.write(selected_keys)
    st.write(conditions)
    st.write(master_ctx)

# Run engine
results = evaluate_fe(conditions, master_ctx)
primary, backup = recommend(results)

st.subheader("🏆 Recommendation")
c1, c2 = st.columns(2)
with c1:
    st.success(f"Primary: {primary}")
with c2:
    st.info(f"Backup: {backup}")

st.caption("Payment compatibility is shown under each carrier (does not filter recommendations until you confirm payment type).")

st.markdown("---")
st.subheader("📋 Carrier Breakdown (with Payment Options)")

def pay_badge(ok: bool, label: str) -> str:
    return f"🟢 {label}" if ok else f"🔴 {label}"

for carrier, data in results.items():
    with st.expander(f"{carrier} — {data['tier']}"):
        pays = data.get("payment", {})
        st.write(
            f"{pay_badge(pays.get('ACH', False), 'ACH')}   "
            f"{pay_badge(pays.get('CHIME_OR_ONLINE', False), 'Chime/Online')}   "
            f"{pay_badge(pays.get('DIRECT_EXPRESS', False), 'Direct Express')}"
        )
        if data.get("why"):
            st.write("**Why (top reasons):**")
            for line in data["why"][:15]:
                st.write(f"- {line}")
