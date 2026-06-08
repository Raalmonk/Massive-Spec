import sys
import os
import json

# --- 🟢 必须最先执行：设置 AWS 假环境变量 ---
# 只有先设置了这些，后面导入 lorgs 时 boto3 才不会报错
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ.setdefault("AWS_ACCESS_KEY_ID", "testing")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "testing")

# --- 路径修复 (保留你之前的修改) ---
current_path = os.path.abspath(__file__)
scripts_dir = os.path.dirname(current_path)
project_root = os.path.dirname(scripts_dir)

if project_root not in sys.path:
    sys.path.append(project_root)

# --- 🔴 只有上面都设置好了，才能导入 lorgs ---
from lorgs import data
# ... (后面的代码保持不变)
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
            if name in spells_dict:
                entry = spells_dict[name]
            else:
                entry = {
                    "name": name,
                    "id": d["spell_id"],
                    "cooldown": d["cooldown"],
                    "icon": d["icon"],
                    "duration": d.get("duration", 0),
                    "show": d.get("show", True),
                    "color": d.get("color", ""),
                    "desc": d.get("desc", ""),
                    "tags": d.get("tags", []),
                    "specs": []
                }
                spells_dict[name] = entry

            if spec.full_name_slug not in entry["specs"]:
                entry["specs"].append(spec.full_name_slug)
            count += 1

    # Write to file
    output_file = "spell_data.json"
    with open(output_file, "w") as f:
        json.dump(spells_dict, f, indent=2)

    print(f"Exported {len(spells_dict)} unique spells to {output_file}.")

if __name__ == "__main__":
    main()
