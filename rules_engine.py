def evaluate_client(age, smoker=False, oxygen=False, adls=False,
                    diabetes=False, a1c=None,
                    cancer=False, cancer_timeline=None,
                    heart=False, heart_timeline=None,
                    dialysis=False):

    carriers = {
        "Americo": "Level",
        "Mutual of Omaha": "Level",
        "Transamerica": "Level",
        "Corebridge": "Level",
        "Aetna": "Level",
        "Royal Neighbors": "Level",
        "American Amicable": "Level",
    }

    # AGE 91+
    if age >= 91:
        return {c: "Decline" for c in carriers}

    # AGE 86–90
    if 86 <= age <= 90:
        for c in carriers:
            carriers[c] = "Decline"
        carriers["Aetna"] = "Level"
        return carriers

    # SMOKER 71–80 (Corebridge MAX rule only)
    if smoker and 71 <= age <= 80:
        carriers["Corebridge"] = "Decline"

    # ADLs
    if adls:
        for c in carriers:
            carriers[c] = "Decline"
        if 50 <= age <= 80:
            carriers["Corebridge"] = "Guaranteed Issue"
        if 81 <= age <= 90:
            carriers["Aetna"] = "Level"
        return carriers

    # OXYGEN
    if oxygen:
        for c in carriers:
            carriers[c] = "Decline"
        if 50 <= age <= 80:
            carriers["Corebridge"] = "Guaranteed Issue"
        if 81 <= age <= 90:
            carriers["Aetna"] = "Level"
        return carriers

    # DIABETES
    if diabetes and a1c:
        if a1c >= 10:
            carriers["Transamerica"] = "Level"
            carriers["Aetna"] = "Level"
        elif 8.7 <= a1c < 10:
            carriers["Corebridge"] = "Graded"

    # CANCER
    if cancer and cancer_timeline:
        if cancer_timeline == "Within 12 months":
            carriers["Transamerica"] = "Graded"
        elif cancer_timeline == "12-24 months":
            carriers["Corebridge"] = "Graded"

    # HEART
    if heart and heart_timeline:
        if heart_timeline == "Within 12 months":
            carriers["Transamerica"] = "Level"
        elif heart_timeline == "12-24 months":
            carriers["Corebridge"] = "Graded"

    # DIALYSIS
    if dialysis:
        carriers["Transamerica"] = "Graded"

    return carriers
