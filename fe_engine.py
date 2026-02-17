from typing import Dict, List, Tuple, Optional
from spec_engine import load_spec, apply_condition
from payment_rules import get_payment_compatibility

CARRIERS = ["Aetna", "American Amicable", "Americo", "Corebridge", "Ethos", "Mutual of Omaha", "Transamerica"]

_SEVERITY = {
    "DECLINE": 9,
    "GUARANTEED_ISSUE": 6,
    "GRADED": 5,
    "ROP": 5,
    "MODIFIED": 5,
    "SELECT": 3,
    "QUESTION_BASED": 3,
    "NOT_ASKED": 1,
    "LEVEL": 1
}

def _apply_master_tree_overrides(out: Dict[str, dict], ctx: dict) -> Dict[str, dict]:
    """
    Hard gating rules from MASTER DECISION TREE  [oai_citation:1‡MASTER DECISION TREE (1).pdf](sediment://file_0000000004a4722fa36a5ca716d0a852)
    Implements:
      - Age 91+ -> no coverage
      - Age 86–90 -> Aetna only
      - Oxygen -> all decline except Corebridge GI (50–80) OR Aetna (81–90)
      - ADLs/Nursing Home -> same pattern as Oxygen
    """
    age = ctx.get("age")
    oxygen = bool(ctx.get("oxygen", False))
    adls = bool(ctx.get("adls", False))

    if isinstance(age, int):
        if age >= 91:
            for c in out:
                out[c]["tier"] = "DECLINE"
                out[c]["why"].append("MASTER TREE: Age 91+ -> no coverage")
            return out

        if 86 <= age <= 90:
            for c in out:
                if c != "Aetna":
                    out[c]["tier"] = "DECLINE"
                    out[c]["why"].append("MASTER TREE: Age 86–90 -> Aetna only")
            out["Aetna"]["why"].append("MASTER TREE: Age 86–90 -> Aetna only")
            # If oxygen/ADL also present, Aetna still the only path in tree
            return out

    # Oxygen / ADL overrides (apply after age gate)
    if oxygen or adls:
        # set everyone decline first
        for c in out:
            out[c]["tier"] = "DECLINE"
            out[c]["why"].append("MASTER TREE: Oxygen/ADL -> most carriers decline; exceptions apply")

        if isinstance(age, int) and 81 <= age <= 90:
            out["Aetna"]["tier"] = "LEVEL"
            out["Aetna"]["why"].append("MASTER TREE: Oxygen/ADL ages 81–90 -> Aetna only option")
        else:
            # ages 50–80 -> Corebridge GIWL exception per tree
            out["Corebridge"]["tier"] = "GUARANTEED_ISSUE"
            out["Corebridge"]["why"].append("MASTER TREE: Oxygen/ADL ages 50–80 -> Corebridge GIWL")
        return out

    return out

def evaluate_fe(conditions: List[Tuple[str, dict]], master_ctx: dict) -> Dict[str, dict]:
    """
    conditions: list of (condition_key, ctx_for_that_condition)
    master_ctx: dict with master-tree inputs (age, smoker, oxygen, adls) and optional shared fields
    """
    spec = load_spec()
    out = {c: {"tier": "LEVEL", "why": [], "payment": {}} for c in CARRIERS}

    # Apply all grid conditions (worst-case merge by severity)
    for cond_key, ctx in conditions:
        r = apply_condition(spec, cond_key, ctx or {})
        for carrier, payload in r.items():
            if carrier not in out:
                continue
            cur = out[carrier]["tier"]
            new = payload["tier"]
            if _SEVERITY.get(new, 1) >= _SEVERITY.get(cur, 1):
                out[carrier]["tier"] = new
            why = payload.get("why")
            if why:
                out[carrier]["why"].append(f"{cond_key}: {why}")

    # Apply master-tree overrides last (hard gates)
    out = _apply_master_tree_overrides(out, master_ctx)

    # Attach payment compatibility (display only)
    for carrier in out:
        out[carrier]["payment"] = get_payment_compatibility(carrier)

    return out

def recommend(carrier_results: Dict[str, dict]) -> Tuple[Optional[str], Optional[str]]:
    """
    Tier priority: LEVEL/NOT_ASKED > SELECT/QUESTION_BASED > GRADED/MODIFIED/ROP > GI > DECLINE
    Tie-breaker: affordability order (Americo, MOO, AmAm, Corebridge, Transamerica, Aetna, Ethos)
    """
    tier_rank = {
        "LEVEL": 1, "NOT_ASKED": 1,
        "SELECT": 2, "QUESTION_BASED": 2,
        "GRADED": 3, "MODIFIED": 3, "ROP": 3,
        "GUARANTEED_ISSUE": 4,
        "DECLINE": 9
    }
    affordability = {n: i for i, n in enumerate(["Americo","Mutual of Omaha","American Amicable","Corebridge","Transamerica","Aetna","Ethos"])}

    eligible = [(c, d["tier"]) for c, d in carrier_results.items()]
    eligible.sort(key=lambda x: (tier_rank.get(x[1], 9), affordability.get(x[0], 999)))
    primary = eligible[0][0] if eligible else None
    backup = eligible[1][0] if len(eligible) > 1 else None
    return primary, backup
