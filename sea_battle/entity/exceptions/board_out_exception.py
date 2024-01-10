from entity.exceptions.board_exception import BoardException


class BoardOutException(BoardException):
    def __str__(self):
        return "Такой координаты не сущесвует на доске!"

