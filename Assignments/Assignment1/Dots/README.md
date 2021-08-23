# Dots environment

In this folder is the implementation for minimax agent alongside with random agent implementation and the implementation for [Dots environment](https://www.wikiwand.com/en/Dots_(game)). This game is for two players versus each others in order to fill the biggest area on the board.

This game has a huge search space for this game, the depth of the tree is O((n*m)!) and the width of the tree is O(n*m). So, searching for the full tree will be computationally expensive. Thus, optimization tricks can be applied such as: Alpha-beta prunning (Not implemented), maximum depth( horizon) maximum width (possible actions/observability) for the search tree to search in (Both are implemented), moreover I have implemented a feature that can randomly sample the action from the available actions set not just a systematically approach to sample the actions that will be discovered from the available actions set. Also, another optimization trick can be made is to memorize the states of the tree in order not to be computed again every time the tree node is being visited (But not implemented).

Moreover searching online not searching and construct the full tree is much efficient.

I have tested with 5x4 env:

- Max. depth: 5, Max. width: 30 -> worst computation time for single move -> Too much (Did not finish)
- Max depth: 5, Max width: 10 -> worst computation time for single move: ~30s -> not too good 
- Max depth: 5, Max width: 7 -> worst computation time for single move: ~5s -> not good performance
- Max depth: 5, Max width: 5 -> worst computation time for single move: ~2s -> not good performance
- Max depth: 8, Max width:3 -> worst computation time for single move: ~200s -> but kinda good
- Max depth: 4, Max width:20 -> worst computation time for single move: ~80 -> Good performance vs random agent


With different bad other parameters:
![Image](https://github.com/hany606/PAI_Fall21IU/blob/main/Assignments/Assignment1/figures/Dots_tie.png?raw=true)
![Image](https://github.com/hany606/PAI_Fall21IU/blob/main/Assignments/Assignment1/figures/Dots_tie2.png?raw=true)

With x2 speed and 7x7, max_depth=3, max_width=10, random_exploration=True
![Image](https://github.com/hany606/PAI_Fall21IU/blob/main/Assignments/Assignment1/figures/Dots_red.png?raw=true)
![Image](https://github.com/hany606/PAI_Fall21IU/blob/main/Assignments/Assignment1/figures/Dots_red2.png?raw=true)
![Image](https://github.com/hany606/PAI_Fall21IU/blob/main/Assignments/Assignment1/figures/Dots_red3.png?raw=true)
![Visualization](https://github.com/hany606/PAI_Fall21IU/blob/main/Assignments/Assignment1/figures/dots_red1_x2.gif)
![Visualization](https://github.com/hany606/PAI_Fall21IU/blob/main/Assignments/Assignment1/figures/dots_red2_x2.gif)
![Visualization](https://github.com/hany606/PAI_Fall21IU/blob/main/Assignments/Assignment1/figures/dots_red3_x2.gif)


