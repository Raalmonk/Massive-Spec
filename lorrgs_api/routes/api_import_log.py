"""Routes for importing one user's FF Logs pull into the local timeline."""

from __future__ import annotations

import re
import json
import os
import time
from contextlib import contextmanager
from datetime import datetime
from datetime import timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs
from urllib.parse import urlparse

import fastapi
import pydantic

from lorgs.clients.wcl import InvalidReport
from lorgs.models.warcraftlogs_report import Report

router = fastapi.APIRouter(tags=["import_log"], prefix="/import_log")
IMPORT_LOG_HOURLY_LIMIT = int(os.getenv("MSPEC_IMPORT_LOG_HOURLY_LIMIT", "2500"))
IMPORT_LOG_LIMIT_MESSAGE = "正在使用的玩家过多，请稍后"
RUNTIME_DIR = Path(os.getenv("MSPEC_RUNTIME_DIR", ".runtime"))
IMPORT_LOG_RATE_STATE_PATH = RUNTIME_DIR / "import_log_rate_limit.json"
IMPORT_LOG_RATE_LOCK_PATH = RUNTIME_DIR / "import_log_rate_limit.lock"


@contextmanager
def import_log_rate_lock():
    """Cross-process lock for the import-log hourly counter."""
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    with IMPORT_LOG_RATE_LOCK_PATH.open("a+b") as lock_file:
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(lock_file.fileno(), msvcrt.LK_LOCK, 1)
            try:
                yield
            finally:
                lock_file.seek(0)
                msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def check_import_log_hourly_limit() -> None:
    """Allow at most IMPORT_LOG_HOURLY_LIMIT import-log backend queries per UTC hour."""
    if IMPORT_LOG_HOURLY_LIMIT <= 0:
        return

    hour_key = datetime.now(timezone.utc).strftime("%Y%m%d%H")
    with import_log_rate_lock():
        state = {"hour": hour_key, "count": 0}
        if IMPORT_LOG_RATE_STATE_PATH.exists():
            try:
                state = json.loads(IMPORT_LOG_RATE_STATE_PATH.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                state = {"hour": hour_key, "count": 0}

        if state.get("hour") != hour_key:
            state = {"hour": hour_key, "count": 0}

        count = int(state.get("count") or 0)
        if count >= IMPORT_LOG_HOURLY_LIMIT:
            raise fastapi.HTTPException(status_code=429, detail=IMPORT_LOG_LIMIT_MESSAGE)

        IMPORT_LOG_RATE_STATE_PATH.write_text(
            json.dumps({"hour": hour_key, "count": count + 1, "updated_at": int(time.time())}),
            encoding="utf-8",
        )


class ImportLogRequest(pydantic.BaseModel):
    url: str


class ImportLogCastsRequest(ImportLogRequest):
    source_id: int


def parse_fflogs_url(url: str) -> tuple[str, int]:
    """Return the report code and fight id from a FF Logs report URL."""
    parsed = urlparse(url.strip())
    match = re.search(r"/reports/([A-Za-z0-9]+)", parsed.path)
    report_id = match.group(1) if match else ""

    query = parse_qs(parsed.query)
    fight_values = query.get("fight") or []
    fight_raw = fight_values[0] if fight_values else ""

    if not report_id:
        raise fastapi.HTTPException(status_code=400, detail="Could not find report id in URL.")
    if not fight_raw.isdigit():
        raise fastapi.HTTPException(status_code=400, detail="URL must include a numeric fight query parameter.")

    return report_id, int(fight_raw)


async def load_fight_from_url(url: str):
    report_id, fight_id = parse_fflogs_url(url)
    report = Report(report_id=report_id)

    try:
        await report.load(raise_errors=True)
    except InvalidReport:
        raise fastapi.HTTPException(status_code=404, detail="Report not found.")
    except PermissionError:
        raise fastapi.HTTPException(status_code=401, detail="No permission to view this report.")

    fight = report.get_fight(fight_id=fight_id)
    if not fight:
        raise fastapi.HTTPException(status_code=404, detail="Fight not found in report.")

    await fight.load(raise_errors=True)
    return report, fight


@router.post("/players")
async def list_import_log_players(payload: ImportLogRequest) -> dict[str, Any]:
    """List player choices for the fight in a pasted FF Logs URL."""
    check_import_log_hourly_limit()
    report, fight = await load_fight_from_url(payload.url)
    players = [
        {
            "source_id": player.source_id,
            "name": player.name,
            "class_slug": player.class_slug,
            "spec_slug": player.spec_slug,
            "total": player.total,
        }
        for player in fight.players
    ]

    return {
        "report_id": report.report_id,
        "fight_id": fight.fight_id,
        "title": report.title,
        "duration": fight.duration,
        "kill": fight.kill,
        "percent": fight.percent,
        "players": players,
    }


@router.post("/casts")
async def load_import_log_casts(payload: ImportLogCastsRequest) -> dict[str, Any]:
    """Load one selected player's casts for the fight in a pasted FF Logs URL."""
    check_import_log_hourly_limit()
    report, fight = await load_fight_from_url(payload.url)
    player = fight.get_player(source_id=payload.source_id)
    if not player:
        raise fastapi.HTTPException(status_code=404, detail="Player not found in fight.")

    await player.load(raise_errors=True)

    casts = []
    spells = {}
    for cast in player.casts:
        spell = cast.spell
        casts.append(
            {
                "spell_id": cast.spell_id,
                "ts": cast.timestamp,
                "c": cast.counter,
                "duration": (cast.duration or (spell.duration * 1000 if spell else 0)) / 1000,
            }
        )
        if spell:
            spells[str(cast.spell_id)] = {
                "id": cast.spell_id,
                "name": spell.name,
                "icon": f"./images/spells/{spell.icon}" if spell.icon else None,
                "duration": spell.duration or 0,
                "cd": spell.cooldown or 0,
                "color": spell.color or "#666666",
            }

    return {
        "report_id": report.report_id,
        "fight_id": fight.fight_id,
        "title": report.title,
        "duration": fight.duration,
        "kill": fight.kill,
        "percent": fight.percent,
        "player": {
            "source_id": player.source_id,
            "name": player.name,
            "class_slug": player.class_slug,
            "spec_slug": player.spec_slug,
            "total": player.total,
        },
        "phases": [phase.model_dump(by_alias=True) for phase in fight.phases],
        "casts": casts,
        "spells": spells,
    }
