# Tic-Tac-Toe Reinforcement Learning

This project implements the classic Tic-Tac-Toe game, enhanced with Reinforcement Learning techniques. The agent learns optimal strategies through trial-and-error using concepts such as rewards and policies from the field of RL.

## Features
- Playable Tic-Tac-Toe game with a human-vs-agent mode.
- Implementation of basic RL concepts (e.g., policy, reward).
- Firebase integration for storing game data.

## Installation

### 1. Clone the repository
Clone the project repository to your local machine:
```bash
git clone https://github.com/ali-asanjarany/Tic-Tac-Toe-Reinforcement-Learning.git
cd Tic-Tac-Toe-Reinforcement-Learning
```

### 2. Install required dependencies
Install the dependencies listed in requirements.txt:

```bash
pip install -r requirements.txt
```
### 3. Run the game
To play the game, run the following command:

```bash
python main.py
```
## Prerequisites
- Python 3.8 or higher
- Firebase Admin SDK
## Project Structure

The project is organized as follows:


1. **`TicTacToe` Class**:
   - Manages the game board and logic.
   - Includes methods to:
     - Validate moves.
     - Check game status (win, tie, or continue).
     - Alternate turns between the player and the agent.

2. **`Agent` Class**:
   - Implements the reinforcement learning agent.
   - Uses Q-learning to improve decision-making over time.
   - Includes methods to:
     - Choose the best action using epsilon-greedy policy.
     - Update the value function based on rewards and transitions.
     - Save and load data from Firebase.

3. **`TextBasedGame` Class**:
   - Provides a text-based interface for the game.
   - Allows human players to compete against the agent via terminal.
   - Displays the game board and tracks scores.

4. **Firebase Integration**:
   - The project integrates with Firebase Realtime Database to:
     - Save the agent's learned value function.
     - Load existing values to continue improving the agent's performance.
   - A `firebase-credentials.json` file is required for authentication.

---

## How to Play

1. Run the game using the command `python main.py`.
2. Choose your move by entering the row and column number (e.g., `1, 2`).
3. The agent (X) will automatically make its move after you.
4. The game ends when one player wins or all cells are filled.

---

## Technologies Used

- **Python**: For the main game logic and agent implementation.
- **Tkinter**: For the graphical user interface (GUI) of the game.
- **Reinforcement Learning**: The agent uses Q-learning and other strategies to improve its moves over time.
- **Firebase**: Used for data storage (game statistics and user authentication).

---

## Learning Highlights

- **Policy and Reward**: The agent learns to choose optimal actions based on rewards.
- **Symmetry Handling**: Reducing redundant states to improve learning efficiency and reduce computation.
- **Exploration vs Exploitation**: Implementing strategies like epsilon-greedy to balance exploration and exploitation in the learning process.

---

## Contributing

Contributions are welcome! If you'd like to contribute, feel free to open issues or submit pull requests.

### Steps to contribute:

1. Fork this repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- Thanks to the contributors and developers who have helped in the development of Reinforcement Learning tools and libraries used in this project.
- Special thanks to the Firebase documentation for providing helpful resources to integrate Firebase with Python.
