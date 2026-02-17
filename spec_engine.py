import json
from decision_tiers import ALLOWED_TIERS, NORMALIZE_TO_UI

DEFAULT_CARRIERS = [
    "Aetna",
    "American Amicable",
    "Americo",
    "Corebridge",
    "Ethos",
    "Mutual of Omaha",
    "Transamerica"
]

def load_spec(path="fe_rules_spec.json"):
    with open(path, "r") as f:
        return json.load(f)

def validate_spec(spec):
    problems = []
    if "conditions" not in spec:
        problems.append("Missing top-level 'conditions'")
        return problems

    for cond_name, cond in spec["conditions"].items():
        rules = cond.get("rules", [])
        for i, rule in enumerate(rules):
            sets = rule.get("set", {})
            for carrier, payload in sets.items():
                tier = payload.get("tier")
                if tier not in ALLOWED_TIERS:
                    problems.append(f"{cond_name}.rules[{i}].set[{carrier}].tier invalid: {tier}")
    return problems

def _match_when(when, ctx):
    if not when:
        return True

    def _get_num(key):
        v = ctx.get(key)
        return v if isinstance(v, (int, float)) else None
    # ---- numeric comparisons ----
    if "age_at_diagnosis_lt" in when:
        v = _get_num("age_at_diagnosis")
        if v is None or not (v < when["age_at_diagnosis_lt"]):
            return False

    if "age_at_diagnosis_lte" in when:
        v = _get_num("age_at_diagnosis")
        if v is None or not (v <= when["age_at_diagnosis_lte"]):
            return False

    if "years_since_event_lte" in when:

        v = _get_num("years_since_event")
        if v is None or not (v <= when["years_since_event_lte"]):
            return False

    if "years_since_event_gt" in when:
        v = _get_num("years_since_event")
        if v is None or not (v > when["years_since_event_gt"]):
            return False

    if "months_since_lte" in when:
        v = _get_num("months_since")
        if v is None or not (v <= when["months_since_lte"]):
            return False

    # ---- boolean flags ----
    if "flag_true" in when:

        # Derived flags for kidney disease subtype
        subtype = ctx.get("subtype")
        if isinstance(subtype, str):
            st = subtype.strip().lower()
            ctx.setdefault("subtype_is_dialysis", st == "dialysis")
            ctx.setdefault("subtype_is_failure_or_disease", st in ("failure", "disease", "failure_or_disease"))

        flag = when["flag_true"]

        # Derived flags for AMPUTATION cause handling
        cause = ctx.get("cause")
        if isinstance(cause, str):
            c = cause.strip().lower()
            ctx.setdefault("cause_is_disease", c == "disease")
            ctx.setdefault("cause_is_diabetes", c == "diabetes")
            ctx.setdefault("cause_is_disease_or_diabetes", c in ("disease", "diabetes"))

        if ctx.get(flag) is not True:
            return False

    # ---- list membership ----
    if "complications_any" in when:
        comps = set(ctx.get("complications") or [])
        needed = set(when["complications_any"])
        if comps.isdisjoint(needed):
            return False

    return True

def apply_condition(spec, condition_key, ctx, carriers=None):
    carriers = carriers or DEFAULT_CARRIERS
    out = {c: {"tier": "LEVEL", "ui": NORMALIZE_TO_UI["LEVEL"], "why": "Default baseline"} for c in carriers}

    condition = spec["conditions"].get(condition_key)
    if not condition:
        return out

    rules = condition.get("rules", [])
    rules = sorted(rules, key=lambda r: int(r.get("priority", 0)))

    for rule in rules:
        when = rule.get("when", {})
        if _match_when(when, ctx):
            for carrier, payload in rule.get("set", {}).items():
                if carrier in out:
                    tier = payload["tier"]
                    out[carrier] = {
                        "tier": tier,
                        "ui": NORMALIZE_TO_UI.get(tier, "Level"),
                        "why": payload.get("why", "Rule matched")
                    }
    return out
