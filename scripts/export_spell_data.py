import json
import os
import sys

# Ensure we can import lorgs
sys.path.append(os.getcwd())

# Import lorgs data (which loads all classes, specs, spells)
from lorgs import data

def main():
    spells_dict = {}

    print("Exporting spell data...")

    # Iterate over all specs to find all registered spells
    # We use a set of spell IDs to avoid processing the same spell multiple times
    # (though keying by name implicitly handles duplicates)

    count = 0
    for spec in sorted(data.classes.ALL_SPECS):
        for spell in spec.spells:
            # Convert to dict
            d = spell.as_dict()

            name = d["name"]

            # Construct the entry for spell_data.json
            # It maps Name -> { name, id, cooldown, icon, duration }
            entry = {
                "name": name,
                "id": d["spell_id"],
                "cooldown": d["cooldown"],
                "icon": d["icon"],
                "duration": d.get("duration", 0),
                "show": d.get("show", True),
            }

            spells_dict[name] = entry
            count += 1

    # Write to file
    output_file = "spell_data.json"
    with open(output_file, "w") as f:
        json.dump(spells_dict, f, indent=2)

    print(f"Exported {len(spells_dict)} unique spells to {output_file}.")

if __name__ == "__main__":
    main()
