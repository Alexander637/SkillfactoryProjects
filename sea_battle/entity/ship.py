from entity.dot import Dot


class Ship:
    def __init__(self, bow, ship_length, orientation):
        self.bow = bow
        self.ship_length = ship_length
        self.orientation = orientation
        self.ship_lives = ship_length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.ship_length):
            current_x = self.bow.x
            current_y = self.bow.y

            if self.orientation == 0:
                current_x += i

            elif self.orientation == 1:
                current_y += i

            ship_dots.append(Dot(current_x, current_y))

        return ship_dots

    def hit(self, shot):
        return shot in self.dots
