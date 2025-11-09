#I acknowledge the use of CHATGPT-5 (https://chatgpt.com/) to create the code of this file 
# board.py

class Board:
    def __init__(self):
        self.cells = [' ' for _ in range(9)]

    def display(self):
        print("\n")
        for i in range(3):
            print(f" {self.cells[3*i]} | {self.cells[3*i+1]} | {self.cells[3*i+2]} ")
            if i < 2:
                print("---|---|---")
        print("\n")

    def update_cell(self, index, symbol):
        if self.cells[index] == ' ':
            self.cells[index] = symbol
            return True
        return False

    def is_full(self):
        return ' ' not in self.cells

    def check_winner(self, symbol):
        win_conditions = [
            [0,1,2], [3,4,5], [6,7,8],  # rows
            [0,3,6], [1,4,7], [2,5,8],  # columns
            [0,4,8], [2,4,6]            # diagonals
        ]
        return any(all(self.cells[i] == symbol for i in condition) for condition in win_conditions)
