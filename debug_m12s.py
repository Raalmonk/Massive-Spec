import os
import asyncio
import json
from datetime import datetime

# =================配置区域=================
# 1. 设置 AWS 区域 (绕过 boto3 报错)
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"

os.environ["WCL_CLIENT_ID"] = "a0e16bba-fba8-432d-a317-4a6a83d98728"
os.environ["WCL_CLIENT_SECRET"] = "Rowpl4stVguifS4YJbzow1HCjh1g2uNuGNaFYRPk"
# 2. 填入你的 WCL/FFLogs 报告信息
# 示例: https://www.fflogs.com/reports/a:123456abcdef#fight=5
REPORT_ID = "vyHg3TtcKp614LkD"   # 替换为你的报告 ID
FIGHT_ID = 33                      # 替换为你要测试的 Fight ID (根据你之前的报错信息改成了 33)
TARGET_SPEC = "redmage-redmage"        # 你要抓取的职业
# ==========================================

from lorgs.models.warcraftlogs_report import Report
from lorgs.models.warcraftlogs_fight import Fight

import lorgs.data

async def test_load_casts():
    print(f"1. 初始化报告: {REPORT_ID}")
    report = Report(report_id=REPORT_ID)
    
    # 关键步骤：加载报告的元数据 (MasterData)
    # 这会从 FFLogs 获取所有战斗的列表和准确的开始时间
    print("2. 正在从 FFLogs 加载报告元数据...")
    await report.load()
    
    # 从报告中获取自动生成的 Fight 对象（包含正确的时间戳）
    fight = report.get_fight(fight_id=FIGHT_ID)
    
    if not fight:
        print(f"❌ 错误: 在报告中找不到 Fight ID {FIGHT_ID}")
        print(f"   可用 Fight IDs: {[f.fight_id for f in report.fights]}")
        return

    print(f"✅ 找到战斗: {fight.boss.name if fight.boss else 'Unknown'} (ID: {fight.fight_id})")
    print(f"   开始时间: {fight.start_time}")

    # 3. 加载玩家列表 (Summary)
    if not fight.players:
        print("3. 正在加载战斗摘要(Summary)以获取玩家列表...")
        await fight.load()

    # 4. 查找目标职业玩家
    target_player = None
    for player in fight.players:
        if player.spec_slug == TARGET_SPEC:
            target_player = player
            break
            
    if not target_player:
        print(f"❌ 未找到职业为 {TARGET_SPEC} 的玩家。")
        print("   可用职业:", [p.spec_slug for p in fight.players])
        return

    print(f"4. 正在加载 {target_player.name} ({target_player.spec_slug}) 的施法数据...")
    
    # 5. 加载详细施法数据
    # 这会触发 process_query_result 并在 player.casts 里填充数据
    await target_player.load()

    # 6. 结果验证
    data = target_player.as_dict()
    casts = data.get('casts', [])
    
    print(f"\n🎉 成功! 共抓取到 {len(casts)} 次施法")
    
    if casts:
        print("\n=== 前 10 个技能的时间轴样本 ===")
        for cast in casts[:10]:
            # 转换时间戳为 mm:ss 格式
            raw_ts = cast.get('ts') or cast.get('timestamp') or 0
            ts_sec = raw_ts / 1000
            time_str = f"{int(ts_sec // 60)}:{int(ts_sec % 60):02d}"
            spell_id = cast.get('id') or cast.get('spell_id')
            print(f"[{time_str}] 技能ID: {cast['spell_id']}")
            
        # 保存为文件供 Web 端测试
        filename = f"debug_data_{target_player.name}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"\n完整数据已保存至: {filename}")

if __name__ == "__main__":
    asyncio.run(test_load_casts())