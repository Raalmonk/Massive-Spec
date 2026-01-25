import json
import logging
import os
import sys

# --- 1. 环境配置 ---
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ.setdefault("AWS_ACCESS_KEY_ID", "testing")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "testing")
os.environ["WCL_CLIENT_ID"] = "dummy"
os.environ["WCL_CLIENT_SECRET"] = "dummy"

sys.path.append(os.getcwd())

# --- 2. 导入业务模块 ---
from lorgs.logger import logger
# 【修复】同时导入 SpellTag 和 SpellType
from lorgs.models.wow_spell import SpellTag, SpellType 

# 日志设置
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# 导入数据
try:
    from lorgs.data.classes import ALL_SPECS
    from lorgs.data.expansions.dawntrail.raids.arcadion_heavyweight import ARCADION_HEAVYWEIGHT
except ImportError as e:
    logger.error(f"Failed to import lorgs modules: {e}")
    sys.exit(1)


# --- 3. 辅助函数 ---
def get_spell_category(spell):
    """根据技能属性计算前端分类"""
    tags = spell.tags or []
    
    # 优先级 1: 团减 (Group Mit)
    if SpellTag.RAID_MIT in tags:
        return "RAID_MIT" 
    
    # 优先级 2: 单减 (Single Mit) - 包括坦克减伤
    if SpellTag.TANK_MIT in tags or SpellTag.SINGLE_MIT in tags:
        return "SINGLE_MIT" 
    
    # 优先级 3: 功能性 / 药水
    # 【修复】使用 SpellType.POTION 来判断药水
    if spell.spell_type == SpellType.POTION:
        return "UTILITY"
    if SpellTag.UTILITY in tags:
        return "UTILITY"
        
    # 默认: 爆发/主要技能 (CD)
    return "MAJOR"

def parse_time(time_str):
    if isinstance(time_str, (int, float)): return time_str
    if not time_str: return 0
    try:
        if ":" in time_str:
            m, s = time_str.split(":")
            return int(m) * 60 + int(s)
        return int(time_str)
    except:
        return 0

# --- 4. 核心生成逻辑 ---

def generate_player_spells():
    """生成所有职业的技能文件 (spells_spec-slug.json)"""
    logger.info(">>> 开始生成职业技能数据...")
    
    all_specs = sorted(list(ALL_SPECS), key=lambda s: s.full_name_slug)
    
    count = 0
    for spec in all_specs:
        spec_slug = spec.full_name_slug
        spells_data = []
        
        for spell in spec.all_spells:
            # 【修复】传入整个 spell 对象
            cat = get_spell_category(spell)
            
            spell_obj = {
                "spell_id": spell.spell_id,
                "name": spell.name,
                "icon": spell.icon,
                "cooldown": spell.cooldown,
                "duration": spell.duration,
                "color": spell.color,
                "show": spell.show,
                "category": cat,
                "debug_tags": [str(t) for t in (spell.tags or [])]
            }
            spells_data.append(spell_obj)

        filename = f"front_end/data/spells_{spec_slug}.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, "w") as f:
            json.dump(spells_data, f, indent=2)
            
        logger.info(f"  [OK] {spec.name:<15} -> {filename} ({len(spells_data)} spells)")
        count += 1

    logger.info(f">>> 完成！共生成 {count} 个职业文件。\n")


def generate_boss_spells():
    """生成 Boss 时间轴数据"""
    if not ARCADION_HEAVYWEIGHT: return

    logger.info(">>> 开始生成 Boss 时间轴数据...")
    
    filename_map = {
        "vamp-fatale": "m9s",
        "red-hot-and-deep-blue": "m10s",
        "the-tyrant": "m11s",
        "lindwurm": "m12s_p1",
        "lindwurm-ii": "m12s_p2"
    }

    for boss in ARCADION_HEAVYWEIGHT.bosses:
        short_name = filename_map.get(boss.full_name_slug, boss.full_name_slug)
        filename = f"front_end/data/boss_{short_name}.json" 

        mechanics_data = []
        for cast in boss.spells:
            mechanics_data.append({
                "id": cast.spell_id,
                "name": cast.name,
                "time": parse_time(getattr(cast, "time", 0)),
                "duration": getattr(cast, "duration", 0),
                "color": getattr(cast, "color", ""),
                "icon": getattr(cast, "icon", ""),
                "type": "mechanic"
            })
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            json.dump(mechanics_data, f, indent=2)
        logger.info(f"  [OK] {boss.name:<20} -> {filename}")

    logger.info(">>> Boss 数据完成。\n")


if __name__ == "__main__":
    generate_player_spells()
    generate_boss_spells()