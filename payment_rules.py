def get_payment_compatibility(carrier: str) -> dict:
    """
    Returns dict:
    {
      "ACH": True/False,
      "CHIME_OR_ONLINE": True/False,
      "DIRECT_EXPRESS": True/False
    }
    Based on MASTER DECISION TREE.
    """

    c = carrier.upper()

    # ACH works for all
    ach = True

    # Direct Express only Transamerica or Corebridge
    direct = c in {"TRANSAMERICA", "COREBRIDGE"}

    # Chime/Online banks: MOO, Corebridge, Transamerica, Royal Neighbors
    chime = c in {"MUTUAL OF OMAHA", "COREBRIDGE", "TRANSAMERICA", "ROYAL NEIGHBORS"}

    return {
        "ACH": ach,
        "CHIME_OR_ONLINE": chime,
        "DIRECT_EXPRESS": direct
    }


def apply_payment_method_filter(carriers: dict, payment_method: str) -> dict:
    '''
    Backwards-compatible helper for older tests/scripts.
    carriers: dict of carrier -> anything (keys used)
    payment_method: ACH | CHIME_OR_ONLINE | DIRECT_EXPRESS
    returns: dict carrier -> {eligible: bool, why: str}
    '''
    pm = (payment_method or "").strip().upper()
    result = {c: {"eligible": True, "why": "Payment method OK"} for c in carriers.keys()}

    if pm == "ACH":
        return result

    if pm == "DIRECT_EXPRESS":
        for c in result:
            ok = get_payment_compatibility(c).get("DIRECT_EXPRESS", False)
            if not ok:
                result[c] = {"eligible": False, "why": "Direct Express only (use Transamerica or Corebridge)"}
        return result

    if pm == "CHIME_OR_ONLINE":
        for c in result:
            ok = get_payment_compatibility(c).get("CHIME_OR_ONLINE", False)
            if not ok:
                result[c] = {"eligible": False, "why": "Chime/Online banks (use MOO/Corebridge/Transamerica/Royal Neighbors)"}
        return result

    # Unknown: don't block
    for c in result:
        result[c] = {"eligible": True, "why": "Unknown payment method (no filter applied)"}
    return result
