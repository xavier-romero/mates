# Mates

A fun math quiz game built in Python. Test your arithmetic skills by answering addition, subtraction, multiplication, and division questions to reach a target score. The game features dynamic scoring based on question difficulty and time penalties for slower responses.

## Features

- **Multiple Operations**: Supports addition (+), subtraction (-), multiplication (*), and division (/).
- **Adaptive Scoring**: Questions are scored based on difficulty (e.g., larger numbers or complex operations earn more points).
- **Time Penalties**: Answer quickly to avoid score deductions. Full score is awarded for answers within 5 seconds.
- **Retry Mechanism**: Incorrect answers are queued for retry after a few new questions.
- **Configurable**: Easily adjust operations, ranges, scores, and penalties via `config.py`.

## Installation

1. Ensure you have Python 3.x installed on your system.
2. Clone or download this repository.
3. No additional dependencies are required (uses only the Python standard library).

## Usage

Run the game by executing the main script:

```bash
python mates.py
```

The game will prompt you with math questions. Enter your answers as integers. Press Ctrl+C to exit at any time.

- Reach the target score (default: 2500) to win.
- View your progress and final statistics upon completion.

## Configuration

Edit `config.py` to customize the game:

- **OPERATIONS**: Define which operations to include, along with min/max ranges and base scores.
- **TIME_NO_PENALTY**: Time limit in seconds for full score.
- **PENALTY_PER_SECOND**: Score deduction per second over the limit.
- **TARGET_SCORE**: Score needed to complete the game.

Example configuration:
```python
OPERATIONS = {
    "+": {"min": 1, "max": 99, "score": 150},
    "-": {"min": 1, "max": 99, "score": 200},
    "*": {"min": 0, "max": 10, "score": 200},
    "/": {"min": 1, "max": 10, "score": 300},
}
```

## Contributing

Feel free to submit issues or pull requests to improve the game!

## License

This project is open-source. See LICENSE for details (if applicable).