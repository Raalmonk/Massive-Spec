import asyncio
import aiohttp
import os
import json
import sys

# Credentials
CLIENT_ID = os.environ.get("WCL_CLIENT_ID")
CLIENT_SECRET = os.environ.get("WCL_CLIENT_SECRET")
TOKEN_URL = "https://www.fflogs.com/oauth/token"
API_URL = "https://www.fflogs.com/api/v2/client"

async def get_token(session):
    if not CLIENT_ID or not CLIENT_SECRET:
        print("Error: WCL_CLIENT_ID and WCL_CLIENT_SECRET must be set.")
        sys.exit(1)

    auth = aiohttp.BasicAuth(CLIENT_ID, CLIENT_SECRET)
    data = {"grant_type": "client_credentials"}
    async with session.post(TOKEN_URL, auth=auth, data=data) as resp:
        if resp.status != 200:
            print(f"Failed to get token: {resp.status} {await resp.text()}")
            sys.exit(1)
        json_resp = await resp.json()
        return json_resp["access_token"]

async def query_graphql(session, token, query, variables=None):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    json_data = {"query": query, "variables": variables}
    async with session.post(API_URL, headers=headers, json=json_data) as resp:
        if resp.status != 200:
            print(f"GraphQL Query Failed: {resp.status} {await resp.text()}")
            return None
        return await resp.json()

async def fetch_rankings(session, token, region=None):
    # Boss 101 - checking if it exists or if I should use a known boss ID.
    # The user explicitly said "Boss 101". I will trust this.

    query = """
    query($region: String) {
        worldData {
            encounter(id: 101) {
                characterRankings(
                    metric: healercombineddps,
                    filter: "classes.WhiteMage.gte.1 AND classes.Scholar.gte.1",
                    serverRegion: $region,
                    includeCombatantInfo: true,
                    page: 1
                )
            }
        }
    }
    """
    variables = {"region": region}
    data = await query_graphql(session, token, query, variables)

    if not data or "errors" in data:
        print(f"Error fetching rankings: {data}")
        return []

    try:
        rankings = data["data"]["worldData"]["encounter"]["characterRankings"]["rankings"]
        return rankings # Return all to filter client-side
    except (KeyError, TypeError) as e:
        print(f"Error parsing rankings for region {region}: {e}")
        if data:
             print(json.dumps(data, indent=2))
        return []

async def fetch_fight_summary(session, token, report_id, fight_id):
    query = """
    query($reportID: String!, $fightID: Int!) {
        reportData {
            report(code: $reportID) {
                table(fightIDs: [$fightID], dataType: Summary)
            }
        }
    }
    """
    variables = {"reportID": report_id, "fightID": fight_id}
    data = await query_graphql(session, token, query, variables)
    try:
        # table returns generic JSON data in 'data' field or structured?
        # In WCL v2, table returns { data: { composition: [...] } } or similar?
        # Actually it returns the raw JSON structure for the table.
        # But 'table' field itself returns "JSON".
        # Wait, the return type of table is JSON.

        table_data = data["data"]["reportData"]["report"]["table"]
        # If it's pure JSON, it might be a dict already if aiohttp parsed it?
        # Or maybe it's a sub-field.

        if isinstance(table_data, dict) and "data" in table_data:
             # Sometimes it's wrapped in data?
             # Let's check lorgs/models/warcraftlogs_fight.py: summary_data = report_data.report.summary
             # summary is alias for table(..., dataType: Summary).
             pass

        return table_data
    except (KeyError, TypeError):
        print(f"Error fetching summary data: {json.dumps(data, indent=2)}")
        return {}

async def fetch_events(session, token, report_id, fight_id, start_time, end_time, source_ids):
    # Fetch all casts for the fight and filter in Python to avoid empty list issues with API filtering.

    query = """
    query($reportID: String!, $fightID: Int!, $startTime: Float!, $endTime: Float!) {
        reportData {
            report(code: $reportID) {
                events(
                    fightIDs: [$fightID],
                    dataType: Casts,
                    startTime: $startTime,
                    endTime: $endTime,
                    limit: 10000
                ) {
                    data
                    nextPageTimestamp
                }
            }
        }
    }
    """
    variables = {
        "reportID": report_id,
        "fightID": fight_id,
        "startTime": start_time,
        "endTime": end_time
    }

    data = await query_graphql(session, token, query, variables)

    if not data or "errors" in data:
        print(f"Error fetching events: {data}")
        return []

    try:
        events = data["data"]["reportData"]["report"]["events"]["data"]
        # Handle pagination if necessary, but user didn't explicitly ask for full pagination logic, just "Fetch the timeline events".
        # 10000 limit should be enough for casts in a single fight for 2 players.
        return events
    except (KeyError, TypeError) as e:
        print(f"Error parsing events: {e}")
        return []

async def main():
    async with aiohttp.ClientSession() as session:
        token = await get_token(session)
        print("Authentication successful.")

        results = []

        for region in [None, "CN"]: # None for Global
            region_name = region if region else "GL"
            print(f"Fetching rankings for {region_name}...")
            rankings = await fetch_rankings(session, token, region)

            if not rankings:
                print(f"No rankings found for {region_name}.")
                continue

            valid_rank_count = 0
            for i, rank_data in enumerate(rankings):
                if valid_rank_count >= 3:
                    break

                report = rank_data.get("report", {})
                report_id = report.get("code")
                fight_id = report.get("fightID")

                fight_start_abs = rank_data.get("startTime")
                report_start_abs = report.get("startTime")
                duration = rank_data.get("duration")

                if not (report_id and fight_id and fight_start_abs and report_start_abs and duration):
                    continue

                rel_start = fight_start_abs - report_start_abs
                rel_end = rel_start + duration

                # Fetch Composition (Summary)
                summary = await fetch_fight_summary(session, token, report_id, fight_id)
                composition = summary.get("data", {}).get("composition", [])

                whm = next((c for c in composition if c["type"] == "WhiteMage"), None)
                sch = next((c for c in composition if c["type"] == "Scholar"), None)

                players_result = []
                source_ids = []

                if whm and sch:
                    print(f"Processing Rank {i+1} ({region_name}) - Found WHM and SCH")
                    players_result.append({"name": whm["name"], "spec": "WhiteMage", "id": whm["id"]})
                    source_ids.append(whm["id"])
                    players_result.append({"name": sch["name"], "spec": "Scholar", "id": sch["id"]})
                    source_ids.append(sch["id"])
                else:
                    # Skip if we don't have both
                    continue

                # Fetch Events
                print(f"  Fetching events for Report {report_id}, Fight {fight_id}...")
                events = await fetch_events(session, token, report_id, fight_id, rel_start, rel_end, source_ids)

                if not events:
                    print("  Warning: Event list is empty! Skipping.")
                    continue
                else:
                    print(f"  Retrieved {len(events)} events.")

                # Process Events
                for p in players_result:
                    p_events = []
                    for e in events:
                        if e.get("sourceID") == p["id"]:
                            p_events.append({
                                "time": e.get("timestamp") - rel_start,
                                "id": e.get("abilityGameID"),
                                "type": e.get("type")
                            })
                    p["casts"] = p_events
                    # Remove internal ID from output
                    del p["id"]

                valid_rank_count += 1
                results.append({
                    "rank": valid_rank_count,
                    "region": region_name,
                    "report_id": report_id,
                    "fight_id": fight_id,
                    "total_dps": rank_data.get("amount"),
                    "players": players_result
                })

        with open("healer_top_ranks.json", "w") as f:
            json.dump(results, f, indent=2)
            print("Successfully saved data to healer_top_ranks.json")

if __name__ == "__main__":
    asyncio.run(main())
