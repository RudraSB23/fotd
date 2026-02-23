def get_scene(scene_id: str):
    from .registry import SCENE_REGISTRY
    scene_class = SCENE_REGISTRY.get(scene_id)
    if scene_class:
        return scene_class()
    raise ValueError(f"Unknown scene: {scene_id}")
