from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class GameState:
    player_name: str = "Unknown"
    identity_fragments: List[str] = field(default_factory=list)
    corruption_level: int = 0
    stability: int = 3
    npc_relationships: Dict[str, int] = field(default_factory=dict)
    current_node_id: str = "intro"

    def apply_effect(self, effect: str) -> None:
        if effect.startswith("stability+"):
            amount = int(effect.split("+")[-1])
            self.stability += amount
        elif effect.startswith("stability-"):
            amount = int(effect.split("-")[-1])
            self.stability -= amount
        elif effect.startswith("corruption+"):
            amount = int(effect.split("+")[-1])
            self.corruption_level += amount
        elif effect.startswith("corruption-"):
            amount = int(effect.split("-")[-1])
            self.corruption_level -= amount
        elif effect.startswith("fragment:"):
            frag = effect.split(":", 1)[1]
            if frag not in self.identity_fragments:
                self.identity_fragments.append(frag)

    def relationship_delta(self, npc: str, delta: int) -> None:
        self.npc_relationships[npc] = self.npc_relationships.get(npc, 0) + delta

    def ending(self) -> str:
        if self.corruption_level >= 5:
            return "collapse"
        if self.stability >= 6:
            return "restoration"
        if 3 <= self.corruption_level <= 4 and 2 <= self.stability <= 4:
            return "merge"
        return "undetermined"


