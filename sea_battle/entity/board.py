from entity.dot import Dot
from entity.exceptions.board_wrong_ship_exception import BoardWrongShipException
from entity.exceptions.board_out_exception import BoardOutException
from entity.exceptions.board_used_exception import BoardUsedException


class Board:
    def __init__(self, hide=False, size=6) -> None:
        self.hide = hide
        self.size = size

        self.count_affected_ships = 0

        self.field = [["0"] * size for _ in range(size)]

        self.busy_ships = []
        self.ships = []

    def __str__(self):
        res_field = ""
        res_field += f"  | {' | '.join(map(str, range(1, self.size + 1)))} |"
        for i, j in enumerate(self.field):
            res_field += f"\n{i + 1} | " + " | ".join(j) + " | "

        if self.hide:
            res_field = res_field.replace("■", "0")

        return res_field

    def out_of_field(self, dot):
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                current = Dot(d.x + dx, d.y + dy)
                if not (self.out_of_field(current)) and current not in self.busy_ships:
                    if verb:
                        self.field[current.x][current.y] = "."
                    self.busy_ships.append(current)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out_of_field(d) or d in self.busy_ships:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy_ships.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, dot):
        if self.out_of_field(dot):
            raise BoardOutException()
        if dot in self.busy_ships:
            raise BoardUsedException()

        self.busy_ships.append(dot)

        for ship in self.ships:
            if ship.hit(dot):
                ship.ship_lives -= 1
                self.field[dot.x][dot.y] = "X"
                if ship.ship_lives == 0:
                    self.count_affected_ships += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[dot.x][dot.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.busy_ships = []
