import csv
import os

# Map Job Codes (from CSV) to Metadata
# ID: Arbitrary distinct ID for now (avoiding 1-13 WoW classes if possible, but existing scholar uses 28)
JOBS = {
    "PLD": {"id": 19, "name": "Paladin", "role": "TANK", "color": "#A8D2E6", "filename": "paladin.py"},
    "WAR": {"id": 21, "name": "Warrior", "role": "TANK", "color": "#CF2621", "filename": "warrior.py"},
    "DRK": {"id": 32, "name": "Dark Knight", "role": "TANK", "color": "#D126CC", "filename": "darkknight.py"},
    "GNB": {"id": 37, "name": "Gunbreaker", "role": "TANK", "color": "#796D30", "filename": "gunbreaker.py"},

    "WHM": {"id": 24, "name": "White Mage", "role": "HEAL", "color": "#FFF0F5", "filename": "whitemage.py"},
    "AST": {"id": 33, "name": "Astrologian", "role": "HEAL", "color": "#FFE74A", "filename": "astrologian.py"},
    "SCH": {"id": 28, "name": "Scholar", "role": "HEAL", "color": "#8657FF", "filename": "scholar.py"},
    "SGE": {"id": 40, "name": "Sage", "role": "HEAL", "color": "#80A0F0", "filename": "sage.py"},

    "DRG": {"id": 22, "name": "Dragoon", "role": "MDPS", "color": "#4164CD", "filename": "dragoon.py"},
    "RPR": {"id": 39, "name": "Reaper", "role": "MDPS", "color": "#965A90", "filename": "reaper.py"},
    "MNK": {"id": 20, "name": "Monk", "role": "MDPS", "color": "#D69C00", "filename": "monk.py"},
    "SAM": {"id": 34, "name": "Samurai", "role": "MDPS", "color": "#E46D04", "filename": "samurai.py"},
    "NIN": {"id": 30, "name": "Ninja", "role": "MDPS", "color": "#AF1964", "filename": "ninja.py"},
    "VPR": {"id": 41, "name": "Viper", "role": "MDPS", "color": "#108010", "filename": "viper.py"}, # Placeholder color

    "BRD": {"id": 23, "name": "Bard", "role": "RDPS", "color": "#91BA5E", "filename": "bard.py"},
    "MCH": {"id": 31, "name": "Machinist", "role": "RDPS", "color": "#6EE1D6", "filename": "machinist.py"},
    "DNC": {"id": 38, "name": "Dancer", "role": "RDPS", "color": "#E2B0AF", "filename": "dancer.py"},

    "SMN": {"id": 27, "name": "Summoner", "role": "RDPS", "color": "#2D9B78", "filename": "summoner.py"},
    "RDM": {"id": 35, "name": "Red Mage", "role": "RDPS", "color": "#E87B7B", "filename": "redmage.py"},
    "BLM": {"id": 25, "name": "Black Mage", "role": "RDPS", "color": "#A579D6", "filename": "blackmage.py"},
    "PCT": {"id": 42, "name": "Pictomancer", "role": "RDPS", "color": "#E060E0", "filename": "pictomancer.py"}, # Placeholder color
}

TYPO_FIXES = {
    "Repirsal": "Reprisal",
    "Phlegam III": "Phlegma III",
    "Subtractice Palette": "Subtractive Palette",
    "Painlfare": "Painflare",
    "Enshround": "Enshroud",
    "Recitaion": "Recitation",
}

def clean_spell_name(name):
    name = name.strip()
    if not name:
        return None
    return TYPO_FIXES.get(name, name)

def parse_csv(filepath):
    # CSV Structure based on analysis:
    # 0: Job Name (Code)
    # 1-11: Burst (11 cols)
    # 12-20: Self Mit (9 cols)
    # 21-32: Raid Mit (12 cols)

    jobs_spells = {}

    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

        # Skip header
        # Row 0 is header: ,Burst,,,,,,,,,,,Self Mit,,,,,,,,Raid Mit,,,,,,,,,,,

        for row in rows[1:]:
            if not row or not row[0]:
                continue

            job_code = row[0].strip()
            if job_code not in JOBS:
                print(f"Skipping unknown job code: {job_code}")
                continue

            burst_spells = [clean_spell_name(x) for x in row[1:12]]
            self_mit_spells = [clean_spell_name(x) for x in row[12:21]]
            raid_mit_spells = [clean_spell_name(x) for x in row[21:33]]

            jobs_spells[job_code] = {
                "burst": [x for x in burst_spells if x],
                "self_mit": [x for x in self_mit_spells if x],
                "raid_mit": [x for x in raid_mit_spells if x]
            }

    return jobs_spells

def generate_job_file(job_code, spells):
    job_data = JOBS[job_code]
    class_var = job_data["name"].upper().replace(" ", "_")
    spec_var = f"{class_var}_MAIN"

    content = f"""\"\"\"Define the {job_data['name']} Class and its Spec and Spells.\"\"\"

# pylint: disable=line-too-long
# pylint: disable=bad-whitespace
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
# fmt: off

# IMPORT LOCAL LIBRARIES
from lorgs.data.constants import *
from lorgs.data.roles import *
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import SpellTag


################################################################################
# Class
#
{class_var} = WowClass(id={job_data['id']}, name="{job_data['name']}", color="{job_data['color']}")

################################################################################
# Specs
#
{spec_var} = WowSpec(role={job_data['role']}, wow_class={class_var}, name="{job_data['name']}")


################################################################################
# Spells
#
"""

    def add_spells(spell_list, tags=None):
        out = ""
        for spell_name in spell_list:
            tag_str = ""
            if tags:
                tag_list = [f"SpellTag.{t}" for t in tags]
                tag_str = f", tags=[{', '.join(tag_list)}]"

            # Using placeholder ID and Icon
            # We use show=False by default for some? No, default is True.
            # But the csv implies they are important.
            out += f'{spec_var}.add_spell(spell_id=0, cooldown=0, name="{spell_name}", icon="placeholder.jpg"{tag_str})\n'
        return out

    # Burst -> DAMAGE
    if spells["burst"]:
        content += "\n# Burst / Cooldowns\n"
        content += add_spells(spells["burst"], tags=["DAMAGE"])

    # Self Mit -> DEFENSIVE
    if spells["self_mit"]:
        content += "\n# Self Mitigation\n"
        content += add_spells(spells["self_mit"], tags=["DEFENSIVE"])

    # Raid Mit -> RAID_CD
    if spells["raid_mit"]:
        content += "\n# Party Mitigation\n"
        content += add_spells(spells["raid_mit"], tags=["RAID_CD"])

    return content

def main():
    parsed_spells = parse_csv("fflorrgs.csv")

    for job_code, spells in parsed_spells.items():
        job_data = JOBS[job_code]
        content = generate_job_file(job_code, spells)

        filepath = os.path.join("lorgs", "data", "classes", job_data["filename"])
        print(f"Generating {filepath}...")
        with open(filepath, "w") as f:
            f.write(content)

    print("Done.")

if __name__ == "__main__":
    main()
