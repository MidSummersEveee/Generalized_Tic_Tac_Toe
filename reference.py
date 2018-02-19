import random

class DrawTicTacToe:
    def __init__(self):  # create an empty board
        self.board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]

    def printboard(self):  # print the board
        print("""                                                                                                                                                                                                          
          {} | {} | {}                                                                                                                                                                                                     
         -----------                                                                                                                                                                                                       
          {} | {} | {}                                                                                                                                                                                                     
         -----------                                                                                                                                                                                                       
          {} | {} | {}                                                                                                                                                                                                     
        """.format(*self.board))

    def alreadymove(self, player):  # get all moves already made by a player
        steps = []
        for i in range(0, len(self.board)):
            if self.board[i] == player:
                steps.append(i)
        return steps

    def canmove(self):  # return available spaces on the board
        spaces = []
        for i in range(0, len(self.board)):
            if self.board[i] == " ":
                spaces.append(i)
        return spaces

    def move(self, location, player):  # move a step on the board
        self.board[location] = player

    def whowins(self):  # check who wins
        results = ([0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6])

        for i in ("X", "O"):
            locations = self.alreadymove(i)
            for result in results:
                res = True
                for loc in result:
                    if loc not in locations:
                        res = False
                if res:
                    return i

    def over(self):  # return True if X wins, O wins, or draw
        if self.whowins() != None:
            return True
        for i in self.board:
            if i == " ":
                return False
        return True

    def winner(self):  # return the winner
        if self.whowins() == "X":
            return "X"
        elif self.whowins() == "O":
            return "O"
        elif self.over() == True:
            return "Draw. Nobody"

    def minimax1(self, state, far, player):  # analyze recursively possible states and choose the best move (currently only for "X")
        if far == 0 or state.over():
            if state.whowins() == "O":
                return 0
            elif state.whowins() == "X":
                return 100
            else:
                return 50

        if player == "X":
            finalscore = 0
            for i in state.canmove():
                state.move(i, player)
                score = self.minimax1(state, far - 1, alterplayer1(player))
                state.move(i, " ")
                finalscore = max(finalscore, score)
            return finalscore

        if player == "O":
            finalscore = 100
            for j in state.canmove():
                state.move(j, player)
                score = self.minimax1(state, far - 1, alterplayer1(player))
                state.move(j, " ")
                finalscore = min(finalscore, score)
            return finalscore

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
            for i in state.canmove():
                state.move(i, player)
                score = self.minimax2(state, far - 1, alterplayer2(player))
                state.move(i, " ")
                finalscore = max(finalscore, score)
            return finalscore

        if player == "X":
            finalscore = 100
            for j in state.canmove():
                state.move(j, player)
                score = self.minimax2(state, far - 1, alterplayer2(player))
                state.move(j, " ")
                finalscore = min(finalscore, score)
            return finalscore

def alterplayer1(player):  # return the opposite player
    if player == "O":
        return "X"
    else:
        return "O"

def alterplayer2(player):  # return the opposite player
    if player == "X":
        return "O"
    else:
        return "X"

def bestmove1(state, far, player):  # use minimax to find optimal move (currently only for "X")
    middlescore = 50
    decision = []
    for i in state.canmove():
        state.move(i, player)
        score = state.minimax1(state, far - 1, alterplayer1(player))
        state.move(i, " ")

        if score > middlescore:
            decision = [i]
        elif score == middlescore:
            decision.append(i)

    if len(decision) > 0:
        return random.choice(decision)
    else:
        return random.choice(state.canmove())

def bestmove2(state, far, player):  # use minimax to find optimal move (currently only for "O")
    middlescore = 50
    decision = []
    for i in state.canmove():
        state.move(i, player)
        score = state.minimax2(state, far - 1, alterplayer2(player))
        state.move(i, " ")

        if score > middlescore:
            decision = [i]
        elif score == middlescore:
            decision.append(i)

    if len(decision) > 0:
        return random.choice(decision)
    else:
        return random.choice(state.canmove())

if __name__ == '__main__':
    newgame = DrawTicTacToe()

    print("Computer1 is X. The first step is a random start.")
    random.seed()  # give a random start
    firststep = random.randint(0, 8)
    newgame.move(firststep, "X")
    newgame.printboard()

    while newgame.over() == False:
        print("Computer2 is choosing to move...")
        bestchoice2 = bestmove2(newgame, -1, "O")
        newgame.move(bestchoice2, "O")
        newgame.printboard()

        if newgame.over() == True:
            break

        print("Computer1 is choosing to move...")
        bestchoice1 = bestmove1(newgame, -1, "X")
        newgame.move(bestchoice1, "X")
        newgame.printboard()

    print(newgame.winner() + " wins.")