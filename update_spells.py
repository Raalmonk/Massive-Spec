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
    from lorgs.data.expansions.dawntrail.raids import ARCADION_HEAVYWEIGHT, FUTURES_REWRITTEN, LEGACY_ULTIMATES_ZONE
    import lorgs.data.items.potions # 确保药水和冲刺被加载
except ImportError as e:
    logger.error(f"Failed to import lorgs modules: {e}")
    sys.exit(1)


BOSS_TIMELINE_COLORS = {
    "mech": "#facc15",
    "tb": "#60a5fa",
    "aoe": "#fb923c",
}

BOSS_TIMELINE_FILENAME_MAP = {
    "vamp-fatale": "m9s",
    "red-hot-and-deep-blue": "m10s",
    "the-tyrant": "m11s",
    "lindwurm": "m12s_p1",
    "lindwurm-ii": "m12s_p2",
    "futures-rewritten": "futures_rewritten",
    "the-unending-coil-of-bahamut": "the_unending_coil_of_bahamut",
    "the-weapons-refrain": "the_weapons_refrain",
    "the-epic-of-alexander": "the_epic_of_alexander",
    "dragonsongs-reprise": "dragonsongs_reprise",
    "the-omega-protocol": "the_omega_protocol",
}


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


def get_boss_timeline_type_from_tags(tags):
    tags = tags or []
    if SpellTag.TANK_MIT in tags or SpellTag.SINGLE_MIT in tags:
        return "tb"
    if SpellTag.RAID_MIT in tags or SpellTag.RAID_CD in tags:
        return "aoe"
    return "mech"


def serialize_boss_timeline_event(event):
    item = event.as_dict()
    item["type"] = item.get("type") or "mech"
    item["color"] = item.get("color") or BOSS_TIMELINE_COLORS.get(item["type"], BOSS_TIMELINE_COLORS["mech"])
    return item


def serialize_boss_cast(cast):
    event_type = get_boss_timeline_type_from_tags(getattr(cast, "tags", []))
    return {
        "id": cast.spell_id,
        "name": cast.name,
        "time": parse_time(getattr(cast, "time", 0)),
        "duration": getattr(cast, "duration", 0),
        "color": getattr(cast, "color", "") or BOSS_TIMELINE_COLORS.get(event_type, BOSS_TIMELINE_COLORS["mech"]),
        "icon": getattr(cast, "icon", ""),
        "type": event_type,
        "name_i18n": getattr(cast, "name_i18n", {}),
    }


def get_bosses_for_timeline_generation():
    return [
        *ARCADION_HEAVYWEIGHT.bosses,
        FUTURES_REWRITTEN,
        *LEGACY_ULTIMATES_ZONE.bosses,
    ]

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
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(spells_data, f, indent=2, ensure_ascii=False)
            
        logger.info(f"  [OK] {spec.name:<15} -> {filename} ({len(spells_data)} spells)")
        count += 1

    logger.info(f">>> 完成！共生成 {count} 个职业文件。\n")


def generate_boss_spells():
    """生成 Boss 时间轴数据"""
    if not ARCADION_HEAVYWEIGHT: return

    logger.info(">>> 开始生成 Boss 时间轴数据...")

    for boss in get_bosses_for_timeline_generation():
        short_name = BOSS_TIMELINE_FILENAME_MAP.get(boss.full_name_slug, boss.full_name_slug.replace("-", "_"))
        filename = f"front_end/data/{short_name}.json"

        boss_timeline = getattr(boss, "boss_timeline", None)
        mechanics_data = (
            [serialize_boss_timeline_event(event) for event in boss_timeline]
            if boss_timeline is not None
            else [serialize_boss_cast(cast) for cast in boss.spells]
        )
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(mechanics_data, f, indent=2, ensure_ascii=False)
        logger.info(f"  [OK] {boss.name:<20} -> {filename}")

    logger.info(">>> Boss 数据完成。\n")


if __name__ == "__main__":
    generate_player_spells()
    generate_boss_spells()
