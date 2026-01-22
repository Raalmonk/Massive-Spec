import os
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"

from lorgs.data.expansions.dawntrail.raids.arcadion_heavyweight import RED_HOT_AND_DEEP_BLUE, VAMP_FATALE, THE_TYRANT
# The import below should trigger the side effects
import lorgs.data.expansions.dawntrail.raids

print(f"M9S Casts: {len(VAMP_FATALE.spells)}")
print(f"M10S Casts: {len(RED_HOT_AND_DEEP_BLUE.spells)}")
print(f"M11S Casts: {len(THE_TYRANT.spells)}")
