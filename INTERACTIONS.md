# Fragments of the Lattice: Master Script & Interaction Guide

This document contains the complete dialogue script for the Lattice, including current implementation and planned future nodes.

---

## 🟢 PHASE 1: Boot & Initialization

### Node 0x01: Startup & Onboarding

**Music**: `noname.mp3` -> `melancholia.mp3`

- **Visual**: A black screen. A cursor blinks, waiting.
- **Narrative**:
  - "You don’t remember sitting down here. You don’t remember EVERYTHING."
  - "The Lattice, a broken archive that recalls what humanity has forgotten."
  - "Its corridors bend with memory, but corruption crawls through the code."
  - "Identities blur. Timelines knot."
  - "You are the Caretaker. The one who should hold it together… or what remains of them."
- **Prompt**: `[INPUT REQUIRED] Initiate Lattice Core [Y/Y]`

### Node 0x02: Initiating Sequence (Glitched)

**Sound**: `scary_static.mp3`

- **System Logs**:
  - `[BOOT] Initializing Lattice Core...`
  - `[BOOT] Loading Memory Nodes...`
  - `[BOOT] Stabilizing Echo Channels...`
  - `[BOOT] Synchronizing Identity Fragments...`
  - `[BOOT] Fetching Fragment Memory...`
- **Echo Interference (Red/Glitch)**:
  - "DO NOT PROCEED."
  - "THE LATTICE SEES YOU."
  - "Fragments will claim your mind."
  - "Your actions are being recorded…"
  - "ECHOES OF THE PAST ARE WATCHING."
- **Failure State**: `[ERR] A fatal error occured. > Press [Enter] to retry:`

### Node 0x03: Memory Load & Reboot

**Visual**: `NODES REALIGNING` progress bar

- **Prompt**: `[INPUT REQUIRED] Load Memory: [Y/Y]`
- **Boot Logs**:
  - `Identity: [UNRESOLVED]`
  - `Location: Node-01 [UNRESOLVED]`
  - `Stability: [███░░░] (3/6)`
- **Atmosphere**:
  - "You awaken in a dim corridor of fractured light."
  - "Walls flicker between stone, glass, and raw code."
  - "half pixel, half memory."
- **Identity Registry**:
  - `... Who... are you? ...`
  - **Choice (Silent Name)**:
    - "I see you are shy from telling me your name..."
    - "Are you hiding from yourself?"
    - "Oh well... looks like you gotta use your old name..."
  - **Outcome**: Player is registered as `{player_name}` (default: `Caretaker`).

---

## 🟢 PHASE 2: Node 0x1 - The Corridor

### The Echo's Wake

- **Animation**: The screen floods with the player's name in red static.
- **Echo**: "...{player_name}..."
- **Narrative**: "The corridor shivers. Something presses against the walls of code."

### Choice A: Explore the Corridor (Corruption Path)

- **Description**: "The corridor's walls ripple like liquid glass as it extends indefinitely."
- **Narrative**: "Every step reverberates... but as static bursts against your consciousness."
- **Reflections**: "Sometimes showing someone else… or SOMEONE YOU MIGHT HAVE BEEN."
- **The Echo (Quote)**: `"Every step… closer to yourself… or to me…"`
- **Prompt**: "The air hums with fractured memory. Explore or Stand still?"

### Choice B: Stand Still (Stability Path)

- **Description**: "The silence stretches... The corridor holds its breath with you."
- **The Echo**: `"> Thank you... I need more time to reach you..."`
- **Narrative**: "A flicker passes along the glass walls. Not corruption this time, but memory."
- **Discovery**: `Fragment located... | identity shard detected... [Shard 001 Collection]`
- **The Echo**: `"...don’t forget... caretaker... you are still here..."`

### Node 0x1 Transition

- **Path: Follow**: "You surrender to the pull. The corridor stops being a place and begins to feel like a pulse."
- **Echo**: `"...good... much better... don't you feel the weight lifting?..."`
- **Path: Resist**: "You plant your feet and refuse the guiding whispers."
- **Echo**: `"...obstinate... you always were... persistent..."`

---

## 🟢 PHASE 3: Node 0x2 - Fragment Alpha (Ava)

### The Encounter

- **Narrative**: "The scenery shifts. The endless corridor collapses into a single, small room."
- **Ava's Appearance**: "There is a flicker in the center—a figure made of data shards."
- **Echo**: `"...Ava?..."`
- **Ava**: `"Is... is someone there? The Lattice... it feels so empty today."`

### Branching Dialogue (Phase 1)

- **Menu**: `ChoiceMenu("")`
  - **Opt 1: "I am here. I'm the Caretaker."**
    - **Ava**: `"Caretaker? I remember that word. It sounded... safe. Once."` (Stability +1)
  - **Opt 2: "You're just a fragment. Stay still."**
    - **Ava**: `"Fragment?" Her static ripples harshly. "I am... I was... I..."` (Corruption +1)
    - **Ava**: `"You speak like the Architect. Cold. Calculating. But you're here. That means the nodes are failing, doesn't it?"`
  - **Opt 3: (Remain silent)**
    - **Ava**: `"Hello?" No one answers but the hum of the walls.`
    - **Ava**: `"The silence... it's the loudest part of the glitch."`

### Ava's Introduction (Universal)

- **Ava**: `"Wait... you aren't one of them. You're... whole. Mostly. I was Ava. 0x41. 0x76. 0x61. Before the bleed started."`
- **Ava**: `"I used to manage the Great Records. I remember sunlight hitting a physical book once... or maybe I just downloaded that sensation. In the Lattice, it's hard to tell what's a memory and what's just a cached file."`

### The Puzzle Tutorial (Phase 2)

- **Ava**: `"Listen, Caretaker. The Lattice is collapsing. To stay here, to reach the Archive, you have to stabilize the nodes manually."`
- **Ava**: `"I can feel a fracture forming right now. Look at the console. It's scrambled code. You have to type the correct string before the time runs out, or the corruption will spread."`
- **TUTORIAL PROMPT**:
  - **Scrambled Text**: `C0RRUPT10N` -> **Requirement**: Type `CORRUPTION` in 10 seconds.
- **Outcome: Success**:
  - **Ava**: `"Good. Fast. Very fast. That's how we stay alive in here."`
- **Outcome: Failure**:
  - **Ava**: `"Too slow... the static... it's getting louder. Be careful, or you'll end up like me. A whisper in the dark."`

### Conclusion

- **Echo**: `"...don't let her fade... or perhaps... let the code recycle her..."`
- **Cliffhanger**: `TO BE CONTINUED IN NODE 0x3...`

---

## 🔴 PHASE 4: Node 0x3+ (Future Script)

### Node 0x3: The Archive (Expansion)

- **Narrative**: The room expands into a library of glowing data cubes.
- **Lore Revelation**: Documentation found here hints that the Architect intentionally "shattered" humanity to save it from a non-specified "End".
- **The Echo**: `"Why restore a memory of a world that burned? Let them sleep in the static."`

### Node 0x4: Elias (The Cynic)

- **Dialogue**: `"You're still trying to fix the leaks? The ship sank decades ago, Architect."`
- **Choice**: Restore Elias (giving him back a painful memory) or Delete Elias (mercy via oblivion).
- **Consequence**: Impacts whether Elias appears as a "ghostly aid" or "void interference" in the final puzzle.

### Node 0x7: Lyra (The Observer)

- **Dialogue**: `"I've watched you loops these nodes a thousand times. Every time, you think you're choosing. Every time, you're just executing."`
- **Choice**: Challenge Lyra's nihilism or accept it.
- **Hidden Metric**: If `stability > 7`, Lyra reveals the location of the **Identity Mirror**.

---

## 🔴 PHASE 5: The Final Threshold

### Node 0x9: The Ending Protocol

- **The Echo Manifests**: For the first time, a mirror image of the player appears.
- **Ending A: Restoration Protocol (Stability >= 8)**
  - **Dialogue**: `"The Lattice is clean. The memories are safe. But there is no room for a ghost like you."`
  - **Action**: Player fades into the loading dots. Silence.
- **Ending B: Collapse (Corruption >= 8)**
  - **Dialogue**: `"Finally. The loop breaks. The code bleeds out. Let there be nothing."`
  - **Action**: Visual meltdown. Screen turns white. Game closes.
- **Ending C: Integration (Balance)**
  - **Dialogue**: `"We are the archive. We are the architects of our own haunting. Let us continue."`
  - **Action**: Screen turns magenta. The game begins again, but with "The Echo" as the player's name.
