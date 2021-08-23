# Tiktikl environment

It has the same implementation for minimax as in Dots environment, but here the search space is not that huge as in Dots, so the maximum depth and width constraints are loose, only the depth is constrained with 4 moves ahead in order to avoid the cyclic graphs, this can be solved by storing the states of the environment and checking if we passed this state twice in one search that means it is a cycle and return to the previous search value (But not implmented now). Here is the implementation of [Tiktikl environment](http://cyclowiki.org/wiki/%D0%A2%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D0%BB%D1%8C)

![Image](https://github.com/hany606/PAI_Fall21IU/blob/main/Assignments/Assignment1/figures/Tiks_red.png?raw=true)
![Image](https://github.com/hany606/PAI_Fall21IU/blob/main/Assignments/Assignment1/figures/Tiks_red1.png?raw=true)
![Image](https://github.com/hany606/PAI_Fall21IU/blob/main/Assignments/Assignment1/figures/Dots_red3.png?raw=true)
![Visualization](https://github.com/hany606/PAI_Fall21IU/blob/main/Assignments/Assignment1/figures/tiks1.gif)
![Visualization](https://github.com/hany606/PAI_Fall21IU/blob/main/Assignments/Assignment1/figures/tiks2.gif)


