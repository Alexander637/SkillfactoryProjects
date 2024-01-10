from entity.board import Board
from random import randint
from entity.ship import Ship
from entity.dot import Dot
from entity.exceptions.board_wrong_ship_exception import BoardWrongShipException
from entity.artificial_intelligance import AI
from entity.user import User


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hide = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def try_board_create(self):
        ship_len_arr = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for i in ship_len_arr:
            while True:
                attempts += 1
                if attempts > 1000:
                    return None
                ship = Ship(Dot(randint(0, self.size - 1), randint(0, self.size - 1)), i, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass

        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board_create()
        return board

    @staticmethod
    def greet():
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def show_boards(self):
        print("-" * 20)
        print("Доска пользователя:")
        print(self.us.board)
        print("-" * 20)
        print("Доска компьютера:")
        print(self.ai.board)

    def loop(self):
        num = 0
        while True:
            self.show_boards()
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count_affected_ships == len(self.ai.board.ships):
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count_affected_ships == len(self.us.board.ships):
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()
