wid=500
ht=600

#color
WHITE=(255,255,255)
black=(0,0,0)
lightBlue=(190,190,190)

#Boards
testboard=[[0 for i in range(9)] for j in range(9)]
testboard2=[
    [7, 8, 5, 4, 3, 9, 1, 2, 6],
    [6, 1, 2, 8, 7, 5, 3, 4, 9],
    [4, 9, 3, 6, 2, 1, 5, 7, 8],
    [8, 5, 7, 0, 4, 3, 2, 6, 1],
    [2, 6, 1, 7, 5, 8, 9, 3, 4],
    [9, 3, 4, 1, 6, 2, 7, 0, 5],
    [5, 7, 8, 3, 9, 4, 6, 1, 2],
    [1, 2, 6, 5, 8, 7, 4, 9, 3],
    [3, 4, 9, 2, 1, 6, 8, 5, 0]
]

#size and Pos
gridPos=(25,120)
cellSize=50
gridSize=9*cellSize