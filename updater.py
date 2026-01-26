import asyncio
import datetime
import json
import logging
import os
import sys
import time

from dotenv import load_dotenv

load_dotenv()

# --- 1. 环境配置 ---
os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
os.environ.setdefault("AWS_ACCESS_KEY_ID", "testing")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "testing")

# WCL 密钥
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
    # 注意：不再需要导入 ARCADION_HEAVYWEIGHT 或 SpellTag，因为不需要生成静态文件了
except ImportError as e:
    logger.error(f"Failed to import lorgs modules: {e}")
    sys.exit(1)


# --- 核心逻辑 ---

# 修改函数签名，增加 timestamp_folder 参数
async def _do_update_spec(spec, boss_slug, timestamp_folder):
    """(内部函数) 只负责获取并保存排名数据"""
    spec_slug = spec.full_name_slug
    
    # 1. 获取排名数据 (网络请求) - 保持不变
    ranking = SpecRanking.get_or_create(
        boss_slug=boss_slug,
        spec_slug=spec_slug,
        difficulty="mythic",
        metric=spec.role.metric,
    )
    
    # 这里的 clear_old=True 配合我们之前的讨论，保证数据纯净
    await ranking.load(limit=80, clear_old=True)
    
    # 2. 序列化数据 - 保持不变
    data = ranking.model_dump(exclude_unset=True, by_alias=True)

    # 3. 保存实时文件 (给前端用) - 保持不变
    current_filename = f"front_end/data/spec_ranking_{spec_slug}_{boss_slug}.json"
    os.makedirs(os.path.dirname(current_filename), exist_ok=True)
    
    with open(current_filename, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, default=str)

    # ==============================================================================
    # 4. [修改] 历史归档 (带时间戳)
    # ==============================================================================
    # 归档目录结构: archives/2026-01-26/14-00/
    # 我们把日期和时间分级存储，这样文件夹不会太乱
    # 或者直接 archives/2026-01-26_14-00/
    
    # 这里使用传入的 timestamp_folder，例如 "archives/2026-01-26/14_00"
    os.makedirs(timestamp_folder, exist_ok=True)
    
    archive_filename = os.path.join(timestamp_folder, f"spec_ranking_{spec_slug}_{boss_slug}.json")
    
    with open(archive_filename, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, default=str)
        
    # logger.info(f"Archived: {archive_filename}")

async def update_spec_with_retry(spec, boss_slug, timestamp_folder):
    """带重试机制的更新函数"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # 传递参数给 _do_update_spec
            await _do_update_spec(spec, boss_slug, timestamp_folder)
            return 
        except aiohttp.ClientResponseError as e:
            if e.status == 429:
                wait_time = 15 * (attempt + 1)
                logger.warning(f"Rate Limit (429). Waiting {wait_time}s...")
                await asyncio.sleep(wait_time)
            else:
                logger.error(f"HTTP Error {e.status}: {e}")
                return 
        except Exception as e:
            logger.error(f"Error updating {spec.full_name_slug}: {e}")
            return

async def main():
    WarcraftlogsClient._instance = None 

    try:
        # Boss 轮换列表
        BOSS_ROTATION = [
            "vamp-fatale", "red-hot-and-deep-blue", "the-tyrant", "lindwurm", "lindwurm-ii"
        ]

        # 获取当前时间
        now = datetime.datetime.now(datetime.timezone.utc)
        current_hour = now.hour
        cycle_index = current_hour % len(BOSS_ROTATION)
        target_boss = BOSS_ROTATION[cycle_index]

        # ======================================================================
        # [新增] 生成本轮抓取的统一归档目录名
        # 格式: archives/2026-01-26/02h_lindwurm/ (包含日期、小时、和当前Boss)
        # 这样你就清楚每个文件夹里存的是几点钟抓的哪个Boss的数据
        # ======================================================================
        date_str = now.strftime("%Y-%m-%d")     # 2026-01-26
        time_str = now.strftime("%Hh_%Mm")      # 14h_30m
        
        # 最终路径: archives/2026-01-26/14h_30m_lindwurm/
        archive_batch_dir = os.path.join(
            "archives", 
            date_str, 
            f"{time_str}_{target_boss}"
        )
        
        logger.info(f"=== Work Cycle: Hour {current_hour} | Boss: {target_boss} ===")
        logger.info(f"=== Archive Target: {archive_batch_dir} ===")

        all_specs = sorted(list(ALL_SPECS), key=lambda s: s.full_name_slug)

        for i, spec in enumerate(all_specs):
            logger.info(f"[{i+1}/{len(all_specs)}] Updating {spec.full_name_slug}...")
            
            # 传入 archive_batch_dir
            await update_spec_with_retry(spec, boss_slug=target_boss, timestamp_folder=archive_batch_dir)
            
            await asyncio.sleep(3)

    finally:
        logger.info("Closing HTTP Session...")
        if WarcraftlogsClient._instance and WarcraftlogsClient._instance.session:
            await WarcraftlogsClient._instance.session.close()
            await asyncio.sleep(0.25)
        logger.info("Done.")

if __name__ == "__main__":
    asyncio.run(main())