# tic-tac-toe playout
import copy
import random
import numpy as np


class mcts_node:
    def __init__(self, parent=None, move=None, state=None, player_id=None, game=None):
        self.childnode = []
        self.move = move
        self.state = state
        self.visit = 0
        self.value = 0
        self.parent = parent
        self.player_id = player_id
        self.game = game
        if game.is_terminal(state):
            self.untried_node = []
        else:
            self.untried_node = game.board_blank(state)

    def select_by_ucb(self):
        reward_li = []
        for i in self.childnode:
            ucb = (i.value / i.visit) + np.sqrt(2 * np.log(self.visit) / i.visit)
            reward_li.append(ucb)
        if self.player_id == 0:
            num = np.argmax(reward_li)
        else:
            num = np.argmin(reward_li)
        return self.childnode[num]

    def expand(self, move, state):
        child = mcts_node(parent=self, move=move, state=state, player_id=1 - self.player_id, game=self.game)
        self.untried_node.remove(move)
        self.childnode.append(child)
        return child

    def backpropagation(self, reward):
        self.visit += 1
        self.value += reward


class TicTacToe:
    def __init__(self):
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
        for i in state:
            for j in i:
                if j == ' ':
                    return False
        return True

    def is_win(self, state, player_id):
        a = self.players[player_id]
        li = []
        for i in range(3):
            if state[i] == [a, a, a]:
                return True
            for j in range(3):
                if state[i][j] == a:
                    li.append([i, j])
        pat = [[[i, j] for i in [0, 1, 2]] for j in [0, 1, 2]] + [[[0, 0], [1, 1], [2, 2]]] + [[[0, 2], [1, 1], [2, 0]]]
        for i in pat:
            x = 0
            for j in i:
                if j in li:
                    x += 1
            if x == 3:
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
        x, y = move
        char = self.players[player_id]
        new_state[x][y] = char
        return new_state

    def board_blank(self, state):
        blank = []
        for i in range(3):
            for j in range(3):
                if state[i][j] == ' ':
                    blank.append([i, j])
        return blank


def mcts(game, begin_state, iteration):
    mstnode = mcts_node(parent=None, move=None, state=begin_state, player_id=0, game=game)

    for i in range(iteration):
        node = mstnode
        state = begin_state
        id = mstnode.player_id

        while node.untried_node == [] and node.childnode != []:
            node = node.select_by_ucb()
            state = game.make_move(state, node.move, id)
            id = 1 - id

        if node.untried_node != []:
            m = random.choice(node.untried_node)
            state = game.make_move(state, m, id)
            id = 1 - id
            node = node.expand(m, state)

        while not game.is_terminal(state) and game.board_blank(state) != []:
            state = game.make_move(state, move=random.choice(game.board_blank(state)), player_id=id)
            id = 1 - id

        while node is not None:
            node.backpropagation(game.reward(state))
            node = node.parent

    return mstnode
