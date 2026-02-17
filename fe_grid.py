def apply_fe_grid(carriers, age,
                  diabetes=False, a1c=None,
                  chf=False,
                  afib=False,
                  copd=False,
                  stroke=False):

    # Diabetes grid refinement
    if diabetes:
        # MOO diagnosed before 50 → Graded
        if age < 50:
            carriers["Mutual of Omaha"] = "Graded"

        # A1C high refinement
        if a1c and a1c >= 10:
            carriers["Corebridge"] = "Decline"

    # CHF grid refinement (example)
    if chf:
        carriers["Americo"] = "Decline"
        carriers["Mutual of Omaha"] = "Decline"

    # AFIB refinement
    if afib:
        carriers["Americo"] = "Decline"

    # COPD refinement
    if copd:
        carriers["Americo"] = "Decline"

    # Stroke refinement
    if stroke:
        carriers["Americo"] = "Decline"

    return carriers
