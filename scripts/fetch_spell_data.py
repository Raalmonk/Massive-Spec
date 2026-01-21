import csv
import json
import os
import time
import requests
from bs4 import BeautifulSoup

# File paths
CSV_FILE = "fflorrgs.csv"
DATA_FILE = "spell_data.json"
WIKI_BASE_URL = "https://ffxiv.consolegameswiki.com/wiki/"
ACTION_CSV_FILE = "ffxiv-datamining/csv/en/Action.csv"

# Typo fixes
TYPO_FIXES = {
    "Repirsal": "Reprisal",
    "Phlegam III": "Phlegma III",
    "Subtractice Palette": "Subtractive Palette",
    "Painlfare": "Painflare",
    "Enshround": "Enshroud",
    "Recitaion": "Recitation",
    "Summon Bahamut ": "Summon Bahamut",
    "Summon Solar BahaMut": "Summon Solar Bahamut",
    "Embloden": "Embolden",
    "Geirskougul": "Geirskogul",
    "Shake it Off": "Shake It Off",
}

def clean_spell_name(name):
    if not name:
        return None
    name = name.strip()
    return TYPO_FIXES.get(name, name)

def get_spells_from_csv(filepath):
    spells = set()
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
        for row in rows[1:]:
            if not row or not row[0]:
                continue
            for col in row[1:33]:
                spell = clean_spell_name(col)
                if spell:
                    spells.add(spell)
    return sorted(list(spells))

def load_action_csv(filepath):
    """Loads Action.csv and returns a dict mapping Name -> Data."""
    mapping = {}
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found. IDs will be missing.")
        return mapping

    print(f"Loading {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                name = row.get('Name')
                if not name:
                    continue

                is_pvp = row.get('IsPvP', 'False').lower() == 'true'
                if is_pvp:
                    continue

                action_id = row.get('#')
                if not action_id:
                    continue

                # recast_ms = int(row.get('Recast100ms', 0))
                # We prioritize the wiki for cooldown, so we don't need it from CSV unless fallback.
                # But storing it for fallback is good.

                mapping[name] = {
                    "id": int(action_id),
                    "cooldown": int(row.get('Recast100ms', 0)) / 10.0
                }

            except Exception as e:
                continue

    return mapping

def fetch_spell_data(spell_name, csv_data):
    print(f"Fetching data for: {spell_name}")
    url_name = spell_name.replace(" ", "_")
    url = f"{WIKI_BASE_URL}{url_name}"

    data = {
        "name": spell_name,
        "id": 0,
        "cooldown": 0,
        "icon": ""
    }

    # Pre-fill ID from CSV (Primary source for ID)
    if spell_name in csv_data:
        data["id"] = csv_data[spell_name]["id"]
        # Default cooldown from CSV as fallback
        data["cooldown"] = csv_data[spell_name]["cooldown"]
    else:
        print(f"  [CSV] ID not found for {spell_name}")

    try:
        resp = requests.get(url, headers={"User-Agent": "FFLorrgs-Agent/1.0"})
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')

            # Find Icon (Primary goal of Wiki scrape)
            infobox = soup.find(class_="action-infobox-icon")
            if infobox:
                img = infobox.find("img")
                if img and img.get("alt"):
                    data["icon"] = img.get("alt").replace("File:", "")

            if not data["icon"]:
                img = soup.find("img", alt=f"{spell_name}.png")
                if img:
                     data["icon"] = f"{spell_name}.png"
                else:
                    data["icon"] = f"{url_name}.png"

            # Parse Recast from Wiki (Primary source for Cooldown)
            found_recast = False
            # Check table structure with headings (th) and data (td)
            for tr in soup.find_all("tr"):
                th = tr.find("th")
                td = tr.find("td")
                # sometimes it is dt/dd in a dl
                pass

            # The wiki structure seemed to use dl/dt/dd in the div wrapper in my earlier inspection
            # <div class="wrapper"><dl><dt>Recast</dt><dd>120s</dd> ...

            for dt in soup.find_all("dt"):
                if "Recast" in dt.get_text():
                    dd = dt.find_next_sibling("dd")
                    if dd:
                        val = dd.get_text().lower().replace("s", "").strip()
                        try:
                            # Prefer Wiki Cooldown
                            data["cooldown"] = float(val)
                            found_recast = True
                        except ValueError:
                            pass

            if not found_recast:
                # Try table format (th/td) just in case
                for tr in soup.find_all("tr"):
                    th = tr.find("th")
                    td = tr.find("td")
                    if th and td and "Recast" in th.get_text():
                        val = td.get_text().lower().replace("s", "").strip()
                        try:
                            data["cooldown"] = float(val)
                        except ValueError:
                            pass

        else:
            print(f"  [Wiki] Error fetching {url}: {resp.status_code}")
            if not data["icon"]:
                data["icon"] = f"{url_name}.png"

    except Exception as e:
        print(f"  [Wiki] Exception fetching {spell_name}: {e}")
        if not data["icon"]:
            data["icon"] = f"{url_name}.png"

    return data

def main():
    spells = get_spells_from_csv(CSV_FILE)
    print(f"Found {len(spells)} unique spells.")

    csv_mapping = load_action_csv(ACTION_CSV_FILE)

    data = {}
    # We will OVERWRITE existing data to ensure we get the Wiki cooldowns this time
    # But we can keep ID if we want? No, rebuild is safer.
    # Actually, we should keep data if we already ran it, but I want to update cooldowns.
    # So I will force update.

    changed = False
    for spell in spells:
        # Optimization: If we already have the Wiki Cooldown (how to know?), skip.
        # But I don't know if the previous run used CSV or Wiki.
        # So I will rerun all. It takes < 2 mins.

        spell_data = fetch_spell_data(spell, csv_mapping)
        data[spell] = spell_data
        changed = True

        time.sleep(0.1) # Faster

        if changed:
            with open(DATA_FILE, 'w') as f:
                json.dump(data, f, indent=2)
            changed = False

    print("Done.")

if __name__ == "__main__":
    main()
