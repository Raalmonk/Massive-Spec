import asyncio
import os
import sys
import json
import argparse
import dotenv

# 加载环境变量
dotenv.load_dotenv()
sys.path.append(os.getcwd())

from lorgs.clients import wcl

def clean_spec_name(name):
    return name.replace(" ", "")

async def fetch_healer_rankings_v2(boss_id, spec1, spec2, limit_global=45, limit_cn=25):
    client = wcl.WarcraftlogsClient.get_instance()
    
    s1_clean = clean_spec_name(spec1)
    s2_clean = clean_spec_name(spec2)
    
    # 构造过滤器：寻找同时包含这两个职业的战斗
    filter_exp = f"classes.{s1_clean}.gte.1 AND classes.{s2_clean}.gte.1"
    
    print(f"=== 1. 抓取排名: {spec1} + {spec2} (Boss: {boss_id}) ===")
    print(f"   过滤器: {filter_exp}")

    def build_query(region_arg=""):
        return f"""
            characterRankings(
                metric: healercombineddps,
                filter: "{filter_exp}",
                page: 1,
                {region_arg}
            )
        """

    query = f"""
    worldData {{
        encounter(id: {boss_id}) {{
            global: {build_query()}
            cn: {build_query('serverRegion: "CN"')}
        }}
    }}
    """
    
    print("   正在发送请求...")
    try:
        result = await client.query(query)
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return

    encounter_data = result.get("worldData", {}).get("encounter", {})
    
    # 标记区域
    ranks_global = encounter_data.get("global", {}).get("rankings", [])
    for r in ranks_global: r['_region'] = ""
    
    ranks_cn = encounter_data.get("cn", {}).get("rankings", [])
    for r in ranks_cn: r['_region'] = "CN"
    
    # 合并 & 排序
    merged_ranks = ranks_global[:limit_global] + ranks_cn[:limit_cn]
    merged_ranks.sort(key=lambda x: x.get("amount", 0), reverse=True)
    
    if not merged_ranks:
        print("❌ 未找到任何符合条件的记录。")
        return

    print(f"\n✅ 最终列表 ({len(merged_ranks)}条):")
    for i, rank in enumerate(merged_ranks[:10]):
        r_code = rank.get("report", {}).get("code")
        r_reg = rank.get("_region") or "GL"
        print(f"   [{i+1}] [{r_reg}] DPS: {rank.get('amount'):.2f} | {rank.get('name')} & {rank.get('nameTwo')} | Report: {r_code}")

    # 处理第一名
    top_rank = merged_ranks[0]
    await process_timeline_direct(client, boss_id, top_rank)

async def process_timeline_direct(client, boss_id, rank_data):
    report_code = rank_data.get("report", {}).get("code")
    fight_id = rank_data.get("report", {}).get("fightID")
    region = rank_data.get("_region", "")
    
    print(f"\n=== 2. 生成时间轴数据 ({report_code} / Fight {fight_id}) [Region: {region or 'Global'}] ===")
    
    # 1. 获取玩家列表
    print("   正在获取玩家列表 (MasterData)...")
    master_query = f"""
    reportData {{
        report(code: "{report_code}") {{
            masterData {{
                actors(type: "Player") {{ id, name, subType }}
            }}
        }}
    }}
    """
    
    try:
        master_res = await client.query(master_query, region=region)
        actors = master_res.get("reportData", {}).get("report", {}).get("masterData", {}).get("actors", [])
    except Exception as e:
        print(f"❌ 获取玩家列表失败: {e}")
        return

    name1 = rank_data.get("name")
    name2 = rank_data.get("nameTwo")
    
    p1 = next((a for a in actors if a['name'] == name1), None)
    p2 = next((a for a in actors if a['name'] == name2), None)
    
    if not p1 or not p2:
        print(f"❌ 无法匹配玩家 ID: {name1}, {name2}")
        return

    print(f"   H1: {p1['name']} (ID: {p1['id']}, Spec: {p1['subType']})")
    print(f"   H2: {p2['name']} (ID: {p2['id']}, Spec: {p2['subType']})")
    
    # 2. 抓取施法记录
    # 注意：dataType: Casts 包含 'cast'(瞬发/读条结束) 和 'begincast'(读条开始)
    filter_expr = f"source.id = {p1['id']} or source.id = {p2['id']}"
    events_query = f"""
    reportData {{
        report(code: "{report_code}") {{
            events(
                fightIDs: [{fight_id}],
                dataType: Casts,
                filterExpression: "{filter_expr}",
                limit: 10000
            ) {{ data }}
        }}
    }}
    """
    
    print("   正在下载施法记录 (Events)...")
    try:
        events_res = await client.query(events_query, region=region)
        events = events_res.get("reportData", {}).get("report", {}).get("events", {}).get("data", [])
    except Exception as e:
        print(f"❌ 获取施法记录失败: {e}")
        return
    
    if not events:
        print("❌ 警告：下载到的事件列表为空！可能是 API 限制或过滤条件错误。")
        return

    # --- 调试信息：看看前几个事件是什么 ---
    print(f"   ⬇️  API 返回了 {len(events)} 个事件。前 2 个样本：")
    for e in events[:2]:
        print(f"      Type: {e.get('type')} | Time: {e.get('timestamp')} | Ability: {e.get('abilityGameID')}")

    # 3. 生成 JSON
    timeline = {
        "meta": {
            "boss": boss_id,
            "dps": rank_data.get("amount"),
            "duration": rank_data.get("duration"),
            "report": report_code,
            "fight": fight_id,
            "region": region
        },
        "rows": [
            # 使用 API 返回的真实职业 (subType)，而不是脚本入参
            {"label": p1['name'], "spec": p1['subType'], "casts": []},
            {"label": p2['name'], "spec": p2['subType'], "casts": []}
        ]
    }
    
    start_time = rank_data.get("startTime", 0)
    
    valid_types = ['cast', 'begincast'] # 放宽过滤条件
    
    for cast in events:
        c_type = cast.get('type')
        if c_type not in valid_types: 
            continue
            
        t = (cast.get("timestamp") - start_time) / 1000.0
        sid = cast.get("abilityGameID")
        
        # 构造事件对象
        # 可以在这里根据 type 区分是开始读条还是瞬发，比如加个 extra info
        obj = {"t": t, "id": sid} 
        
        source_id = cast.get("sourceID")
        
        if source_id == p1['id']:
            timeline["rows"][0]["casts"].append(obj)
        elif source_id == p2['id']:
            timeline["rows"][1]["casts"].append(obj)
            
    # 文件名加上职业简称防重名
    filename = f"timeline_{p1['subType']}_{p2['subType']}_{report_code}.json"
    with open(filename, "w") as f:
        json.dump(timeline, f, indent=2)
        
    print(f"\n✅ 完成！文件已保存: {filename}")
    print(f"   Row 1 ({p1['name']}): {len(timeline['rows'][0]['casts'])} events")
    print(f"   Row 2 ({p2['name']}): {len(timeline['rows'][1]['casts'])} events")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--boss", type=int, default=101, help="Boss ID")
    parser.add_argument("--spec1", type=str, default="WhiteMage")
    parser.add_argument("--spec2", type=str, default="Scholar")
    args = parser.parse_args()

    asyncio.run(fetch_healer_rankings_v2(args.boss, args.spec1, args.spec2))