from datetime import datetime
import hashlib
import os
import shutil
from storage.json_storage import (
    load_cases,
    save_cases,
    load_suspects,
    save_suspects,
    load_evidence,
    save_evidence,
    load_clues,
    save_clues,
    load_witnesses,
    save_witnesses,
    load_notes,
    save_notes,
    load_evidence_files,
    save_evidence_files
    )
   
from utils.validators import(
      validate_required,
      validate_case_id,
      validate_choice,
      validate_suspect_id,
      validate_age,
      validate_evidence_id,
      validate_clue_id,
      validate_witness_id,
      validate_note_id
    )
cases = load_cases()
suspects = load_suspects()
evidence = load_evidence()
clues = load_clues()
witnesses = load_witnesses()
notes = load_notes()
evidence_files = load_evidence_files()
APP_NAME = "DIGITAL DETECTIVE"

def green_line(length=60):
    print("\033[92m" + "-" * length + "\033[0m")

def double_green_line(lenght=60):
    ("\033[92m" + "=" * lenght + "\033[0m")

def case_management():
    while True:
        double_green_line(50)
        print("              CASE MANAGEMENT")
        double_green_line(50)
        print("1. Create Case")
        print("2. View All Cases")
        print("3. View Case Details")
        print("4. Update Case")
        print("5. Delete Case")
        print("6. Back to Main Menu")
        double_green_line(50)

        choice = input("Enter your choice: ")

        if choice == "1":
            create_case()

        elif choice == "2":
            view_all_cases()

        elif choice == "3":
            view_case_details()

        elif choice == "4":
            update_case()

        elif choice == "5":
            delete_case()

        elif choice == "6":
            break

        else:
            print("Invalid choice. Please try again.")

def create_case():
    print("\n--- CREATE NEW CASE ---")

    try:
        case_id = input("Enter Case ID: ")
        case_id = validate_case_id(case_id, cases)

        title = input("Enter Case Title: ")
        title = validate_required(title, "Case Title")

        description = input("Enter Case Description: ")
        description = validate_required(description, "Description")

        case_type = input("Enter Case Type: ")
        case_type = validate_required(case_type, "Case Type")

        location = input("Enter Location: ")
        location = validate_required(location, "Location")

        print("\nStatus Options:")
        print("1. OPEN")
        print("2. UNDER_INVESTIGATION")
        print("3. CLOSED")
        print("4. COLD")

        status_options = {
            "1": "OPEN",
            "2": "UNDER_INVESTIGATION",
            "3": "CLOSED",
            "4": "COLD"
        }

        status_choice = input("Select Status: ")
        status = validate_choice(
            status_choice,
            status_options,
            "status"
        )

        print("\nPriority Options:")
        print("1. LOW")
        print("2. MEDIUM")
        print("3. HIGH")
        print("4. CRITICAL")

        priority_options = {
            "1": "LOW",
            "2": "MEDIUM",
            "3": "HIGH",
            "4": "CRITICAL"
        }

        priority_choice = input("Select Priority: ")
        priority = validate_choice(
            priority_choice,
            priority_options,
            "priority"
        )

        case = {
            "id": case_id,
            "title": title,
            "description": description,
            "type": case_type,
            "location": location,
            "created_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "status": status,
            "priority": priority
        }

        cases.append(case)
        save_cases(cases)

        print("\nCase created successfully!")
        print(f"Case ID: {case_id}")

    except ValueError as error:
        print(f"\nError: {error}")


def view_all_cases():
    print("\n--- ALL CASES ---")

    if not cases:
        print("No cases found.")
        return

    for case in cases:
        green_line(50)
        print(f"ID       : {case['id']}")
        print(f"Title    : {case['title']}")
        print(f"Status   : {case['status']}")
        print(f"Priority : {case['priority']}")
        print(f"Created  : {case['created_at']}")


def view_case_details():
    print("\n--- CASE DETAILS ---")

    case_id = input("Enter Case ID: ").strip()

    for case in cases:
        if case["id"] == case_id:

            green_line(50)
            print("CASE INFORMATION")
            green_line(50)

            print(f"Case ID     : {case['id']}")
            print(f"Title       : {case['title']}")
            print(f"Description : {case['description']}")
            print(f"Type        : {case['type']}")
            print(f"Location    : {case['location']}")
            print(f"Created At  : {case['created_at']}")
            print(f"Status      : {case['status']}")
            print(f"Priority    : {case['priority']}")

            return

    print("Case not found.")


def update_case():
    print("\n--- UPDATE CASE ---")

    case_id = input("Enter Case ID: ").strip()

    for case in cases:

        if case["id"] == case_id:

            print("\nPress Enter to keep the current value.")

            title = input(
                f"Title [{case['title']}]: "
            ).strip()

            description = input(
                f"Description [{case['description']}]: "
            ).strip()

            location = input(
                f"Location [{case['location']}]: "
            ).strip()

            if title:
                case["title"] = title

            if description:
                case["description"] = description

            if location:
                case["location"] = location

            print("\nStatus Options:")
            print("1. OPEN")
            print("2. UNDER_INVESTIGATION")
            print("3. CLOSED")
            print("4. COLD")
            print("5. Keep Current Status")

            status_choice = input("Select Status: ")

            status_options = {
                "1": "OPEN",
                "2": "UNDER_INVESTIGATION",
                "3": "CLOSED",
                "4": "COLD"
            }

            if status_choice in status_options:
                case["status"] = status_options[status_choice]

            print("\nPriority Options:")
            print("1. LOW")
            print("2. MEDIUM")
            print("3. HIGH")
            print("4. CRITICAL")
            print("5. Keep Current Priority")

            priority_choice = input("Select Priority: ")

            priority_options = {
                "1": "LOW",
                "2": "MEDIUM",
                "3": "HIGH",
                "4": "CRITICAL"
            }

            if priority_choice in priority_options:
                case["priority"] = priority_options[priority_choice]
            save_cases(cases)
            
            print("\nCase updated successfully!")
            return

    print("Case not found.")


def delete_case():
    print("\n--- DELETE CASE ---")

    case_id = input("Enter Case ID: ").strip()

    for case in cases:

        if case["id"] == case_id:

            print(f"\nCase Found: {case['title']}")

            confirmation = input(
                "Are you sure you want to delete this case? (yes/no): "
            ).strip().lower()

            if confirmation == "yes":
                cases.remove(case)
                save_cases(cases)
                print("Case deleted successfully.")

            else:
                print("Deletion cancelled.")

            return

    print("Case not found.")

def suspect_management():
    while True:
        double_green_line(50)
        print("            SUSPECT MANAGEMENT")
        double_green_line(50)

        print("1. Add Suspect")
        print("2. View All Suspects")
        print("3. View Suspect Details")
        print("4. Update Suspect")
        print("5. Delete Suspect")
        print("6. Search Suspects")
        print("7. Back to Main Menu")

        double_green_line(50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_suspect()

        elif choice == "2":
            view_all_suspects()

        elif choice == "3":
            view_suspect_details()

        elif choice == "4":
            update_suspect()

        elif choice == "5":
            delete_suspect()

        elif choice == "6":
            search_suspects()

        elif choice == "7":
            break

        else:
            print("\nInvalid choice.")


def add_suspect():
    print("\n--- ADD SUSPECT ---")

    try:
        suspect_id = input("Enter Suspect ID: ")
        suspect_id = validate_suspect_id(
            suspect_id,
            suspects
        )

        case_id = validate_required(
            input("Enter Case ID: "),
            "Case ID"
        )

        # Check whether case exists
        case_exists = False

        for case in cases:
            if case["id"] == case_id:
                case_exists = True
                break

        if not case_exists:
            raise ValueError(
                "The specified Case ID does not exist."
            )

        name = validate_required(
            input("Enter Name: "),
            "Name"
        )

        age = validate_age(
            input("Enter Age: ")
        )

        gender = validate_required(
            input("Enter Gender: "),
            "Gender"
        )

        occupation = validate_required(
            input("Enter Occupation: "),
            "Occupation"
        )

        address = validate_required(
            input("Enter Address: "),
            "Address"
        )

        print("\nRisk Level:")
        print("1. LOW")
        print("2. MEDIUM")
        print("3. HIGH")
        print("4. CRITICAL")

        risk_options = {
            "1": "LOW",
            "2": "MEDIUM",
            "3": "HIGH",
            "4": "CRITICAL"
        }

        risk_choice = input("Select Risk Level: ")

        risk_level = validate_choice(
            risk_choice,
            risk_options,
            "risk level"
        )

        relationship = validate_required(
            input("Enter Relationship: "),
            "Relationship"
        )

        alibi = input(
            "Enter Alibi: "
        ).strip()

        notes = input(
            "Enter Notes: "
        ).strip()

        suspect = {
            "id": suspect_id,
            "case_id": case_id,
            "name": name,
            "age": age,
            "gender": gender,
            "occupation": occupation,
            "address": address,
            "risk_level": risk_level,
            "relationship": relationship,
            "alibi": alibi,
            "notes": notes
        }

        suspects.append(suspect)
        save_suspects(suspects)

        print("\nSuspect added successfully!")

    except ValueError as error:
        print(f"\nError: {error}")


def view_all_suspects():
    print("\n--- ALL SUSPECTS ---")

    if not suspects:
        print("No suspects found.")
        return

    for suspect in suspects:
        green_line(50)
        print(f"ID       : {suspect['id']}")
        print(f"Name     : {suspect['name']}")
        print(f"Case ID  : {suspect['case_id']}")
        print(f"Age      : {suspect['age']}")
        print(f"Risk     : {suspect['risk_level']}")


def view_suspect_details():
    print("\n--- SUSPECT DETAILS ---")

    suspect_id = input(
        "Enter Suspect ID: "
    ).strip()

    for suspect in suspects:

        if suspect["id"] == suspect_id:

            green_line(50)
            print("SUSPECT INFORMATION")
            green_line(50)

            print(f"Suspect ID  : {suspect['id']}")
            print(f"Case ID     : {suspect['case_id']}")
            print(f"Name        : {suspect['name']}")
            print(f"Age         : {suspect['age']}")
            print(f"Gender      : {suspect['gender']}")
            print(f"Occupation  : {suspect['occupation']}")
            print(f"Address     : {suspect['address']}")
            print(f"Risk Level  : {suspect['risk_level']}")
            print(f"Relationship: {suspect['relationship']}")
            print(f"Alibi       : {suspect['alibi']}")
            print(f"Notes       : {suspect['notes']}")

            return

    print("Suspect not found.")


def update_suspect():
    print("\n--- UPDATE SUSPECT ---")

    suspect_id = input(
        "Enter Suspect ID: "
    ).strip()

    for suspect in suspects:

        if suspect["id"] == suspect_id:

            print("\nPress Enter to keep current value.")

            name = input(
                f"Name [{suspect['name']}]: "
            ).strip()

            occupation = input(
                f"Occupation [{suspect['occupation']}]: "
            ).strip()

            address = input(
                f"Address [{suspect['address']}]: "
            ).strip()

            relationship = input(
                f"Relationship [{suspect['relationship']}]: "
            ).strip()

            alibi = input(
                f"Alibi [{suspect['alibi']}]: "
            ).strip()

            notes = input(
                f"Notes [{suspect['notes']}]: "
            ).strip()

            if name:
                suspect["name"] = name

            if occupation:
                suspect["occupation"] = occupation

            if address:
                suspect["address"] = address

            if relationship:
                suspect["relationship"] = relationship

            if alibi:
                suspect["alibi"] = alibi

            if notes:
                suspect["notes"] = notes

            save_suspects(suspects)

            print("\nSuspect updated successfully!")
            return

    print("Suspect not found.")


def delete_suspect():
    print("\n--- DELETE SUSPECT ---")

    suspect_id = input(
        "Enter Suspect ID: "
    ).strip()

    for suspect in suspects:

        if suspect["id"] == suspect_id:

            confirmation = input(
                "Are you sure? (yes/no): "
            ).strip().lower()

            if confirmation == "yes":

                suspects.remove(suspect)
                save_suspects(suspects)

                print(
                    "Suspect deleted successfully!"
                )

            else:
                print("Deletion cancelled.")

            return

    print("Suspect not found.")


def search_suspects():
    print("\n--- SEARCH SUSPECTS ---")

    keyword = input(
        "Enter name, occupation, or risk level: "
    ).strip().lower()

    found = False

    for suspect in suspects:

        if (
            keyword in suspect["name"].lower()
            or keyword in suspect["occupation"].lower()
            or keyword in suspect["risk_level"].lower()
        ):

            green_line(50)
            print(f"ID      : {suspect['id']}")
            print(f"Name    : {suspect['name']}")
            print(f"Case ID : {suspect['case_id']}")
            print(f"Risk    : {suspect['risk_level']}")

            found = True

    if not found:
        print("No matching suspects found.")

def evidence_management():
    while True:

        double_green_line(50)
        print("            EVIDENCE MANAGEMENT")
        double_green_line(50)

        print("1. Add Evidence")
        print("2. View All Evidence")
        print("3. View Evidence Details")
        print("4. Update Evidence")
        print("5. Delete Evidence")
        print("6. Search Evidence")
        print("7. Back to Main Menu")

        double_green_line(50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_evidence()

        elif choice == "2":
            view_all_evidence()

        elif choice == "3":
            view_evidence_details()

        elif choice == "4":
            update_evidence()

        elif choice == "5":
            delete_evidence()

        elif choice == "6":
            search_evidence()

        elif choice == "7":
            break

        else:
            print("\nInvalid choice.")

def add_evidence():
    print("\n--- ADD EVIDENCE ---")

    try:
        evidence_id = input("Enter Evidence ID: ")

        evidence_id = validate_evidence_id(
            evidence_id,
            evidence
        )

        case_id = validate_required(
            input("Enter Case ID: "),
            "Case ID"
        )

        case_exists = False

        for case in cases:
            if case["id"] == case_id:
                case_exists = True
                break

        if not case_exists:
            raise ValueError(
                "The specified Case ID does not exist."
            )

        print("\nEvidence Type:")
        print("1. PHYSICAL")
        print("2. DIGITAL")
        print("3. DOCUMENT")
        print("4. PHOTO")
        print("5. VIDEO")
        print("6. OTHER")

        type_options = {
            "1": "PHYSICAL",
            "2": "DIGITAL",
            "3": "DOCUMENT",
            "4": "PHOTO",
            "5": "VIDEO",
            "6": "OTHER"
        }

        type_choice = input("Select Evidence Type: ")

        evidence_type = validate_choice(
            type_choice,
            type_options,
            "evidence type"
        )

        description = validate_required(
            input("Enter Description: "),
            "Description"
        )

        location_found = validate_required(
            input("Enter Location Found: "),
            "Location Found"
        )

        collected_by = validate_required(
            input("Collected By: "),
            "Collected By"
        )

        chain_of_custody = input(
            "Enter Chain of Custody: "
        ).strip()

        notes = input(
            "Enter Notes: "
        ).strip()

        # Generate SHA-256 hash from evidence information


        hash_data = (
            evidence_id
            + case_id
            + evidence_type
            + description
            + location_found
            + collected_by
        )

        evidence_hash = hashlib.sha256(
            hash_data.encode("utf-8")
        ).hexdigest()

        item = {
            "id": evidence_id,
            "case_id": case_id,
            "type": evidence_type,
            "description": description,
            "location_found": location_found,
            "collected_by": collected_by,
            "collected_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "chain_of_custody": chain_of_custody,
            "hash": evidence_hash,
            "notes": notes
        }

        evidence.append(item)

        save_evidence(evidence)

        print("\nEvidence added successfully!")
        print(f"Evidence ID: {evidence_id}")
        print(f"SHA-256 Hash: {evidence_hash}")

    except ValueError as error:
        print(f"\nError: {error}")

def view_all_evidence():
    print("\n--- ALL EVIDENCE ---")

    if not evidence:
        print("No evidence found.")
        return

    for item in evidence:

        green_line(50)
        print(f"ID       : {item['id']}")
        print(f"Case ID  : {item['case_id']}")
        print(f"Type     : {item['type']}")
        print(f"Collected: {item['collected_at']}")

def view_evidence_details():
    print("\n--- EVIDENCE DETAILS ---")

    evidence_id = input(
        "Enter Evidence ID: "
    ).strip()

    for item in evidence:

        if item["id"] == evidence_id:

            green_line(50)
            print("EVIDENCE INFORMATION")
            green_line(50)

            print(f"Evidence ID       : {item['id']}")
            print(f"Case ID           : {item['case_id']}")
            print(f"Type              : {item['type']}")
            print(f"Description       : {item['description']}")
            print(f"Location Found    : {item['location_found']}")
            print(f"Collected By      : {item['collected_by']}")
            print(f"Collected At      : {item['collected_at']}")
            print(f"Chain of Custody  : {item['chain_of_custody']}")
            print(f"SHA-256 Hash      : {item['hash']}")
            print(f"Notes             : {item['notes']}")

            return

    print("Evidence not found.")

def update_evidence():
    print("\n--- UPDATE EVIDENCE ---")

    evidence_id = input(
        "Enter Evidence ID: "
    ).strip()

    for item in evidence:

        if item["id"] == evidence_id:

            print("\nPress Enter to keep current value.")

            description = input(
                f"Description [{item['description']}]: "
            ).strip()

            location = input(
                f"Location [{item['location_found']}]: "
            ).strip()

            collected_by = input(
                f"Collected By [{item['collected_by']}]: "
            ).strip()

            custody = input(
                f"Chain of Custody [{item['chain_of_custody']}]: "
            ).strip()

            notes = input(
                f"Notes [{item['notes']}]: "
            ).strip()

            if description:
                item["description"] = description

            if location:
                item["location_found"] = location

            if collected_by:
                item["collected_by"] = collected_by

            if custody:
                item["chain_of_custody"] = custody

            if notes:
                item["notes"] = notes

            save_evidence(evidence)

            print("\nEvidence updated successfully!")
            return

    print("Evidence not found.")

def delete_evidence():
    print("\n--- DELETE EVIDENCE ---")

    evidence_id = input(
        "Enter Evidence ID: "
    ).strip()

    for item in evidence:

        if item["id"] == evidence_id:

            confirmation = input(
                "Are you sure? (yes/no): "
            ).strip().lower()

            if confirmation == "yes":

                evidence.remove(item)
                save_evidence(evidence)

                print(
                    "Evidence deleted successfully!"
                )

            else:
                print("Deletion cancelled.")

            return

    print("Evidence not found.")

def search_evidence():
    while True:
        double_green_line(50)
        print("             SEARCH EVIDENCE")
        double_green_line(50)

        print("1. Search by Evidence ID")
        print("2. Search by Type")
        print("3. Search by Location")
        print("4. Search by Collector")
        print("5. Search by Case ID")
        print("6. Back")

        double_green_line(50)

        choice = input("Enter your choice: ").strip()

        if choice == "6":
            break

        if choice not in ["1", "2", "3", "4", "5"]:
            print("Invalid choice.")
            continue

        keyword = input("Enter search value: ").strip().lower()

        if not keyword:
            print("Search value cannot be empty.")
            continue

        results = []

        for item in evidence:

            if choice == "1":
                if keyword in item["id"].lower():
                    results.append(item)

            elif choice == "2":
                if keyword in item["type"].lower():
                    results.append(item)

            elif choice == "3":
                if keyword in item["location_found"].lower():
                    results.append(item)

            elif choice == "4":
                if keyword in item["collected_by"].lower():
                    results.append(item)

            elif choice == "5":
                if keyword in item["case_id"].lower():
                    results.append(item)

        if not results:
            print("\nNo matching evidence found.")
            continue

        print("\n--- SEARCH RESULTS ---")

        for item in results:
            green_line(60)
            print(f"Evidence ID : {item['id']}")
            print(f"Case ID     : {item['case_id']}")
            print(f"Type        : {item['type']}")
            print(f"Description : {item['description']}")
            print(f"Location    : {item['location_found']}")
            print(f"Collected By: {item['collected_by']}")

        green_line(60)

def clue_management():
    while True:

        double_green_line(50)
        print("              CLUE MANAGEMENT")
        double_green_line(50)

        print("1. Add Clue")
        print("2. View All Clues")
        print("3. View Clue Details")
        print("4. Update Clue")
        print("5. Delete Clue")
        print("6. Search Clues")
        print("7. Back to Main Menu")

        double_green_line(50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_clue()

        elif choice == "2":
            view_all_clues()

        elif choice == "3":
            view_clue_details()

        elif choice == "4":
            update_clue()

        elif choice == "5":
            delete_clue()

        elif choice == "6":
            search_clues()

        elif choice == "7":
            break

        else:
            print("\nInvalid choice.")

def add_clue():
    print("\n--- ADD CLUE ---")

    try:
        clue_id = input("Enter Clue ID: ")

        clue_id = validate_clue_id(
            clue_id,
            clues
        )

        case_id = validate_required(
            input("Enter Case ID: "),
            "Case ID"
        )

        # Check case
        case_exists = False

        for case in cases:
            if case["id"] == case_id:
                case_exists = True
                break

        if not case_exists:
            raise ValueError(
                "The specified Case ID does not exist."
            )

        title = validate_required(
            input("Enter Clue Title: "),
            "Clue Title"
        )

        description = validate_required(
            input("Enter Description: "),
            "Description"
        )

        source = validate_required(
            input("Enter Source: "),
            "Source"
        )

        print("\nImportance:")
        print("1. LOW")
        print("2. MEDIUM")
        print("3. HIGH")
        print("4. CRITICAL")

        importance_options = {
            "1": "LOW",
            "2": "MEDIUM",
            "3": "HIGH",
            "4": "CRITICAL"
        }

        importance_choice = input(
            "Select Importance: "
        )

        importance = validate_choice(
            importance_choice,
            importance_options,
            "importance"
        )

        print("\nStatus:")
        print("1. NEW")
        print("2. INVESTIGATING")
        print("3. VERIFIED")
        print("4. DISMISSED")

        status_options = {
            "1": "NEW",
            "2": "INVESTIGATING",
            "3": "VERIFIED",
            "4": "DISMISSED"
        }

        status_choice = input(
            "Select Status: "
        )

        status = validate_choice(
            status_choice,
            status_options,
            "clue status"
        )

        notes = input(
            "Enter Notes: "
        ).strip()

        clue = {
            "id": clue_id,
            "case_id": case_id,
            "title": title,
            "description": description,
            "source": source,
            "importance": importance,
            "status": status,
            "notes": notes,
            "created_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        clues.append(clue)

        save_clues(clues)

        print("\nClue added successfully!")
        print(f"Clue ID: {clue_id}")

    except ValueError as error:
        print(f"\nError: {error}")

def view_all_clues():
    print("\n--- ALL CLUES ---")

    if not clues:
        print("No clues found.")
        return

    for clue in clues:

        green_line(60)

        print(f"ID         : {clue['id']}")
        print(f"Case ID    : {clue['case_id']}")
        print(f"Title      : {clue['title']}")
        print(f"Importance : {clue['importance']}")
        print(f"Status     : {clue['status']}")
        print(f"Source     : {clue['source']}")

def view_clue_details():
    print("\n--- CLUE DETAILS ---")

    clue_id = input(
        "Enter Clue ID: "
    ).strip()

    for clue in clues:

        if clue["id"] == clue_id:

            green_line(60)
            print("CLUE INFORMATION")
            green_line(60)

            print(f"Clue ID     : {clue['id']}")
            print(f"Case ID     : {clue['case_id']}")
            print(f"Title       : {clue['title']}")
            print(f"Description : {clue['description']}")
            print(f"Source      : {clue['source']}")
            print(f"Importance  : {clue['importance']}")
            print(f"Status      : {clue['status']}")
            print(f"Notes       : {clue['notes']}")
            print(f"Created At  : {clue['created_at']}")

            return

    print("Clue not found.")

def update_clue():
    print("\n--- UPDATE CLUE ---")

    clue_id = input(
        "Enter Clue ID: "
    ).strip()

    for clue in clues:

        if clue["id"] == clue_id:

            print("\nPress Enter to keep current value.")

            title = input(
                f"Title [{clue['title']}]: "
            ).strip()

            description = input(
                f"Description [{clue['description']}]: "
            ).strip()

            source = input(
                f"Source [{clue['source']}]: "
            ).strip()

            notes = input(
                f"Notes [{clue['notes']}]: "
            ).strip()

            if title:
                clue["title"] = title

            if description:
                clue["description"] = description

            if source:
                clue["source"] = source

            if notes:
                clue["notes"] = notes

            print("\nImportance:")
            print("1. LOW")
            print("2. MEDIUM")
            print("3. HIGH")
            print("4. CRITICAL")
            print("5. Keep Current")

            importance_choice = input(
                "Select Importance: "
            ).strip()

            importance_options = {
                "1": "LOW",
                "2": "MEDIUM",
                "3": "HIGH",
                "4": "CRITICAL"
            }

            if importance_choice in importance_options:
                clue["importance"] = (
                    importance_options[importance_choice]
                )

            print("\nStatus:")
            print("1. NEW")
            print("2. INVESTIGATING")
            print("3. VERIFIED")
            print("4. DISMISSED")
            print("5. Keep Current")

            status_choice = input(
                "Select Status: "
            ).strip()

            status_options = {
                "1": "NEW",
                "2": "INVESTIGATING",
                "3": "VERIFIED",
                "4": "DISMISSED"
            }

            if status_choice in status_options:
                clue["status"] = (
                    status_options[status_choice]
                )

            save_clues(clues)

            print("\nClue updated successfully!")
            return

    print("Clue not found.")

def delete_clue():
    print("\n--- DELETE CLUE ---")

    clue_id = input(
        "Enter Clue ID: "
    ).strip()

    for clue in clues:

        if clue["id"] == clue_id:

            print(f"Clue: {clue['title']}")

            confirmation = input(
                "Are you sure? (yes/no): "
            ).strip().lower()

            if confirmation == "yes":

                clues.remove(clue)

                save_clues(clues)

                print(
                    "Clue deleted successfully!"
                )

            else:
                print("Deletion cancelled.")

            return

    print("Clue not found.")

def search_clues():
    while True:

        double_green_line(50)
        print("               SEARCH CLUES")
        double_green_line(50)

        print("1. Search by Clue ID")
        print("2. Search by Title")
        print("3. Search by Source")
        print("4. Search by Importance")
        print("5. Search by Status")
        print("6. Search by Case ID")
        print("7. Back")

        double_green_line(50)

        choice = input("Enter your choice: ").strip()

        if choice == "7":
            break

        if choice not in ["1", "2", "3", "4", "5", "6"]:
            print("Invalid choice.")
            continue

        keyword = input(
            "Enter search value: "
        ).strip().lower()

        if not keyword:
            print("Search value cannot be empty.")
            continue

        results = []

        for clue in clues:

            if choice == "1":
                value = clue["id"]

            elif choice == "2":
                value = clue["title"]

            elif choice == "3":
                value = clue["source"]

            elif choice == "4":
                value = clue["importance"]

            elif choice == "5":
                value = clue["status"]

            else:
                value = clue["case_id"]

            if keyword in value.lower():
                results.append(clue)

        if not results:
            print("\nNo matching clues found.")
            continue

        print("\n--- SEARCH RESULTS ---")

        for clue in results:

            green_line(60)

            print(f"Clue ID    : {clue['id']}")
            print(f"Case ID    : {clue['case_id']}")
            print(f"Title      : {clue['title']}")
            print(f"Source     : {clue['source']}")
            print(f"Importance : {clue['importance']}")
            print(f"Status     : {clue['status']}")

        green_line(60)

def witness_management():
    while True:

        double_green_line(50)
        print("            WITNESS MANAGEMENT")
        double_green_line(50)

        print("1. Add Witness")
        print("2. View All Witnesses")
        print("3. View Witness Details")
        print("4. Update Witness")
        print("5. Delete Witness")
        print("6. Search Witnesses")
        print("7. Back to Main Menu")

        double_green_line(50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_witness()

        elif choice == "2":
            view_all_witnesses()

        elif choice == "3":
            view_witness_details()

        elif choice == "4":
            update_witness()

        elif choice == "5":
            delete_witness()

        elif choice == "6":
            search_witnesses()

        elif choice == "7":
            break

        else:
            print("\nInvalid choice.")

def add_witness():
    print("\n--- ADD WITNESS ---")

    try:
        witness_id = input("Enter Witness ID: ")

        witness_id = validate_witness_id(
            witness_id,
            witnesses
        )

        case_id = validate_required(
            input("Enter Case ID: "),
            "Case ID"
        )

        # Check whether case exists
        case_exists = False

        for case in cases:
            if case["id"] == case_id:
                case_exists = True
                break

        if not case_exists:
            raise ValueError(
                "The specified Case ID does not exist."
            )

        name = validate_required(
            input("Enter Name: "),
            "Name"
        )

        age = validate_age(
            input("Enter Age: "),
        )

        gender = validate_required(
            input("Enter Gender: "),
            "Gender"
        )

        contact = validate_required(
            input("Enter Contact: "),
            "Contact"
        )

        address = validate_required(
            input("Enter Address: "),
            "Address"
        )

        statement = validate_required(
            input("Enter Statement: "),
            "Statement"
        )

        print("\nCredibility:")
        print("1. LOW")
        print("2. MEDIUM")
        print("3. HIGH")
        print("4. VERY HIGH")

        credibility_options = {
            "1": "LOW",
            "2": "MEDIUM",
            "3": "HIGH",
            "4": "VERY HIGH"
        }

        credibility_choice = input(
            "Select Credibility: "
        ).strip()

        credibility = validate_choice(
            credibility_choice,
            credibility_options,
            "credibility"
        )

        notes = input(
            "Enter Notes: "
        ).strip()

        witness = {
            "id": witness_id,
            "case_id": case_id,
            "name": name,
            "age": age,
            "gender": gender,
            "contact": contact,
            "address": address,
            "statement": statement,
            "credibility": credibility,
            "notes": notes,
            "created_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        witnesses.append(witness)

        save_witnesses(witnesses)

        print("\nWitness added successfully!")
        print(f"Witness ID: {witness_id}")

    except ValueError as error:
        print(f"\nError: {error}")

def view_all_witnesses():
    print("\n--- ALL WITNESSES ---")

    if not witnesses:
        print("No witnesses found.")
        return

    for witness in witnesses:

        green_line(60)

        print(f"ID           : {witness['id']}")
        print(f"Case ID      : {witness['case_id']}")
        print(f"Name         : {witness['name']}")
        print(f"Age          : {witness['age']}" " years")
        print(f"Credibility  : {witness['credibility']}")

def view_witness_details():
    print("\n--- WITNESS DETAILS ---")

    witness_id = input(
        "Enter Witness ID: "
    ).strip()

    for witness in witnesses:

        if witness["id"] == witness_id:

            green_line(60)
            print("WITNESS INFORMATION")
            green_line(60)

            print(f"Witness ID  : {witness['id']}")
            print(f"Case ID     : {witness['case_id']}")
            print(f"Name        : {witness['name']}")
            print(f"Age         : {witness['age']}")
            print(f"Gender      : {witness['gender']}")
            print(f"Contact     : {witness['contact']}")
            print(f"Address     : {witness['address']}")
            print(f"Statement   : {witness['statement']}")
            print(f"Credibility : {witness['credibility']}")
            print(f"Notes       : {witness['notes']}")
            print(f"Created At  : {witness['created_at']}")

            return

    print("Witness not found.")

def update_witness():
    print("\n--- UPDATE WITNESS ---")

    witness_id = input(
        "Enter Witness ID: "
    ).strip()

    for witness in witnesses:

        if witness["id"] == witness_id:

            print("\nPress Enter to keep current value.")

            name = input(
                f"Name [{witness['name']}]: "
            ).strip()

            contact = input(
                f"Contact [{witness['contact']}]: "
            ).strip()

            address = input(
                f"Address [{witness['address']}]: "
            ).strip()

            statement = input(
                f"Statement [{witness['statement']}]: "
            ).strip()

            notes = input(
                f"Notes [{witness['notes']}]: "
            ).strip()

            if name:
                witness["name"] = name

            if contact:
                witness["contact"] = contact

            if address:
                witness["address"] = address

            if statement:
                witness["statement"] = statement

            if notes:
                witness["notes"] = notes

            print("\nCredibility:")
            print("1. LOW")
            print("2. MEDIUM")
            print("3. HIGH")
            print("4. VERY HIGH")
            print("5. Keep Current")

            credibility_choice = input(
                "Select Credibility: "
            ).strip()

            credibility_options = {
                "1": "LOW",
                "2": "MEDIUM",
                "3": "HIGH",
                "4": "VERY HIGH"
            }

            if credibility_choice in credibility_options:
                witness["credibility"] = (
                    credibility_options[credibility_choice]
                )

            save_witnesses(witnesses)

            print("\nWitness updated successfully!")
            return

    print("Witness not found.")

def delete_witness():
    print("\n--- DELETE WITNESS ---")

    witness_id = input(
        "Enter Witness ID: "
    ).strip()

    for witness in witnesses:

        if witness["id"] == witness_id:

            print(f"Witness: {witness['name']}")

            confirmation = input(
                "Are you sure? (yes/no): "
            ).strip().lower()

            if confirmation == "yes":

                witnesses.remove(witness)

                save_witnesses(witnesses)

                print(
                    "Witness deleted successfully!"
                )

            else:
                print("Deletion cancelled.")

            return

    print("Witness not found.")

def search_witnesses():
    while True:

        double_green_line(50)
        print("             SEARCH WITNESSES")
        double_green_line(50)

        print("1. Search by Witness ID")
        print("2. Search by Name")
        print("3. Search by Contact")
        print("4. Search by Credibility")
        print("5. Search by Case ID")
        print("6. Back")

        double_green_line(50)

        choice = input("Enter your choice: ").strip()

        if choice == "6":
            break

        if choice not in ["1", "2", "3", "4", "5"]:
            print("Invalid choice.")
            continue

        keyword = input(
            "Enter search value: "
        ).strip().lower()

        if not keyword:
            print("Search value cannot be empty.")
            continue

        results = []

        for witness in witnesses:

            if choice == "1":
                value = witness["id"]

            elif choice == "2":
                value = witness["name"]

            elif choice == "3":
                value = witness["contact"]

            elif choice == "4":
                value = witness["credibility"]

            else:
                value = witness["case_id"]

            if keyword in value.lower():
                results.append(witness)

        if not results:
            print("\nNo matching witnesses found.")
            continue

        print("\n--- SEARCH RESULTS ---")

        for witness in results:

            green_line(60)

            print(f"Witness ID  : {witness['id']}")
            print(f"Case ID     : {witness['case_id']}")
            print(f"Name        : {witness['name']}")
            print(f"Contact     : {witness['contact']}")
            print(f"Credibility : {witness['credibility']}")

        green_line(60)

def investigation_notes():
    while True:

        double_green_line(50)
        print("          INVESTIGATION NOTES")
        double_green_line(50)

        print("1. Add Note")
        print("2. View All Notes")
        print("3. View Note Details")
        print("4. Update Note")
        print("5. Delete Note")
        print("6. Search Notes")
        print("7. Back to Main Menu")

        double_green_line(50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_note()

        elif choice == "2":
            view_all_notes()

        elif choice == "3":
            view_note_details()

        elif choice == "4":
            update_note()

        elif choice == "5":
            delete_note()

        elif choice == "6":
            search_notes()

        elif choice == "7":
            break

        else:
            print("\nInvalid choice.")

def add_note():
    print("\n--- ADD INVESTIGATION NOTE ---")

    try:
        note_id = input("Enter Note ID: ").strip()

        note_id = validate_note_id(
            note_id,
            notes
        )

        case_id = validate_required(
            input("Enter Case ID: "),
            "Case ID"
        )

        case_exists = False

        for case in cases:
            if case["id"] == case_id:
                case_exists = True
                break

        if not case_exists:
            raise ValueError(
                "The specified Case ID does not exist."
            )

        title = validate_required(
            input("Enter Note Title: "),
            "Note Title"
        )

        content = validate_required(
            input("Enter Note Content: "),
            "Note Content"
        )

        author = validate_required(
            input("Enter Author: "),
            "Author"
        )

        print("\nCategory:")
        print("1. INTERVIEW")
        print("2. OBSERVATION") 
        print("3. LEAD")
        print("4. ANALYSIS")
        print("5. FOLLOW_UP")
        print("6. ADMINISTRATIVE")  

        category_Options = {

         "1": "INTERVIEW",
         "2": "OBSERVATION",
         "3": "LEAD",
         "4": "ANALYSIS",
         "5": "FOLLOW_UP",
         "6": "ADMINISTRATIVE"
        }
        
        category_choice = input(
            "Select Category: "
        ).strip()

        category = validate_choice(
           
            category_choice,
            category_Options,
            "category"
        )
    

        print("\nPriority:")
        print("1. LOW")
        print("2. MEDIUM")
        print("3. HIGH")
        print("4. CRITICAL")

        priority_options = {
            "1": "LOW",
            "2": "MEDIUM",
            "3": "HIGH",
            "4": "CRITICAL"
        }

        priority_choice = input(
            "Select Priority: "
        ).strip()

        priority = validate_choice(
            priority_choice,
            priority_options,
            "priority"
        )

        current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        note = {
            "id": note_id,
            "case_id": case_id,
            "title": title,
            "content": content,
            "author": author,
            "category": category,
            "priority": priority,
            "created_at": current_time,
            "updated_at": current_time
        }

        notes.append(note)

        save_notes(notes)

        print("\nInvestigation note added successfully!")
        print(f"Note ID: {note_id}")

    except ValueError as error:
        print(f"\nError: {error}")

def view_all_notes():
    print("\n--- ALL INVESTIGATION NOTES ---")

    if not notes:
        print("No investigation notes found.")
        return

    for note in notes:

        green_line(60)

        print(f"ID       : {note['id']}")
        print(f"Case ID  : {note['case_id']}")
        print(f"Title    : {note['title']}")
        print(f"Category : {note['category']}")
        print(f"Priority : {note['priority']}")
        print(f"Author   : {note['author']}")

def view_note_details():
    print("\n--- NOTE DETAILS ---")

    note_id = input(
        "Enter Note ID: "
    ).strip()

    for note in notes:

        if note["id"] == note_id:

            green_line(60)
            print("INVESTIGATION NOTE INFORMATION")
            green_line(60)

            print(f"Note ID    : {note['id']}")
            print(f"Case ID    : {note['case_id']}")
            print(f"Title      : {note['title']}")
            print(f"Content    : {note['content']}")
            print(f"Author     : {note['author']}")
            print(f"Category   : {note['category']}")
            print(f"Priority   : {note['priority']}")
            print(f"Created At : {note['created_at']}")
            print(f"Updated At : {note['updated_at']}")

            return

    print("Note not found.")

def update_note():
    print("\n--- UPDATE INVESTIGATION NOTE ---")

    note_id = input(
        "Enter Note ID: "
    ).strip()

    for note in notes:

        if note["id"] == note_id:

            print("\nPress Enter to keep current value.")

            title = input(
                f"Title [{note['title']}]: "
            ).strip()

            content = input(
                f"Content [{note['content']}]: "
            ).strip()

            author = input(
                f"Author [{note['author']}]: "
            ).strip()

            category = input(
                f"Category [{note['category']}]: "
            ).strip()

            if title:
                note["title"] = title

            if content:
                note["content"] = content

            if author:
                note["author"] = author

            if category:
                note["category"] = category

            print("\nPriority:")
            print("1. LOW")
            print("2. MEDIUM")
            print("3. HIGH")
            print("4. CRITICAL")
            print("5. Keep Current")

            priority_options = {
                "1": "LOW",
                "2": "MEDIUM",
                "3": "HIGH",
                "4": "CRITICAL"
            }

            priority_choice = input(
                "Select Priority: "
            ).strip()

            if priority_choice in priority_options:
                note["priority"] = (
                    priority_options[priority_choice]
                )

            note["updated_at"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            save_notes(notes)

            print("\nNote updated successfully!")
            return

    print("Note not found.")

def delete_note():
    print("\n--- DELETE INVESTIGATION NOTE ---")

    note_id = input(
        "Enter Note ID: "
    ).strip()

    for note in notes:

        if note["id"] == note_id:

            print(f"Note: {note['title']}")

            confirmation = input(
                "Are you sure? (yes/no): "
            ).strip().lower()

            if confirmation == "yes":

                notes.remove(note)

                save_notes(notes)

                print(
                    "Note deleted successfully!"
                )

            else:
                print("Deletion cancelled.")

            return

    print("Note not found.")

def search_notes():

    while True:

        double_green_line(50)
        print("              SEARCH NOTES")
        double_green_line(50)

        print("1. Search by Note ID")
        print("2. Search by Title")
        print("3. Search by Category")
        print("4. Search by Author")
        print("5. Search by Priority")
        print("6. Search by Case ID")
        print("7. Back")

        double_green_line(50)

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "7":
            break

        if choice not in [
            "1", "2", "3", "4", "5", "6"
        ]:
            print("Invalid choice.")
            continue

        keyword = input(
            "Enter search value: "
        ).strip().lower()

        if not keyword:
            print(
                "Search value cannot be empty."
            )
            continue

        results = []

        for note in notes:

            if choice == "1":
                value = note["id"]

            elif choice == "2":
                value = note["title"]

            elif choice == "3":
                value = note["category"]

            elif choice == "4":
                value = note["author"]

            elif choice == "5":
                value = note["priority"]

            else:
                value = note["case_id"]

            if keyword in value.lower():
                results.append(note)

        if not results:
            print(
                "\nNo matching notes found."
            )
            continue

        print("\n--- SEARCH RESULTS ---")

        for note in results:

            green_line(60)

            print(f"Note ID   : {note['id']}")
            print(f"Case ID   : {note['case_id']}")
            print(f"Title     : {note['title']}")
            print(f"Category  : {note['category']}")
            print(f"Author    : {note['author']}")
            print(f"Priority  : {note['priority']}")

        green_line(60)

def global_search():
    while True:

        double_green_line(50)
        print("                 GLOBAL SEARCH")
        double_green_line(50)

        print("1. Search Cases")
        print("2. Search Suspects")
        print("3. Search Evidence")
        print("4. Search Clues")
        print("5. Search Witnesses")
        print("6. Search Investigation Notes")
        print("7. Search Everything")
        print("8. Back to Main Menu")

        double_green_line(50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            search_cases_global()

        elif choice == "2":
            search_suspects_global()

        elif choice == "3":
            search_evidence_global()

        elif choice == "4":
            search_clues_global()

        elif choice == "5":
            search_witnesses_global()

        elif choice == "6":
            search_notes_global()

        elif choice == "7":
            search_everything()

        elif choice == "8":
            break

        else:
            print("\nInvalid choice.")

def search_cases_global():

    print("\n--- SEARCH CASES ---")

    keyword = input(
        "Enter Case ID, Title, Type, or Location: "
    ).strip().lower()

    if not keyword:
        print("Search value cannot be empty.")
        return

    results = []

    for case in cases:

        if (
            keyword in case["id"].lower()
            or keyword in case["title"].lower()
            or keyword in case["type"].lower()
            or keyword in case["location"].lower()
        ):
            results.append(case)

    if not results:
        print("\nNo matching cases found.")
        return

    print("\n--- CASE SEARCH RESULTS ---")

    for case in results:

        green_line(60)
        print(f"Case ID  : {case['id']}")
        print(f"Title    : {case['title']}")
        print(f"Type     : {case['type']}")
        print(f"Location : {case['location']}")
        print(f"Status   : {case['status']}")
        print(f"Priority : {case['priority']}")

def search_suspects_global():

    print("\n--- SEARCH SUSPECTS ---")

    keyword = input(
        "Enter Suspect ID, Name, Occupation, or Case ID: "
    ).strip().lower()

    if not keyword:
        print("Search value cannot be empty.")
        return

    results = []

    for suspect in suspects:

        if (
            keyword in suspect["id"].lower()
            or keyword in suspect["name"].lower()
            or keyword in suspect["occupation"].lower()
            or keyword in suspect["case_id"].lower()
        ):
            results.append(suspect)

    if not results:
        print("\nNo matching suspects found.")
        return

    print("\n--- SUSPECT SEARCH RESULTS ---")

    for suspect in results:

        green_line(60)
        print(f"Suspect ID : {suspect['id']}")
        print(f"Case ID    : {suspect['case_id']}")
        print(f"Name       : {suspect['name']}")
        print(f"Occupation : {suspect['occupation']}")
        print(f"Risk Level : {suspect['risk_level']}")

def search_evidence_global():

    print("\n--- SEARCH EVIDENCE ---")

    case_id = input(
        "Enter Case ID first: "
    ).strip()

    if not case_id:
        print("Case ID cannot be empty.")
        return

    results = []

    for item in evidence:

        if item["case_id"] == case_id:
            results.append(item)

    if not results:
        print(
            "\nNo evidence found for this Case ID."
        )
        return

    print("\nEvidence Search Options:")
    print("1. Evidence ID")
    print("2. Description")
    print("3. Type")
    print("4. Location")
    print("5. Collector")
    print("6. View All Evidence")

    choice = input(
        "Select search option: "
    ).strip()

    if choice == "6":

        filtered_results = results

    elif choice in ["1", "2", "3", "4", "5"]:

        keyword = input(
            "Enter search value: "
        ).strip().lower()

        if not keyword:
            print("Search value cannot be empty.")
            return

        filtered_results = []

        for item in results:

            if choice == "1":
                value = item["id"]

            elif choice == "2":
                value = item["description"]

            elif choice == "3":
                value = item["type"]

            elif choice == "4":
                value = item["location_found"]

            else:
                value = item["collected_by"]

            if keyword in value.lower():
                filtered_results.append(item)

    else:
        print("Invalid choice.")
        return

    if not filtered_results:
        print("\nNo matching evidence found.")
        return

    print("\n--- EVIDENCE SEARCH RESULTS ---")

    for item in filtered_results:

        green_line(60)
        print(f"Evidence ID : {item['id']}")
        print(f"Case ID     : {item['case_id']}")
        print(f"Description : {item['description']}")
        print(f"Type        : {item['type']}")
        print(f"location_found    : {item['location_found']}")
        print(f"collected_by   : {item['collected_by']}")

def search_clues_global():

    print("\n--- SEARCH CLUES ---")

    keyword = input(
        "Enter Clue ID, Title, Source, or Case ID: "
    ).strip().lower()

    if not keyword:
        print("Search value cannot be empty.")
        return

    results = []

    for clue in clues:

        if (
            keyword in clue["id"].lower()
            or keyword in clue["title"].lower()
            or keyword in clue["source"].lower()
            or keyword in clue["case_id"].lower()
        ):
            results.append(clue)

    if not results:
        print("\nNo matching clues found.")
        return

    print("\n--- CLUE SEARCH RESULTS ---")

    for clue in results:

        green_line(60)
        print(f"Clue ID     : {clue['id']}")
        print(f"Case ID     : {clue['case_id']}")
        print(f"Title       : {clue['title']}")
        print(f"Source      : {clue['source']}")
        print(f"Importance  : {clue['importance']}")
        print(f"Status      : {clue['status']}")

def search_witnesses_global():

    print("\n--- SEARCH WITNESSES ---")

    keyword = input(
        "Enter Witness ID, Name, Contact, or Case ID: "
    ).strip().lower()

    if not keyword:
        print("Search value cannot be empty.")
        return

    results = []

    for witness in witnesses:

        if (
            keyword in witness["id"].lower()
            or keyword in witness["name"].lower()
            or keyword in witness["contact"].lower()
            or keyword in witness["case_id"].lower()
        ):
            results.append(witness)

    if not results:
        print("\nNo matching witnesses found.")
        return

    print("\n--- WITNESS SEARCH RESULTS ---")

    for witness in results:

        green_line(60)
        print(f"Witness ID  : {witness['id']}")
        print(f"Case ID     : {witness['case_id']}")
        print(f"Name        : {witness['name']}")
        print(f"Contact     : {witness['contact']}")
        print(f"Credibility : {witness['credibility']}")

def search_notes_global():

    print("\n--- SEARCH INVESTIGATION NOTES ---")

    keyword = input(
        "Enter Note ID, Title, Author, Category, or Case ID: "
    ).strip().lower()

    if not keyword:
        print("Search value cannot be empty.")
        return

    results = []

    for note in notes:

        if (
            keyword in note["id"].lower()
            or keyword in note["title"].lower()
            or keyword in note["author"].lower()
            or keyword in note["category"].lower()
            or keyword in note["case_id"].lower()
        ):
            results.append(note)

    if not results:
        print("\nNo matching notes found.")
        return

    print("\n--- NOTE SEARCH RESULTS ---")

    for note in results:

        green_line(60)
        print(f"Note ID  : {note['id']}")
        print(f"Case ID  : {note['case_id']}")
        print(f"Title    : {note['title']}")
        print(f"Author   : {note['author']}")
        print(f"Category : {note['category']}")
        print(f"Priority : {note['priority']}")

def search_everything():

    print("\n--- SEARCH EVERYTHING ---")

    keyword = input(
        "Enter search keyword: "
    ).strip().lower()

    if not keyword:
        print("\nSearch keyword cannot be empty.")
        return

    results_found = False

    
    # CASES
    

    case_results = []

    for item in cases:

        searchable_text = " ".join([
            str(item.get("id", "")),
            str(item.get("title", "")),
            str(item.get("description", "")),
            str(item.get("type", "")),
            str(item.get("location", "")),
            str(item.get("status", "")),
            str(item.get("priority", ""))
        ]).lower()

        if keyword in searchable_text:
            case_results.append(item)

    if case_results:

        results_found = True

        print("\n" + "=" * 60)
        print("CASE RESULTS")
        print("=" * 60)

        for item in case_results:

            green_line(60)

            print(
                f"Case ID   : {item.get('id', 'N/A')}"
            )

            print(
                f"Title     : {item.get('title', 'N/A')}"
            )

            print(
                f"Type      : {item.get('type', 'N/A')}"
            )

            print(
                f"Location  : {item.get('location', 'N/A')}"
            )

            print(
                f"Status    : {item.get('status', 'N/A')}"
            )

    
    # SUSPECTS
    

    suspect_results = []

    for item in suspects:

        searchable_text = " ".join([
            str(item.get("id", "")),
            str(item.get("case_id", "")),
            str(item.get("name", "")),
            str(item.get("age", "")),
            str(item.get("gender", "")),
            str(item.get("occupation", "")),
            str(item.get("address", "")),
            str(item.get("relationship", "")),
            str(item.get("alibi", "")),
            str(item.get("notes", "")),
            str(item.get("risk_level", "")),
            str(item.get("risk", ""))
        ]).lower()

        if keyword in searchable_text:
            suspect_results.append(item)

    if suspect_results:

        results_found = True

        print("\n" + "=" * 60)
        print("SUSPECT RESULTS")
        print("=" * 60)

        for item in suspect_results:

            green_line(60)

            print(
                f"Suspect ID : {item.get('id', 'N/A')}"
            )

            print(
                f"Case ID    : {item.get('case_id', 'N/A')}"
            )

            print(
                f"Name       : {item.get('name', 'N/A')}"
            )

            print(
                f"Occupation : {item.get('occupation', 'N/A')}"
            )

            print(
                f"Risk       : {item.get('risk_level', item.get('risk', 'N/A'))}"
            )

    
    # EVIDENCE
    

    evidence_results = []

    for item in evidence:

        searchable_text = " ".join([
            str(item.get("id", "")),
            str(item.get("case_id", "")),
            str(item.get("description", "")),
            str(item.get("type", "")),
            str(item.get("location", "")),
            str(item.get("collector", "")),
            str(item.get("notes", ""))
        ]).lower()

        if keyword in searchable_text:
            evidence_results.append(item)

    if evidence_results:

        results_found = True

        print("\n" + "=" * 60)
        print("EVIDENCE RESULTS")
        print("=" * 60)

        for item in evidence_results:

            green_line(60)

            print(
                f"Evidence ID : {item.get('id', 'N/A')}"
            )

            print(
                f"Case ID     : {item.get('case_id', 'N/A')}"
            )

            print(
                f"Description : {item.get('description', 'N/A')}"
            )

            print(
                f"Type        : {item.get('type', 'N/A')}"
            )

            print(
                f"Location    : {item.get('location', 'N/A')}"
            )

            print(
                f"Collector   : {item.get('collector', 'N/A')}"
            )

    
    # CLUES
    

    clue_results = []

    for item in clues:

        searchable_text = " ".join([
            str(item.get("id", "")),
            str(item.get("case_id", "")),
            str(item.get("title", "")),
            str(item.get("description", "")),
            str(item.get("source", "")),
            str(item.get("importance", "")),
            str(item.get("status", "")),
            str(item.get("notes", ""))
        ]).lower()

        if keyword in searchable_text:
            clue_results.append(item)

    if clue_results:

        results_found = True

        print("\n" + "=" * 60)
        print("CLUE RESULTS")
        print("=" * 60)

        for item in clue_results:

            green_line(60)

            print(
                f"Clue ID     : {item.get('id', 'N/A')}"
            )

            print(
                f"Case ID     : {item.get('case_id', 'N/A')}"
            )

            print(
                f"Title       : {item.get('title', 'N/A')}"
            )

            print(
                f"Source      : {item.get('source', 'N/A')}"
            )

            print(
                f"Importance  : {item.get('importance', 'N/A')}"
            )

            print(
                f"Status      : {item.get('status', 'N/A')}"
            )

    
    # WITNESSES
    

    witness_results = []

    for item in witnesses:

        searchable_text = " ".join([
            str(item.get("id", "")),
            str(item.get("case_id", "")),
            str(item.get("name", "")),
            str(item.get("age", "")),
            str(item.get("gender", "")),
            str(item.get("contact", "")),
            str(item.get("address", "")),
            str(item.get("statement", "")),
            str(item.get("credibility", "")),
            str(item.get("notes", ""))
        ]).lower()

        if keyword in searchable_text:
            witness_results.append(item)

    if witness_results:

        results_found = True

        print("\n" + "=" * 60)
        print("WITNESS RESULTS")
        print("=" * 60)

        for item in witness_results:

            green_line(60)

            print(
                f"Witness ID  : {item.get('id', 'N/A')}"
            )

            print(
                f"Case ID     : {item.get('case_id', 'N/A')}"
            )

            print(
                f"Name        : {item.get('name', 'N/A')}"
            )

            print(
                f"Contact     : {item.get('contact', 'N/A')}"
            )

            print(
                f"Credibility : {item.get('credibility', 'N/A')}"
            )

    # INVESTIGATION NOTES

    note_results = []

    for item in notes:

        searchable_text = " ".join([
            str(item.get("id", "")),
            str(item.get("case_id", "")),
            str(item.get("title", "")),
            str(item.get("content", "")),
            str(item.get("description", "")),
            str(item.get("priority", "")),
            str(item.get("category", "")),
            str(item.get("notes", ""))
        ]).lower()

        if keyword in searchable_text:
            note_results.append(item)

    if note_results:

        results_found = True

        print("\n" + "=" * 60)
        print("INVESTIGATION NOTE RESULTS")
        print("=" * 60)

        for item in note_results:

            green_line(60)

            print(
                f"Note ID    : {item.get('id', 'N/A')}"
            )

            print(
                f"Case ID    : {item.get('case_id', 'N/A')}"
            )

            print(
                f"Title      : {item.get('title', 'N/A')}"
            )

            print(
                f"Priority   : {item.get('priority', 'N/A')}"
            )

    
    # NO RESULTS
    
    if not results_found:

        print("\n" + "=" * 60)
        print("NO RESULTS FOUND")
        print("=" * 60)

        print(
            f"No records matched: '{keyword}'"
        )

    print("\n" + "=" * 60)

def case_analysis():
    while True:

        double_green_line(50)
        print("                CASE ANALYSIS")
        double_green_line(50)

        print("1. Analyze Case")
        print("2. Case Statistics")
        print("3. Suspect Analysis")
        print("4. Evidence Analysis")
        print("5. Clue Analysis")
        print("6. Witness Analysis")
        print("7. Investigation Summary")
        print("8. Back to Main Menu")

        double_green_line(50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            analyze_case()

        elif choice == "2":
            case_statistics()

        elif choice == "3":
            suspect_analysis()

        elif choice == "4":
            evidence_analysis()

        elif choice == "5":
            clue_analysis()

        elif choice == "6":
            witness_analysis()

        elif choice == "7":
            investigation_summary()

        elif choice == "8":
            break

        else:
            print("\nInvalid choice.")

def analyze_case():

    print("\n--- COMPLETE CASE ANALYSIS ---")

    case_id = input(
        "Enter Case ID: "
    ).strip()

    selected_case = None

    for case in cases:
        if case["id"] == case_id:
            selected_case = case
            break

    if not selected_case:
        print("\nCase not found.")
        return

    case_suspects = [
        suspect for suspect in suspects
        if suspect["case_id"] == case_id
    ]

    case_evidence = [
        item for item in evidence
        if item["case_id"] == case_id
    ]

    case_clues = [
        clue for clue in clues
        if clue["case_id"] == case_id
    ]

    case_witnesses = [
        witness for witness in witnesses
        if witness["case_id"] == case_id
    ]

    case_notes = [
        note for note in notes
        if note["case_id"] == case_id
    ]

    print("\n" + "=" * 60)
    print("                CASE ANALYSIS REPORT")
    print("=" * 60)

    print(f"Case ID       : {selected_case['id']}")
    print(f"Title         : {selected_case['title']}")
    print(f"Type          : {selected_case['type']}")
    print(f"Location      : {selected_case['location']}")
    print(f"Status        : {selected_case['status']}")
    print(f"Priority      : {selected_case['priority']}")

    print("\n--- CASE RECORD COUNTS ---")

    print(f"Suspects      : {len(case_suspects)}")
    print(f"Evidence      : {len(case_evidence)}")
    print(f"Clues         : {len(case_clues)}")
    print(f"Witnesses     : {len(case_witnesses)}")
    print(f"Notes         : {len(case_notes)}")

    print("\n--- SUSPECTS ---")

    if case_suspects:

        for suspect in case_suspects:

            print(
                f"ID: {suspect['id']} | "
                f"Name: {suspect['name']} | "
                f"Risk: {suspect['risk_level']}"
            )

    else:
        print("No suspects recorded.")

    if case_evidence:

        print("\n--- EVIDENCE ---")

        for item in case_evidence:

            print(
                f"ID: {item['id']} | "
                f"Type: {item['type']} | "
                f"Description: {item['description']}"
            )

    else:
        print("No evidence recorded.")

    print("\n--- CLUES ---")

    if case_clues:

        for clue in case_clues:

            print(
                f"ID: {clue['id']} | "
                f"Title: {clue['title']} | "
                f"Status: {clue['status']}"
            )

    else:
        print("No clues recorded.")

    print("\n--- WITNESSES ---")

    if case_witnesses:

        for witness in case_witnesses:

            print(
                f"ID: {witness['id']} | "
                f"Name: {witness['name']} | "
                f"Credibility: {witness['credibility']}"
            )

    else:
        print("No witnesses recorded.")

    print("\n--- INVESTIGATION NOTES ---")

    if case_notes:

        for note in case_notes:

            print(
                f"ID: {note['id']} | "
                f"Title: {note['title']} | "
                f"Priority: {note['priority']}"
            )

    else:
        print("No investigation notes recorded.")

    print("=" * 60)

def case_statistics():

    print("\n--- CASE STATISTICS ---")

    case_id = input(
        "Enter Case ID: "
    ).strip()

    case_exists = any(
        case["id"] == case_id
        for case in cases
    )

    if not case_exists:
        print("\nCase not found.")
        return

    suspect_count = sum(
        1 for suspect in suspects
        if suspect["case_id"] == case_id
    )

    evidence_count = sum(
        1 for item in evidence
        if item["case_id"] == case_id
    )

    clue_count = sum(
        1 for clue in clues
        if clue["case_id"] == case_id
    )

    witness_count = sum(
        1 for witness in witnesses
        if witness["case_id"] == case_id
    )

    note_count = sum(
        1 for note in notes
        if note["case_id"] == case_id
    )

    green_line(50)

    print(f"Case ID              : {case_id}")
    print(f"Total Suspects       : {suspect_count}")
    print(f"Total Evidence       : {evidence_count}")
    print(f"Total Clues          : {clue_count}")
    print(f"Total Witnesses      : {witness_count}")
    print(f"Total Notes          : {note_count}")

    green_line(50)

def suspect_analysis():

    print("\n--- SUSPECT ANALYSIS ---")

    case_id = input(
        "Enter Case ID: "
    ).strip()

    case_suspects = [
        suspect for suspect in suspects
        if suspect["case_id"] == case_id
    ]

    if not case_suspects:
        print("\nNo suspects found for this case.")
        return

    risk_count = {
        "LOW": 0,
        "MEDIUM": 0,
        "HIGH": 0,
        "CRITICAL": 0
    }

    for suspect in case_suspects:

        risk = suspect["risk_level"]

        if risk in risk_count:
            risk_count[risk] += 1

    print("\n--- SUSPECT RISK ANALYSIS ---")

    print(f"Total Suspects : {len(case_suspects)}")
    print(f"LOW            : {risk_count['LOW']}")
    print(f"MEDIUM         : {risk_count['MEDIUM']}")
    print(f"HIGH           : {risk_count['HIGH']}")
    print(f"CRITICAL       : {risk_count['CRITICAL']}")

    print("\n--- SUSPECT DETAILS ---")

    for suspect in case_suspects:

        green_line(50)

        print(f"ID           : {suspect['id']}")
        print(f"Name         : {suspect['name']}")
        print(f"Age          : {suspect['age']}")
        print(f"Occupation   : {suspect['occupation']}")
        print(f"Risk Level   : {suspect['risk_level']}")
        print(f"Relationship : {suspect['relationship']}")
        print(f"Alibi        : {suspect['alibi']}")

def evidence_analysis():

    print("\n--- EVIDENCE ANALYSIS ---")

    case_id = input(
        "Enter Case ID: "
    ).strip()

    case_evidence = [
        item for item in evidence
        if item["case_id"] == case_id
    ]

    if not case_evidence:
        print("\nNo evidence found for this case.")
        return

    type_count = {}

    for item in case_evidence:

        evidence_type = item["type"]

        if evidence_type not in type_count:
            type_count[evidence_type] = 0

        type_count[evidence_type] += 1

    print("\n--- EVIDENCE STATISTICS ---")

    print(
        f"Total Evidence: {len(case_evidence)}"
    )

    print("\nEvidence by Type:")

    for evidence_type, count in type_count.items():

        print(
            f"{evidence_type}: {count}"
        )

    print("\n--- EVIDENCE DETAILS ---")

    for item in case_evidence:

        green_line(50)

        print(f"Evidence ID : {item['id']}")
        print(f"Description : {item['description']}")
        print(f"Type        : {item['type']}")

        # Collector is displayed only if it exists
        if "collector" in item:
            print(f"Collector   : {item['collector']}")

        # Location is displayed only if it exists
        if "location" in item:
            print(f"Location    : {item['location']}")

        green_line(50)



def clue_analysis():

    print("\n--- CLUE ANALYSIS ---")

    case_id = input(
        "Enter Case ID: "
    ).strip()

    case_clues = [
        clue for clue in clues
        if clue["case_id"] == case_id
    ]

    if not case_clues:
        print("\nNo clues found for this case.")
        return

    importance_count = {
        "LOW": 0,
        "MEDIUM": 0,
        "HIGH": 0,
        "CRITICAL": 0
    }

    status_count = {}

    for clue in case_clues:

        importance = clue["importance"]

        if importance in importance_count:
            importance_count[importance] += 1

        status = clue["status"]

        if status not in status_count:
            status_count[status] = 0

        status_count[status] += 1

    print("\n--- CLUE STATISTICS ---")

    print(f"Total Clues : {len(case_clues)}")

    print("\nBy Importance:")

    for level, count in importance_count.items():

        print(f"{level}: {count}")

    print("\nBy Status:")

    for status, count in status_count.items():

        print(f"{status}: {count}")

def witness_analysis():

    print("\n--- WITNESS ANALYSIS ---")

    case_id = input(
        "Enter Case ID: "
    ).strip()

    case_witnesses = [
        witness for witness in witnesses
        if witness["case_id"] == case_id
    ]

    if not case_witnesses:
        print("\nNo witnesses found for this case.")
        return

    credibility_count = {
        "LOW": 0,
        "MEDIUM": 0,
        "HIGH": 0,
        "VERY HIGH": 0
    }

    for witness in case_witnesses:

        credibility = witness["credibility"]

        if credibility in credibility_count:
            credibility_count[credibility] += 1

    print("\n--- WITNESS CREDIBILITY ANALYSIS ---")

    print(
        f"Total Witnesses : {len(case_witnesses)}"
    )

    for level, count in credibility_count.items():

        print(
            f"{level}: {count}"
        )

def investigation_summary():

    print("\n--- INVESTIGATION SUMMARY ---")

    case_id = input(
        "Enter Case ID: "
    ).strip()

    selected_case = None

    for case in cases:

        if case["id"] == case_id:
            selected_case = case
            break

    if not selected_case:
        print("\nCase not found.")
        return

    suspect_count = sum(
        1 for suspect in suspects
        if suspect["case_id"] == case_id
    )

    evidence_count = sum(
        1 for item in evidence
        if item["case_id"] == case_id
    )

    clue_count = sum(
        1 for clue in clues
        if clue["case_id"] == case_id
    )

    witness_count = sum(
        1 for witness in witnesses
        if witness["case_id"] == case_id
    )

    note_count = sum(
        1 for note in notes
        if note["case_id"] == case_id
    )

    double_green_line(60)
    print("              INVESTIGATION SUMMARY")
    double_green_line(60)

    print(f"Case ID   : {selected_case['id']}")
    print(f"Title     : {selected_case['title']}")
    print(f"Status    : {selected_case['status']}")
    print(f"Priority  : {selected_case['priority']}")

    print("\nInvestigation Records")
    green_line(60)

    print(f"Suspects   : {suspect_count}")
    print(f"Evidence   : {evidence_count}")
    print(f"Clues      : {clue_count}")
    print(f"Witnesses  : {witness_count}")
    print(f"Notes      : {note_count}")

    print("\nOverall Assessment")
    green_line(60)

    total_records = (
        suspect_count
        + evidence_count
        + clue_count
        + witness_count
        + note_count
    )

    if total_records == 0:

        print(
            "Insufficient investigation data."
        )

    elif total_records < 3:

        print(
            "Limited investigation data available."
        )

    elif total_records < 6:

        print(
            "Moderate amount of investigation data available."
        )

    else:

        print(
            "Substantial investigation data available."
        )

    green_line(60)

def generate_report():

    while True:

        double_green_line(60)
        print("              GENERATE REPORT")
        double_green_line(60)

        print("1. Generate Case Report")
        print("2. View Generated Report")
        print("3. Back to Main Menu")

        double_green_line(60)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_case_report()

        elif choice == "2":
            view_generated_reports()

        elif choice == "3":
            print("\nReturning to Main Menu...")
            break

        else:
            print("\nInvalid choice. Please select 1, 2, or 3.")


def create_case_report():

    print("\n--- GENERATE CASE REPORT ---")

    case_id = input("Enter Case ID: ").strip()

    selected_case = None

    for case in cases:
        if case["id"] == case_id:
            selected_case = case
            break

    if not selected_case:
        print("\nCase not found.")
        return

    case_suspects = [
        suspect for suspect in suspects
        if suspect["case_id"] == case_id
    ]

    case_evidence = [
        item for item in evidence
        if item["case_id"] == case_id
    ]

    case_clues = [
        clue for clue in clues
        if clue["case_id"] == case_id
    ]

    case_witnesses = [
        witness for witness in witnesses
        if witness["case_id"] == case_id
    ]

    case_notes = [
        note for note in notes
        if note["case_id"] == case_id
    ]

    report = []

    # ==================================================
    # REPORT HEADER
    # ==================================================

    report.append("=" * 60)
    report.append("                 DIGITAL DETECTIVE")
    report.append("              INVESTIGATION REPORT")
    report.append("=" * 60)
    report.append("")

    # ==================================================
    # CASE INFORMATION
    # ==================================================

    report.append("CASE INFORMATION")
    report.append("-" * 60)

    report.append(
        f"Case ID       : {selected_case['id']}"
    )

    report.append(
        f"Title         : {selected_case['title']}"
    )

    report.append(
        f"Description   : {selected_case['description']}"
    )

    report.append(
        f"Case Type     : {selected_case['type']}"
    )

    report.append(
        f"Location      : {selected_case['location']}"
    )

    report.append(
        f"Status        : {selected_case['status']}"
    )

    report.append(
        f"Priority      : {selected_case['priority']}"
    )

    report.append(
        f"Created At    : {selected_case['created_at']}"
    )

    report.append("")

    # ==================================================
    # SUSPECTS
    # ==================================================

    report.append("SUSPECTS")
    report.append("-" * 60)

    if case_suspects:

        for suspect in case_suspects:

            report.append(
                f"Suspect ID   : {suspect['id']}"
            )

            report.append(
                f"Name         : {suspect['name']}"
            )

            report.append(
                f"Age          : {suspect['age']}"
            )

            report.append(
                f"Gender       : {suspect['gender']}"
            )

            report.append(
                f"Occupation   : {suspect['occupation']}"
            )

            report.append(
                f"Risk Level   : {suspect['risk_level']}"
            )

            report.append(
                f"Relationship : {suspect['relationship']}"
            )

            report.append(
                f"Alibi        : {suspect['alibi']}"
            )

            report.append("")

    else:

        report.append("No suspects recorded.")
        report.append("")

    # ==================================================
    # EVIDENCE
    # ==================================================

    report.append("EVIDENCE")
    report.append("-" * 60)

    if case_evidence:

        for item in case_evidence:

            report.append(
                f"Evidence ID : {item['id']}"
            )

            report.append(
                f"Description : {item['description']}"
            )

            report.append(
                f"Type        : {item['type']}"
            )

            if "collector" in item:
                report.append(
                    f"Collector   : {item['collector']}"
                )

            if "location" in item:
                report.append(
                    f"Location    : {item['location']}"
                )

            report.append("")

    else:

        report.append("No evidence recorded.")
        report.append("")

    # ==================================================
    # CLUES
    # ==================================================

    report.append("CLUES")
    report.append("-" * 60)

    if case_clues:

        for clue in case_clues:

            report.append(
                f"Clue ID     : {clue['id']}"
            )

            report.append(
                f"Title       : {clue['title']}"
            )

            report.append(
                f"Description : {clue['description']}"
            )

            report.append(
                f"Source      : {clue['source']}"
            )

            report.append(
                f"Importance  : {clue['importance']}"
            )

            report.append(
                f"Status      : {clue['status']}"
            )

            report.append(
                f"Notes       : {clue['notes']}"
            )

            report.append("")

    else:

        report.append("No clues recorded.")
        report.append("")

    # ==================================================
    # WITNESSES
    # ==================================================

    report.append("WITNESSES")
    report.append("-" * 60)

    if case_witnesses:

        for witness in case_witnesses:

            report.append(
                f"Witness ID  : {witness['id']}"
            )

            report.append(
                f"Name        : {witness['name']}"
            )

            report.append(
                f"Age         : {witness['age']}"
            )

            report.append(
                f"Gender      : {witness['gender']}"
            )

            report.append(
                f"Contact     : {witness['contact']}"
            )

            report.append(
                f"Statement   : {witness['statement']}"
            )

            report.append(
                f"Credibility : {witness['credibility']}"
            )

            report.append("")

    else:

        report.append("No witnesses recorded.")
        report.append("")

    # ==================================================
    # INVESTIGATION NOTES
    # ==================================================

    report.append("INVESTIGATION NOTES")
    report.append("-" * 60)

    if case_notes:

        for note in case_notes:

            report.append(
                f"Note ID    : {note['id']}"
            )

            report.append(
                f"Title      : {note['title']}"
            )

            report.append(
                f"Priority   : {note['priority']}"
            )

            report.append(
                f"Content    : {note['content']}"
            )

            report.append("")

    else:

        report.append(
            "No investigation notes recorded."
        )

        report.append("")

    # ==================================================
    # CASE STATISTICS
    # ==================================================

    report.append("CASE STATISTICS")
    report.append("-" * 60)

    report.append(
        f"Total Suspects  : {len(case_suspects)}"
    )

    report.append(
        f"Total Evidence  : {len(case_evidence)}"
    )

    report.append(
        f"Total Clues     : {len(case_clues)}"
    )

    report.append(
        f"Total Witnesses : {len(case_witnesses)}"
    )

    report.append(
        f"Total Notes     : {len(case_notes)}"
    )

    report.append("")

    # ==================================================
    # REPORT FOOTER
    # ==================================================

    report.append("=" * 60)
    report.append("              END OF INVESTIGATION REPORT")
    report.append("=" * 60)

    # Convert list into proper multi-line text
    report_text = "\n".join(report)

    filename = f"case_{case_id}_report.txt"

    try:

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(report_text)

        print("\nReport generated successfully!")
        print(f"Report File: {filename}")

    except Exception as error:

        print(
            f"\nError generating report: {error}"
        )

def view_generated_reports():

    print("\n--- VIEW GENERATED REPORT ---")

    case_id = input("Enter Case ID: ").strip()

    filename = f"case_{case_id}_report.txt"

    try:

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            report_lines = file.readlines()

        print()

        for line in report_lines:

            line = line.rstrip("\n")

            # Separator line
            if line.strip() and (
                set(line.strip()) == {"="} or
                set(line.strip()) == {"-"}
            ):
                print("\033[92m" + line + "\033[0m")
            else:
                print(line)

    except FileNotFoundError:

        print("\nReport not found.")
        print("Please generate the report first.")

    except Exception as error:

        print(f"\nError reading report: {error}")

def evidence_files_management():

    while True:

        double_green_line(50)
        print("             EVIDENCE FILES")
        double_green_line(50)

        print("1. Add Evidence File")
        print("2. View All Evidence Files")
        print("3. View Evidence File Details")
        print("4. Delete Evidence File")
        print("5. Search Evidence Files")
        print("6. Back to Main Menu")

        double_green_line(50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_evidence_file()

        elif choice == "2":
            view_all_evidence_files()

        elif choice == "3":
            view_evidence_file_details()

        elif choice == "4":
            delete_evidence_file()

        elif choice == "5":
            search_evidence_files()

        elif choice == "6":
            break

        else:
            print("\nInvalid choice.")

def add_evidence_file():

    print("\n--- ADD EVIDENCE FILE ---")

    file_id = input(
        "Enter Evidence File ID: "
    ).strip()

    if not file_id:
        print("\nEvidence File ID cannot be empty.")
        return

    for item in evidence_files:

        if item["id"] == file_id:
            print("\nError: This Evidence File ID already exists.")
            return

    case_id = input(
        "Enter Case ID: "
    ).strip()

    if not case_id:
        print("\nCase ID cannot be empty.")
        return

    case_exists = False

    for case in cases:

        if case["id"] == case_id:
            case_exists = True
            break

    if not case_exists:
        print("\nError: The specified Case ID does not exist.")
        return

    source_path = input(
        "Enter Evidence File Path: "
    ).strip()

    if not source_path:
        print("\nFile path cannot be empty.")
        return

    if not os.path.isfile(source_path):

        print("\nError: File does not exist.")
        return

    description = input(
        "Enter Description: "
    ).strip()

    file_type = input(
        "Enter File Type: "
    ).strip()

    try:

        evidence_folder = "evidence_files"

        os.makedirs(
            evidence_folder,
            exist_ok=True
        )

        original_name = os.path.basename(
            source_path
        )

        destination = os.path.join(
            evidence_folder,
            f"{file_id}_{original_name}"
        )

        shutil.copy2(
            source_path,
            destination
        )

        file_record = {
            "id": file_id,
            "case_id": case_id,
            "file_name": original_name,
            "stored_path": destination,
            "file_type": file_type,
            "description": description,
            "created_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        evidence_files.append(
            file_record
        )

        save_evidence_files(
            evidence_files
        )

        print("\nEvidence file added successfully!")

        print(
            f"Evidence File ID: {file_id}"
        )

        print(
            f"Stored At: {destination}"
        )

    except Exception as error:

        print(
            f"\nError: {error}"
        )

def view_all_evidence_files():

    print("\n--- ALL EVIDENCE FILES ---")

    if not evidence_files:

        print("No evidence files found.")
        return

    for item in evidence_files:

        green_line(60)

        print(
            f"ID          : {item['id']}"
        )

        print(
            f"Case ID     : {item['case_id']}"
        )

        print(
            f"File Name   : {item['file_name']}"
        )

        print(
            f"File Type   : {item['file_type']}"
        )

        print(
            f"Description : {item['description']}"
        )

        print(
            f"Created At  : {item['created_at']}"
        )

    green_line(60)

def view_evidence_file_details():

    print("\n--- EVIDENCE FILE DETAILS ---")

    file_id = input(
        "Enter Evidence File ID: "
    ).strip()

    for item in evidence_files:

        if item["id"] == file_id:

            green_line(60)
            print("EVIDENCE FILE INFORMATION")
            green_line(60)

            print(
                f"Evidence File ID : {item['id']}"
            )

            print(
                f"Case ID          : {item['case_id']}"
            )

            print(
                f"File Name        : {item['file_name']}"
            )

            print(
                f"File Type        : {item['file_type']}"
            )

            print(
                f"Description      : {item['description']}"
            )

            print(
                f"Stored Path      : {item['stored_path']}"
            )

            print(
                f"Created At       : {item['created_at']}"
            )

            return

    print("\nEvidence file not found.")

def delete_evidence_file():

    print("\n--- DELETE EVIDENCE FILE ---")

    file_id = input(
        "Enter Evidence File ID: "
    ).strip()

    for item in evidence_files:

        if item["id"] == file_id:

            print(
                f"\nFile Name: {item['file_name']}"
            )

            confirmation = input(
                "Are you sure? (yes/no): "
            ).strip().lower()

            if confirmation != "yes":

                print("Deletion cancelled.")
                return

            try:

                stored_path = item["stored_path"]

                if os.path.exists(stored_path):

                    os.remove(
                        stored_path
                    )

                evidence_files.remove(
                    item
                )

                save_evidence_files(
                    evidence_files
                )

                print(
                    "\nEvidence file deleted successfully!"
                )

            except Exception as error:

                print(
                    f"\nError deleting file: {error}"
                )

            return

    print("\nEvidence file not found.")

def search_evidence_files():

    double_green_line(50)
    print("          SEARCH EVIDENCE FILES")
    double_green_line(50)

    case_id = input(
        "Enter Case ID: "
    ).strip()

    if not case_id:
        print("\nCase ID cannot be empty.")
        return

    case_files = [
        item for item in evidence_files
        if item["case_id"] == case_id
    ]

    if not case_files:

        print(
            "\nNo evidence files found for this case."
        )

        return

    print("\nSearch By:")

    print("1. File Name")
    print("2. File Type")
    print("3. Description")
    print("4. Evidence File ID")
    print("5. Show All Files")
    print("6. Back")

    double_green_line(50)

    choice = input(
        "Enter your choice: "
    ).strip()

    if choice == "6":
        return

    if choice == "5":

        results = case_files

    elif choice in ["1", "2", "3", "4"]:

        keyword = input(
            "Enter search value: "
        ).strip().lower()

        if not keyword:

            print(
                "\nSearch value cannot be empty."
            )

            return

        results = []

        for item in case_files:

            if choice == "1":
                value = item["file_name"]

            elif choice == "2":
                value = item["file_type"]

            elif choice == "3":
                value = item["description"]

            else:
                value = item["id"]

            if keyword in str(value).lower():

                results.append(
                    item
                )

    else:

        print("\nInvalid choice.")
        return

    if not results:

        print("\nNo matching evidence files found.")
        return

    print("\n--- SEARCH RESULTS ---")

    for item in results:

        green_line(60)

        print(
            f"Evidence File ID : {item['id']}"
        )

        print(
            f"Case ID          : {item['case_id']}"
        )

        print(
            f"File Name        : {item['file_name']}"
        )

        print(
            f"File Type        : {item['file_type']}"
        )

        print(
            f"Description      : {item['description']}"
        )

    green_line(60)

def settings_management():

    while True:

        double_green_line(50)
        print("                 SETTINGS")
        double_green_line(50)

        print("1. View System Information")
        print("2. View Storage Information")
        print("3. Change Application Name")
        print("4. Reset All Data")
        print("5. Back to Main Menu")

        double_green_line(50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_system_information()

        elif choice == "2":
            view_storage_information()

        elif choice == "3":
            change_application_name()

        elif choice == "4":
            reset_all_data()

        elif choice == "5":
            break

        else:
            print("\nInvalid choice.")


def change_application_name():

    global APP_NAME

    print("\n--- CHANGE APPLICATION NAME ---")

    print(
        f"Current Name: {APP_NAME}"
    )

    new_name = input(
        "Enter New Application Name: "
    ).strip()

    if not new_name:

        print(
            "\nApplication name cannot be empty."
        )

        return

    APP_NAME = new_name

    print(
        "\nApplication name updated successfully!"
    )

    print(
        f"New Name: {APP_NAME}"
    )

def view_system_information():

    double_green_line(50)
    print("             SYSTEM INFORMATION")
    double_green_line(50)

    print(
        f"Application Name : {APP_NAME}"
    )

    print(
        "Application Type  : Digital Investigation System"
    )

    print(
        "Storage Type      : JSON"
    )

    print(
        "Evidence Storage  : Local File System"
    )

    print(
        "Status            : Running"
    )

    double_green_line(50)

def view_storage_information():

    double_green_line(50)
    print("             STORAGE INFORMATION")
    double_green_line(50)

    print(
        f"Cases             : {len(cases)}"
    )

    print(
        f"Suspects          : {len(suspects)}"
    )

    print(
        f"Evidence          : {len(evidence)}"
    )

    print(
        f"Clues             : {len(clues)}"
    )

    print(
        f"Witnesses         : {len(witnesses)}"
    )

    print(
        f"Investigation Notes : {len(notes)}"
    )

    print(
        f"Evidence Files    : {len(evidence_files)}"
    )

    double_green_line(50)

def reset_all_data():

    double_green_line(50)
    print("              RESET ALL DATA")
    double_green_line(50)

    print(
        "WARNING: This will delete all stored"
    )

    print(
        "cases, suspects, evidence, clues,"
    )

    print(
        "witnesses and investigation notes."
    )

    double_green_line(50)

    confirmation = input(
        "Type RESET to continue: "
    ).strip()

    if confirmation != "RESET":

        print(
            "\nReset cancelled."
        )

        return

    try:

        cases.clear()
        suspects.clear()
        evidence.clear()
        clues.clear()
        witnesses.clear()
        notes.clear()
        evidence_files.clear()

        save_cases(cases)
        save_suspects(suspects)
        save_evidence(evidence)
        save_clues(clues)
        save_witnesses(witnesses)
        save_notes(notes)
        save_evidence_files(evidence_files)

        print(
            "\nAll application data has been reset successfully!"
        )

    except Exception as error:

        print(
            f"\nError while resetting data: {error}"
        )



def show_main_menu():

    while True:

        double_green_line(50)
        print("              DIGITAL DETECTIVE")
        double_green_line(50)

        print("1. Case Management")
        print("2. Suspect Management")
        print("3. Evidence Management")
        print("4. Clue Management")
        print("5. Witness Management")
        print("6. Investigation Notes")
        print("7. Search")
        print("8. Case Analysis")
        print("9. Generate Report")
        print("10. Evidence Files")
        print("11. Settings")
        print("12. Exit")

        double_green_line(50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            case_management()

        elif choice == "2":
            suspect_management()

        elif choice == "3":
            evidence_management()

        elif choice == "4":
            clue_management()

        elif choice == "5":
            witness_management()

        elif choice == "6":
           investigation_notes()

        elif choice == "7":
            global_search()
            
        elif choice == "8":
           case_analysis()

        elif choice == "9":
            generate_report()

        elif choice == "10":
            evidence_files_management()

        elif choice == "11":
            settings_management()

        elif choice == "12":
            print("\nThank you for using Digital Detective!")
            break

        else:
            print("\nInvalid choice. Please select 1-12.")


if __name__ == "__main__":
    show_main_menu()