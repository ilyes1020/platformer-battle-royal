# Platformer Battle Royale (Arduino controls included)
A 2D beat 'em up game where you battle multiple opponents and advance through challenging levels to become the ultimate champion.<br>
You can control the game using an Arduino joystick and a push button.<br>
It represents my first ever coding project. Built using Python and Pygame.
## Features
- Multiple levels with increasing difficulty
- Various enemy types
- Health
- Music and sound effects
- Arduino joystick and push button support
## Installation
1. Clone the repository
2. Install the required dependencies:
   ```bash
    pip install -r requirements.txt
   ```
### Optional: Arduino Joystick and Push Button Setup
3. Connect your Arduino joystick and push button to your computer.
4. Upload the Arduino code from the `Manette_projet2/Manette_projet2.ino` file to your Arduino board (using the Arduino IDE).
5. Install the joystick dependencies:
   ```bash
    pip install -r requirements_joystick.txt
   ```
6. Run the file `Joystick.py` to translate Arduino inputs to keyboard inputs:
   ```bash
    python Joystick.py
   ```
## Running the Game
Run the game using the following command:
```bash
python main.py
```
## Controls
All the controls are listed on the start screen.

