import asyncio
import datetime
import json
import logging
import os
import sys

from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# --- 1. 环境配置 (保持一致) ---
os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
os.environ.setdefault("AWS_ACCESS_KEY_ID", "testing")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "testing")

# WCL 密钥检查
if not os.getenv("WCL_CLIENT_ID") or not os.getenv("WCL_CLIENT_SECRET"):
    print("Error: WCL_CLIENT_ID and WCL_CLIENT_SECRET must be set in environment variables or .env file.")
    sys.exit(1)

# 确保能找到 lorgs 包
sys.path.append(os.getcwd())

# --- 导入业务模块 ---
from lorgs.logger import logger
from lorgs.clients.wcl.client import WarcraftlogsClient

# 日志设置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 导入核心数据
try:
    from lorgs.data.classes import ALL_SPECS
    from lorgs.models.warcraftlogs_ranking import SpecRanking
except ImportError as e:
    logger.error(f"Failed to import lorgs modules: {e}")
    sys.exit(1)


# --- 配置目标 ---

# 目标职业 Slug 列表
# FF14 Tanks: Paladin, Warrior, Dark Knight, Gunbreaker
# DPS: Samurai, Black Mage
TARGET_SPEC_SLUGS = [
    "paladin-paladin",
    "warrior-warrior",
    "darkknight-darkknight",
    "gunbreaker-gunbreaker",
    "samurai-samurai",
    "blackmage-blackmage"
]

# 目标 Boss Slug 列表 (5个本)
TARGET_BOSS_SLUGS = [
    "vamp-fatale",           # M1S
    "red-hot-and-deep-blue", # M2S
    "the-tyrant",            # M3S
    "lindwurm",              # M4S P1
    "lindwurm-ii"            # M4S P2
]


# --- 核心逻辑 ---

async def update_single_entry(spec, boss_slug):
    """更新单个条目，返回 (Success: bool, Message: str)"""
    spec_slug = spec.full_name_slug
    try:
        # 1. 获取/创建 Ranking 对象
        ranking = SpecRanking.get_or_create(
            boss_slug=boss_slug,
            spec_slug=spec_slug,
            difficulty="mythic",
            metric=spec.role.metric,
        )
        
        # 2. 从 WCL 加载数据 (clear_old=True 确保数据新鲜)
        # limit=80 与 manual_updater.py 保持一致
        await ranking.load(limit=80, clear_old=True)
        
        # 3. 保存回数据库 (清除潜在的脏数据)
        ranking.save()

        # 4. 生成前端 JSON 文件
        data = ranking.model_dump(exclude_unset=True, by_alias=True)
        filename = f"front_end/data/spec_ranking_{spec_slug}_{boss_slug}.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, default=str)
            
        return True, f"Updated: {filename}"

    except Exception as e:
        return False, str(e)


async def main():
    WarcraftlogsClient._instance = None # 初始化 Session

    # 1. 筛选目标 Spec 对象
    target_specs = [s for s in ALL_SPECS if s.full_name_slug in TARGET_SPEC_SLUGS]
    
    # 按照 Tanks 先, 然后 Samurai, Blackmage 的顺序排序 (可选，方便查看日志)
    # 这里简单按字母顺序排序，或者保持我们在列表中定义的顺序
    target_specs.sort(key=lambda s: TARGET_SPEC_SLUGS.index(s.full_name_slug) if s.full_name_slug in TARGET_SPEC_SLUGS else 999)

    if not target_specs:
        logger.error("未找到任何匹配的目标职业，请检查 TARGET_SPEC_SLUGS 配置。")
        return

    logger.info(f"准备更新以下职业: {[s.full_name_slug for s in target_specs]}")
    logger.info(f"准备更新以下 Boss: {TARGET_BOSS_SLUGS}")

    results = [] # 存储结果 [ (Boss, Spec, Success, Message) ]

    try:
        total_tasks = len(target_specs) * len(TARGET_BOSS_SLUGS)
        current_task = 0

        # 2. 循环执行更新
        for boss_slug in TARGET_BOSS_SLUGS:
            logger.info(f"=== 开始处理 Boss: {boss_slug} ===")
            
            for spec in target_specs:
                current_task += 1
                logger.info(f"[{current_task}/{total_tasks}]正在更新: {spec.full_name_slug} @ {boss_slug} ...")
                
                success, msg = await update_single_entry(spec, boss_slug)
                
                results.append({
                    "boss": boss_slug,
                    "spec": spec.full_name_slug,
                    "success": success,
                    "msg": msg
                })

                if not success:
                    logger.error(f"  -> 失败: {msg}")
                
                # 稍微休眠避免速率限制
                await asyncio.sleep(1)

    finally:
        # 清理资源
        logger.info("关闭 HTTP Session...")
        if WarcraftlogsClient._instance and WarcraftlogsClient._instance.session:
            await WarcraftlogsClient._instance.session.close()
            await asyncio.sleep(0.25)

    # --- 3. 打印最终报告 ---
    print("\n" + "="*50)
    print("           更 新 报 告 (Update Report)")
    print("="*50)
    
    success_count = sum(1 for r in results if r['success'])
    fail_count = sum(1 for r in results if not r['success'])
    
    print(f"总计任务: {len(results)} | 成功: {success_count} | 失败: {fail_count}\n")

    if fail_count > 0:
        print("--- [!] 失败列表 ---")
        for res in results:
            if not res['success']:
                print(f"[X] {res['spec']} @ {res['boss']}")
                print(f"    Reason: {res['msg']}")
        print("-" * 20)
    
    print("\n--- [OK] 成功列表摘要 ---")
    # 按 Boss 分组打印成功的信息
    for boss in TARGET_BOSS_SLUGS:
        specs_done = [r['spec'] for r in results if r['success'] and r['boss'] == boss]
        if specs_done:
            print(f"{boss}: {len(specs_done)}/{len(target_specs)} 个职业更新完成")
            # print(f"  -> {', '.join(specs_done)}") # 如果想看详细列表可以取消注释

    print("="*50 + "\n")

if __name__ == "__main__":
    asyncio.run(main())