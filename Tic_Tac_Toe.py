# Import necessary libraries
import random
import requests
import json
import os

# Firebase configuration
FIREBASE_API_KEY = "AIzaSyChF6pviZ-a3BOHgoAcjSSqInAj_f8hcwM"
DATABASE_URL = "https://tic-tac-toe1999-default-rtdb.firebaseio.com"

class TicTacToe:
    def __init__(self
                 ):
        # Initialize the game board and the starting player
        self.board = ["-"] * 9  # 9 empty cells for the board
        self.current_player = "X"  # Starting player
        self.winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
    
    # Setting initial score for human and agent.
        self.agent_score = 0
        self.human_score = 0
        self.tie = 0

    def map_position(self, position):
        """ Map the input position (1-9) to the reversed board's index (0-8)."""
        mapping = [0, 1, 2, 3, 4, 5, 6, 7, 8]  # Mapping for reversed board
        if 0 <= position <= 8:  # Ensure position is within valid range
            return mapping[position]
        else:
            raise ValueError("Position out of range")

       
    def reset_board(self):
        """ Reset the game board for a new game. """
        self.board = ["-"] * 9
        self.current_player = "X"
    
    def make_move(self, position):
        """ Place the current player's symbol in the specified position. """
        mapped_position = self.map_position(position)  # Map the position to reversed board
        if self.board[mapped_position] == "-":
            self.board[mapped_position] = self.current_player
            return True
        return False

    def check_game_over(self):
        """ Check if the game has ended in a win or tie. """
        for combo in self.winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != "-":
                return "win"
        if "-" not in self.board:
            return "tie"
        return "play"
    
    def update_score(self):
        result = self.check_game_over()
        if result == "win":
            if self.current_player == "X":
                self.agent_score += 1
            else:
                self.human_score += 1
        elif result == "tie":
            self.tie  += 1

    def switch_player(self):
        """ Alternate between "X" and "O" for the current player. """
        self.current_player = "O" if self.current_player == "X" else "X"

    def display_board_text(self):
        # Display the board in text format (reversed)
        for i in range(6, -1, -3):  # Start from the bottom row (6-8) and move up
            print(f" {self.board[i]} | {self.board[i+1]} | {self.board[i+2]} ")
            if i > 0:
                print("-----------")


class Agent:
    def __init__(self, epsilon=0.1, alpha=0.5, gamma=0.9):
        # Learning parameters
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.value_function = {}
        
        # Load initial values from Firebase
        self.load_values_from_firebase()

    def get_state_value(self, state):
        # Get the value of a given state, defaulting to 0.5 if not seen
        return self.value_function.get(state, 0.5)

    def update_value(self, prev_state, reward, next_state):
        prev_value = self.get_state_value(prev_state)
        next_value = self.get_state_value(next_state)
        new_value = prev_value + self.alpha * (reward + self.gamma * next_value - prev_value)
        
        print(f"Updating state {prev_state} from {prev_value} to {new_value}")  # Debug print
        
        self.value_function[prev_state] = new_value
        self.update_value_in_firebase(prev_state, new_value)

    def choose_action(self, game):
        available_positions = [i for i, x in enumerate(game.board) if x == "-"]
        
        # Get current state before move
        current_state = "".join(game.board)
        print(f"Current state: {current_state}")  # Debug print

        if random.random() < self.epsilon:
            position = random.choice(available_positions)
        else:
            best_value = -float('inf')
            best_position = None
            
            for pos in available_positions:
                # Try the move
                game.board[pos] = game.current_player
                state = "".join(game.board)
                value = self.get_state_value(state)
                print(f"Considering position {pos} with value {value}")  # Debug print
                
                # Undo the move
                game.board[pos] = "-"
                
                if value > best_value:
                    best_value = value
                    best_position = pos
            
            position = best_position if best_position is not None else random.choice(available_positions)

        # Make the move and get new state
        game.board[position] = game.current_player
        new_state = "".join(game.board)
        
        # Update value function and Firebase
        reward = 0  # You can modify this based on game outcome
        self.update_value(current_state, reward, new_state)
        
        # Undo the move (since the actual game will make it)
        game.board[position] = "-"
        
        return position

    def update_value_in_firebase(self, state, value):
        try:
            # Using REST API with API Key
            url = f"{DATABASE_URL}/tic_tac_toe_values/{state}.json?auth={FIREBASE_API_KEY}"
            response = requests.put(url, json=value)
            
            if response.status_code == 200:
                print(f"Successfully updated state {state} with value {value}")
            else:
                print(f"Failed to update Firebase: {response.text}")
                
        except Exception as e:
            print(f"Error updating Firebase: {str(e)}")

    def load_values_from_firebase(self):
        try:
            # Using REST API with API Key
            url = f"{DATABASE_URL}/tic_tac_toe_values.json?auth={FIREBASE_API_KEY}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    self.value_function = {state: float(value) for state, value in data.items()}
                    print(f"Loaded {len(self.value_function)} states from Firebase")
                else:
                    print("No existing values found in Firebase")
            else:
                print(f"Failed to load from Firebase: {response.text}")
                
        except Exception as e:
            print(f"Error loading from Firebase: {str(e)}")

class TextBasedGame:
    def __init__(self):
        self.game = TicTacToe()
        self.agent = Agent()
        # Predefined messages
        self.messages = {
            "win": [
                "Congratulations! You won! 🎉 Ready for the next round?",
                "Amazing victory! 👏 Let’s see how you do in the next round!",
                "You’re the master of this game! 😎 Shall we start again?",
            ],
            "lose": [
                "The Agent won this time, but you can do better in the next round! 💪",
                "The Agent claimed this round, but you’re getting stronger! 🤖 Ready for a rematch?",
                "Don’t worry, losing is part of the journey! 🌟 The next round is yours!",
            ],
            "tie": [
                "It’s a draw! 🤝 Let’s try again!",
                "You tied! Looks like it’s a close match! 😄 Ready for another round?",
                "Great match! Let’s see what happens in the next round! 🚀",
            ],
        }

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def start_game(self):
        while True:
            self.clear_screen()
            print(f"\nScore - Human (O): {self.game.human_score}  Agent (X): {self.game.agent_score}  Tie: {self.game.tie}\n")
            self.game.display_board_text()

            if self.game.current_player == "X":
                print("\nAgent's turn...")
                position = self.agent.choose_action(self.game)
                self.game.make_move(position)
            else:
                while True:
                    try:
                        print("\nYour turn! Enter position (1-9): ")
                        print("Board positions are numbered like this:")
                        print(" 7 | 8 | 9 ")
                        print("-----------")
                        print(" 4 | 5 | 6 ")
                        print("-----------")
                        print(" 1 | 2 | 3 ")
                        
                        position = int(input()) - 1  # User input (1-9)
                        mapped_position = self.game.map_position(position)  # Map position for reversed board
                        if 0 <= mapped_position <= 8 and self.game.make_move(position):
                            break
                        print("Invalid move! Try again.")
                    except ValueError:
                        print("Please enter a number between 1 and 9!")

            result = self.game.check_game_over()
            if result == "win":
                if self.game.current_player == "O":
                    self.display_message("win")  # Player won
                else:
                    self.display_message("lose")  # Agent won
                self.clear_screen()
                self.game.display_board_text()
                winner = "Human" if self.game.current_player == "O" else "Agent"
                print(f"\n{winner} wins!")
                self.game.update_score()
                self.play_again()
                break
            elif result == "tie":
                self.clear_screen()
                self.game.display_board_text()
                print("\nIt's a tie!")
                self.display_message("tie")
                self.game.update_score()
                self.play_again()
                break

            self.game.switch_player()

    def display_message(self, result):
        """ Display a random message based on the game outcome. """
        print("\n" + random.choice(self.messages[result]))

    def play_again(self):
        while True:
            choice = input("\nPlay again? (y/n): ").lower()
            if choice == 'y':
                self.game.reset_board()
                self.start_game()
                break
            elif choice == 'n':
                print("\nThanks for playing!")
                break
            else:
                print("Please enter 'y' or 'n'")

if __name__ == "__main__":
    game = TextBasedGame()
    game.start_game()