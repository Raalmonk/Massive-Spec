from __future__ import annotations

# IMPORT STANRD LIBRARIES
import typing
from typing import Optional

# IMPORT LOCAL LIBRARIES
from lorgs.clients import wcl
from lorgs.limit_breaks import LIMIT_BREAKS
from lorgs.limit_breaks import is_limit_break_spell_id
from lorgs.models.warcraftlogs_actor import BaseActor
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import WowSpell, build_spell_query


DANCER_SPEC_SLUG = "dancer-dancer"
DANCE_PARTNER_CAST_ID = 16006
DANCE_PARTNER_AURA_IDS = {1824, 2027}


class Player(BaseActor):
    """A PlayerCharater in a Fight (or report)."""

    name: str = ""
    class_slug: str = ""
    spec_slug: str = ""
    guid: int = 0

    total: float = 0

    deaths: list = []
    resurrects: list = []
    dance_partners: list = []

    def __str__(self) -> str:
        return f"Player(id={self.source_id} name={self.name} spec={self.spec})"

    def summary(self) -> dict[str, typing.Any]:
        return {
            "name": self.name,
            "source_id": self.source_id,
            "class": self.class_slug,
            "spec": self.spec_slug,
            "role": self.spec.role.code if self.spec else "",
        }

    def as_dict(self) -> dict[str, typing.Any]:
        return {
            **self.summary(),
            "total": int(self.total),
            "casts": [cast.dict() for cast in self.casts],
            "deaths": self.deaths,
            "resurrects": self.resurrects,
            "dance_partners": self.dance_partners,
        }

    ##########################
    # Attributes
    #
    @property
    def class_(self) -> WowClass:
        return WowClass.get(name_slug=self.class_slug)  # type: ignore

    @property
    def spec(self) -> WowSpec:
        return WowSpec.get(full_name_slug=self.spec_slug)  # type: ignore

    def get_actor_type(self):
        return self.spec

    ############################################################################
    # Query
    #

    def get_sub_query(self):

        def get_filter(target_type="source"):
            if self.guid > 0:
                return f"{target_type}.id={self.guid}"
            if self.source_id > 0:
                return f"{target_type}.id={self.source_id}"
            elif self.name:
                return f"{target_type}.name='{self.name}'"
            return ""

        source_filter = get_filter("source")
        target_filter = get_filter("target")

        # Casts
        casts_query = build_spell_query(*self.actor_type.all_spells)
        if casts_query and source_filter:
            casts_query = f"{source_filter} and ({casts_query})"

        # Limit Break is a raid event: every row should show it, regardless of who pressed it.
        limit_break_query = build_spell_query(*LIMIT_BREAKS)
        casts_query = self.combine_queries(casts_query, limit_break_query)

        # Auras
        auras_query = build_spell_query(*self.actor_type.all_buffs, *self.actor_type.all_debuffs)
        if auras_query and target_filter:
            auras_query = f"{target_filter} and ({auras_query})"

        # Events
        events_query = build_spell_query(*self.actor_type.all_events)
        if events_query and source_filter:
            events_query = f"{source_filter} and ({events_query})"

        resurrection_query = ""
        if self.resurrects and target_filter:
            resurrection_query = f"{target_filter} and type='resurrect'"

        dance_partner_query = ""
        if self.spec_slug == DANCER_SPEC_SLUG and source_filter:
            aura_ids = ",".join(str(spell_id) for spell_id in sorted(DANCE_PARTNER_AURA_IDS))
            dance_partner_query = (
                f"{source_filter} and ("
                f"(type='cast' and ability.id = {DANCE_PARTNER_CAST_ID}) or "
                f"(type='applybuff' and ability.id in ({aura_ids})) or "
                f"(type='removebuff' and ability.id in ({aura_ids}))"
                f")"
            )

        return self.combine_queries(casts_query, auras_query, events_query, resurrection_query, dance_partner_query)

    ############################################################################
    # Process
    #

    def process_death_events(self, death_events: list[wcl.DeathEvent]):
        """Add the Death Events the the Players.

        Args:
            death_events[list[dict]]

        """

        # TODO: add during model validation?
        # ABILITY_OVERWRITES = {}
        # ABILITY_OVERWRITES[1] = {"name": "Melee", "guid": 260421, "abilityIcon": "ability_meleedamage.jpg"}
        # ABILITY_OVERWRITES[3] = {"name": "Fall Damage"}

        # new list so that pydantic's "exclude unset" doesn't exclude it.
        self.deaths = []

        for death_event in death_events:
            target_id = death_event.id
            if self._has_source_id and (target_id != self.source_id):
                continue

            death_ability = death_event.ability
            # death_ability_id = death_ability.guid
            # death_ability = ABILITY_OVERWRITES.get(death_ability_id) or death_ability

            death_data = {
                "ts": death_event.deathTime,
                "spell_name": death_ability.name,
                "spell_icon": death_ability.abilityIcon,
            }
            self.deaths.append(death_data)

    def process_event_resurrect(self, event: "wcl.ReportEvent"):
        fight_start = self.fight.start_time_rel if self.fight else 0

        data: dict[str, typing.Any] = {}
        data["ts"] = event.timestamp - fight_start

        spell_id = event.abilityGameID
        spell = WowSpell.get(spell_id=spell_id)
        if spell:
            data["spell_name"] = spell.name
            data["spell_icon"] = spell.icon

        # new list so that pydantic's "exclude unset" doesn't exclude it.
        self.resurrects = []

        # Look for the Source ID
        source_id = event.sourceID
        if self.fight and self.fight.report:
            source_player = self.fight.get_player(source_id=source_id)
            if source_player:
                data["source_name"] = source_player.name
                data["source_class"] = source_player.class_slug

        self.resurrects.append(data)

    def process_event(self, event: "wcl.ReportEvent") -> wcl.ReportEvent:
        # Ankh doesn't shows as a regular spell
        spell_id = event.abilityGameID
        if spell_id in (21169,):  # Ankh
            event.type = "resurrect"

        if event.type == "resurrect":
            self.process_event_resurrect(event)
            event.abilityGameID = -1

        return super().process_event(event)

    def process_events(self, events: list[wcl.ReportEvent]) -> list[wcl.ReportEvent]:
        if self.spec_slug != DANCER_SPEC_SLUG:
            return super().process_events(events)

        fight_start = self.fight.start_time_rel if self.fight else 0
        partners_by_source_id: dict[int, dict[str, typing.Any]] = {}
        for event in events:
            spell_id = event.abilityGameID
            is_closed_position = event.type == "cast" and spell_id == DANCE_PARTNER_CAST_ID
            is_partner_aura = event.type in ("applybuff", "removebuff") and spell_id in DANCE_PARTNER_AURA_IDS
            if not is_closed_position and not is_partner_aura:
                continue

            target_id = event.targetID
            if target_id <= 0 or target_id == self.source_id:
                continue

            timestamp = max(0, event.timestamp - fight_start)
            partner = partners_by_source_id.setdefault(
                target_id,
                {
                    "source_id": target_id,
                    "first_ts": timestamp,
                    "last_ts": timestamp,
                    "event_count": 0,
                },
            )
            partner["first_ts"] = min(partner["first_ts"], timestamp)
            partner["last_ts"] = max(partner["last_ts"], timestamp)
            partner["event_count"] += 1

        self.dance_partners = sorted(partners_by_source_id.values(), key=lambda partner: partner["first_ts"])
        return super().process_events(events)

    def should_include_cast_event(self, event: "wcl.ReportEvent", cast_actor_id: int) -> bool:
        if event.type == "cast" and is_limit_break_spell_id(event.abilityGameID):
            return True
        return super().should_include_cast_event(event, cast_actor_id)
