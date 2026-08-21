
def validate_required(value, field_name):
    """Check that a required field is not empty."""

    if not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")

    return value.strip()


def validate_case_id(case_id, cases):
    """Validate that the Case ID is present and unique."""

    case_id = validate_required(case_id, "Case ID")

    for case in cases:
        if case["id"] == case_id:
            raise ValueError("This Case ID already exists.")

    return case_id


def validate_choice(choice, options, field_name):
    """Validate a menu choice."""

    if choice not in options:
        raise ValueError(
            f"Invalid {field_name}. Please select a valid option."
        )

    return options[choice]


def validate_suspect_id(suspect_id, suspects):
    """Validate that the Suspect ID is present and unique."""

    suspect_id = validate_required(
        suspect_id,
        "Suspect ID"
    )

    for suspect in suspects:
        if suspect["id"] == suspect_id:
            raise ValueError(
                "This Suspect ID already exists."
            )

    return suspect_id


def validate_age(age):
    """Validate suspect age."""

    try:
        age = int(age)
    except ValueError:
        raise ValueError("Age must be a number.")

    if age < 1 or age > 120:
        raise ValueError(
            "Age must be between 1 and 120."
        )

    return age


def validate_evidence_id(evidence_id, evidence):
    """Validate that Evidence ID is unique."""

    evidence_id = validate_required(
        evidence_id,
        "Evidence ID"
    )

    for item in evidence:
        if item["id"] == evidence_id:
            raise ValueError(
                "This Evidence ID already exists."
            )

    return evidence_id

def validate_clue_id(clue_id, clues):
    """Validate that Clue ID is unique."""

    clue_id = validate_required(
        clue_id,
        "Clue ID"
    )

    for clue in clues:
        if clue["id"] == clue_id:
            raise ValueError(
                "This Clue ID already exists."
            )

    return clue_id

def validate_witness_id(witness_id, witnesses):
    """Validate that Witness ID is unique."""

    witness_id = validate_required(
        witness_id,
        "Witness ID"
    )

    for witness in witnesses:
        if witness["id"] == witness_id:
            raise ValueError(
                "This Witness ID already exists."
            )

    return witness_id

def validate_note_id(note_id, notes):
    """Validate that Notes ID is unique."""
    note_id = validate_required(
        note_id,
        "Note ID"
    )

    for note in notes:
        if note["id"] == note_id:
            raise ValueError(
                "this Note ID already exists."
            )

    return note_id

