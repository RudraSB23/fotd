# Fragments of the Lattice

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-informational?style=for-the-badge)
![Genre](https://img.shields.io/badge/Genre-Terminal%20Horror%20%7C%20Narrative-8B0000?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow?style=for-the-badge)

**Terminal-based psychological horror where you debug your own collapsing mind.**

> _You awaken in a dead terminal. A presence whispers your name in the static._

</div>

---

## 🎮 About

**Fragments of the Lattice** traps you inside **The Lattice** – a decaying digital archive containing humanity's forgotten consciousness. As the **Caretaker**, you stabilize fractured memory nodes while **The Echo** – a corrupted fragment of yourself – fights to unravel everything.

**Core Loop:**

```
Navigate → Choose (Stability or Corruption) → Solve Stabilization Puzzle → Echo Interferes → Repeat
```

Every decision shifts your **Stability ↔ Corruption** balance, unlocking 3 distinct endings.

> [!NOTE]
> **🚧 Work in Progress** — This game is actively being developed. Nodes 0x1 and 0x2 are playable; Nodes 0x3 through 0x9 are planned or partially scripted. Expect rough edges, missing content, and frequent updates.

---

## ✨ Features

- **🧠 Branching Narrative** – Corruption/Stability choices shape dialogue, relationships, endings
- **💥 Real-Time Glitch Engine** – Live text corruption, screen-melting effects, leetspeak scrambling
- **⏱️ Timed Puzzles** – Decrypt strings under pressure or lose the node to static
- **🎨 Cinematic ASCII** – Animated logo, full-screen art sequences
- **🔊 Immersive Audio** – 80s synth soundtrack + layered SFX (pygame-powered)
- **💾 Smart Saves** – Multi-slot JSON with scene restoration + integrity checks
- **🎮 Terminal Native** – Curses rendering, F11 fullscreen calibration

---

## 📱 Preview

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

> _Screen glitches. Red cursor blinks. **THE LATTICE SEES YOU.**_

---

## ⚙️ Quick Start

### Prerequisites

- **Python 3.11+**
- **Windows**: `pip install windows-curses pygame`

### Install & Play

```bash
git clone https://github.com/RudraSB23/fotd.git
cd fotd
pip install -r requirements.txt
python main.py
```

**Pro Tip:** F11 fullscreen + dark theme + monospace font (`Cascadia Code`).

---

## 🎮 Controls

| Key    | Action           |
| ------ | ---------------- |
| ↑↓     | Navigate choices |
| ⏎      | Select           |
| ⌫      | Puzzle backspace |
| Esc    | Pause menu       |
| Ctrl+C | Quit             |

---

## 🧠 Mechanics Deep Dive

### Stability ↔ Corruption

```
Choices & puzzles shift your balance:
Corruption ≥5  → Glitchy menus
Corruption ≥8  → Screen meltdown
Stability ≥7   → Hidden paths
```

### Stabilization Puzzles

```
Decrypt leetspeak under timer pressure:
C0RRUP710N → Type "CORRUPTION" in 10s
Fail → Node corrupts → Echo grows stronger
```

### The Echo

A corrupted fragment of **yourself** that:

- Whispers during choices
- Alters puzzles at high corruption
- Manifests in endings

---

## 🗂️ Repo Structure

```
fotd/
├── main.py           # Entry point
├── scenes/           # Modular narrative (0x1 Corridor, 0x2 Ava)
├── engine/           # Core systems
│   ├── state_manager.py
│   ├── save_manager.py
│   ├── console_effects.py
│   └── elements.py
├── assets/
│   ├── ascii_art/
│   └── sounds/       # 80s synth + glitch SFX
└── saves/            # Auto-save slots
```

---

## 🎵 Soundtrack Credits

- **Boot Theme**: [Melancholia](https://www.youtube.com/watch?v=u9WsZoceais)
- **Main Menu Theme**: [Fragments of the Lattice](https://www.youtube.com/watch?v=1YG0QCl9USI)

---

## 📜 License

Unlicensed prototype. Contact for commercial inquiries.

---

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-000000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/RudraSB23/fotd)

"Stabilize the nodes... or let the static claim you."\_

</div>
