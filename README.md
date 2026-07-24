# Turtle Pong

A fun and competitive Pong game built with Python's Turtle graphics library! Play against an AI opponent and try to achieve the highest score.

## Overview

Turtle Pong is a classic Pong game where you control a paddle on the left side of the screen and compete against a computer-controlled AI opponent on the right. Rally the ball back and forth, earning points each time you hit the ball successfully. The game features three difficulty levels (Easy, Medium, and Hard) that affect ball speed and acceleration, making for increasingly challenging gameplay.

## What You Need

- Python 3.x
- The `turtle` module (included with standard Python installations)

## How to Run

To start the game, open your terminal and run:

```bash
python turtlepong.py
```

The game will launch in a new window. Click anywhere on the screen to begin.

## How to Play

### Controls

- **Move Up:** Press `W` or the `Up` Arrow key
- **Move Down:** Press `S` or the `Down` Arrow key
- **Start Game:** Click anywhere on the screen (after launching)
- **Play Again:** Press `R` after the game ends

### Game Mechanics

1. The ball starts at the center and moves toward either you or the AI
2. Use your paddle to hit the ball back to the opponent
3. You earn 1 point each time you successfully hit the ball
4. If the ball passes your paddle, the game ends
5. The ball's speed increases with each successful hit, making the game progressively harder
6. Try to get the highest score before missing!

### Difficulty Levels

When you start a game, you'll be prompted to choose a difficulty:

- **Easy (1):** Slower ball speed (starts at 4 pixels/frame, increases by 0.4)
- **Medium (2):** Moderate ball speed (starts at 5 pixels/frame, increases by 0.75) - *default*
- **Hard (3):** Fast ball speed (starts at 6 pixels/frame, increases by 1.1)

## Leaderboard

Your top 5 scores are automatically saved and displayed when the game ends. **Note:** Only scores from Hard mode are saved to the leaderboard, so challenge yourself on the hardest difficulty to make your mark!

## Game Features

- **Three Difficulty Levels:** Customize your gaming experience
- **AI Opponent:** Smart computer opponent with randomized movement
- **Score Tracking:** Keep track of your best performances
- **Leaderboard:** Compete against your own high scores (Hard mode only)
- **Smooth Graphics:** Powered by Python's Turtle graphics for retro fun

Enjoy the game and good luck beating your high scores!
