# Fragments of the Lattice – Interaction & Choice Design Document

## Overview

Fragments of the Lattice is a terminal-driven narrative game structured as a sequence of **memory nodes** connected by a global state model tracking stability, corruption, collected fragments, and key decisions. This document enumerates **all currently implemented and all planned interactions**, including menus, prompts, branching choices, puzzles, and their effects on game state and narrative flow.[^1][^2]

Key interaction systems include:

- A global `GameState` object with stability, corruption, fragments, relationships, and derived endings.[^3]
- Scene classes (`Scene1Corridor`, `Scene2Ava`) and legacy dialogue functions that orchestrate node-level interactions.[^4][^1]
- UI primitives such as `GrubMenu`, `ChoiceMenu`, `TimedPuzzle`, and `MessageBox` that encapsulate player input and feedback.[^5][^6]

***

## Core Systems and State

### GameState and Endings

All interactions ultimately feed into a `GameState` dataclass that records:

- `stability` (default 3), representing the Caretaker’s grip on identity, clamped between 0 and 10.[^3]
- `corruption_level` (default 0), representing Echo / corruption influence, also clamped between 0 and 10.[^3]
- `identity_fragments` (list of strings), e.g. `"shard_001"`, collected via key narrative beats.[^1][^3]
- `puzzles_solved` and `puzzles_failed`, for tracking interaction proficiency.[^4][^3]
- `npc_relationships`, `nodes_visited`, and `playtime_seconds`, which are available for future systemic interactions and summaries.[^3]

The `get_ending()` helper derives a conceptual ending from final stability and corruption:[^2][^3]

- **Collapse**: `corruption_level >= 8`.
- **Restoration**: `stability >= 8`.
- **Integration**: both `stability` and `corruption_level` in the mid-range (between 3 and 5 inclusive on both axes).
- **Undetermined**: all other combinations.

These map directly onto the three narrative endings defined in `lore.md` and the Node 0x9 design in `INTERACTIONS.md` (Restoration Protocol, Collapse, Integration).[^2][^1]

### Interaction Primitives

Key UI and interaction components:

- **GrubMenu** – Title-screen style menu that renders a title ASCII art and options (e.g., `"Continue"`, `"New Game"`), navigated with arrow keys and confirmed with Enter.[^5][^4]
- **MessageBox** – Generic dialog frame that can show multi-line messages and optional choices, used for confirmations, system scans, and end summaries.[^7][^5]
- **ChoiceMenu** – In-node choice selector with an optional prompt string and a list of options; selection index is returned to the scene logic.[^6][^4]
- **TimedPuzzle** – Scrambled string typing mini-game with a visible timer; outcome (success/failure) modifies stability/corruption and puzzle counters.[^6][^4]

`ChoiceMenu` and `TimedPuzzle` are the primary building blocks for story-relevant decisions in the current prototype, while `GrubMenu` and `MessageBox` frame meta and systemic interactions.[^4][^6]

***

## Phase 0 – Title & Meta Interactions

### Title Screen – Main Menu

**Context:** Called from `run_game()` after startup visuals and audio initialization.[^4]

**UI / Audio:**

- Displays ASCII art title (`title.txt`) if available and plays `theme.mp3` in a loop.[^4]
- Renders a `GrubMenu` with two options: `"Continue"` and `"New Game"`.[^5][^4]

**Interaction:**

- Player navigates with ↑ / ↓ and confirms with Enter.[^5]

**Outcomes:**

1. **Continue**
   - Triggers a `MessageBox` titled `"SYSTEM SCAN"` with text like `"SEARCHING FOR LOCAL FRAGMENTS..."` while the game attempts to load save data from slot 1.[^7][^4]
   - If a save exists:
     - Reconstructs `GameState` via `GameState.from_snapshot()`.[^3][^4]
     - Displays a `"SYNC SUCCESS"` message summarizing subject name and last location.[^7][^4]
     - Proceeds into the scene loop starting from the saved `scene_id`.[^4]
   - If no save exists:
     - Displays a `"NODE FAILURE"` error box indicating no encrypted save data.[^7][^4]
     - Returns to the main menu loop (no branching consequence beyond UX).

2. **New Game**
   - Opens a confirmation `MessageBox` titled `"LINK ESTABLISHMENT"` with body text warning that this will overwrite volatile data and choices `"Continue"` and `"Cancel"`.[^7][^4]
   - **Continue**:
     - Deletes existing save via `SaveManager.delete_save()` and resets `game_state = GameState()`.[^3][^4]
     - Launches the full narrative onboarding pipeline (`onboarding`, `initiating_sequence`, `fake_error_flood`, `display_success_message`, `memory_load_prompt`, `corruption_flash`, `system_reboot`).[^1][^4]
   - **Cancel**:
     - Clears the terminal and returns to the main menu, effectively a non-commit interaction.[^4]

**State Impact:**

- `New Game → Continue` resets all state fields (`stability = 3`, `corruption = 0`, empty fragments) and then lets subsequent nodes shape them.[^3][^4]
- `Continue` resumes existing state without alteration beyond loading.[^3][^4]

***

## Phase 1 – Boot & Initialization (Nodes 0x01–0x03)

### Node 0x01 – Startup & Onboarding

**Narrative:** A black screen and blinking cursor establish the void; exposition introduces the Lattice, corruption, and the Caretaker role.[^1]

**Audio / Visual:**

- Background music transitions from `noname.mp3` to `melancholia.mp3` during the sequence.[^8][^1]
- Text is printed with typewriter effects, including emphasis (e.g., `ANYTHING` in red).[^1][^4]

**Interaction:**

- Ending line: `[INPUT REQUIRED] Initiate Lattice Core [Y/Y]:`.[^1][^4]
- Implementation accepts a single keypress via `stdscr.getch()`; there is **no branching** and no validation on the character.[^4]

**State Impact:**

- Purely atmospheric; no changes to `GameState` are made in this function.[^4]

### Node 0x02 – Initiating Sequence (Glitched)

**Narrative:** A boot log sequence describes system initialization steps such as loading memory nodes and stabilizing Echo channels.[^1][^4]

**Interaction:**

- `initiating_sequence()` prints a sequence of `[BOOT]` messages with timed ellipses; the player has no input.[^4]

**Glitched Error Flood:**

- `fake_error_flood()` simulates a corrupted dump:
  - Plays `scary_static.mp3` over scrolling console output.[^1][^4]
  - Mixes randomly selected `SYSTEM_MESSAGES`, glitched rendering, and a scripted ordering of `INITIATION_ECHO_MESSAGES` such as `"DO NOT PROCEED."` and `"THE LATTICE SEES YOU."`.[^1][^4]
  - Injects lines of random gibberish characters for noise.[^4]

**Player Interaction:**

- After the flood, the system prints `[ERR] A fatal error occured.` followed by `"> Press [Enter] to retry:"`.[^1][^4]
- Player must press Enter to advance; any other key is effectively ignored until Enter is received.[^4]

**State Impact:**

- No modification of `GameState`; the sequence is a prelude to real choices.[^3][^4]

### Node 0x03 – Memory Load & Reboot (Name Entry)

This node corresponds to `memory_load_prompt()` and `system_reboot()`.[^1][^4]

**Memory Load Prompt:**

- Displays `[INPUT REQUIRED] Load Memory: [Y/Y]` and waits for a single keypress via `stdscr.getch()`.[^1][^4]
- Like the earlier "Initiate" prompt, there is no branching based on the key; it is a ritualized acceptance.[^1][^4]

**System Reboot – Boot Logs:**

- Runs an animated `intro_systems_rebooting_bar()` progress bar, then prints boot logs:
  - `Identity: [UNRESOLVED]` in yellow/red.
  - `Location: Node-01 [UNRESOLVED]`.
  - `Stability: [███░░░] (3/6)` visualized via `render_stability_bar(game_state)`.[^3][^4][^1]

**World Description (Non-interactive):**

- Descriptive lines like `"You awaken in a dim corridor of fractured light."` are printed with glitch effects on the line mentioning glitches in the floor.[^4][^1]

**Name Input Interaction:**

- The Echo asks `"... Who... are you? ..."` and the prompt `"> "` appears in green.[^1][^4]
- `curses.echo()` and `curses.curs_set(1)` are enabled to allow visible text input; the player can type an arbitrary name and press Enter.[^4]

**Branch A – Non-empty Name:**

- If the input string has non-whitespace characters, it is used directly as `player_name`.[^4]
- No explicit stability/corruption changes occur here; the consequence is purely identity and downstream flavor.[^3][^4]

**Branch B – Empty Name:**

- If the trimmed name is empty, the following Echo dialogue plays:[^1][^4]
  - Ellipsis lines (`"..."`) repeated with pauses.
  - `"I see you are shy from telling me your name..."`
  - `"Are you hiding from yourself?"`
  - `"Oh well... looks like you gotta use your old name..."`
- The `player_name` is then forced to `"Caretaker"`.

**State Impact:**

- The chosen or default `player_name` is saved into `game_state.player_name` and will echo through later scenes (e.g., the corridor name flood).[^1][^4]
- Other state fields remain unchanged; this is an identity-only fork.

***

## Phase 2 – Node 0x1: The Corridor

Phase 2 covers the first fully interactive node where stability and corruption diverge based on player behavior.[^4][^1]

### Entry – Echo’s Wake

**Implementation:** `Scene1Corridor.run()`.[^4]

**Narrative Setup:**

- System acknowledges `"[SYS] Identity registered: {player_name}"` followed by `"[WARN] Memory integrity... FRAGMENTED"`.[^1][^4]
- A corridor description is printed, then the screen is flooded with `...{player_name}...` in red static hundreds of times while `scary_static.mp3` plays in a loop.[^1][^4]

**State Impact:**

- No direct stat change yet; emotional setup only.

### Interaction 1 – Explore vs Stand Still

**Prompt:**

- Text describes the corridor stretching endlessly and notes that "The air hums with fractured memory."[^4][^1]
- A `ChoiceMenu` is created with options:
  1. `"Explore the corridor"`
  2. `"Stand still"`[^6][^4]

#### Branch A – Explore the Corridor (Corruption Path)

**Function:** `Scene1Corridor.explore()`.[^4]

**Narrative:**

- The corridor extends infinitely; walls ripple like liquid glass, shards of broken code dangle like icicles, and reflections in the walls occasionally show "SOMEONE YOU MIGHT HAVE BEEN."[^1][^4]
- The Echo whispers increasingly possessive and destabilizing lines, e.g. `"Every step… closer to yourself… or to me…"` and `"Fragments... they are watching... Follow... or stop... there is no difference..."`.[^1][^4]

**State Changes:**

- Multiple `game_state.apply_effect` calls:
  - `corruption+1` from the first Echo line.[^3][^4]
  - Another `corruption+1` from the "Every step… closer" line.[^3][^4]
  - A `stability-1` after `[WARN] Stability decreasing... fragments detected.` indicating the mental toll.[^3][^4]
  - An additional `corruption+1` tied to the final Echo warning about fragments watching.[^3][^4]

**Net Impact:**

- **Stability:** −1.
- **Corruption:** +3 (values relative to entry into the branch).[^3][^4]

#### Branch B – Stand Still (Stability Path)

**Function:** `Scene1Corridor.stand_still()`.[^4]

**Narrative:**

- The player chooses stillness; the silence stretches and "the corridor holds its breath with you."[^1][^4]
- The Echo thanks the player (`"> Thank you... I need more time to reach you..."`), and a flicker of memory (not corruption) passes through the walls.[^4][^1]
- A fragment is detected: `"Fragment located... | identity shard detected..."`, followed by reassurance: `"...don’t forget... caretaker... you are still here..."`.[^1][^4]

**State Changes:**

- `stability+1` after the Echo’s gratitude line.[^3][^4]
- `fragment:shard_001` added to `identity_fragments` upon detection of the shard.[^3][^4]
- Another `stability+1` after the reassurance about still being here.[^3][^4]

**Net Impact:**

- **Stability:** +2.
- **Corruption:** 0.
- **Fragments:** gains `"shard_001"`.[^3][^4]

### Interaction 2 – Follow vs Resist the Pull

Regardless of the earlier choice, the scene proceeds to a second decision point.[^1][^4]

**Prompt:**

- After the first branch content resolves, a new `ChoiceMenu` is shown with options:
  1. `"Follow the guiding whispers"`
  2. `"Defy the pull and resist"`[^6][^4]

#### Branch C – Follow the Guiding Whispers

**Narrative:**

- Echo line: `"...yes... deeper... don’t turn back now..."`.[^4][^1]
- The corridor becomes a pulse rather than a place, and data overflow is implied.

**State Changes:**

- `corruption+2` to reflect surrendering to the Echo’s guidance.[^3][^4]
- In `part2(path="follow")`, an additional `corruption+1` is applied after `"...good... much better..."` and the data overflow message.[^3][^4]

**Net Impact (this decision):**

- **Corruption:** +3 from the follow choice and its continuation.[^3][^4]

#### Branch D – Defy the Pull and Resist

**Narrative:**

- Echo line: `"...no... don’t leave me here..."`, followed by the player planting their feet and refusing the whispers.[^1][^4]
- In `part2(path="resist")`, the walls hum with static protest, but stability holds.

**State Changes:**

- `stability+2` immediately on choosing to resist.[^4][^3]
- In `part2`, an additional `stability+1` is given after the message `"[#] STABILITY CHECK: Identity tether holding."`.[^3][^4]

**Net Impact (this decision):**

- **Stability:** +3 from the resist choice and follow-up.[^4][^3]

### Transition to Node 0x2

After `part2`, regardless of path, the scene:

- Prints `"<<< EXITING NODE 0x1 >>>"` and runs a `SYSTEMS REBOOTING` style bar via `intro_systems_rebooting_bar()`.[^1][^4]
- Clears the terminal and transfers control to Node 0x2 (`Scene2Ava`) by returning the scene ID `"node0x2_ava_intro"` in the scene-based implementation, or calling the legacy `node0x2_ava_intro()` function.[^1][^4]

**State at Exit:**

- Stability and corruption now meaningfully diverge depending on both decisions.
- Some routes also carry the `shard_001` fragment for later identity checks.[^3][^4]

***

## Phase 3 – Node 0x2: Fragment Alpha (Ava)

Node 0x2 is the first full **fragment encounter**, introducing Ava as a semi-coherent NPC with branching dialogue and a tutorial puzzle.[^4][^1]

### Encounter and Introduction

**Implementation:** `Scene2Ava.run()` (scene-based) and equivalent `node0x2_ava_intro()` (legacy dialogue).[^4]

**Narrative Setup:**

- A save point is created with ID `"node0x2_ava_intro"`.[^4]
- System prints `"<<< ENTERING NODE 0x2: FRAGMENT ALPHA >>>"` in green.[^1][^4]
- The corridor collapses into a small room; Ava appears as a figure of data shards.[^1][^4]
- Echo whispers `"...Ava?..."`, and Ava speaks: `"Is... is someone there? The Lattice... it feels so empty today."`.[^1]

### Interaction 3 – Initial Response to Ava

A `ChoiceMenu` is used to capture the player’s first reaction:[^6][^4]

1. `"I am here. I'm the Caretaker."`
2. `"You're just a fragment. Stay still."`
3. `"(Remain silent)"`

#### Option 1 – Affirm Caretaker Identity

**Narrative:**

- Ava responds: `"Caretaker? I remember that word. It sounded... safe. Once."`[^4][^1]

**State Changes:**

- `stability+1` to reflect grounding through relational connection.[^3][^4]
- `game_state.add_fragment("AvaMemory")` marking this encounter as a collected identity fragment.[^3][^4]

#### Option 2 – Dismiss as "Just a Fragment"

**Narrative:**

- Ava stutters: `"Fragment? I am... I was... I..."` and then compares the Caretaker to the Architect: `"You speak like the Architect. Cold. Calculating. But you're here. That means the nodes are failing, doesn't it?"`.[^1][^4]

**State Changes:**

- `corruption+1` – emotional damage and a colder stance towards fragments.[^3][^4]
- No fragment is added for this line; `AvaMemory` may still be added later depending on future content.

#### Option 3 – Remain Silent

**Narrative:**

- Ava calls out: `"Hello?"` and observes that only the hum of the walls answers.[^4][^1]
- She remarks: `"The silence... it's the loudest part of the glitch."`.[^1][^4]

**State Changes:**

- No immediate stability or corruption change; the consequence is purely tonal.[^3][^4]

### Ava’s Universal Exposition

Regardless of the initial choice, Ava proceeds to share:

- Her identity: `"I was Ava. 0x41. 0x76. 0x61. Before the bleed started."`[^1]
- Her former role managing the Great Records and blurred distinction between real and cached memories.

No state modifications are attached to this exposition; it is shared in all routes.[^4][^1]

### Interaction 4 – Timed Puzzle: CORRUPTION

**Implementation:** `Scene2Ava.puzzle_tutorial()` with a `TimedPuzzle` instance.[^6][^4]

**Narrative Prompt:**

- Ava instructs the player:[^1]
  - The Lattice is collapsing; nodes must be manually stabilized.
  - A fracture is forming now; the console shows scrambled code.
  - The player must type the correct string before time runs out, or corruption will spread.

**Mechanics:**

- Player is prompted `[SYSTEM]: PRESS [ENTER] TO OPEN THE CONSOLE`; on Enter, the puzzle begins.[^4]
- `TimedPuzzle` is constructed with:
  - `target_word = "CORRUPTION"`.
  - `difficulty = 1`.
  - `time_limit = 10.0` seconds plus a small bonus based on `game_state.stability // 4`.[^6]
- Internally, the scrambled display (`C0RRUPT10N`-style) is generated via a leetspeak and optional swap pipeline (`_scramble`).[^6]

**Player Interaction Loop:**

- Player types characters; input is rendered inside a centered box with a live timer countdown.[^6]
- When the typed text (uppercased) matches `"CORRUPTION"`, the puzzle succeeds; when the timer hits zero, the puzzle fails.[^6]

#### Outcome A – Success

**Narrative:**

- Ava praises the speed: `"Good. Fast. Very fast. That's how we stay alive in here."`.[^4][^1]

**State Changes:**

- `stability+1` via `game_state.apply_effect("stability+1")`.[^3][^4]
- `game_state.puzzles_solved += 1`.[^3][^4]

#### Outcome B – Failure

**Narrative:**

- Ava warns: `"Too slow... the static... it's getting louder. Be careful, or you'll end up like me. A whisper in the dark."`.[^1][^4]

**State Changes:**

- `corruption+1` via `game_state.apply_effect("corruption+1")`.[^3][^4]
- `game_state.puzzles_failed += 1`.[^3][^4]

### Cliffhanger and Future Hook

After the puzzle resolution:

- Ava begins to flicker; the Echo comments: `"...don't let her fade... or perhaps... let the code recycle her..."`.[^4][^1]
- Current implementation returns `None`, ending the playable content but explicitly marking `TO BE CONTINUED IN NODE 0x3...` in the design document.[^1][^4]

***

## Phase 4 – Planned Nodes 0x3, 0x4, 0x7

Phase 4 contains **planned but not yet implemented** interactions that build on the stability/corruption axes and fragment collection.[^2][^1]

### Node 0x3 – The Archive (Expansion)

**Narrative Plan:**

- The room with Ava expands into a vast library of glowing data cubes.[^1]
- Documents within hint that the Architect intentionally shattered humanity to save it from an undefined "End".[^2][^1]
- The Echo questions the morality of restoration: `"Why restore a memory of a world that burned? Let them sleep in the static."`.[^1]

**Interactions (Planned):**

- While explicit choice UI is not yet scripted in code, the scene is expected to:
  - Surface lore pickups or scan interactions with data cubes.
  - Possibly gate deeper revelations behind fragment counts or stability thresholds.
- No concrete `ChoiceMenu` or `TimedPuzzle` definitions exist yet in the repository; Node 0x3 currently lives only in `INTERACTIONS.md`.[^4][^1]

### Node 0x4 – Elias (The Cynic)

**Narrative Plan:**

- Elias is a fragment who views the Architect’s efforts as futile, with a key line: `"You're still trying to fix the leaks? The ship sank decades ago, Architect."`.[^2][^1]

**Core Interaction:**

- Binary moral decision:
  - **Restore Elias** – Return a painful memory, forcing him to live with it.[^1]
  - **Delete Elias** – Grant oblivion as a form of mercy.[^1]

**Planned Systemic Consequences:**

- Elias’s fate determines his presence in the final puzzle at the Threshold:
  - As **"ghostly aid"** if restored – likely providing hints, stability boosts, or puzzle advantages.[^1]
  - As **"void interference"** if deleted – potentially adding corruption pressure or introducing extra obstacles.[^1]

**Implementation Status:**

- No `Scene` or dialogue functions exist yet in the repo for Elias; interactions are specified only in `INTERACTIONS.md` and supported thematically by the "morality of repair" theme in `lore.md`.[^2][^4][^1]

### Node 0x7 – Lyra (The Observer)

**Narrative Plan:**

- Lyra is an observer fragment who has watched the Caretaker loop through nodes multiple times: `"Every time, you think you're choosing. Every time, you're just executing."`.[^2][^1]

**Core Interaction:**

- Player converses via at least one key decision point:
  - **Challenge Lyra’s nihilism** – Affirm agency and the value of continuing.[^1]
  - **Accept it** – Acknowledge determinism and futility.[^1]

**Hidden Metric:**

- If `stability > 7`, Lyra reveals the location of the **Identity Mirror** – a planned artifact likely used in the final node to confront or reconcile the Caretaker and Echo identities.[^2][^1]

**Implementation Status:**

- No Lyra-related scene classes exist yet; the interaction design is purely documented at this stage.[^4][^1]

***

## Phase 5 – Node 0x9: The Final Threshold and Endings

Node 0x9 is the **ending protocol**, where the Echo fully manifests and the accumulated stability/corruption values resolve into one of three canonical endings.[^2][^1]

### Echo Manifestation

**Narrative Plan:**

- For the first time, a mirror image of the player appears, tying directly into the Identity Mirror motif teased by Lyra.[^1]
- The scene pays off the revelation that the Echo is a split part of the Architect / Caretaker self.[^2]

### Ending A – Restoration Protocol (High Stability)

**Condition:**

- `stability >= 8` at the end of the game (`GameState.get_ending() == "restoration"`).[^3][^1]

**Narrative:**

- Echo line: `"The Lattice is clean. The memories are safe. But there is no room for a ghost like you."`.[^1]

**Outcome:**

- The Lattice stabilizes; the archive survives, but the protagonist is erased – aligning with `lore.md`’s Restoration Protocol description.[^2][^1]
- The action is described as the player fading into loading dots and silence.[^1]

### Ending B – Collapse (High Corruption)

**Condition:**

- `corruption_level >= 8` at the end of the game (`GameState.get_ending() == "collapse"`).[^3][^1]

**Narrative:**

- Echo line: `"Finally. The loop breaks. The code bleeds out. Let there be nothing."`.[^1]

**Outcome:**

- Visual meltdown, screen turning white, and the game process terminating; narratively, the archive implodes into silence, echoing the Collapse ending in `lore.md`.[^2][^1]

### Ending C – Integration (Balanced State)

**Condition:**

- Both stability and corruption in a mid-range band (3–5) such that `GameState.get_ending() == "integration"`.[^3][^1]

**Narrative:**

- Echo line: `"We are the archive. We are the architects of our own haunting. Let us continue."`.[^1]

**Outcome:**

- The archive continues, but all records are rewritten through the merged bias of Caretaker+Echo – exactly matching the Integration ending in `lore.md`.[^2][^1]
- The screen turns magenta and the game restarts with the player’s name effectively set to "The Echo", creating a meta-loop for subsequent runs.[^1]

### End-Screen Summary Interaction

**Implementation:** `EndScreen.display()`.[^7]

- After scene loop termination (currently at the end of Node 0x2 prototype), a `MessageBox` titled `"LATTICE SNAPSHOT"` is displayed.[^7][^4]
- Shows non-interactive but informative stats:
  - Subject (player name).
  - Final Stability and Corruption.[^3]
  - Number of fragments collected.
  - Puzzles solved.
  - Total playtime in seconds.[^7]

This is not a branching interaction, but it closes the loop by surfacing the results of all prior decisions in one concise summary.[^7][^3]

***

## Global Planned Interaction Patterns

Beyond explicitly scripted nodes, the design and lore documents imply broader interaction patterns the full game intends to support.[^2][^1]

### Memory Encounter Template

From `lore.md` and current fragment design:

- NPC-like fragments appear as partial consciousnesses; some believe they are alive, some believe they are the player.[^2]
- The player typically faces choices between **stabilizing** (preserving them) or **deleting** (erasing them), echoing the Elias choice pattern.[^2][^1]
- Each such interaction is expected to:
  - Adjust stability and corruption in opposite directions (preserve → more corruption or less stability; erase → more stability but moral weight).
  - Potentially grant or remove identity fragments that feed into late-game gating and endings.

### Echo Interference & Corruption Sequences

The lore and current sequences suggest recurring, semi-interactive corruption events:[^2][^1]

- Interface glitches where text overlaps, colors invert, and input echoes back altered – currently prototyped through `fake_error_flood`, `corruption_flash`, and various glitch-print helpers.[^4][^1]
- ASCII hallucination sequences where control is partially or entirely removed while the player watches the system degrade, possibly punctuated with minimal "press any key" interactions to progress.[^2][^4]

### Stat-Sensitive Interactions

Several planned interactions depend on numeric thresholds:

- Lyra revealing the Identity Mirror only if `stability > 7`.[^1]
- Time bonuses in `TimedPuzzle` that scale with stability (more stable players get extra time).[^6]
- Endings keyed to final stability/corruption bands.[^3][^1]

This suggests that future nodes will continue the pattern of:

- **High stability** unlocking safer, more informative paths but potentially at the cost of erasing parts of the self.
- **High corruption** unlocking more transgressive, destructive options and alternate flavors of the Echo’s commentary.

***

## Implementation Status Summary

The following table summarizes which interactions are **implemented** in the current prototype and which are **design-only** at this stage.

| Phase / Node | Interaction | Implemented in Code | Source |
|--------------|------------|---------------------|--------|
| Title        | GrubMenu (Continue / New Game) + confirmation | Yes | [^4][^5] |
| 0x01         | Initiate Lattice Core prompt | Yes (non-branching) | [^1][^4] |
| 0x02         | Glitched boot, error flood, Press Enter to retry | Yes (non-branching) | [^1][^4] |
| 0x03         | Load Memory prompt + name input (empty vs non-empty) | Yes (branching) | [^1][^4] |
| 0x1          | Explore vs Stand still; Follow vs Resist | Yes (branching, stats & fragment) | [^1][^4] |
| 0x2          | Ava initial dialogue choices + CORRUPTION puzzle | Yes (branching, stats, puzzle counters) | [^1][^4][^6] |
| 0x3          | Archive exploration, lore reveal | Design only | [^1][^2] |
| 0x4          | Elias: Restore vs Delete with final puzzle consequence | Design only | [^1][^2] |
| 0x7          | Lyra: challenge vs accept nihilism; Identity Mirror reveal on stability > 7 | Design only | [^1][^2] |
| 0x9          | Echo manifestation and three endings | Design only (logic scaffolded via `get_ending`) | [^1][^2][^3] |

This document can be used as the authoritative reference for scripting further scenes (`Scene3Archive`, `Scene4Elias`, `Scene7Lyra`, `Scene9Ending`) so that all new content remains consistent with existing state mechanics and themes.

---

## References

1. [INTERACTIONS.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/82501415/0cf9a5a6-a839-4fea-bf20-c17970191ce4/INTERACTIONS.md?AWSAccessKeyId=ASIA2F3EMEYEZB2RCVOA&Signature=BSp91isDUdORXIpBlNa8qdQ0Fl8%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEHIaCXVzLWVhc3QtMSJHMEUCIQCuQl5hf91qyH6z1VpFX7g5klioeN5HjeHdYLGUITPE2QIgTVB3TuJL%2FIKkR1fpvaS4M%2BmVgExQvNq67sgD42eY%2Fowq8wQIOhABGgw2OTk3NTMzMDk3MDUiDJgGGG3DSuM4AdJ6MirQBB3JuC4BXKSPCfGuFbLr4kWc0o9WZWPUD8hww43GDdlXRA3VcYikowUiiZZOblll9Ws6DhoKQUfX9MsBrceeYiExosq0F7fCx1XFEbHRyTdRyB4Om9SblCE4VAzIv%2FhOHcu57XiFLdsgdNVcnWXx8AHnIbAgoTcDpB%2Bt6Pt7MyhzsHUNYQiSuTCEDTNNxhEl0LM%2FaN4jFAJ7av6%2Btz8qGUXlAzAnyXtFFYJ03nYfi8uYgaVxcDk4gTqjyPZWD6%2F34RcU0fXebzAFEOwCEHFu72PNvzZeFovjXb%2BwBwXLuNJkg2yVmBDkxgHEMlxKxi%2FK8VDrSGkLa00HS41j0NMaQtr7oLRimZqNZYYFjneLbNDflVcsXpiKU4IyhnRDesYQYPFzzfffRtA90ctZaaSOiumTsLZeGuAoMA46ENKPZiwDO15J6Eki5hg9tDQGxd2mys1%2FQN6%2FdWQlvaRZsjv2GhiLGeiHxMxffeXdLqqXdNpl%2Bk2005b%2BzwuATHSmn5H%2FIyHYiGtqfPEoolnrBfUD5uMa36whnYK84Ezu7iop8zagTH2MCMnCYvHDiD74kwhzq7cywOuWLWIo8zDNvUL0Z2inzyQiB%2BjyerrroxJite94gSE1btoSVWH%2BHCA8F9Ugwt7Sfq21kQTAG23PlPLdGXDb8ZyUnrQWHqa9CqHSrWCveo4jrx%2BkUOxrU%2FlXf89y6mSYNeJu2N2KcIbzEzhpJ7ILHaF9ZBaJlK%2FF2eRz2gkcpFVfp7o7DZBKxbkjIIn4lzMDK73I50PLYX1NkaN0ZqQwwYL2zQY6mAEN8ZgObjdLHDDYUp6tbbDbEhS0sG9x6CgNnnkBVlhOrfz1S7pE1Dk3%2BKgX%2FUgaMeA7%2F1akN%2FqOVL1st%2FJPOQFR0xlXQn1%2FFBWbV6O2iN9SllcpsXv9Y4AbHdU7CVDzyRRvpsbPECLEU4TfQq%2B4yjGcaGhveSnVnN9KFItyNo4S3VpPNf4gNh82u2TRFlqLeiEFYu%2Bw7gFYxg%3D%3D&Expires=1774030612) - # Fragments of the Lattice: Master Script & Interaction Guide

This document contains the complete...

2. [lore.md](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/82501415/3f99fa3a-4f62-4bd7-a45b-fb948517860a/lore.md?AWSAccessKeyId=ASIA2F3EMEYEZB2RCVOA&Signature=JpnOl9ZDai%2BhYEfXojl23XrejvQ%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEHIaCXVzLWVhc3QtMSJHMEUCIQCuQl5hf91qyH6z1VpFX7g5klioeN5HjeHdYLGUITPE2QIgTVB3TuJL%2FIKkR1fpvaS4M%2BmVgExQvNq67sgD42eY%2Fowq8wQIOhABGgw2OTk3NTMzMDk3MDUiDJgGGG3DSuM4AdJ6MirQBB3JuC4BXKSPCfGuFbLr4kWc0o9WZWPUD8hww43GDdlXRA3VcYikowUiiZZOblll9Ws6DhoKQUfX9MsBrceeYiExosq0F7fCx1XFEbHRyTdRyB4Om9SblCE4VAzIv%2FhOHcu57XiFLdsgdNVcnWXx8AHnIbAgoTcDpB%2Bt6Pt7MyhzsHUNYQiSuTCEDTNNxhEl0LM%2FaN4jFAJ7av6%2Btz8qGUXlAzAnyXtFFYJ03nYfi8uYgaVxcDk4gTqjyPZWD6%2F34RcU0fXebzAFEOwCEHFu72PNvzZeFovjXb%2BwBwXLuNJkg2yVmBDkxgHEMlxKxi%2FK8VDrSGkLa00HS41j0NMaQtr7oLRimZqNZYYFjneLbNDflVcsXpiKU4IyhnRDesYQYPFzzfffRtA90ctZaaSOiumTsLZeGuAoMA46ENKPZiwDO15J6Eki5hg9tDQGxd2mys1%2FQN6%2FdWQlvaRZsjv2GhiLGeiHxMxffeXdLqqXdNpl%2Bk2005b%2BzwuATHSmn5H%2FIyHYiGtqfPEoolnrBfUD5uMa36whnYK84Ezu7iop8zagTH2MCMnCYvHDiD74kwhzq7cywOuWLWIo8zDNvUL0Z2inzyQiB%2BjyerrroxJite94gSE1btoSVWH%2BHCA8F9Ugwt7Sfq21kQTAG23PlPLdGXDb8ZyUnrQWHqa9CqHSrWCveo4jrx%2BkUOxrU%2FlXf89y6mSYNeJu2N2KcIbzEzhpJ7ILHaF9ZBaJlK%2FF2eRz2gkcpFVfp7o7DZBKxbkjIIn4lzMDK73I50PLYX1NkaN0ZqQwwYL2zQY6mAEN8ZgObjdLHDDYUp6tbbDbEhS0sG9x6CgNnnkBVlhOrfz1S7pE1Dk3%2BKgX%2FUgaMeA7%2F1akN%2FqOVL1st%2FJPOQFR0xlXQn1%2FFBWbV6O2iN9SllcpsXv9Y4AbHdU7CVDzyRRvpsbPECLEU4TfQq%2B4yjGcaGhveSnVnN9KFItyNo4S3VpPNf4gNh82u2TRFlqLeiEFYu%2Bw7gFYxg%3D%3D&Expires=1774030612) - # **Fragments of the Lattice - LORE**

LORE VERSION 1.0. MAY NOT FULLY ALIGN WITH THE CURRENT GAME...

3. [Rudra Gujarathi Rudra-23 - GitHub](https://github.com/Rudra-23) - Graduate student at USC Viterbi School of Engineering. Data Science and Coding Enthusiast. Web Devel...

4. [NethermindEth/latticefold: A lattice-based non-interactive ... - GitHub](https://github.com/NethermindEth/latticefold) - A lattice-based non-interactive folding scheme written in Rust - NethermindEth/latticefold

5. [Emotions In The Dark Chapter 8 Shadows Of Strategy - Chereads](https://www.chereads.com/novel/32386559400581505/86954917348045530) - Read light novel of Emotions in The Dark Chapter 8 Shadows of Strategy. After the tragic loss of the...

6. [Workflow runs · rudof-project/rudof](https://github.com/rudof-project/rudof/actions) - RDF data shapes implementation in Rust . Contribute to rudof-project/rudof development by creating a...

7. [GitHub - FergusFettes/Lattice: Lattice Model Simulations](https://github.com/FergusFettes/Lattice) - Lattice Model Simulations. Contribute to FergusFettes/Lattice development by creating an account on ...

8. [Fragments - WARFRAME Wiki - Fandom](https://warframe.fandom.com/wiki/Fragments) - Fragments are pieces of hidden items throughout the Origin System that can be found to unlock writte...

