import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")

        # Player info
        self.player1 = ""
        self.player2 = ""
        self.current_player = "X"
        self.board = [' ' for _ in range(9)]
        self.buttons = []

        # Add a flag to determine if Player 2 is a bot
        self.bot_enabled = True  # Set to True for Bot, or adjust as you like

        # Show start screen first
        self.show_start_screen()

    def show_start_screen(self):
        """Display player name entry screen before starting the game."""
        self.start_frame = tk.Frame(self.root)
        self.start_frame.pack(pady=20)

        tk.Label(self.start_frame, text="Enter Player 1 name (X):", font=("Arial", 12)).grid(row=0, column=0, pady=5)
        self.player1_entry = tk.Entry(self.start_frame, font=("Arial", 12))
        self.player1_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.start_frame, text="Enter Player 2 name (O):", font=("Arial", 12)).grid(row=1, column=0, pady=5)
        self.player2_entry = tk.Entry(self.start_frame, font=("Arial", 12))
        self.player2_entry.grid(row=1, column=1, pady=5)

        # Bot checkbox
        self.bot_var = tk.IntVar(value=1)
        bot_checkbox = tk.Checkbutton(self.start_frame, text="Play against Bot (O)", variable=self.bot_var)
        bot_checkbox.grid(row=2, column=0, columnspan=2, pady=5)

        start_button = tk.Button(self.start_frame, text="Start Game", font=("Arial", 12), command=self.start_game)
        start_button.grid(row=3, column=0, columnspan=2, pady=10)

    def start_game(self):
        """Initialize the game after players enter their names."""
        self.player1 = self.player1_entry.get().strip() or "Player 1"
        self.player2 = self.player2_entry.get().strip() or "Player 2"
        self.bot_enabled = self.bot_var.get() == 1

        # Hide start screen
        self.start_frame.destroy()

        # Create game board
        self.status_label = tk.Label(self.root, text=f"{self.player1}'s (X) turn", font=("Arial", 14))
        self.status_label.grid(row=0, column=0, columnspan=3, pady=10)

        self.create_board()

        self.restart_button = tk.Button(self.root, text="Restart", font=("Arial", 12), command=self.reset_game)
        self.restart_button.grid(row=4, column=0, columnspan=3, pady=10)

        # If bot starts and is O, do nothing; otherwise, if bot is X and player2 is bot, start with bot
        if self.current_player == "O" and self.bot_enabled:
            self.root.after(500, self.perform_bot_move)  # Extra handling if bot is X, not needed here

    def create_board(self):
        """Create the 3x3 board buttons."""
        for i in range(9):
            button = tk.Button(self.root, text=' ', font=("Arial", 20), width=5, height=2,
                               command=lambda i=i: self.make_move(i))
            button.grid(row=1 + i // 3, column=i % 3)
            self.buttons.append(button)

    def make_move(self, index):
        # Human move only
        if self.board[index] == ' ' and (
            (self.current_player == "X") or
            (self.current_player == "O" and not self.bot_enabled)
        ):
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)

            if self.check_winner(self.current_player):
                winner = self.player1 if self.current_player == "X" else self.player2
                self.status_label.config(text=f"{winner} ({self.current_player}) wins!")
                self.disable_buttons()
            elif ' ' not in self.board:
                self.status_label.config(text="It's a draw!")
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                # Change status: indicate bot is thinking instead of always showing Player 2 name
                if self.bot_enabled and self.current_player == "O":
                    self.status_label.config(text="Bot is thinking...")
                    self.root.after(800, self.perform_bot_move)
                else:
                    next_player = self.player1 if self.current_player == "X" else self.player2
                    self.status_label.config(text=f"{next_player}'s ({self.current_player}) turn")

    def perform_bot_move(self):
        available_moves = [i for i, mark in enumerate(self.board) if mark == ' ']
        if not available_moves or self.current_player != "O":
            return
        move = random.choice(available_moves)
        self.board[move] = self.current_player
        self.buttons[move].config(text=self.current_player)

        if self.check_winner(self.current_player):
            winner = self.player1 if self.current_player == "X" else self.player2
            self.status_label.config(text=f"{winner} ({self.current_player}) wins!")
            self.disable_buttons()
        elif ' ' not in self.board:
            self.status_label.config(text="It's a draw!")
        else:
            self.current_player = 'X'
            # Always player 1's turn after bot
            self.status_label.config(text=f"{self.player1}'s (X) turn")

    def check_winner(self, symbol):
        win_conditions = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        return any(all(self.board[i] == symbol for i in condition) for condition in win_conditions)

    def disable_buttons(self):
        for button in self.buttons:
            button.config(state=tk.DISABLED)

    def reset_game(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = "X"
        self.status_label.config(text=f"{self.player1}'s (X) turn")
        for button in self.buttons:
            button.config(text=' ', state=tk.NORMAL)
        # Bot may start as O, so nothing extra needed

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()
