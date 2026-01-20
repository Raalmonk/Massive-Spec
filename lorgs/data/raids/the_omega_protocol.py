# lorgs/data/raids/the_omega_protocol.py
from lorgs.models.raid_boss import RaidBoss

# Define the Boss
# ID: 1068 is The Omega Protocol (Ultimate) in FF Logs
OMEGA_PROTOCOL = RaidBoss(
    id=1068,
    name="The Omega Protocol (Ultimate)",
    nick="TOP",
    icon="top_icon.jpg" # Placeholder
)

boss = OMEGA_PROTOCOL

# --- Phase 1: Omega ---

# Program Loop (Cast) - ID: 31544 (Example ID, needs verification)
boss.add_cast(
    spell_id=31544,
    name="Program Loop",
    duration=5,
    color="#ff0000",
    icon="program_loop.jpg"
)

# Pantokrator (Cast) - ID: 31550
boss.add_cast(
    spell_id=31550,
    name="Pantokrator",
    duration=8,
    color="#ff0000",
    icon="pantokrator.jpg"
)

# --- Phase 2: Omega-M/F ---

# Firewall (Buff/Mechanic) - Example
# boss.add_buff(...)

# Note: We will add accurate Spell IDs later. This structure is just to get the system running.
