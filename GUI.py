import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Pillow library for image handling
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
        self.bot_enabled = True  # Default

        # Show start screen first
        self.show_start_screen()

    def show_start_screen(self):
        """Display player name entry screen before starting the game."""
        self.start_frame = tk.Frame(self.root, bg="#222831")
        self.start_frame.pack(pady=30, padx=30, fill="both", expand=True)

        # Load and display game logo
        try:
            image = Image.open("1021366.png")
            image = image.resize((200, 200))  # Resize to fit nicely
            self.logo = ImageTk.PhotoImage(image)
            logo_label = tk.Label(self.start_frame, image=self.logo, bg="#222831")
            logo_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))
        except Exception as e:
            print(f"Image load error: {e}")

        # Labels and entries with styling
        label_style = {"bg": "#222831", "fg": "white", "font": ("Arial", 12, "bold")}
        entry_style = {"font": ("Arial", 12), "bg": "#eeeeee", "bd": 2}

        tk.Label(self.start_frame, text="Enter Player 1 name (X):", **label_style).grid(row=1, column=0, pady=5, sticky="e")
        self.player1_entry = tk.Entry(self.start_frame, **entry_style)
        self.player1_entry.grid(row=1, column=1, pady=5, padx=10)

        tk.Label(self.start_frame, text="Enter Player 2 name (O):", **label_style).grid(row=2, column=0, pady=5, sticky="e")
        self.player2_entry = tk.Entry(self.start_frame, **entry_style)
        self.player2_entry.grid(row=2, column=1, pady=5, padx=10)

        # Bot checkbox
        self.bot_var = tk.IntVar(value=1)
        bot_checkbox = tk.Checkbutton(
            self.start_frame,
            text="Play against Bot (O)",
            variable=self.bot_var,
            bg="#222831",
            fg="white",
            font=("Arial", 12, "bold"),
            activebackground="#222831",
            activeforeground="white",
            selectcolor="#393E46"
        )
        bot_checkbox.grid(row=3, column=0, columnspan=2, pady=10)

        # Start button
        start_button = tk.Button(
            self.start_frame,
            text="Start Game",
            font=("Arial", 13, "bold"),
            bg="#00ADB5",
            fg="white",
            activebackground="#008B8F",
            activeforeground="white",
            relief="flat",
            width=15,
            command=self.start_game
        )
        start_button.grid(row=4, column=0, columnspan=2, pady=20)

    def start_game(self):
        """Initialize the game after players enter their names."""
        self.player1 = self.player1_entry.get().strip() or "Player 1"
        self.player2 = self.player2_entry.get().strip() or "Player 2"
        self.bot_enabled = self.bot_var.get() == 1

        # Hide start screen
        self.start_frame.destroy()

        # Create game board
        self.status_label = tk.Label(self.root, text=f"{self.player1}'s (X) turn", font=("Arial", 14), bg="#222831", fg="white")
        self.status_label.grid(row=0, column=0, columnspan=3, pady=10)

        self.create_board()

        self.restart_button = tk.Button(
            self.root, text="Restart", font=("Arial", 12, "bold"),
            bg="#00ADB5", fg="white", activebackground="#008B8F",
            relief="flat", command=self.reset_game
        )
        self.restart_button.grid(row=4, column=0, columnspan=3, pady=10)

    def create_board(self):
        """Create the 3x3 board buttons."""
        for i in range(9):
            button = tk.Button(
                self.root, text=' ', font=("Arial", 20, "bold"),
                width=5, height=2, bg="#393E46", fg="white",
                activebackground="#00ADB5", relief="flat",
                command=lambda i=i: self.make_move(i)
            )
            button.grid(row=1 + i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(button)

    def make_move(self, index):
        if self.board[index] == ' ' and (
            (self.current_player == "X") or
            (self.current_player == "O" and not self.bot_enabled)
        ):
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)

            if self.check_winner(self.current_player):
                winner = self.player1 if self.current_player == "X" else self.player2
                self.status_label.config(text=f"{winner} ({self.current_player}) wins!", fg="#00FFAB")
                self.disable_buttons()
            elif ' ' not in self.board:
                self.status_label.config(text="It's a draw!", fg="#FFD369")
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                if self.bot_enabled and self.current_player == "O":
                    self.status_label.config(text="Bot is thinking...", fg="#EEEEEE")
                    self.root.after(800, self.perform_bot_move)
                else:
                    next_player = self.player1 if self.current_player == "X" else self.player2
                    self.status_label.config(text=f"{next_player}'s ({self.current_player}) turn", fg="white")

    def perform_bot_move(self):
        available_moves = [i for i, mark in enumerate(self.board) if mark == ' ']
        if not available_moves or self.current_player != "O":
            return
        move = random.choice(available_moves)
        self.board[move] = self.current_player
        self.buttons[move].config(text=self.current_player)

        if self.check_winner(self.current_player):
            self.status_label.config(text="Bot (O) wins!", fg="#FF4C29")
            self.disable_buttons()
        elif ' ' not in self.board:
            self.status_label.config(text="It's a draw!", fg="#FFD369")
        else:
            self.current_player = 'X'
            self.status_label.config(text=f"{self.player1}'s (X) turn", fg="white")

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
        self.status_label.config(text=f"{self.player1}'s (X) turn", fg="white")
        for button in self.buttons:
            button.config(text=' ', state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#222831")
    game = TicTacToeGUI(root)
    root.mainloop()
