import copy
import random
import numpy as np


class ConnectFour:
    def __init__(self):
        # 7x6
        self.players = ['X', 'O']

    def is_terminal(self, state):
        if self.is_draw(state):
            return True
        elif self.is_win(state, 0) or self.is_win(state, 1):
            return True
        return False

    def is_draw(self, state):
        if self.is_win(state, 0) or self.is_win(state, 1):
            return False
        for i in range(7):
            if state[i][0] == ' ':
                return False
        return True

    def is_win(self, state, player_id):
        li = []
        for i in range(7):
            for j in range(6):
                if state[i][j] == self.players[player_id]:
                    li.append([i, j])
        for i in li:
            if [i[0] + 1, i[1]] in li and [i[0] + 2, i[1]] in li and [i[0] + 3, i[1]] in li:
                return True
            if [i[0], i[1] + 1] in li and [i[0], i[1] + 2] in li and [i[0], i[1] + 3] in li:
                return True
            if [i[0] + 1, i[1] + 1] in li and [i[0] + 2, i[1] + 2] in li and [i[0] + 3, i[1] + 3] in li:
                return True
            if [i[0] - 1, i[1] + 1] in li and [i[0] - 2, i[1] + 2] in li and [i[0] - 3, i[1] + 3] in li:
                return True
        return False

    def reward(self, state):
        if self.is_draw(state):
            return 0
        elif self.is_win(state, 0):
            return 1
        elif self.is_win(state, 1):
            return -1

    def make_move(self, state, move, player_id):
        new_state = copy.deepcopy(state)
        for i in range(6):
            if state[move][i] != ' ':
                char = self.players[player_id]
                new_state[move][i - 1] = char
                return new_state
        char = self.players[player_id]
        new_state[move][5] = char
        return new_state

    def board_blank(self, state):
        blank = []
        for i in range(7):
            if state[i][0] == ' ':
                blank.append(i)
        return blank