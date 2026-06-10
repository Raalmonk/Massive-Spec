import json
import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()

# --- 1. 环境配置 ---
os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
os.environ.setdefault("AWS_ACCESS_KEY_ID", "testing")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "testing")

if not os.getenv("WCL_CLIENT_ID") or not os.getenv("WCL_CLIENT_SECRET"):
    print("Error: WCL_CLIENT_ID and WCL_CLIENT_SECRET must be set in environment variables or .env file.")
    sys.exit(1)

sys.path.append(os.getcwd())

# --- 2. 导入业务模块 ---
from lorgs.logger import logger
from lorgs.models.wow_spell import SpellTag, SpellType 

# 日志设置
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# 导入数据
try:
    from lorgs.data.classes import ALL_SPECS
    from lorgs.data.expansions.dawntrail.raids.arcadion_heavyweight import ARCADION_HEAVYWEIGHT
    import lorgs.data.items.potions # 确保药水和冲刺被加载
except ImportError as e:
    logger.error(f"Failed to import lorgs modules: {e}")
    sys.exit(1)


# --- 3. 辅助函数 ---
def get_spell_category(spell):
    """根据技能属性计算前端分类 (增强版)"""
    tags = spell.tags or []
    
    # --- 团减 / 团辅 (Group Mit) ---
    # 你的逻辑: RAID_CD (奶妈大招) 也算进团减组
    if SpellTag.RAID_MIT in tags or SpellTag.RAID_CD in tags:
        return "RAID_MIT" 
    
    # --- 单减 / 个人减伤 (Single Mit) ---
    # 你的逻辑: DEFENSIVE (个人减伤) 算进单减组
    if SpellTag.TANK_MIT in tags or SpellTag.SINGLE_MIT in tags or SpellTag.DEFENSIVE in tags:
        return "SINGLE_MIT" 
    
    # --- 功能性 / 药水 ---
    if spell.spell_type == SpellType.POTION or SpellTag.UTILITY in tags:
        return "UTILITY"

    if SpellTag.OTHER in tags:
        return "OTHER"
        
    # --- 默认: 爆发/主要技能 (CD) ---
    # 包括 SpellTag.DAMAGE
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
    
    # 按字母顺序排序
    all_specs = sorted(list(ALL_SPECS), key=lambda s: s.full_name_slug)
    
    count = 0
    for spec in all_specs:
        spec_slug = spec.full_name_slug
        spells_data = []

        slot_orders = {}
        for i, spell in enumerate(spec.all_spells):
            slot = getattr(spell, "display_slot", "") or str(spell.spell_id)
            slot_orders[slot] = min(slot_orders.get(slot, i), i)
        
        # 遍历该职业的所有可用技能
        # enumerat提供索引 i，用作 load_order
        for i, spell in enumerate(spec.all_spells):
            
            cat = get_spell_category(spell)
            display_slot = getattr(spell, "display_slot", "")
            slot_order = slot_orders.get(display_slot or str(spell.spell_id), i)
            
            spell_obj = {
                "spell_id": spell.spell_id,
                "name": spell.name,
                "icon": spell.icon,
                "cooldown": spell.cooldown,
                "duration": spell.duration,
                "color": spell.color,
                
                # --- 核心修复 ---
                "load_order": slot_order,       # 1. 同一上下位技能共用显示位置
                "show": spell.show,    # 是否显示
                "category": cat,       # 2. 使用增强后的分类逻辑
                "level": getattr(spell, "level", 0),
                "display_slot": display_slot,
                
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
