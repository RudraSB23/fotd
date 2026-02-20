# Fragments of the Lattice

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-informational?style=for-the-badge)
![Genre](https://img.shields.io/badge/Genre-Terminal%20Horror%20%7C%20Narrative-8B0000?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow?style=for-the-badge)

**A terminal-based narrative horror game where memory, corruption, and identity collide.**

_You are the Caretaker. Something is watching._

</div>

---

## 🖥️ About the Game

**Fragments of the Lattice** is a text-driven horror experience rendered entirely in your terminal. You are the **Caretaker** — an entity awakened inside _The Lattice_, a decaying digital archive of human consciousness. As you navigate fractured memory nodes, a presence known as **The Echo** trails your every keystroke.

The game blends atmospheric ASCII art, real-time glitch effects, branching narrative choices, and timed decryption puzzles into a single, immersive terminal session. Every decision you make tips the balance between **Stability** and **Corruption** — and your ending is determined by where that needle lands.

> [!NOTE]
> **🚧 Work in Progress** — This game is actively being developed. Nodes 0x1 and 0x2 are playable; Nodes 0x3 through 0x9 are planned or partially scripted. Expect rough edges, missing content, and frequent updates.

---

## ✨ Features

- **Branching Narrative** — Choices shape your corruption/stability stats and unlock different dialogue paths and endings.
- **Real-Time Glitch Engine** — Live text distortion, screen-wide corruption flashes, and character-level leetspeak scrambling.
- **Timed Stabilization Puzzles** — Decrypt corrupted strings under pressure before the static consumes the node.
- **ASCII Art Sequences** — Full-screen art for the title, intro, and key story moments.
- **Atmospheric Soundtrack** — Background music and layered sound effects powered by `pygame.mixer`, preloaded asynchronously.
- **Persistent Save System** — JSON-based save/load with in-terminal feedback messages.
- **Multiple Endings** — Three distinct endings determined by your final Stability vs. Corruption score.

---

## 🖼️ Preview

```
    ███████╗██████╗░░█████╗░░██████╗░███╗░░░███╗███████╗███╗░░██╗████████╗░██████╗  ░█████╗░███████╗
    ██╔════╝██╔══██╗██╔══██╗██╔════╝░████╗░████║██╔════╝████╗░██║╚══██╔══╝██╔════╝  ██╔══██╗██╔════╝
    █████╗░░██████╔╝███████║██║░░██╗░██╔████╔██║█████╗░░██╔██╗██║░░░██║░░░╚█████╗░  ██║░░██║█████╗░░
    ██╔══╝░░██╔══██╗██╔══██║██║░░╚██╗██║╚██╔╝██║██╔══╝░░██║╚████║░░░██║░░░░╚═══██╗  ██║░░██║██╔══╝░░
    ██║░░░░░██║░░██║██║░░██║╚██████╔╝██║░╚═╝░██║███████╗██║░╚███║░░░██║░░░██████╔╝  ╚█████╔╝██║░░░░░
    ╚═╝░░░░░╚═╝░░╚═╝╚═╝░░╚═╝░╚═════╝░╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚══╝░░░╚═╝░░░╚═════╝░  ░╚════╝░╚═╝░░░░░

        ████████╗██╗░░██╗███████╗  ██╗░░░░░░█████╗░████████╗████████╗██╗░█████╗░███████╗
        ╚══██╔══╝██║░░██║██╔════╝  ██║░░░░░██╔══██╗╚══██╔══╝╚══██╔══╝██║██╔══██╗██╔════╝
        ░░░██║░░░███████║█████╗░░  ██║░░░░░███████║░░░██║░░░░░░██║░░░██║██║░░╚═╝█████╗░░
        ░░░██║░░░██╔══██║██╔══╝░░  ██║░░░░░██╔══██║░░░██║░░░░░░██║░░░██║██║░░██╗██╔══╝░░
        ░░░██║░░░██║░░██║███████╗  ███████╗██║░░██║░░░██║░░░░░░██║░░░██║╚█████╔╝███████╗
        ░░░╚═╝░░░╚═╝░░╚═╝╚══════╝  ╚══════╝╚═╝░░╚═╝░░░╚═╝░░░░░░╚═╝░░░╚═╝░╚════╝░╚══════╝


                                        > Continue
                                          New Game


```

> _The screen glitches. A red cursor blinks. THE LATTICE SEES YOU._

---

## ⚙️ Requirements

| Dependency | Version  | Purpose                    |
| ---------- | -------- | -------------------------- |
| `Python`   | `3.11+`  | Core runtime               |
| `pygame`   | `2.x`    | Audio management           |
| `curses`   | Built-in | Terminal rendering & input |

> **Windows note:** `curses` is not included in the standard library on Windows. Install the `windows-curses` package.

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/fragments-of-the-lattice.git
cd fragments-of-the-lattice
```

### 2. Create a Virtual Environment _(recommended)_

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Game

```bash
python main.py
```

The game will launch in your terminal. For the best experience, use a **full-screen terminal** with a dark background and a monospace font (e.g., `Cascadia Code`, `Fira Mono`, `Consolas`).

---

## 🎮 Controls

| Key         | Action                         |
| ----------- | ------------------------------ |
| `↑` / `↓`   | Navigate menu / choice options |
| `Enter`     | Confirm selection              |
| `Backspace` | Delete character (puzzles)     |
| `ESC`       | Open pause menu                |
| `Ctrl+C`    | Trigger quit confirmation      |

> **During Timed Puzzles:** Type the un-corrupted target word into the active input field before the countdown reaches zero.

---

## 🗂️ Project Structure

```
fragments-of-the-lattice/
├── main.py        # Game entry point
├── dialogue.py    # Story & scenes
├── saves.json     # Auto-generated save file
├── assets/
│   ├── ascii_art/ # Title & intro art
│   ├── images/    # Logo
│   └── sounds/    # Music & sound effects
└── engine/        # Game engine (internal)
```

---

## 🧠 Game Mechanics

### Stability vs. Corruption

Every choice you make adjusts one of two core stats. Certain dialogue options, puzzle outcomes, and NPC interactions will push you toward **order** or **chaos**.

| Threshold        | Effect                                          |
| ---------------- | ----------------------------------------------- |
| `Corruption ≥ 5` | Choice menus begin glitching (corrupted arrows) |
| `Corruption ≥ 8` | Forced Glitch Mode activates                    |
| `Stability ≥ 7`  | Unlock hidden content (e.g., Identity Mirror)   |

### Narrative Nodes

The story progresses through numbered **Nodes**, each representing a fractured memory location:

- **Node 0x1 — The Corridor:** Your first encounter with The Echo.
- **Node 0x2 — Fragment Alpha (Ava):** A data-fragment NPC who teaches you stabilization.
- **Node 0x3+ — The Archive & Beyond:** _(In development)_

### Endings

Your final stats determine which of three endings you receive:

| Ending          | Condition        |
| --------------- | ---------------- |
| **Restoration** | `Stability ≥ 8`  |
| **Collapse**    | `Corruption ≥ 8` |
| **Integration** | Balanced stats   |

---

## 🤝 Contributing

Contributions, bug reports, and narrative suggestions are welcome!

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit: `git commit -m "feat: describe your change"`
4. Push to your branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please keep code modular and consistent with the existing engine architecture. New narrative content should be added to `dialogue.py` as named scene functions.

---

## 📜 License

This project is currently unlicensed. All rights reserved by the author. Contact the repository owner for usage inquiries.

---

## 🎖️ Credits

- **Design, Writing & Engineering** — Rudra Singh Bhardwaj
- **Audio** — Various artists (see `assets/sounds/` for individual tracks)
- **Rendering Engine** — Built on Python's `curses` standard library
- **Audio Engine** — Powered by [`pygame`](https://www.pygame.org/)

---

<div align="center">

_"The Lattice is collapsing. Stabilize the nodes — or let the static take you."_

</div>
