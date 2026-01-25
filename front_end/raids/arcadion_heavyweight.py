from lorgs.models.raid_boss import RaidBoss
from lorgs.models.raid_zone import RaidZone

ARCADION_HEAVYWEIGHT = RaidZone(
    id=73,
    name="Arcadion: Heavyweight",
    icon="achievement_raid_arcadion.jpg", # Placeholder
)

VAMP_FATALE = ARCADION_HEAVYWEIGHT.add_boss(id=101, name="Vamp Fatale", nick="M9S", icon="boss_vamp_fatale.jpg")
RED_HOT_AND_DEEP_BLUE = ARCADION_HEAVYWEIGHT.add_boss(id=102, name="Red Hot and Deep Blue", nick="M10S", icon="boss_red_hot.jpg")
THE_TYRANT = ARCADION_HEAVYWEIGHT.add_boss(id=103, name="The Tyrant", nick="M11S", icon="boss_tyrant.jpg")
LINDWURM = ARCADION_HEAVYWEIGHT.add_boss(id=104, name="Lindwurm", nick="M12S P1", icon="boss_lindwurm.jpg")
LINDWURM_II = ARCADION_HEAVYWEIGHT.add_boss(id=105, name="Lindwurm II", nick="M12S P2", icon="boss_lindwurm_ii.jpg")
