import termios
from sys import stdin
def getkey():
    old = termios.tcgetattr(stdin)
    new = termios.tcgetattr(stdin)
    new[3] = new[3] & ~termios.ICANON & ~termios.ECHO
    new[6][termios.VMIN] = 1
    new[6][termios.VTIME] = 0
    termios.tcsetattr(stdin, termios.TCSANOW, new)
    key = None
    try:
        key = stdin.read(1)
    finally:
        termios.tcsetattr(stdin, termios.TCSAFLUSH, old)
    return key

def display(board):
    print("".join([board[x*3:x*3+3]+"\n" for x in range(3)]))

def finished(board,turn):
    win = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for section in win:
        X = True
        O = True
        for pos in section:
            if board[pos]=="X":
                O = False
            if board[pos]=="O":
                X = False
            if board[pos]==".":
                O,X=False,False
        if X:
            if turn=="X":
                return ({""},{},{})
            else:
                return ({},{""},{})
        if O:
            if turn=="O":
                return ({""},{},{})
            else:
                return ({},{""},{})
    if board.count(".")==0:
        return ({},{},{""})
    return ""

def partitionMoves(board,free,t):
    turn = "O"
    if t: turn="X"

    finish = finished(board,turn)
    if finish != "":
        return finish

    good,bad,neutral=set(),set(),set()

    for x in free:
        newBoard = board[:x]+turn+board[x+1:]
        tmpGood,tmpBad,tmpNeut = partitionMoves(newBoard,free[:free.index(x)]+free[free.index(x)+1:],not t)
        if tmpGood:
            bad.add(x)
        elif tmpNeut:
            neutral.add(x)
        else:
            good.add(x)
    return good,bad,neutral

def play(board,turn):
    free = [idx for idx in range(len(board)) if board[idx]=="."]
    good,bad,neutral=partitionMoves(board,free,turn)
    if good:
        move = good.pop()
        if move=="":
            if turn:
                print("X won")
            else:
                print("O won")
            return("")
    elif neutral:
        move = neutral.pop()
        if move=="":
            print("tie")
    else:
        move = bad.pop()
        if move=="":
            if turn:
                print("O won")
            else:
                print("X won")
            return("")
    if turn:
        board = board[:move]+"X"+board[move+1:]
    else:
        board = board[:move]+"O"+board[move+1:]
    return board

import sys
if len(sys.argv)>1:
    board = sys.argv[1]
    if len(sys.argv)>2:
        human = sys.argv[2]
    else:
        human = "X"
else:
    board = "."*9
    human = "X"

#if turn is true its X, if false its O
turn = board.count("X")==board.count("O")

finish = finished(board,turn)
while finish=="":
    display(board)
    if turn == (human=="O"):
        p = play(board,turn)
        if p == "":
            break
        board = p
        turn = not turn
    else:
        print("move? ",end="",flush=True)
        pos = int(getkey())
        print(pos)
        while pos >= len(board) or board[pos]!=".":
            print("position must be empty and on the board")
            print("move? ",end="",flush=True)
            pos = int(getkey())
            print(pos)
        board = board[:pos]+human+board[pos+1:]
        turn = not turn
    finish = finished(board,turn)

display(board)

if finish[0]:
    if turn == (human=="X"):
        print("you won!")
    else:
        print("you lost :(")
elif finish[1]:
    if turn == (human=="O"):
        print("you won!")
    else:
        print("you lost :(")
else:
    print("it's a tie")
