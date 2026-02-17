"""
Deterministic follow-up prompts based on underwriting grid language.
We do NOT change tiers here; we only tell the agent what questions to ask next.
"""

from typing import Dict, List

# Conditions that explicitly require "Check Med List" or equivalent
MED_LIST_REQUIRED = {
    "CHRONIC_PAIN_6_OR_MORE_FILLS_OF_NARCOTIC_PAIN_PRESCRIPTIONS",
    "BLOOD_CLOTS",
    "NEUROPATHY",
}

STENT_FOLLOWUP = {"BLOOD_CLOTS", "CORONARY_ARTERY_DISEASE"}
INHALER_FOLLOWUP = {"BRONCHITIS_CHRONIC", "EMPHYSEMA_CHRONIC", "ASTHMA_CHRONIC"}
NARCOTIC_FOLLOWUP = {"CHRONIC_PAIN_6_OR_MORE_FILLS_OF_NARCOTIC_PAIN_PRESCRIPTIONS"}

def build_followups(selected_condition_keys: List[str]) -> Dict[str, List[str]]:
    keys = set(selected_condition_keys)
    followups: Dict[str, List[str]] = {}

    # Diabetes followups (call flow) — not "med list", but still deterministic intake
    if "DIABETES" in keys:
        followups["DIABETES_FOLLOWUP"] = [
            "Ask: age at diagnosis and most recent A1C?",
            "Ask: insulin use? any complications (neuropathy/retinopathy/nephropathy)?",
        ]

    if keys & MED_LIST_REQUIRED:
        followups["MED_LIST_REQUIRED"] = [
            "Ask: full medication list (name + dose + frequency).",
            "Ask: what each medication is for (diagnosis).",
        ]

    if keys & STENT_FOLLOWUP:
        followups["STENT_FOLLOWUP"] = [
            "Ask: stents? when placed? how many? any recent procedures?",
        ]

    if keys & INHALER_FOLLOWUP:
        followups["INHALER_FOLLOWUP"] = [
            "Ask: inhaler use? which inhalers? frequency? any oxygen use?",
        ]

    if keys & NARCOTIC_FOLLOWUP:
        followups["NARCOTIC_FOLLOWUP"] = [
            "Ask: narcotic/opioid prescriptions? how many fills? which meds? pain management program?",
        ]

    return followups

def annotate_carrier_notes(carrier_results: Dict[str, dict], followups: Dict[str, List[str]]) -> Dict[str, dict]:
    if not followups:
        return carrier_results

    note_lines = []
    for k, prompts in followups.items():
        for p in prompts:
            note_lines.append(f"FOLLOWUP/{k}: {p}")

    for carrier in carrier_results:
        carrier_results[carrier].setdefault("why", [])
        carrier_results[carrier]["why"].extend(note_lines)

    return carrier_results
