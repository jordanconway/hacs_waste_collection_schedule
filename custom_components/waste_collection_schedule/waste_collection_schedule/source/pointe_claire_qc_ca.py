import re
from typing import Literal

from waste_collection_schedule import Collection  # type: ignore[attr-defined]
from waste_collection_schedule.exceptions import SourceArgumentNotFoundWithSuggestions
from waste_collection_schedule.service.ICS import ICS

TITLE = "Pointe-Claire (QC)"
DESCRIPTION = "Source for Pointe-Claire, Québec waste collection schedules."
URL = "https://www.pointe-claire.ca"
TEST_CASES = {
    "Sector A": {"sector": "A"},
    "Sector B": {"sector": "B"},
}

ICON_MAP = {
    "Organic Waste": "mdi:compost",
    "Recyclables": "mdi:recycle",
    "Household Waste": "mdi:trash-can",
    "Bulky Items": "mdi:sofa",
    "Christmas Tree Collection": "mdi:pine-tree",
}

HOW_TO_GET_ARGUMENTS_DESCRIPTION = {
    "en": "Find your collection sector on the City of Pointe-Claire website at https://www.pointe-claire.ca/en/residents/public-works/waste-management/",
    "fr": "Trouvez votre secteur de collecte sur le site de la Ville de Pointe-Claire à https://www.pointe-claire.ca/residents/travaux-publics/gestion-des-dechets/",
}

PARAM_DESCRIPTIONS = {
    "en": {
        "sector": "Collection sector (A or B)",
    },
    "fr": {
        "sector": "Secteur de collecte (A ou B)",
    },
}

PARAM_TRANSLATIONS = {
    "en": {
        "sector": "Sector",
    },
    "fr": {
        "sector": "Secteur",
    },
}

ICS_SECTOR_A = """\
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Pointe-Claire//Waste Collection Sector A//EN
X-WR-CALNAME:Pointe-Claire Sector A Collection 2026-2027
BEGIN:VEVENT
SUMMARY:Organic Waste (Sector A)
RRULE:FREQ=WEEKLY;BYDAY=MO;UNTIL=20270329T000000Z
DTSTART:20260406T070000
DURATION:PT1H
DESCRIPTION:Matières organiques collection.
END:VEVENT
BEGIN:VEVENT
SUMMARY:Recyclables (Sector A)
RRULE:FREQ=WEEKLY;BYDAY=WE;UNTIL=20270331T000000Z
DTSTART:20260401T070000
DURATION:PT1H
DESCRIPTION:Matières recyclables collection.
END:VEVENT
BEGIN:VEVENT
SUMMARY:Household Waste (Sector A)
RRULE:FREQ=WEEKLY;INTERVAL=2;BYDAY=TU;UNTIL=20270323T000000Z
DTSTART:20260407T070000
DURATION:PT1H
DESCRIPTION:Déchets domestiques collection.
END:VEVENT
BEGIN:VEVENT
SUMMARY:Bulky Items (Sector A)
RRULE:FREQ=MONTHLY;BYDAY=1WE;UNTIL=20270303T000000Z
DTSTART:20260401T070000
DURATION:PT1H
DESCRIPTION:Encombrants collection.
END:VEVENT
BEGIN:VEVENT
SUMMARY:Christmas Tree Collection (Sector A)
DTSTART:20270107T070000
DURATION:PT1H
DESCRIPTION:Special collection for Christmas trees.
END:VEVENT
BEGIN:VEVENT
SUMMARY:Christmas Tree Collection (Sector A)
DTSTART:20270114T070000
DURATION:PT1H
DESCRIPTION:Special collection for Christmas trees.
END:VEVENT
END:VCALENDAR
"""

ICS_SECTOR_B = """\
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Pointe-Claire//Waste Collection Sector B//EN
X-WR-CALNAME:Pointe-Claire Sector B Collection 2026-2027
BEGIN:VEVENT
SUMMARY:Organic Waste (Sector B)
RRULE:FREQ=WEEKLY;BYDAY=MO;UNTIL=20270329T000000Z
DTSTART:20260406T070000
DURATION:PT1H
DESCRIPTION:Weekly organic waste collection.
END:VEVENT
BEGIN:VEVENT
SUMMARY:Recyclables (Sector B)
RRULE:FREQ=WEEKLY;BYDAY=WE;UNTIL=20270331T000000Z
DTSTART:20260401T070000
DURATION:PT1H
DESCRIPTION:Weekly recyclables collection.
END:VEVENT
BEGIN:VEVENT
SUMMARY:Household Waste (Sector B)
RRULE:FREQ=WEEKLY;INTERVAL=2;BYDAY=TH;UNTIL=20270325T000000Z
DTSTART:20260409T070000
DURATION:PT1H
DESCRIPTION:Bi-weekly household waste collection.
END:VEVENT
BEGIN:VEVENT
SUMMARY:Bulky Items (Sector B)
RRULE:FREQ=MONTHLY;BYDAY=1WE;UNTIL=20270303T000000Z
DTSTART:20260401T070000
DURATION:PT1H
DESCRIPTION:Monthly bulky item collection.
END:VEVENT
BEGIN:VEVENT
SUMMARY:Christmas Tree Collection
DTSTART:20270106T070000
DURATION:PT1H
DESCRIPTION:Special collection for Christmas trees.
END:VEVENT
BEGIN:VEVENT
SUMMARY:Christmas Tree Collection
DTSTART:20270113T070000
DURATION:PT1H
DESCRIPTION:Special collection for Christmas trees.
END:VEVENT
END:VCALENDAR
"""

SECTOR_ICS_MAP: dict[str, str] = {
    "A": ICS_SECTOR_A,
    "B": ICS_SECTOR_B,
}

SECTOR_LITERAL = Literal["A", "B"]


class Source:
    def __init__(self, sector: SECTOR_LITERAL):
        self._sector = str(sector).upper().strip()
        self._ics = ICS()

    def fetch(self) -> list[Collection]:
        ics_data = SECTOR_ICS_MAP.get(self._sector)
        if ics_data is None:
            raise SourceArgumentNotFoundWithSuggestions(
                "sector", self._sector, list(SECTOR_ICS_MAP.keys())
            )

        dates = self._ics.convert(ics_data)
        entries = []
        for d in dates:
            # Strip " (Sector A)" / " (Sector B)" suffix for icon lookup
            icon_key = re.sub(r"\s*\(Sector [AB]\)$", "", d[1]).strip()
            entries.append(Collection(d[0], d[1], ICON_MAP.get(icon_key)))
        return entries
