from time import time




def find(board, letter):
    for x, line in enumerate(board):
        for y, c in enumerate(line):
            if c == letter:
                return (x, y)


# Modify board and list in place ; always moving right and bottom (max grid size small)
def move_line(board, res, x):
    res.append('R' + str(x))
    board[x] = [board[x][-1]] + board[x][0:len(board[x])-1]


def move_column(board, res, y):
    res.append('D' + str(y))
    swp = board[-1][y]
    for x in range(len(board) - 2, -1, -1):
        board[x+1][y] = board[x][y]
    board[0][y] = swp



# print('\n'.join([''.join(l) for l in mixed_up_board]))


def loopover(mixed_up_board, solved_board):
    res = []

    bx, by = 0, 0

    print('\n'.join([''.join(l) for l in mixed_up_board]))
    print(mixed_up_board)

    print(find(mixed_up_board, "A"))


    move_line(mixed_up_board, res, 1)

    print('\n'.join([''.join(l) for l in mixed_up_board]))
    print(res)

    move_column(mixed_up_board, res, 3)

    print('\n'.join([''.join(l) for l in mixed_up_board]))
    print(res)


    return None


def to_board(str):
    return [list(row) for row in str.split('\n')]


mixed_up_board = to_board('CWMFJ\nORDBA\nNKGLY\nPHSVE\nXTQUI')
solved_board = to_board('ABCDE\nFGHIJ\nKLMNO\nPQRST\nUVWXY')


start = time()

res = loopover(mixed_up_board, solved_board)

print(res)
print("==> Duration:", time() - start)




