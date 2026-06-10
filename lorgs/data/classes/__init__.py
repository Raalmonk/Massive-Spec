"""All Playable Classes in the Game."""
from __future__ import annotations

# Tanks
from lorgs.data.classes.paladin import *
from lorgs.data.classes.warrior import *
from lorgs.data.classes.darkknight import *
from lorgs.data.classes.gunbreaker import *

# Healers
from lorgs.data.classes.whitemage import *
from lorgs.data.classes.scholar import *
from lorgs.data.classes.astrologian import *
from lorgs.data.classes.sage import *

# Melee DPS
from lorgs.data.classes.dragoon import *
from lorgs.data.classes.reaper import *
from lorgs.data.classes.monk import *
from lorgs.data.classes.samurai import *
from lorgs.data.classes.ninja import *
from lorgs.data.classes.viper import *

# Physical Ranged DPS
from lorgs.data.classes.bard import *
from lorgs.data.classes.machinist import *
from lorgs.data.classes.dancer import *

# Magical Ranged DPS (Casters)
from lorgs.data.classes.summoner import *
from lorgs.data.classes.redmage import *
from lorgs.data.classes.blackmage import *
from lorgs.data.classes.pictomancer import *

from lorgs.data.classes.all_actions import *



# a few collections used to assign trinkets and consumables
# fmt: off
ALL_SPECS = TANK.specs | HEAL.specs | MDPS.specs | RDPS.specs
DPS_SPECS = MDPS.specs | RDPS.specs
