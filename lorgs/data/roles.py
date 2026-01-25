# 文件: lorgs/data/roles.py

from lorgs.models.wow_role import WowRole

################################################################################
# ROLES
#
TANK = WowRole(id=1, code="tank", name="Tank", metric="dps") # 坦克通常看 dps 或 ndps
HEAL = WowRole(id=2, code="heal", name="Healer", metric="hps")

# === 🟢 修改这里 ===
# 显式指定 metric="rdps"，这样 api_spec_rankings.py 就会使用 "rdps" 去查询 API
MDPS = WowRole(
    id=3, 
    code="mdps", 
    name="Melee", 
    metric="rdps",             # <--- 核心修改：默认使用 rdps
    metrics=["rdps", "adps"]   # <--- 可选：更新支持的指标列表
)

RDPS = WowRole(
    id=4, 
    code="rdps", 
    name="Range", 
    metric="rdps",             # <--- 核心修改：默认使用 rdps
    metrics=["rdps", "adps"]   # <--- 可选：更新支持的指标列表
)
# ==================

MIXED = WowRole(id=2001, code="mix", name="Mixed")

ALL_ROLES = [TANK, HEAL, MDPS, RDPS]