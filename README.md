# PythonBeginners

A collection of Python projects for beginners to learn and practice programming fundamentals

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Introduction

Welcome to PythonBeginners! This repository contains a diverse collection of Python projects designed specifically for beginners. Each project focuses on different aspects of Python programming, from GUI applications to game development, helping you build practical skills while having fun.

## Projects

### Source Folder

All projects are located in the `Source/` directory. Here's what you'll find:

| Project | Description | Skills Learned |
|---------|-------------|----------------|
| **2048.py** | Classic 2048 puzzle game with GUI | GUI (tkinter), game logic, state management |
| **AnalogClock.py** | Analog clock display with moving hands | Graphics, time handling, animations |
| **Calculator.py** | Basic calculator with arithmetic operations | GUI design, event handling |
| **Converter.py** | Unit converter for various measurements | Data conversion, user input handling |
| **DigitalClock.py** | Digital clock with date display | Time formatting, real-time updates |
| **Dinosaur.py** | Chrome-style dinosaur runner game | Sprite animation, collision detection |
| **LanguageTrans.py** | Language translation application | API integration, GUI |
| **Snake.py** | Classic snake game | Game loops, coordinate management |
| **Sudoku.py** | Sudoku puzzle solver and game | Backtracking algorithm, grid manipulation |
| **Tetris.py** | Tetris game with rotation mechanics | Game physics, piece management |
| **TicTacToe.py** | Tic-Tac-Toe two-player game | Game state logic, win detection |
| **Triangle.py** | Triangle calculations and visualizer | Math formulas, geometry |
| **WordGuess.py** | Wordle-style word guessing game | String manipulation, pattern matching, scoring system |
| **Weather.py** | Weather information display app | API calls, JSON parsing, UI updates |

## Prerequisites

Before you begin, ensure you have the following:

- **Python 3.6+** installed on your machine. Download from [python.org](https://www.python.org/downloads/)
- Basic understanding of Python syntax (variables, loops, functions, etc.)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/PythonBeginners.git
   cd PythonBeginners
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running Individual Projects

Navigate to the `Source` folder and run any project:

```bash
cd Source
python 2048.py          # Run the 2048 game
python Snake.py         # Run the Snake game
python WordGuess.py     # Run the WordGuess game
python Calculator.py    # Run the Calculator
# ... and so on
```

### Using the Main Launcher

Run `main.py` to launch a menu selector:

```bash
python main.py
```

Then follow the on-screen instructions to select and run a project.

## Project Highlights

### Featured Games

- **2048** - A modern implementation with score tracking, high scores, and smooth animations
- **Snake** - Classic arcade game with increasing difficulty
- **Tetris** - Full-featured tetris with rotation and line clearing
- **TicTacToe** - Two-player game with win/lose detection
- **WordGuess** - Wordle-style word guessing with multiple categories, scoring, and streak bonuses

### GUI Applications

- **Weather** - Real-time weather data with beautiful interface
- **Calculator** - Clean and functional calculator
- **Clocks** - Both analog and digital clock implementations

## Requirements

Most projects use only the Python standard library. Some external dependencies:

```
tkinter     # GUI applications (usually included with Python)
requests    # Weather app
```

## Learning Path

Suggested order for beginners:

1. **Calculator** - Learn basics of GUI programming
2. **DigitalClock/AnalogClock** - Understand time handling
3. **TicTacToe** - Learn game logic and state management
4. **2048/Snake** - Advance to more complex game mechanics
5. **WordGuess** - Learn string manipulation and pattern matching
6. **Weather** - Learn API integration

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Contribution Guidelines

- Follow Python PEP 8 style guidelines
- Add comments for complex logic
- Test your changes before submitting
- Update README if adding new projects

## Common Issues

### Import Errors

If you encounter import errors for `tkinter`:

- **Windows**: Install via Python installer with "tcl/tk and IDLE" option
- **macOS**: `brew install python-tk`
- **Linux**: `sudo apt-get install python3-tk`

### Dependencies

Missing packages? Install them:
```bash
pip install requests
```

## Roadmap

Future additions:
- [ ] Memory game
- [ ] Music player
- [ ] Pomodoro timer
- [ ] Portfolio website generator
- [ ] More WordGuess categories and features

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Linh Dinh**

- GitHub: [@kinaskitaro](https://github.com/kinaskitaro)

## Acknowledgments

- Inspiration from various Python tutorials and coding challenges
- Asset credits for game sprites (see `Source/Assets/` folder)

---

**Happy Coding! 🐍**
