ALLOWED_TIERS = {
    "LEVEL",
    "GRADED",
    "GUARANTEED_ISSUE",
    "DECLINE",
    "SELECT",
    "ROP",
    "MODIFIED",
    "QUESTION_BASED",
    "NOT_ASKED",
}

# For now we normalize everything into these 4 output buckets for the UI.
# We keep the original tier (e.g., SELECT/ROP/MODIFIED) for auditability.
NORMALIZE_TO_UI = {
    "LEVEL": "Level",
    "GRADED": "Graded",
    "GUARANTEED_ISSUE": "Guaranteed Issue",
    "DECLINE": "Decline",
    "SELECT": "Graded",         # carrier-specific tier; treat as non-level until we refine per carrier/product
    "ROP": "Graded",            # return-of-premium or modified style is not true day-1 level
    "MODIFIED": "Graded",
    "QUESTION_BASED": "Level",  # provisional; later we’ll encode the question logic explicitly
    "NOT_ASKED": "Level",        # means no underwriting question for that carrier in this grid row
}
