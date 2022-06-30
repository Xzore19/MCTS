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
