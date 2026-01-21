import json

# 1. 加载你的 spell_data.json (你的字典)
try:
    with open("spell_data.json", "r", encoding="utf-8") as f:
        spell_db = json.load(f)
except FileNotFoundError:
    print("❌ 找不到 spell_data.json，请确认文件位置")
    exit()

# 把字典转换成 ID 为 key 的格式，方便查找
id_to_spell = {}
for name, data in spell_db.items():
    id_to_spell[data['id']] = data
    id_to_spell[data['id']]['name'] = name # 把名字也存进去

# 2. 加载 API 返回的战斗数据 (response.json)
# 也就是你刚才上传的那个 response_1768971124092.json
try:
    with open("response_1768971124092.json", "r", encoding="utf-8") as f:
        fight_data = json.load(f)
except FileNotFoundError:
    print("❌ 找不到 response.json，请把 API 返回的结果保存为这个文件")
    exit()

# 3. 开始比对
print("🔍 开始检查 ID 映射...")
casts = fight_data['players'][0]['casts']
unique_spell_ids = set(c['spell_id'] for c in casts)

missing_spells = []
found_spells = []

for spell_id in unique_spell_ids:
    if spell_id in id_to_spell:
        found_spells.append(f"✅ ID {spell_id} -> {id_to_spell[spell_id]['name']}")
    else:
        # 一些常见的忽略项
        if spell_id == 7: # 自动攻击
            continue 
        missing_spells.append(spell_id)

# 4. 输出结果
print(f"\n--- 成功匹配 {len(found_spells)} 个技能 ---")
# print('\n'.join(found_spells)) # 如果想看所有匹配的可以取消注释

print(f"\n--- ⚠️ 警告：发现 {len(missing_spells)} 个未知 ID (需添加到 spell_data.json) ---")
for mid in missing_spells:
    print(f"❌ ID {mid} 缺失！(可能是爆发药、疾跑或职业量谱技能)")

# 特别提示爆发药
if 34603669 in missing_spells:
    print("\n💡 提示: ID 34603669 是 8级爆发药 (Grade 8 Tincture)，记得加上！")