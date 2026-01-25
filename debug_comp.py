# debug_comp.py
import asyncio
import os
import sys

# 1. 设置伪造 AWS 凭证
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["AWS_SECURITY_TOKEN"] = "testing"
os.environ["AWS_SESSION_TOKEN"] = "testing"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

# 2. 设置路径
sys.path.append(os.getcwd())

# 3. [关键修复] 导入数据模块，这会初始化 RaidBoss 列表
import lorgs.data 

from lorgs.models.warcraftlogs_comp_ranking import CompRanking

async def main():
    boss_slug = "vamp-fatale" 
    print(f"--- Starting Debug for Boss: {boss_slug} ---")
    
    # 获取对象
    ranking = CompRanking.get_or_create(boss_slug=boss_slug)
    
    # 4. 核心步骤：直接调用 load
    print(">>> Calling ranking.load()...")
    # 注意：clear_old=True 会强制重新抓取，这非常重要，否则它可能会直接读缓存而不触发我们的 print
    await ranking.load(limit=5, clear_old=True) 
    print(">>> ranking.load() finished.")
    
    # 5. 打印结果检查
    if ranking.reports:
        print(f"\nSuccessfully loaded {len(ranking.reports)} reports.")
        first_report = ranking.reports[0]
        if first_report.fights:
            first_fight = first_report.fights[0]
            print(f"First Fight ID: {first_fight.fight_id}")
            print(f"First Fight Players Count: {len(first_fight.players)}")
            # 这里是我们最关心的：Composition 到底有没有生成
            print(f"First Fight Composition: {first_fight.composition}")
        else:
            print("First report has no fights.")
    else:
        print("No reports loaded.")

if __name__ == "__main__":
    asyncio.run(main())