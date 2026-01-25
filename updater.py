import asyncio
import datetime
import json
import logging
import os
import sys

# Ensure lorgs module is found
sys.path.append(os.getcwd())

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import Lorgs logic
try:
    from lorgs.data.classes import ALL_SPECS
    from lorgs.models.warcraftlogs_ranking import SpecRanking
except ImportError as e:
    logger.error(f"Failed to import lorgs modules: {e}")
    sys.exit(1)

async def update_spec(spec, boss_slug="vamp-fatale"):
    """Fetch and save data for a single spec."""
    spec_slug = spec.full_name_slug
    logger.info(f"Updating {spec_slug}...")

    try:
        ranking = SpecRanking.get_or_create(
            boss_slug=boss_slug,
            spec_slug=spec_slug,
            difficulty="mythic",
            metric=spec.role.metric,
        )

        # Load data from WCL
        # using limit=80 to match lorrgs_api/routes/api_spec_rankings.py
        await ranking.load(limit=80, clear_old=True)

        # Serialize
        data = ranking.model_dump(exclude_unset=True, by_alias=True)

        # Save to file
        filename = f"front_end/data/spec_ranking_{spec_slug}_{boss_slug}.json"

        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, "w") as f:
            json.dump(data, f)

        logger.info(f"Saved {filename}")

    except Exception as e:
        logger.error(f"Error updating {spec_slug}: {e}")

async def main():
    # 1. Sort Specs
    sorted_specs = sorted(list(ALL_SPECS), key=lambda s: s.full_name_slug)

    # 2. Determine Rotation
    # Cycle is 5 hours.
    # 0-3: 4 specs
    # 4: 5 specs

    current_hour = datetime.datetime.now(datetime.timezone.utc).hour
    cycle_hour = current_hour % 5

    start_idx = cycle_hour * 4
    if cycle_hour < 4:
        end_idx = start_idx + 4
    else:
        end_idx = start_idx + 5

    specs_to_update = sorted_specs[start_idx:end_idx]

    logger.info(f"Hour: {current_hour} (Cycle: {cycle_hour}). Updating {len(specs_to_update)} specs: {[s.full_name_slug for s in specs_to_update]}")

    # 3. Update Specs
    for spec in specs_to_update:
        await update_spec(spec)

if __name__ == "__main__":
    asyncio.run(main())
