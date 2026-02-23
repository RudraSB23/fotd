# engine/state_manager.py - COMPLETE REPLACEMENT
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional
import time
import json

def clamp(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, value))

@dataclass
class GameState:
    player_name: str = "Caretaker"
    identity_fragments: List[str] = field(default_factory=list)
    corruption_level: int = 0
    stability: int = 3
    npc_relationships: Dict[str, int] = field(default_factory=dict)
    current_node_id: str = "intro"
    history: List[Dict] = field(default_factory=list)
    puzzles_solved: int = 0
    puzzles_failed: int = 0
    nodes_visited: int = 0
    playtime_seconds: float = 0.0

    # STAT MANIPULATION - Type Safe
    def apply_stability(self, delta: int) -> None:
        old = self.stability
        self.stability = clamp(self.stability + delta, 0, 10)
        self.history.append({
            "type": "stability",
            "delta": delta,
            "old": old,
            "new": self.stability,
            "timestamp": time.time()
        })

    def apply_corruption(self, delta: int) -> None:
        old = self.corruption_level
        self.corruption_level = clamp(self.corruption_level + delta, 0, 10)
        self.history.append({
            "type": "corruption",
            "delta": delta,
            "old": old,
            "new": self.corruption_level,
            "timestamp": time.time()
        })

    def add_fragment(self, fragment_id: str) -> bool:
        if fragment_id not in self.identity_fragments:
            self.identity_fragments.append(fragment_id)
            self.history.append({
                "type": "fragment",
                "fragment_id": fragment_id,
                "timestamp": time.time()
            })
            return True
        return False

    def relationship_delta(self, npc: str, delta: int) -> None:
        self.npc_relationships[npc] = self.npc_relationships.get(npc, 0) + delta

    # UTILITY
    def snapshot(self) -> Dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.snapshot())

    @classmethod
    def from_snapshot(cls, data: Dict):
        return cls(**data)

    def get_ending(self) -> str:
        if self.corruption_level >= 8:
            return "collapse"
        elif self.stability >= 8:
            return "restoration"
        elif 3 <= self.corruption_level < 6 and 3 <= self.stability < 6:
            return "integration"
        return "undetermined"

    # TEMPORARY - for existing dialogue.py calls
    def apply_effect(self, effect_str: str) -> None:
        if effect_str.startswith("stability+"):
            try:
                self.apply_stability(int(effect_str.split("+")[1]))
            except (IndexError, ValueError):
                pass
        elif effect_str.startswith("stability-"):
            try:
                self.apply_stability(-int(effect_str.split("-")[1]))
            except (IndexError, ValueError):
                pass
        elif effect_str.startswith("corruption+"):
            try:
                self.apply_corruption(int(effect_str.split("+")[1]))
            except (IndexError, ValueError):
                pass
        elif effect_str.startswith("corruption-"):
            try:
                self.apply_corruption(-int(effect_str.split("-")[1]))
            except (IndexError, ValueError):
                pass
        elif effect_str.startswith("fragment:"):
            try:
                self.add_fragment(effect_str.split(":", 1)[1])
            except IndexError:
                pass
