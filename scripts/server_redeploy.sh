#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

PYTHON_BIN="${PYTHON_BIN:-python3}"
DMU_LIMIT="${DMU_LIMIT:-100}"
DMU_DELAY="${DMU_DELAY:-1}"
START_MAIN="${START_MAIN:-1}"
START_UPDATER="${START_UPDATER:-1}"

DEPLOY_LOCK="/tmp/mspec-deploy.lock"
MAIN_LOCK="/tmp/mspec-main.lock"
UPDATER_LOCK="/tmp/mspec-updater.lock"
DMU_LOCK="/tmp/mspec-dmu-refresh.lock"
FRONTEND_DATA_BACKUP_DIR=""

log() {
    printf '[%s] %s\n' "$(date '+%F %T')" "$*"
}

run() {
    log "$*"
    "$@"
}

require_command() {
    if ! command -v "$1" >/dev/null 2>&1; then
        log "ERROR: missing command: $1"
        exit 1
    fi
}

stop_matching_processes() {
    local label="$1"
    local pattern="$2"
    local pids

    pids="$(pgrep -f "$pattern" || true)"
    if [[ -z "${pids}" ]]; then
        log "No running ${label} process found."
        return
    fi

    log "Stopping ${label}: ${pids//$'\n'/ }"
    kill ${pids} 2>/dev/null || true
    sleep 2

    pids="$(pgrep -f "$pattern" || true)"
    if [[ -n "${pids}" ]]; then
        log "Force stopping ${label}: ${pids//$'\n'/ }"
        kill -9 ${pids} 2>/dev/null || true
    fi
}

backup_frontend_data() {
    if [[ ! -d "front_end/data" ]]; then
        log "front_end/data does not exist; skipping backup."
        return
    fi

    FRONTEND_DATA_BACKUP_DIR="${HOME}/mspec-data-backup-$(date '+%F-%H%M%S')"
    run mkdir -p "${FRONTEND_DATA_BACKUP_DIR}"
    run cp -a front_end/data "${FRONTEND_DATA_BACKUP_DIR}/data"
    log "Backed up front_end/data to ${FRONTEND_DATA_BACKUP_DIR}/data"
}

restore_generated_rankings_from_backup() {
    if [[ -z "${FRONTEND_DATA_BACKUP_DIR}" || ! -d "${FRONTEND_DATA_BACKUP_DIR}/data" ]]; then
        log "No front_end/data backup exists; skipping generated ranking restore."
        return
    fi

    log "Restoring generated spec_ranking_*.json files from backup."
    find "${FRONTEND_DATA_BACKUP_DIR}/data" -maxdepth 1 -type f -name 'spec_ranking_*.json' -exec cp -a {} front_end/data/ \;
}

prepare_generated_rankings_for_pull() {
    if [[ -z "${FRONTEND_DATA_BACKUP_DIR}" || ! -d "${FRONTEND_DATA_BACKUP_DIR}/data" ]]; then
        log "ERROR: refusing to clean generated ranking files without a backup."
        exit 1
    fi

    log "Preparing generated ranking files for git pull without using stash."
    log "Tracked spec_ranking files will be restored to HEAD; untracked spec_ranking files will be removed from the working tree."
    log "The server-generated copies are safe in ${FRONTEND_DATA_BACKUP_DIR}/data and will be copied back after pull."

    git checkout -- 'front_end/data/spec_ranking_*.json' 2>/dev/null || true
    git clean -fdx -- 'front_end/data/spec_ranking_*.json'
}

pull_latest_code() {
    log "Pulling latest code with --ff-only..."
    if git pull --ff-only; then
        restore_generated_rankings_from_backup
        return
    fi

    log "git pull failed. This is usually caused by generated front_end/data files."
    log "Current git status:"
    git status --short || true

    prepare_generated_rankings_for_pull
    run git pull --ff-only
    restore_generated_rankings_from_backup
}

check_python_files() {
    run "${PYTHON_BIN}" -m py_compile \
        main.py \
        updater.py \
        update_spells.py \
        scripts/update_all_job_actions.py \
        scripts/verify_all_job_actions_fflogs.py \
        scripts/refresh_boss_all_specs.py \
        scripts/refresh_dancing_mad_all_specs.py \
        lorrgs_api/routes/api_import_log.py \
        lorgs/clients/wcl/client.py \
        lorgs/models/warcraftlogs_ranking.py \
        lorgs/data/classes/all_actions.py \
        lorgs/data/classes/whitemage.py \
        lorgs/data/classes/astrologian.py
}

refresh_dancing_mad() {
    log "Refreshing Dancing Mad all specs now. This can take a while."
    flock -n "${DMU_LOCK}" "${PYTHON_BIN}" scripts/refresh_dancing_mad_all_specs.py \
        --metric rdps \
        --limit "${DMU_LIMIT}" \
        --regions global cn kr \
        --delay "${DMU_DELAY}" 2>&1 | tee -a dmu_refresh.log
}

start_main() {
    if [[ "${START_MAIN}" != "1" ]]; then
        log "START_MAIN=${START_MAIN}; skipping main.py start."
        return
    fi

    log "Starting main.py behind ${MAIN_LOCK}..."
    (exec 9>&-; nohup flock -n "${MAIN_LOCK}" "${PYTHON_BIN}" main.py >> main.log 2>&1 &)
    sleep 3

    if pgrep -f "flock -n ${MAIN_LOCK}|${PYTHON_BIN} main.py|uvicorn.*main:app" >/dev/null 2>&1; then
        log "main.py appears to be running."
    else
        log "WARNING: main.py did not appear to start. Check main.log."
    fi
}

start_updater() {
    if [[ "${START_UPDATER}" != "1" ]]; then
        log "START_UPDATER=${START_UPDATER}; skipping updater.py start."
        return
    fi

    log "Starting updater.py behind ${UPDATER_LOCK}..."
    (exec 9>&-; nohup flock -n "${UPDATER_LOCK}" "${PYTHON_BIN}" updater.py >> updater.log 2>&1 &)
    sleep 3

    if pgrep -f "flock -n ${UPDATER_LOCK}|${PYTHON_BIN} updater.py" >/dev/null 2>&1; then
        log "updater.py appears to be running."
    else
        log "WARNING: updater.py did not appear to start. Check updater.log."
    fi
}

print_processes() {
    log "Current M-Spec processes:"
    ps aux | grep -E "main.py|updater.py|uvicorn.*main:app|mspec-main.lock|mspec-updater.lock" | grep -v grep || true
}

check_dancing_mad_files() {
    "${PYTHON_BIN}" - <<'PY'
import json
from pathlib import Path

specs = [
    "whitemage-whitemage",
    "scholar-scholar",
    "astrologian-astrologian",
    "reaper-reaper",
]

print("[DMU check]")
for spec in specs:
    path = Path("front_end/data") / f"spec_ranking_{spec}_dancing-mad.json"
    if not path.exists():
        print(f"{spec}: missing {path}")
        continue

    data = json.loads(path.read_text(encoding="utf-8"))
    regions = {}
    fights = 0
    for report in data.get("reports", []):
        region = report.get("region") or "??"
        count = len(report.get("fights", []))
        regions[region] = regions.get(region, 0) + count
        fights += count

    print(f"{spec}: fights={fights} regions={regions}")
PY
}

check_http() {
    if ! command -v curl >/dev/null 2>&1; then
        log "curl is not installed; skipping HTTP check."
        return
    fi

    if curl -fsS -I "http://127.0.0.1:5000/" >/dev/null 2>&1; then
        log "HTTP check passed: http://127.0.0.1:5000/"
    else
        log "WARNING: HTTP check failed. Check main.log and your reverse proxy."
    fi
}

main() {
    exec 9>"${DEPLOY_LOCK}"
    if ! flock -n 9; then
        log "Another deploy/restart is already running. Exiting."
        exit 1
    fi

    require_command git
    require_command flock
    require_command "${PYTHON_BIN}"

    log "M-Spec server redeploy started in ${REPO_ROOT}"

    stop_matching_processes "updater.py" "[p]ython[0-9.]* updater.py|flock -n ${UPDATER_LOCK}"
    stop_matching_processes "main.py" "[p]ython[0-9.]* main.py|uvicorn.*main:app|flock -n ${MAIN_LOCK}"

    backup_frontend_data
    pull_latest_code
    check_python_files
    refresh_dancing_mad
    check_dancing_mad_files
    start_main
    start_updater
    print_processes
    check_http

    log "M-Spec server redeploy complete."
}

main "$@"
