# game.py

from Board import Board
from Player import Player

class Game:
    def __init__(self):
        self.board = Board()
        player1_name= input("Please enter the name of player 1 (playing X): ")
        player2_name= input("Please enter the name of player 2 (playing O): ")
        self.player1 = Player(player1_name, "X")
        self.player2 = Player(player2_name, "O")
        self.current_player = self.player1

    def switch_player(self):
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2

    def play(self):
        print("Welcome to Tic Tac Toe!")
        self.board.display()

        while True:
            move = self.current_player.get_move()
            if self.board.update_cell(move, self.current_player.symbol):
                self.board.display()
                if self.board.check_winner(self.current_player.symbol):
                    print(f"{self.current_player.name} wins!")
                    break
                elif self.board.is_full():
                    print("It's a draw!")
                    break
                self.switch_player()
            else:
                print("Cell already taken. Try again.")
