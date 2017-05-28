#!/usr/bin/python
# -*- coding: utf-8 -*-
import random


class TicTacToe(object):
    """ 
    all game logic including min max algorthm 
    """
    def __init__(self, team, board=[], size=3):
        super(TicTacToe, self).__init__()
        self.team = team
        self.size = size
        if not len(board): # if they bring their own board just use that
            board = [[None for x in range(self.size)] for x in range(self.size)]
        self.board = board
        self.winning_states = self.generate_winning_states(self.size)
        self.verdicts = ('I will lose', 'we will Draw', 'I will win')
        # self.count = 0

    def __str__(self):
        """ returns nice repesentation of board in its current state, 
        eg:      X |   |   
                -----------
                   | x | O 
                -----------
                   |   | O   """
        temp = []
        for i, row in enumerate(self.board):
            row_temp = []
            for j, col in enumerate(row):
                if col == None: 
                    col = "   "
                else: 
                    col = " %s " % col
                row_temp.append(col)
                if j < self.size -1:
                    row_temp.append("|")
            temp.append("".join(row_temp))
            if i < self.size -1:
                temp.append("-" * (self.size * 4 -1))
        return "\n".join(temp)


    def generate_winning_states(self, size):
        """ finds all possible wins for any size square board """
        possible_wins = [] # list to store all combos
        for i in range(size):
            # get horizontal lines
            possible_wins.append([(i,j) for j in range(size)])
            # get vertical lines
            possible_wins.append([(j,i) for j in range(size)])
        # get diagonal line left down
        possible_wins.append([(i,i) for i in range(size)])
        # get diagonal line left up
        possible_wins.append([((size-1)-i,i) for i in range(size)])

        return possible_wins


    def available_moves(self, state=None):
        """ checks the moves left on the board """
        availible = []
        for i, row in enumerate(self.board):
            for j, col in enumerate(row):
                if col == state: 
                    availible.append((i,j))
        return availible


    def players_moves(self, player):
        """ checks what moves the player has made -
            is available_moves but renamed for readibility."""
        return self.available_moves(player)


    def winner(self):
        # print "X", self.players_moves("X")
        for player in ('X', 'O'):
            positions = self.players_moves(player)
            for state in self.winning_states:
                win = True
                for pos in state:
                    if pos not in positions:
                        win = False
                if win:
                    return player
        return None


    def complete(self):
        if None not in [j for i in self.board for j in i]:
            # converts 2d list to 1d then check for None
            return True
        if self.winner() != None:
            return True
        return False


    def make_move(self, square, player):
        """ adds move to board, relies on move validation in 
            comobination with availible_moves() """
        x, y = square
        self.board[x][y] = player


    def get_opponent(self, player):
        """Switches players"""
        return "X" if player == "O" else "O"


    def format_thoughts(self, move, val):
        """ create human message for site display """
        m_x, m_y = move
        pos_x = ["left", "center", "right"][m_y]
        pos_y = ["top", "middle", "bottom"][m_x]

        if move == (1,1):
            position = "center"
        elif pos_x == 1:
            position = "{}-{}".format(pos_x, pos_y)
        else:
            position = "{}-{}".format(pos_y, pos_x)

        return "If I go {} {}".format(position, self.verdicts[val+1])


    # 
    #     min-max algo part
    # 
    def alphabeta(self, node, player, alpha, beta):
        # self.count += 1
        if node.complete():
            if node.winner() == self.team:
                return 1 # if we win
            elif self.winner() is None:
                return 0 # if tie
            elif node.winner() != self.team:
                return -1 # if enemy wins
        for move in node.available_moves():
            node.make_move(move, player)
            val = self.alphabeta(node, self.get_opponent(player), alpha, beta)
            node.make_move(move, None)
            if player == self.team:
                if val > alpha:
                    alpha = val
                if alpha >= beta:
                   return beta
            else:
                if val < beta:
                    beta = val
                if beta <= alpha:
                    return alpha
        if player == self.team:
            return alpha
        else:
            return beta


    def determine(self, board, player):
        a = -2
        choices, thoughts = [], []
        if len(board.available_moves()) == 9:
            # if its the first move just go full rando
            choice = (random.randint(0, 2),random.randint(0, 2))
            thoughts = ["First go, I'll just go anaywhere"]
            return choice, thoughts
        for move in board.available_moves():
            board.make_move(move, player)
            val = board.alphabeta(board, board.get_opponent(player), -2, 2)
            board.make_move(move, None)
            thoughts.append(self.format_thoughts(move, val))
            # print self.format_thoughts(move, val)
            if val > a:
                a = val
                choices = [move]
            elif val == a:
                choices.append(move)
        # print "choices:", choices
        # print self.count
        return random.choice(choices), thoughts




def generate_response(sent_board, player):
    """ responses for web requests """
    # set up the board to equal sent request
    game = TicTacToe(team=player, board=sent_board)
    finished = False
    winner = None
    if game.complete():
        finished = True
        new_move = None
        winner = game.winner()
        thoughts = []
    else:
        new_move, thoughts = game.determine(game, player) 
        x, y = new_move
        game.board[x][y] = player
        if game.complete():
            finished = True
            winner = game.winner()
    response = {
        "new_move": new_move,
        "new_board": game.board,
        "finished": finished,
        "winner": winner,
        "thoughts": thoughts
    }
    # print thoughts
    return response