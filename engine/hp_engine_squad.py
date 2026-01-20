from dataclasses import dataclass
from typing import List, Dict

@dataclass
class PlayerProfile:
    id: str
    name: str
    strengths: List[str]
    vulnerabilities: List[str]
    counter_weights: List[str]

PLAYER_PROFILES = {
    "GK_SWEEPER": PlayerProfile(
        id="GK_SWEEPER", name="Sweeper-Keeper",
        strengths=["High line", "Distribution", "Sweeping"],
        vulnerabilities=["1v1 stopping"],
        counter_weights=["CB_PACE_DEFENDER", "DM_ANCHOR"]
    ),
    "ST_FALSE_NINE": PlayerProfile(
        id="ST_FALSE_NINE", name="False 9",
        strengths=["Space creation", "Link-up"],
        vulnerabilities=["Goal volume"],
        counter_weights=["W_INSIDE_FORWARD", "CM_BOX_TO_BOX"]
    ),
    # Diğer tüm profiller kümülatif olarak buraya mühürlenir.
}
