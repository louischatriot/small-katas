from time import time




def find(board, letter):
    for x, line in enumerate(board):
        for y, c in enumerate(line):
            if c == letter:
                return (x, y)


# Modify board and list in place ; always moving right and bottom (max grid size small)
def move_line(board, res, x, _from, _to):
    n = (_to - _from) % len(board[0])

    for _ in range(0, n):
        res.append('R' + str(x))
        board[x] = [board[x][-1]] + board[x][0:len(board[x])-1]


def move_column(board, res, y, _from, _to):
    n = (_to - _from) % len(board)

    for _ in range(0, n):
        res.append('D' + str(y))
        swp = board[-1][y]
        for x in range(len(board) - 2, -1, -1):
            board[x+1][y] = board[x][y]
        board[0][y] = swp



# print('\n'.join([''.join(l) for l in mixed_up_board]))


def loopover(mixed_up_board, solved_board):
    res = []

    N = len(mixed_up_board)
    M = len(mixed_up_board[0])


    print('\n'.join([''.join(l) for l in mixed_up_board]))
    print("===============================")


    # Manually do first line and first column
    l = solved_board[0][0]
    xt, yt = find(mixed_up_board, l)
    move_line(mixed_up_board, res, xt, yt, 0)
    move_column(mixed_up_board, res, 0, xt, 0)

    l = solved_board[0][1]
    xt, yt = find(mixed_up_board, l)
    move_line(mixed_up_board, res, xt, yt, 1)
    move_column(mixed_up_board, res, 1, xt, 0)


    print('\n'.join([''.join(l) for l in mixed_up_board]))
    print("===============================")


    # Forbidden box
    bx, by = 0, 1


    while True:
        if bx < N - 2:
            bx += 1



            for y in range(0, by+1):
                l = solved_board[bx][y]
                xt, yt = find(mixed_up_board, l)

                if xt == bx:
                    pass
                    # TO BE TESTED!
                    # move_line(mixed_up_board, res, bx, yt, by + 1)
                    # move_column(mixed_up_board, res, by+1, xt, xt + 1)
                    # move_line(mixed_up_board, res, bx, by + 1, yt)
                    # move_column(mixed_up_board, res, by+1, xt + 1, xt)
                    # move_line(mixed_up_board, res, bx, by, by - 1)
                elif xt < bx:
                    # yt must be strictly higher than by
                    move_column(mixed_up_board, res, yt, xt, bx+1)
                    move_line(mixed_up_board, res, bx+1, yt, by+1)
                    move_column(mixed_up_board, res, by+1, bx+1, bx)
                    move_line(mixed_up_board, res, bx, by+1, by)


                elif xt > bx:
                    move_line(mixed_up_board, res, xt, yt, by + 1)
                    move_column(mixed_up_board, res, by + 1, xt, bx)
                    move_line(mixed_up_board, res, bx, by, by - 1)

            print('\n'.join([''.join(l) for l in mixed_up_board]))
            print("===============================")






        1/0




    # print(mixed_up_board)

    # print(find(mixed_up_board, "A"))


    # move_line(mixed_up_board, res, 1)

    # print('\n'.join([''.join(l) for l in mixed_up_board]))
    # print(res)

    # move_column(mixed_up_board, res, 3)

    # print('\n'.join([''.join(l) for l in mixed_up_board]))
    # print(res)

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




