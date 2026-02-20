from pathlib import Path
from typing import Optional, List

BASE_DIR = Path(__file__).resolve().parent.parent
ASCII_DIR = BASE_DIR / "assets" / "ascii_art"


def load_ascii_art(filename: str) -> Optional[str]:
    """
    Load a single ASCII art file from the ascii_art directory.
    Returns file content or None if missing/unreadable.
    """
    path = ASCII_DIR / filename
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, OSError):
        print(f"[WARN] Could not load {filename}")
        return None


def load_multiple_ascii_art(filenames: List[str]) -> List[str]:
    """
    Load multiple ASCII art files from the ascii_art directory.
    Returns a list of file contents. Skips missing/unreadable files.
    """
    arts = []
    for filename in filenames:
        content = load_ascii_art(filename)
        if content is not None:
            arts.append(content)
    return arts


