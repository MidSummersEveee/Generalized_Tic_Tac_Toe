import random
import math
import numpy as np

class DrawTicTacToe:
    # class to represent a game

    # scale parameters and board initializer
    def __init__(self, scale, combo):
        self.scale = scale
        self.combo = combo
        self.board = [[" " for x in range(self.scale)] for y in range(self.scale)]
        self.game_winner = ''

        print(f'New game created with a scale of {scale} and a combo of {combo}.')

    # function to display the board of the game
    def printboard(self):
        [[print(self.board[x][y], end=' ') if y < self.scale - 1 else print(self.board[x][y]) for y in range(self.scale)] for x in range(self.scale)]

    # function to place a stone at a given positioon
    def move(self, x, y, player):
        self.board[x][y] = player

    # function to perform generalized row check
    def check_general_rows(self, rows, player):
        current_player = " "
        for row in rows:
            for index, place in enumerate(row):
                check_space = []

                begin = 0
                while len(check_space) < self.combo:
                    if index + begin <= len(row) - 1:
                        if row[index + begin] == player:
                            check_space.append(row[index + begin])
                            begin = begin + 1
                        else:
                            break
                    else:
                        break

                if len(check_space) == self.combo:
                    current_player = player
                    return current_player
        return current_player

    # function to see if we have a winner
    def whowins(self):

        for player in ["X", "O"]:
            # check horizontal
            current_player1 = self.check_general_rows(self.board, player)

            if current_player1 == 'X':
                return "X"
            elif current_player1 == 'O':
                return "O"
            

            # check vertical
            rotated = zip(*self.board[::-1])
            current_player2 = self.check_general_rows(rotated, player)
            if current_player2 == 'X':
                return "X"
            elif current_player2 == 'O':
                return "O"

            matrix = np.array(self.board)

            # check diagonal
            diags = [matrix[::-1, :].diagonal(i) for i in
                     range(-matrix.shape[0] + 1, matrix.shape[1])]
            diags.extend(
                matrix.diagonal(i) for i in range(matrix.shape[1] - 1, -matrix.shape[0], -1))
            current_player3 = self.check_general_rows(diags, player)

            if current_player3 == 'X':
                return "X"
            elif current_player3 == 'O':
                return "O"

    def alreadymove(self, player):  # get all steps already made by a player
        steps = []
        for x in range(self.scale):
            for y in range(self.scale):
                if self.board[x][y] == player:
                    steps.append([x,y])
        return steps

    def canmove(self, player):  # return available spaces on the board
        spaces = []
        sumX = 0
        sumY = 0
        for x in range(self.scale):
            for y in range(self.scale):
                if self.board[x][y] is self.alterplayer2(player):
                    sumX += x
                    sumY += y

        newX = int(sumX/len(self.alreadymove(self.alterplayer2(player))))
        newY = int(sumY/len(self.alreadymove(self.alterplayer2(player))))

        for i in range(newX-self.combo, newX+self.combo):
            for j in range(newY-self.combo, newY+self.combo):
                if i>=0 and i<=self.scale-1 and j>=0 and j<=self.scale-1 and self.board[i][j] is " ":
                    spaces.append([i, j])

        if len(spaces) is 0:
            for m in range(self.scale):
                for n in range(self.scale):
                    if self.board[m][n] is " ":
                        spaces.append([m, n])
        return spaces


    def over(self):  # return True if X wins, O wins, or draw
        if self.whowins() != None:
            return True
        for x in range(self.scale):
            for y in range(self.scale):
                if self.board[x][y] is " ":
                    return False
        return True

    def winner(self):  # return the winner
        if self.whowins() == "X":
            return "X"
        elif self.whowins() == "O":
            return "O"
        elif self.over() == True:
            return "Draw. Nobody"


    def minimax2(self, state, far, player):  # analyze recursively possible states and choose the best move (currently only for "O")
        if far == 0 or state.over():
            if state.whowins() == "X":
                return 0
            elif state.whowins() == "O":
                return 100
            else:
                return 50

        if player == "O":
            finalscore = 0
            if far<=-4:
                return finalscore
            for i in state.canmove(player):
                state.move(i[0], i[1], player)
                score = self.minimax2(state, far - 1, state.alterplayer2(player))
                state.move(i[0], i[1], " ")
                if score == 100:  # Alpha pruning
                    return score
                finalscore = max(finalscore, score)
            return finalscore

        if player == "X":
            finalscore = 100
            if far<=-4:
                return finalscore
            for j in state.canmove(player):
                state.move(j[0], j[1], player)
                score = self.minimax2(state, far - 1, state.alterplayer2(player))
                state.move(j[0], j[1], " ")
                if score == 0:  # Beta pruning
                    return score
                finalscore = min(finalscore, score)
            return finalscore



    def alterplayer2(self, player):  # return the opposite player
        if player == "X":
            return "O"
        else:
            return "X"


def bestmove2(state, far, player):  # use minimax to find optimal move (currently only for "O")
    middlescore = 50
    decision = []
    for i in state.canmove(player):
        state.move(i[0], i[1], player)
        score = state.minimax2(state, far - 1, state.alterplayer2(player))
        state.move(i[0], i[1], " ")

        if score > middlescore:
            decision = [i]
        elif score == middlescore:
            decision.append(i)

    if len(decision) > 0:
        return random.choice(decision)
    else:
        return random.choice(state.canmove(player))

if __name__ == '__main__':
    newgame = DrawTicTacToe(18,8)

    newgame.printboard()

    while newgame.over() == False:
        person_move_x = int(input("Specify x: "))
        person_move_y = int(input("Specify y: "))

        newgame.move(person_move_x, person_move_y, "X")
        newgame.printboard()

        if newgame.over() == True:
            break

        print("Computer choosing move...")

        
        ai_move = bestmove2(newgame, -1, "O")
        ai_move_x = ai_move[0]
        ai_move_y = ai_move[1]
        newgame.move(ai_move_x, ai_move_y, "O")
        newgame.printboard()

    print(newgame.winner() + " wins.")
