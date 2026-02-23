from .node0x1 import Scene1Corridor
from .node0x2 import Scene2Ava

SCENE_REGISTRY = {
    "scene1_identity_sequence": Scene1Corridor,
    "node0x2_ava_intro": Scene2Ava,
    # Add future scenes here
}

def get_scene(scene_id: str):
    scene_class = SCENE_REGISTRY.get(scene_id)
    if scene_class:
        return scene_class()
    raise ValueError(f"Unknown scene: {scene_id}")
