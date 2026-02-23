# Fragments of the Lattice – Production Audit

_Comprehensive professional audit focused on code architecture, systems design, narrative integration, UX, and production readiness._

---

## 1. Critical Improvements (High Impact)

### 1.1 Break Up `dialogue.py` (Monolithic Narrative File)

**Problem**

- `dialogue.py` is a large, monolithic file (~35KB) containing:
  - Scene logic
  - Flow control
  - Narrative content
- All scenes for nodes (0x1, 0x2, future nodes) live in one file.
- Hard to navigate, test, or safely extend as new nodes are added.

**Impact**

- Severely limits scalability as you implement Nodes 0x3–0x9.
- Increases risk of merge conflicts and regressions.
- Encourages copy-paste and inconsistent patterns.

**Recommendation**

Refactor into a **scene-based module structure**:

```bash
scenes/
  ├── __init__.py
  ├── base_scene.py
  ├── node_0x1_corridor.py
  ├── node_0x2_ava.py
  ├── node_0x3_archive.py   # future
  └── ...
```

Example pattern:

```python
# scenes/base_scene.py
from abc import ABC, abstractmethod

class BaseScene(ABC):
    @abstractmethod
    def run(self, stdscr, game_state):
        ...

# scenes/node_0x2_ava.py
from .base_scene import BaseScene

class Scene0x2Ava(BaseScene):
    def run(self, stdscr, game_state):
        # Ava intro & puzzle tutorial here
        ...
```

**Benefits**

- Clear ownership: one scene per file.
- Easier testing and refactoring.
- Enables a registry of scenes for save/load instead of `getattr(dialogue, ...)`.

---

### 1.2 Strengthen `GameState` and Effects Model

**Problem**

- `GameState` is a simple dataclass with:
  - `stability`, `corruption_level`, `identity_fragments`, `npc_relationships` etc. [cite:7]
- `apply_effect()` uses string parsing like `"stability+2"`, `"fragment:AvaMemory"` [cite:7][cite:6].
- No clamping, validation, or unified constraints.
- No history or change tracking.

**Impact**

- Easy to introduce typos (`"stabilty+2"`) that silently fail.
- No guardrails on values (corruption can go arbitrarily high).
- Hard to reason about balancing or debug progression.

**Recommendation**

Move towards a more structured effect system:

```python
from dataclasses import dataclass, field, asdict
from typing import Dict, List
import time

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

@dataclass
class GameState:
    player_name: str = "Unknown"
    identity_fragments: List[str] = field(default_factory=list)
    corruption_level: int = 0
    stability: int = 3
    npc_relationships: Dict[str, int] = field(default_factory=dict)
    current_node_id: str = "intro"
    history: List[Dict] = field(default_factory=list)

    def apply_stability(self, delta: int):
        old = self.stability
        self.stability = clamp(self.stability + delta, 0, 10)
        self.history.append({
            "type": "stability",
            "delta": delta,
            "old": old,
            "new": self.stability,
            "t": time.time(),
        })

    def apply_corruption(self, delta: int):
        old = self.corruption_level
        self.corruption_level = clamp(self.corruption_level + delta, 0, 10)
        self.history.append({
            "type": "corruption",
            "delta": delta,
            "old": old,
            "new": self.corruption_level,
            "t": time.time(),
        })

    def add_fragment(self, frag: str):
        if frag not in self.identity_fragments:
            self.identity_fragments.append(frag)
            self.history.append({
                "type": "fragment",
                "value": frag,
                "t": time.time(),
            })

    def relationship_delta(self, npc: str, delta: int):
        self.npc_relationships[npc] = self.npc_relationships.get(npc, 0) + delta

    def snapshot(self) -> Dict:
        return asdict(self)
```

You can keep `apply_effect()` as a thin legacy wrapper that forwards to these new methods.

**Benefits**

- Type-safe stat changes.
- Centralized clamping and constraints.
- History log can be used for debugging, analytics, or “replay” features.

---

### 1.3 Make Save System Versioned and Robust

**Problem**

- Saves are stored in `saves.json` with a single slot [cite:3].
- Restoration uses `getattr(dialogue, scene_name)` to find a function by name [cite:5][cite:6].
- No versioning or schema handling.
- No integrity checks.

**Impact**

- Any refactor of scene names breaks all existing saves.
- Schema changes to `GameState` risk corrupt or incompatible saves.
- No support for multiple save slots.

**Recommendation**

Introduce a versioned, multi-slot save system:

```python
SAVE_VERSION = "1.0.0"

def hash_state(state_dict: Dict) -> str:
    import hashlib, json
    raw = json.dumps(state_dict, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

class SaveManager:
    @staticmethod
    def save_game(game_state, scene_id: str, slot: int = 1):
        data = {
            "version": SAVE_VERSION,
            "timestamp": time.time(),
            "scene_id": scene_id,
            "state": game_state.snapshot(),
        }
        data["checksum"] = hash_state(data["state"])
        with open(f"saves/slot_{slot}.json", "w") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def load_game(slot: int = 1):
        # Load file, validate version & checksum, handle gracefully if mismatch
        ...
```

Also move from `getattr(dialogue, scene_name)` to a **scene registry** keyed by `scene_id`:

```python
# scenes/__init__.py
SCENE_REGISTRY = {
    "scene1_identity_sequence": Scene1Identity,
    "node0x2_ava_intro": Scene0x2Ava,
    # ...
}

def load_scene(scene_id: str) -> BaseScene:
    return SCENE_REGISTRY[scene_id]()
```

**Benefits**

- Safe refactors: scene implementation can change without breaking saves.
- Forward-compatible with future versions.
- Multiple save slots for production-level UX.

---

### 1.4 Normalize Input Handling and Flush Behavior

**Problem**

- `print_typing()` uses `stdscr.nodelay(True)` and checks `getch()` to allow skipping [cite:9].
- Input buffer isn’t consistently flushed before menus or puzzles.
- Rapid key presses during text output can bleed into the next interaction.

**Impact**

- Players spamming Enter/Space to skip text can accidentally trigger menu selections or puzzle input.

**Recommendation**

Create a centralized helper:

```python
def flush_input(stdscr):
    stdscr.nodelay(True)
    try:
        while stdscr.getch() != -1:
            pass
    except:
        pass
    stdscr.nodelay(False)
    curses.flushinp()
```

Use this:

- After any long typing/glitch segment.
- Right before any `ChoiceMenu.display()` or `TimedPuzzle.display()`.

**Benefits**

- Predictable, consistent input handling.
- Less “ghost input” frustration.

---

### 1.5 Add Error Handling and Logging

**Problem**

- Very minimal error handling.
- `curses.error` is swallowed in multiple places [cite:9].
- No global logging; crashes are opaque to the player and developer.

**Impact**

- Difficult to debug player issues.
- Terminal may be left in a bad state on crashes.
- Audio or file I/O failures give no meaningful feedback.

**Recommendation**

1. **Add Logging**

```python
import logging

logging.basicConfig(
    filename="fotd_debug.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
```

Use `logging.info/error/exception()` throughout:

- Save/load operations.
- Scene transitions.
- Audio failures.

2. **Wrap Main Entry Point**

```python
if __name__ == "__main__":
    try:
        if config.TEST:
            config.SKIP_STARTUP = True
        if not config.SKIP_STARTUP:
            startup_screen(15)
            time.sleep(2)
        curses.wrapper(main_curses)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.exception("Fatal error in main loop")
        try:
            os.system("reset" if os.name != "nt" else "cls")
        except:
            pass
        print("The Lattice crashed. See fotd_debug.log for details.")
```

**Benefits**

- Recoverable crashes.
- Inspectable error history.
- More professional production behavior.

---

## 2. Structural Refactors

### 2.1 Improve AudioManager Feedback and Caching

**Current State**

- AudioManager preloads sounds/music in a background thread and can block until loading is finished [cite:4][cite:5].
- The game may sit waiting with no clear feedback to the user.
- Potential for redundant loads or lack of cache strategy (depending on `audio.py` behavior).

**Refactor Goals**

- Visual feedback when audio assets are still loading.
- Clear caching and reuse semantics.

**Example Extension**

```python
def wait_for_assets(self, stdscr=None):
    if stdscr:
        while not self.is_loading_finished():
            progress = self.loaded_count / max(1, self.total_assets)
            render_progress_bar(stdscr, progress, "Loading Audio...")
            time.sleep(0.05)
    else:
        while not self.is_loading_finished():
            time.sleep(0.1)
```

**Benefits**

- Better perceived performance.
- More explicit load behavior.

---

### 2.2 Unify Console Rendering / Text Effects

**Current State**

- Multiple text helpers: `print_colored`, `print_typing`, `print_glitch`, `echo_line`, `print_centered` [cite:9].
- Each function takes slightly different parameters, with different assumptions.
- Shared logic is duplicated (color mapping, sound playback).

**Refactor Direction**

Introduce a `TextStyle` + `TextRenderer` abstraction:

```python
@dataclass
class TextStyle:
    color: str = Colors.RESET
    typing_speed: float = 0.0      # 0 => instant
    glitch_intensity: float = 0.0  # 0 => none
    play_sound: bool = False

class TextRenderer:
    def __init__(self):
        self.curses_colors = CursesColors()

    def render(self, stdscr, text: str, style: TextStyle, y=None, x=None):
        # Delegate to typing / glitch / static based on style
        ...
```

You can keep compatibility wrappers:

```python
def print_typing(...):
    style = TextStyle(color=color, typing_speed=seconds_per_char, glitch_intensity=0.0)
    renderer.render(stdscr, text, style, y, x)
```

**Benefits**

- Centralized rendering behavior.
- Easy to adjust global behavior (e.g., “accessibility: disable glitch”).

---

### 2.3 Clean Up UI Element Interfaces

**Current State**

- `ChoiceMenu`, `MessageBox`, `TimedPuzzle` each manage both:
  - Layout and rendering.
  - Input handling and control flow. [cite:8]
- APIs are inconsistent (`display(stdscr)` vs combined rendering/input loop).

**Refactor Direction**

Define a generic `UIElement` interface:

```python
class UIElement:
    def render(self, stdscr):
        raise NotImplementedError

    def handle_input(self, key):
        raise NotImplementedError

    def is_complete(self) -> bool:
        return False
```

Example usage in a main loop:

```python
element = ChoiceMenu(...)
while not element.is_complete():
    element.render(stdscr)
    key = stdscr.getch()
    element.handle_input(key)

selection = element.result
```

**Benefits**

- Easier to reason about each UI element.
- Elements can be reused or combined in composite screens.
- Possible to simulate inputs for automated tests.

---

### 2.4 Configuration Management

**Current State**

- `engine/config.py` appears minimal; `config.TEST` and `config.SKIP_STARTUP` are used to control flow [cite:5][cite:6].
- No persistent settings for:
  - Typing speed.
  - Audio volume.
  - Glitch intensity.
  - Accessibility.

**Refactor Direction**

Introduce `config.json`:

```json
{
  "debug": {
    "test_mode": false,
    "skip_startup": false
  },
  "display": {
    "typing_speed": 0.03,
    "glitch_intensity": 0.15
  },
  "audio": {
    "master_volume": 0.8,
    "music_volume": 0.5,
    "sfx_volume": 0.9
  },
  "accessibility": {
    "skip_animations": false,
    "high_contrast": false
  }
}
```

Add loader:

```python
class Config:
    @classmethod
    def load(cls, path="config.json"):
        with open(path) as f:
            data = json.load(f)
        # Set class variables from dict with defaults
        ...
```

**Benefits**

- Player personalization.
- Quick tuning for testing or streaming.
- Simple path to options menu in-game.

---

## 3. Design Enhancements

### 3.1 Make Corruption Mechanically Meaningful

**Current State**

- Corruption affects:
  - Choice menu arrow glitching at high corruption [cite:8].
  - Certain narrative branches and future ending thresholds [cite:6][cite:10].
- Mostly a narrative and cosmetic stat.

**Design Goal**

Corruption should **change how the game feels and behaves**, not just the end state.

**Proposed Corruption Tiers**

- **1–2 (Minor Static)**
  - Occasional cosmetic text glitches.
- **3–4 (Cognitive Drift)**
  - Small chance of menus shuffling options.
- **5–6 (Echo Intrusion)**
  - Echo interjects in choices, overriding text or adding extra options.
- **7–8 (Command Corruption)**
  - Low chance that typed input is altered (e.g., last character flipped).
- **9–10 (Glitch Mode)**
  - Periodic full-screen glitch events; some input “ignored” or delayed.

**Example Injection**

```python
def maybe_echo_interrupt(stdscr, game_state):
    if game_state.corruption_level >= 5 and random.random() < 0.2:
        echo_line("...you're not steering this anymore...", stdscr=stdscr)
```

**Benefits**

- Stronger feedback loop: “I chose corruption” actually feels different moment-to-moment.
- Emphasizes horror / loss of control theme.

---

### 3.2 Reward High Stability with Perks

**Current State**

- Stability mostly gates future content/endings [cite:7][cite:10].
- Immediate moment-to-moment benefits are limited.

**Proposed Stability Tiers**

- **≥4:** Bonus time on puzzles (+2 seconds).
- **≥6:** Unlock “Memory Echo” – ability to replay last choice in certain nodes.
- **≥8:** Reveal hidden dialogue options (e.g., calling out contradictions in fragments).

**Implementation Hooks**

- When constructing `TimedPuzzle`, adjust `time_limit` based on stability.
- Before displaying `ChoiceMenu`, if stability high enough, append extra option.

```python
if game_state.stability >= 6:
    choices.append("[Reconstruct previous state]")
```

**Benefits**

- Encourages varied builds/playstyles.
- Balances corruption path with a tangible “order” path.

---

### 3.3 Deepen Choice Consequences

**Current State**

- Most choices are: `stability+1` / `corruption+1` / add fragment [cite:6][cite:1].
- `npc_relationships` exists but is underused [cite:7].

**Enhancements**

- Use `npc_relationships` to track attitudes:
  - Ava: trustful vs distrustful.
  - Future characters: Elias, Lyra (as per `INTERACTIONS.md`) [cite:1].
- Gate future assistance or sabotage based on these values.

**Example**

- If Ava relationship ≥ 3:
  - She warns before a hard puzzle: “This one feels wrong. Be ready.”
- If Ava relationship ≤ -2:
  - She withholds help or misleads: “No, don’t worry. It’s stable enough.”

**Benefits**

- Choices feel persistent, not one-off.
- Encourages replays with different role-play approaches (cold Architect vs empathetic Caretaker).

---

### 3.4 Add Puzzle Variety

**Current State**

- One main puzzle type: timed typing of a target word from a scrambled version via `TimedPuzzle` [cite:8][cite:6].

**Additional Puzzle Types**

1. **Memory Sequence Puzzle**
   - Show a short sequence of corrupted strings.
   - Player must reproduce them in correct order.

2. **Node Alignment Puzzle**
   - ASCII “fragments” appear out of place; player must select correct ordering.

3. **Binary Choice Timer**
   - High-pressure “yes/no” or “stabilize/delete” within short time window.

4. **Simple Cipher Puzzle**
   - Short strings encoded; player must deduce mapping based on hints from fragments.

**Benefits**

- Reduces monotony.
- Lets you tie puzzle type to narrative context (e.g., librarianship puzzles for Ava, logic puzzles for Architect nodes).

---

## 4. Narrative Improvements

### 4.1 Improve Early Pacing and Hook

**Observation**

- Boot and onboarding are strong atmosphere-wise [cite:6][cite:1][cite:2].
- Nodes 0x1 and 0x2 are mostly setup + tutorial; tension builds slowly.
- No early glimpse of the stakes / climax.

**Enhancement**

Add a short **flash-forward** in the opening sequence:

- Show a corrupted scene where the player confronts their own reflection.
- The Echo speaks as if the ending already happened.
- Then snap back with a “Rewinding…” message.

This can be integrated into `fake_error_flood()` or immediately after initial boot [cite:6].

**Benefits**

- Clarifies stakes early.
- Gives players a narrative “mystery” to chase.

---

### 4.2 Evolve the Echo’s Voice Over Time

**Current State**

- Echo lines are high-quality but tonally similar across scenes [cite:6][cite:2][cite:1].
- The Echo’s arc (from cryptic to intimate) is established in lore but not fully realized in current gameplay.

**Design**

Define Echo phases:

1. **Distant (Node 0x1)**
   - Vague, glitchy: “...Who... are you?...”
2. **Confrontational (Mid Nodes)**
   - Direct accusations: “You built this prison.”
3. **Entangled (Late Nodes)**
   - Intimate, almost collaborative: “We’ve always been the same process.”

Tag Echo lines with phases and choose based on node index and corruption.

**Benefits**

- Reinforces story of self-confrontation.
- Makes the Echo feel like a character, not just a gimmick.

---

### 4.3 Give Ava Stronger Goals and Agency

**Current State**

- Ava introduces the stabilization mechanic and offers exposition [cite:6][cite:1].
- Her personal goals and stakes are only lightly implied.

**Enhancement**

Establish Ava’s explicit desires:

- Wants to restore her full memory (not just remain a fragment).
- Fears being “recycled” by the Architect.
- Asks the player to help preserve certain logs even if it costs stability.

Branching:

- Help Ava (preserve her memories) → boosts relationship, but may increase corruption or risk instability.
- Sacrifice Ava (for stability) → more stable nodes, but she may return later as corrupted opposition.

**Benefits**

- Stronger emotional investment.
- Concretely ties “morality of repair” theme into choices.

---

### 4.4 Integrate Lore Diegetically

**Current State**

- `lore.md` contains excellent meta-story (Caretaker/Architect/Echo twist) [cite:2].
- Most of it is not surfaced in current nodes 0x1–0x2.
- Future nodes are outlined in `INTERACTIONS.md` but not yet in code [cite:1].

**Enhancement**

- Introduce “Archive Logs” as collectibles:
  - Each node can hide 1–3 optional logs.
  - Logs are short excerpts from `lore.md` style text.
- Tie logs to:
  - High stability (clean access).
  - High corruption (unreliable or altered logs).

**Benefits**

- Players discover lore through play.
- Encourages exploration and replay.

---

## 5. Quick Wins

### 5.1 Add Pause Menu

**Why**

- Currently no in-game way to:
  - View stats.
  - Save on demand (beyond scripted saves).
  - Adjust settings.

**Implementation Sketch**

```python
def pause_menu(stdscr, game_state: GameState):
    options = [
        "Resume",
        f"Stability: {game_state.stability}",
        f"Corruption: {game_state.corruption_level}",
        "Save Game",
        "Quit to Title"
    ]
    menu = ChoiceMenu("PAUSED", options, corruption=game_state.corruption_level)
    choice = menu.display(stdscr)
    # Process choice 0..4
```

Trigger on ESC in main loops or scenes.

---

### 5.2 Add Global “Skip Animation” Hotkey

**Why**

- Typing and glitch effects are great the first time, but repeated playthroughs benefit from skipping.

**Implementation**

- In `print_typing()` and `echo_line()`, already using `stdscr.getch()` [cite:9].
- Add detection of a global skip key (e.g., `s` or Space).

```python
if key in [10, 13, 32, ord('s')]:
    skip = True
```

- Make this behavior configurable via `config.json` (`skip_animations`).

---

### 5.3 Basic Colorblind / High-Contrast Mode

**Why**

- Color is heavily used for meaning (red = danger, green = success, etc.) [cite:6][cite:9].
- Some players may struggle distinguishing.

**Implementation**

- At startup, if `Config.accessibility.high_contrast` is true:
  - Remap critical colors to bold white / high-contrast pairs.

```python
if Config.accessibility.high_contrast:
    Colors.RED = Colors.BOLD_WHITE
    Colors.GREEN = Colors.BOLD_YELLOW
    Colors.MAGENTA = Colors.BOLD_WHITE
```

- Ensure reliance on **text labels and icons** as well, not just color.

---

### 5.4 Add Session Stats / Minimal Achievements

**Why**

- Simple metrics add replay motivation:
  - Nodes visited.
  - Puzzles solved vs. failed.
  - Fragments collected.
  - Endings unlocked.

**Implementation**

- Extend `GameState` with counters (`puzzles_solved`, `puzzles_failed`, `nodes_visited`) and update them in relevant functions.
- Show a summary at the end-of-demo / ending screen.

---

### 5.5 Terminal Size Check

**Why**

- ASCII art and frames assume a minimum dimension [cite:9][cite:10].
- Small terminals can cause truncated or broken renders.

**Implementation**

```python
def ensure_min_terminal(stdscr, min_h=30, min_w=100):
    h, w = stdscr.getmaxyx()
    if h < min_h or w < min_w:
        msg = f"Terminal too small ({w}x{h}). Please resize to at least {min_w}x{min_h}."
        print_colored(msg, Colors.BOLD_RED, stdscr=stdscr)
        stdscr.getch()
        sys.exit(1)
```

Call once at the start of `run_game()`.
