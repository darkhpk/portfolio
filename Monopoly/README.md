# Monopoly Game

A Python implementation of the classic Monopoly board game using Pygame.

## Features

- **4 Players**: The game supports 4 players with different colored tokens (Red, Green, Blue, Yellow)
- **Animated Dice Rolling**: Watch an exciting dice animation showing random values before revealing your actual roll
- **Improved Game Flow**: Move first, then decide your action - more control over your turn
- **Gap-Free Board**: Perfectly aligned board squares with no gaps at corners
- **Full Board**: Complete Monopoly board with 40 spaces including:
  - Properties with color groups
  - Railroads
  - Utilities (Electric Company, Water Works)
  - Special spaces (Go, Jail, Free Parking, Go to Jail, Income Tax, Luxury Tax)
  - Chance and Community Chest spaces
- **Property Management**:
  - Buy properties from the bank
  - Pay rent to other players
  - Build houses and hotels on complete color sets
  - Trade properties between players
  - Buy properties from other players
  - Sell properties back to the bank
- **Game Mechanics**:
  - Visual dice rolling animation
  - Player balance tracking
  - Jail mechanics
  - Property ownership visualization
  - On-screen action prompts and help text

## Requirements

- Python 3.x
- Pygame

## Installation

1. Clone or download this repository
2. Create a virtual environment (recommended):
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   pip install pygame
   ```

## How to Run

```powershell
python main.py
```

## Controls

- **SPACE**: Roll the dice with animation and move your piece
- **B**: Buy the property you landed on (after moving)
- **R**: Pay rent on the property you landed on (after moving)
- **H**: Build houses/hotels on your property (after moving, if you own the complete color set)
- **N**: End your turn and pass to the next player
- **T**: Trade properties with another player (before rolling)
- **P**: Buy a property from another player (before rolling)
- **S**: Sell a property to the bank (before rolling)
- **Y/N**: Confirm or decline during property transactions
- **ESC**: Cancel current action
- **1-4**: Select properties during trade/buy/sell operations

## Game Flow

Each turn follows this sequence:
1. **Roll Dice**: Press SPACE to see an animated dice roll
2. **Auto-Move**: Your piece automatically moves to the new position
3. **Take Action**: Based on where you land:
   - **Unowned Property**: Press B to buy or N to skip
   - **Enemy Property**: Press R to pay rent, then N for next turn
   - **Your Property**: Press H to build (if you own the color set) or N to skip
   - **Special Space**: Follow the on-screen instructions, then press N
4. **Next Player**: Press N to end your turn

## Game Rules

1. **Starting the Game**: Each player starts with £1500 and is placed on "Go"
2. **Rolling Dice**: Press SPACE to watch an animated dice roll that shows your result
3. **Movement**: Your token automatically moves to the new position after rolling
4. **Landing on Properties**:
   - **Unowned**: Press B to buy it for the listed price, or N to skip
   - **Owned by Another Player**: Press R to pay rent to the owner
   - **Your Own Property**: Press H to build houses/hotels (if you own all properties in the color group)
5. **Building**: Once you own all properties in a color group, you can build up to 4 houses or 1 hotel
6. **Special Spaces**:
   - **Go**: Collect £200 when landing on it
   - **Income Tax**: Pay £200
   - **Luxury Tax**: Pay £100
   - **Jail**: Just visiting (no penalty)
   - **Go to Jail**: Move directly to jail
   - **Free Parking**: No action required
   - **Chance/Community Chest**: Draw a card (press SPACE to continue)
7. **Jail Mechanics**: If you're in jail, you must roll doubles to get out
8. **Trading**: Before rolling, you can trade (T), buy from players (P), or sell to bank (S)

## Project Structure

```
Monopoly/
├── main.py           # Main game file with all game logic
├── board.py          # Legacy board sprite class (not used)
├── player.py         # Legacy player class (not used)
├── property.py       # Empty file (not used)
├── media/            # Game assets
│   ├── center_image.jpeg
│   └── images.jpeg
└── README.md         # This file
```

## Notes

- The game currently doesn't have a win/lose condition implemented
- Bankruptcy mechanics are not fully implemented
- The game displays player money on the board at all times
- Property ownership is shown by coloring the property square with the owner's color

## Future Enhancements

Potential features to add:
- Bankruptcy detection and player elimination
- Full Chance and Community Chest card implementation
- AI opponents
- Save/Load game functionality
- Sound effects and music
- Improved UI with property cards
- Game statistics and history

## Credits

Created as a portfolio project demonstrating:
- Python programming
- Pygame library usage
- Game logic implementation
- Object-oriented programming
