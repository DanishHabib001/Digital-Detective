import json
from pathlib import Path
import os

DATA_DIR = Path("data")

CASES_FILE = DATA_DIR / "cases.json"
SUSPECTS_FILE = DATA_DIR / "suspects.json"
EVIDENCE_FILE = DATA_DIR / "evidence.json"
CLUES_FILE = DATA_DIR / "clue.json"
WITNESSES_FILE = DATA_DIR / "witnesses.json"
NOTES_FILE = DATA_DIR / "notes.json"

def ensure_data_directory():
    """Create the data directory if it does not exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_json(file_path):
    """Load a JSON file safely."""

    ensure_data_directory()

    if not file_path.exists():
        save_json(file_path, [])
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        print(f"Warning: {file_path.name} contains invalid data.")
        return []

    except json.JSONDecodeError:
        print(
            f"Warning: {file_path.name} is corrupted. "
            "Starting with empty data."
        )
        return []

    except OSError as error:
        print(f"Error reading {file_path.name}: {error}")
        return []


def save_json(file_path, data):
    """Save data safely to a JSON file."""

    ensure_data_directory()

    try:
        temporary_file = file_path.with_suffix(".tmp")

        with open(temporary_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        temporary_file.replace(file_path)

    except OSError as error:
        print(f"Error saving {file_path.name}: {error}")


def load_cases():
    """Load cases from cases.json."""
    return load_json(CASES_FILE)


def save_cases(cases):
    """Save cases to cases.json."""
    save_json(CASES_FILE, cases)


def load_suspects():
    """Load suspects from suspects.json."""
    return load_json(SUSPECTS_FILE)


def save_suspects(suspects):
    """Save suspects to suspects.json."""
    save_json(SUSPECTS_FILE, suspects)
def load_evidence():
    """Load evidence from evidence.json."""
    return load_json(EVIDENCE_FILE)


def save_evidence(evidence):
    """Save evidence to evidence.json."""
    save_json(EVIDENCE_FILE, evidence)

def load_clues():
    """Load clues from clues.json."""
    return load_json(CLUES_FILE)


def save_clues(clues):
    """Save clues to clues.json."""
    save_json(CLUES_FILE, clues)

def load_witnesses():
    """Load witnesses from witnesses.json."""
    return load_json(WITNESSES_FILE)


def save_witnesses(witnesses):
    """Save witnesses to witnesses.json."""
    save_json(WITNESSES_FILE, witnesses)

def load_notes():
    """Load investigation notes."""
    return load_json(NOTES_FILE)


def save_notes(notes):
    """Save investigation notes."""
    save_json(NOTES_FILE, notes)


EVIDENCE_FILES_FILE = "data/evidence_files.json"


def load_evidence_files():

    if not os.path.exists(
        EVIDENCE_FILES_FILE
    ):
        return []

    try:

        with open(
            EVIDENCE_FILES_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (
        json.JSONDecodeError,
        FileNotFoundError
    ):

        return []


def save_evidence_files(
    evidence_files
):

    os.makedirs(
        "data",
        exist_ok=True
    )

    with open(
        EVIDENCE_FILES_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            evidence_files,
            file,
            indent=4
        )