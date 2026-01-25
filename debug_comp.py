# check_bosses.py
import os
import sys

# 1. 确保能导入 lorgs
sys.path.append(os.getcwd())

# 2. 导入数据模块 (这会触发 Boss 的注册)
import lorgs.data 
from lorgs.models.raid_zone import RaidZone

# 3. 打印所有已注册的 Boss
print("--- Loaded Bosses ---")
found = False
for zone in RaidZone.all_zones:
    print(f"\nZone: {zone.name} (ID: {zone.id})")
    for boss in zone.bosses:
        print(f"  - [{boss.id}] {boss.name} (Nick: {boss.nick}) -> Slug: {boss.full_name_slug}")
        if boss.nick == "M12S P2":
            found = True

print("\n-------------------")
if found:
    print("✅ SUCCESS: M12S P2 is loaded in the backend!")
else:
    print("❌ FAILURE: M12S P2 is NOT loaded. Check your imports.")