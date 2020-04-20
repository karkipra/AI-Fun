# Tic Tac Toe Python Game

board = [' ' for x in range(10)]

WON = False
PLAYER = 'X'
COMPUTER = 'O'


def insertLetter(letter, pos):
    board[pos] = letter


def removeLetter(pos):
    board[pos] = ' '


def spaceIsFree(pos):
    return board[pos] == ' '


def printBoard():
    # "board" is a list of 10 strings representing the board (ignore index 0)
    print('   |   |')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('   |   |')


def isWinner(bo, le):
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or  # across the top
            (bo[4] == le and bo[5] == le and bo[6] == le) or  # across the middle
            (bo[1] == le and bo[2] == le and bo[3] == le) or  # across the bottom
            (bo[7] == le and bo[4] == le and bo[1] == le) or  # down the left side
            (bo[8] == le and bo[5] == le and bo[2] == le) or  # down the middle
            (bo[9] == le and bo[6] == le and bo[3] == le) or  # down the right side
            (bo[7] == le and bo[5] == le and bo[3] == le) or  # diagonal
            (bo[9] == le and bo[5] == le and bo[1] == le))  # diagonal


scores = {COMPUTER: 10, PLAYER: -10}


def minimax(board, depth, isMaximizing):
    # get the current player
    currPlayer = COMPUTER if isMaximizing else PLAYER

    # check if base cases are met
    if isWinner(board, currPlayer):
        return scores[currPlayer]
    if isBoardFull(board):
        return 0

    bestScore = -10000 if isMaximizing else 10000

    for index in range(len(board)):
        if 0 < index < 10 and spaceIsFree(index):
            insertLetter(currPlayer, index)
            if isMaximizing:
                score = minimax(board, depth + 1, False)
                bestScore = max(score, bestScore)
            else:
                score = minimax(board, depth + 1, True)
                bestScore = min(score, bestScore)
            removeLetter(index)
    return bestScore


def compMove():
    bestScore = -10000
    bestIndex = 0
    for index in range(len(board)):
        if 0 < index < 10 and spaceIsFree(index):
            insertLetter(COMPUTER, index)
            score = minimax(board, 0, False)
            if (score > bestScore):
                bestScore = score
                bestIndex = index
            removeLetter(index)
    return bestIndex


def playerMove():
    run = True

    while run:
        move = input('Please select position (1-9) to place an \'%s\': ' % PLAYER)
        try:
            move = int(move)
            if 0 < move and move < 10:
                if spaceIsFree(move):
                    run = False
                    insertLetter(PLAYER, move)
                else:
                    print('Sorry, this space is occupied')
            else:
                print('Please type number between 1-9')
        except:
            print('Please type a value number')


def isBoardFull(board):
    return board.count(' ') <= 1


if __name__ == '__main__':

    firstTime = True

    while True:

        print('Welcome!')
        printBoard()

        while not (isBoardFull(board)):

            if isWinner(board, COMPUTER):  # Computer wins
                print('Sorry, %s\'s won this time' % COMPUTER)
                WON = True
                break
            else:
                playerMove()
                printBoard()

            if isWinner(board, PLAYER):  # Player wins
                print('Yay, %s\'s won this time. Good job!' % PLAYER)
                WON = True
                break
            else:
                move = compMove()
                if move == 0:
                    break;
                else:
                    insertLetter(COMPUTER, move)
                    print('Computer places an \'%s\' in position %s' % (COMPUTER, move))
                    printBoard()

        if not WON and isBoardFull(board):
            print('Tie Game!')

        answer = input('Do you want to play again? (Y/N)')
        if answer.lower() == 'y' or answer.lower == 'yes':
            board = [' ' for x in range(10)]
            print('-----------------------------------')
        else:
            break
