#I acknowledge the use of CHATGPT-5 (https://chatgpt.com/) to create the code of this file
# player.py

class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def get_move(self):
        while True:
            try:
                move = int(input(f"{self.name} ({self.symbol}), enter your move (1-9): ")) - 1
                if move in range(9):
                    return move
                else:
                    print("Invalid input. Choose a number between 1 and 9.")
            except ValueError:
                print("Invalid input. Please enter a number.")
