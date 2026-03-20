from .node0x1 import Scene1Corridor
from .node0x2 import Scene2Ava
from .node0x3 import Scene3Archive
from .node0x4 import Scene4Elias
from .node0x7 import Scene7Lyra
from .node0x9 import Scene9Ending

SCENE_REGISTRY = {
    "scene1_identity_sequence": Scene1Corridor,
    "node0x2_ava_intro": Scene2Ava,
    "node0x3_archive": Scene3Archive,
    "node0x4_elias": Scene4Elias,
    "node0x7_lyra": Scene7Lyra,
    "node0x9_ending": Scene9Ending
}

SCENE_NAMES = {
    "scene1_identity_sequence": "Awakening",
    "node0x2_ava_intro": "Ava",
    "node0x3_archive": "The Archive",
    "node0x4_elias": "Elias The Cynic",
    "node0x7_lyra": "Lyra The Observer",
    "node0x9_ending": "The Threshold",
}

def get_scene(scene_id: str):
    scene_class = SCENE_REGISTRY.get(scene_id)
    if scene_class:
        return scene_class()
    raise ValueError(f"Unknown scene: {scene_id}")

def get_scene_name(scene_id: str) -> str:
    return SCENE_NAMES.get(scene_id, f"Unknown Node: {scene_id}")
