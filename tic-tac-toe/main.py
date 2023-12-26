def hi_tic_tac_toe():
    print("Добро пожаловать в игру крестики-нолики!")
    print("------------------------------------------------")
    print("Ввод данных осуществляется по координатам: x, y")
    print("x - по горизонтали")
    print("y - по вертикали")
    print("------------------------------------------------")
    print("")


def show_field(row_column_num):
    print(f"  |  {'  |  '.join(map(str, range(row_column_num)))}  |")
    print("-------" * row_column_num)
    for i, j in enumerate(field):
        print(f"{i} | {" | ".join(j)} | ")
        print("-------" * row_column_num)


def ask(row_column_num):
    while True:
        try:
            x = int(input("Введите координату x: "))
            y = int(input("Введите координату y: "))
            if 0 <= x < row_column_num and 0 <= y < row_column_num:
                if field[x][y] == " - ":
                    return x, y
                else:
                    print("Клетка занята")
            else:
                print("Не верный ввод координат")

        except ValueError:
            print("Ошибка! Введите целое число от 0 до 2.")


def win_check(array):
    for i in range(len(array)):
        symbols = []
        for j in range(len(array[i])):
            symbols.append(array[i][j])
        if all(symbol == " X " for symbol in symbols):
            print("Выиграли крестики!")
            return True
        elif all(symbol == " 0 " for symbol in symbols):
            print("Выиграли нолики!")
            return True

    for i in range(len(array)):
        symbols = []
        for j in range(len(array[i])):
            symbols.append(array[j][i])
        if all(symbol == " X " for symbol in symbols):
            print("Выиграли крестики!")
            return True
        elif all(symbol == " 0 " for symbol in symbols):
            print("Выиграли нолики!")
            return True

    symbols = []
    for i in range(len(array)):
        symbols.append(array[i][i])
    if all(symbol == " X " for symbol in symbols):
        print("Выиграли крестики!")
        return True
    elif all(symbol == " 0 " for symbol in symbols):
        print("Выиграли нолики!")
        return True

    symbols = []
    for i in range(len(array)):
        symbols.append(array[i][len(array) - 1 - i])
    if all(symbol == " X " for symbol in symbols):
        print("Выиграли крестики!")
        return True
    elif all(symbol == " 0 " for symbol in symbols):
        print("Выиграли нолики!")
        return True


hi_tic_tac_toe()
print("Выберите формат поля:")
print("Для выбора поля 3х3 введите цифру 3")
print("Для выбора поля 5х5 введите цифру 5")

while True:
    try:
        rows_columns_amount = int(input("Введите цифру для выбора:"))
        if rows_columns_amount == 3 or rows_columns_amount == 5:
            break
        else:
            print("Поле такого формата не предусмотрено в данной игре")
            print("------------------------------------------------")
    except ValueError:
        print("Ошибка! Введите целое число 3 или 5.")

field = [[" - "] * rows_columns_amount for i in range(rows_columns_amount)]
move_number = 0

while True:
    move_number += 1
    show_field(rows_columns_amount)
    if move_number % 2 == 1:
        print("Ходит крестик")
        x, y = ask(rows_columns_amount)
        field[x][y] = " X "
    else:
        print("Ходит нолик")
        x, y = ask(rows_columns_amount)
        field[x][y] = " 0 "
    if win_check(field):
        show_field(rows_columns_amount)
        break
    if move_number == rows_columns_amount ** 2:
        print("Ничья")
        break
