import asyncio
import datetime
import json
import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()

# --- 1. 环境配置 (保持与 updater.py 一致) ---
os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
os.environ.setdefault("AWS_ACCESS_KEY_ID", "testing")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "testing")

# WCL 密钥检查
if not os.getenv("WCL_CLIENT_ID") or not os.getenv("WCL_CLIENT_SECRET"):
    print("Error: WCL_CLIENT_ID and WCL_CLIENT_SECRET must be set in environment variables or .env file.")
    sys.exit(1)

# 确保能找到 lorgs 包
sys.path.append(os.getcwd())

import aiohttp 

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


# --- 核心逻辑 (复用并增强 updater.py 的逻辑) ---

async def _do_update_single_spec(spec, boss_slug):
    """更新单个 Spec 和 Boss 的数据，并强制清理数据库缓存"""
    spec_slug = spec.full_name_slug
    logger.info(f"Targeting: {boss_slug} vs {spec_slug}")
    
    # 1. 初始化 Ranking 对象
    ranking = SpecRanking.get_or_create(
        boss_slug=boss_slug,
        spec_slug=spec_slug,
        difficulty="mythic",
        metric=spec.role.metric,
    )
    
    # 2. 强制加载 (clear_old=True 清空内存旧数据)
    logger.info("Fetching fresh data from WCL...")
    await ranking.load(limit=80, clear_old=True)
    
    # 3. [关键修复] 强制保存回数据库
    # 这会覆盖数据库中可能存在的“幽灵数据”
    ranking.save()
    logger.info("Database updated (Ghost data cleared).")

    # 4. 生成前端 JSON 文件
    data = ranking.model_dump(exclude_unset=True, by_alias=True)
    filename = f"front_end/data/spec_ranking_{spec_slug}_{boss_slug}.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, "w") as f:
        json.dump(data, f, ensure_ascii=False, default=str)
        
    logger.info(f"JSON generated: {filename}")

async def interactive_main():
    WarcraftlogsClient._instance = None # 重置 Session

    try:
        print("="*40)
        print("   Massive Spec - Manual Updater Tool")
        print("="*40)

        # 1. 询问 Boss
        # 您可以输入: vamp-fatale, the-tyrant 等
        boss_input = input("\n请输入 Boss Slug (例如: vamp-fatale): ").strip()
        if not boss_input:
            print("错误: 必须输入 Boss Slug。")
            return

        # 2. 询问 Spec
        # 您可以输入: paladin-protection, astrologian-astrologian
        # 或者输入 "ALL" 来更新该 Boss 的所有职业
        print(f"\n提示: 输入 'ALL' 更新该 Boss 下所有职业")
        spec_input = input("请输入 Spec Slug (例如: paladin-protection): ").strip()
        
        target_specs = []

        if spec_input.upper() == "ALL":
            target_specs = sorted(list(ALL_SPECS), key=lambda s: s.full_name_slug)
            print(f"--> 已选择全部 {len(target_specs)} 个职业。")
        else:
            # 查找匹配的 Spec
            found = next((s for s in ALL_SPECS if s.full_name_slug == spec_input), None)
            if not found:
                print(f"错误: 找不到名为 '{spec_input}' 的职业。")
                print("可用职业示例:", [s.full_name_slug for s in ALL_SPECS][:5], "...")
                return
            target_specs = [found]

        # 3. 执行确认
        print(f"\n准备更新: Boss=[{boss_input}], Specs=[{len(target_specs)}个]")
        confirm = input("按 Enter 开始 (或输入 n 退出): ")
        if confirm.lower() == 'n':
            return

        # 4. 循环执行
        for i, spec in enumerate(target_specs):
            print(f"\n[{i+1}/{len(target_specs)}] 处理中: {spec.full_name_slug}...")
            try:
                await _do_update_single_spec(spec, boss_input)
                # 稍微休眠一下避免速率限制，如果是批量更新的话
                if len(target_specs) > 1:
                    await asyncio.sleep(2)
            except Exception as e:
                logger.error(f"更新失败 {spec.full_name_slug}: {e}")

    finally:
        logger.info("Closing HTTP Session...")
        if WarcraftlogsClient._instance and WarcraftlogsClient._instance.session:
            await WarcraftlogsClient._instance.session.close()
            await asyncio.sleep(0.25)
        logger.info("All operations completed.")

if __name__ == "__main__":
    asyncio.run(interactive_main())