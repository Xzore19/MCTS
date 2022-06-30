game = TicTacToe()
root_state = [[' ',' ',' '],
              [' ',' ',' '],
              [' ',' ',' ']]
mst=mcts(game,root_state,100)
print('mst.value:',mst.value/mst.visit)
for i in mst.childnode:
    print(i.state,':',i.value/i.visit)