import asyncio
import datetime
import json
import logging
import os
import sys
import time

# --- 1. 环境配置 ---
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ.setdefault("AWS_ACCESS_KEY_ID", "testing")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "testing")

# WCL 密钥
os.environ["WCL_CLIENT_ID"] = "a0e16bba-fba8-432d-a317-4a6a83d98728"
os.environ["WCL_CLIENT_SECRET"] = "Rowpl4stVguifS4YJbzow1HCjh1g2uNuGNaFYRPk"

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
    # 注意：不再需要导入 ARCADION_HEAVYWEIGHT 或 SpellTag，因为不需要生成静态文件了
except ImportError as e:
    logger.error(f"Failed to import lorgs modules: {e}")
    sys.exit(1)


# --- 核心逻辑 ---

async def _do_update_spec(spec, boss_slug):
    """(内部函数) 只负责获取并保存排名数据"""
    spec_slug = spec.full_name_slug
    
    # 1. 获取排名数据 (网络请求)
    ranking = SpecRanking.get_or_create(
        boss_slug=boss_slug,
        spec_slug=spec_slug,
        difficulty="mythic",
        metric=spec.role.metric,
    )
    
    # limit=80 用于确保有足够的样本
    await ranking.load(limit=80, clear_old=True)
    
    # 2. 序列化数据
    data = ranking.model_dump(exclude_unset=True, by_alias=True)

    # 3. 保存排名文件
    filename = f"front_end/data/spec_ranking_{spec_slug}_{boss_slug}.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, "w") as f:
        json.dump(data, f, ensure_ascii=False, default=str)
        
    # logger.info(f"Saved ranking: {filename}") # 可选：减少日志刷屏

async def update_spec_with_retry(spec, boss_slug):
    """带重试机制的更新函数"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            await _do_update_spec(spec, boss_slug)
            return # 成功则退出
        except aiohttp.ClientResponseError as e:
            if e.status == 429:
                wait_time = 15 * (attempt + 1) # 429 稍微等久一点
                logger.warning(f"Rate Limit (429) for {spec.full_name_slug}. Waiting {wait_time}s... (Attempt {attempt+1}/{max_retries})")
                await asyncio.sleep(wait_time)
            else:
                logger.error(f"HTTP Error {e.status} for {spec.full_name_slug}: {e}")
                return 
        except Exception as e:
            logger.error(f"Error updating {spec.full_name_slug}: {e}")
            return 

async def main():
    WarcraftlogsClient._instance = None # 重置 Session

    try:
        # Boss 轮换列表 (每小时换一个)
        BOSS_ROTATION = [
            "vamp-fatale", "red-hot-and-deep-blue", "the-tyrant", "lindwurm", "lindwurm-ii"
        ]

        current_hour = datetime.datetime.now(datetime.timezone.utc).hour
        cycle_index = current_hour % len(BOSS_ROTATION)
        target_boss = BOSS_ROTATION[cycle_index]

        # 获取所有职业
        all_specs = sorted(list(ALL_SPECS), key=lambda s: s.full_name_slug)
        logger.info(f"=== Work Cycle: Hour {current_hour} | Boss: {target_boss} | Specs: {len(all_specs)} ===")

        # 执行爬取
        for i, spec in enumerate(all_specs):
            logger.info(f"[{i+1}/{len(all_specs)}] Updating {spec.full_name_slug}...")
            
            await update_spec_with_retry(spec, boss_slug=target_boss)
            
            # 礼貌性延迟，防止 429
            await asyncio.sleep(3)
        
        # 注意：这里不再调用 generate_boss_files()

    finally:
        logger.info("Closing HTTP Session...")
        if WarcraftlogsClient._instance and WarcraftlogsClient._instance.session:
            await WarcraftlogsClient._instance.session.close()
            await asyncio.sleep(0.25)
        logger.info("Done.")

if __name__ == "__main__":
    asyncio.run(main())