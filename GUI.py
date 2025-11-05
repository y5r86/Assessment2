import tkinter as tk
from tkinter import messagebox

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.current_player = "X"
        self.board = [' ' for _ in range(9)]
        self.buttons = []

        self.status_label = tk.Label(root, text="Player X's turn", font=("Arial", 14))
        self.status_label.grid(row=0, column=0, columnspan=3, pady=10)

        self.create_board()
        self.restart_button = tk.Button(root, text="Restart", command=self.reset_game)
        self.restart_button.grid(row=4, column=0, columnspan=3, pady=10)

    def create_board(self):
        for i in range(9):
            button = tk.Button(self.root, text=' ', font=("Arial", 20), width=5, height=2,
                               command=lambda i=i: self.make_move(i))
            button.grid(row=1 + i // 3, column=i % 3)
            self.buttons.append(button)

    def make_move(self, index):
        if self.board[index] == ' ':
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)
            if self.check_winner(self.current_player):
                self.status_label.config(text=f"Player {self.current_player} wins!")
                self.disable_buttons()
            elif ' ' not in self.board:
                self.status_label.config(text="It's a draw!")
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.status_label.config(text=f"Player {self.current_player}'s turn")

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
        self.status_label.config(text="Player X's turn")
        for button in self.buttons:
            button.config(text=' ', state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()
