import requests
from bs4 import BeautifulSoup
import sys
from settings import *
from buttonClass import *
from solver import *


class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((wid, ht))
        self.running = True
        self.selected = None
        self.mousePos = None
        self.state = "Play"
        self.finished = False
        self.cellChanged = False
        self.playButtons = []
        self.solution = []
        self.lockedCells = []
        self.incorrectCells = []
        self.font = pygame.font.SysFont("arial", cellSize // 2)
        self.grid = []
        self.getPuzzle("1")
        # self.solvePuzzle(self.solution)

    def run(self):
        while self.running:
            if self.state == "Play":
                self.events()
                self.update()
                self.draw()
        pygame.quit()
        sys.exit()

#### play functions

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouseOnGrid()
                if selected:
                    self.selected = selected
                    print(self.selected)
                else:
                    self.selected = None
                    for buttons in self.playButtons:
                        if buttons.highlighted:
                            buttons.click()

            if event.type == pygame.KEYDOWN:
                if self.selected != None and self.selected not in self.lockedCells:
                    # print(self.selected)
                    if self.isInt(event.unicode):
                        self.grid[self.selected[1]][self.selected[0]] = int(event.unicode)
                        self.cellChanged = True

    def update(self):
        self.mousePos = pygame.mouse.get_pos()
        for button in self.playButtons:
            button.update(self.mousePos)

        if self.cellChanged:
            self.incorrectCells = []
            if self.cellsComplete():
                self.checkallCells()
                if len(self.incorrectCells) == 0:
                    self.finished = True

    def draw(self):
        self.window.fill(WHITE)
        for button in self.playButtons:
            button.draw(self.window)

        if self.selected:
            self.drawSelection(self.window, self.selected)

        self.shadeLockedCells(self.window, self.lockedCells)
        self.shadeincorrectCells(self.window, self.incorrectCells)
        self.drawNumbers(self.window)
        self.drawGrid(self.window)
        pygame.display.update()
        self.cellChanged = False

####Board checks

    def cellsComplete(self):
        for rows in self.grid:
            for num in rows:
                if num == 0:
                    return False
        return True

    def checkallCells(self):
        self.checkRows()
        self.checkCols()
        self.check3_3()

    def checkRows(self):
        for yidx, row in enumerate(self.grid):
            possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for xidx in range(9):
                if self.grid[yidx][xidx] in possibles:
                    possibles.remove(self.grid[yidx][xidx])
                else:
                    if [xidx, yidx] not in self.lockedCells and [xidx, yidx] not in self.incorrectCells:
                        self.incorrectCells.append([xidx, yidx])
                    if [xidx, yidx] in self.lockedCells:
                        for k in range(9):
                            if self.grid[yidx][k] == self.grid[yidx][xidx] and [k, yidx] not in self.lockedCells:
                                self.incorrectCells.append([k, yidx])

    def checkCols(self):
        for xidx in range(9):
            possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for yidx, row in enumerate(self.grid):
                if self.grid[yidx][xidx] in possibles:
                    possibles.remove(self.grid[yidx][xidx])
                else:
                    if [xidx, yidx] not in self.lockedCells and [xidx, yidx] not in self.incorrectCells:
                        self.incorrectCells.append([xidx, yidx])
                    if [xidx, yidx] in self.lockedCells:
                        for k in range(9):
                            if self.grid[k][xidx] == self.grid[yidx][xidx] and [xidx, k] not in self.lockedCells:
                                self.incorrectCells.append([xidx, k])

    def check3_3(self):
        for x in range(3):
            for y in range(3):
                possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                for i in range(3):
                    for j in range(3):
                        xidx = x * 3 + i
                        yidx = y * 3 + j
                        if self.grid[yidx][xidx] in possibles:
                            possibles.remove(self.grid[yidx][xidx])
                        else:
                            if [xidx, yidx] not in self.lockedCells and [xidx, yidx] not in self.incorrectCells:
                                self.incorrectCells.append([xidx, yidx])
                            if [xidx, yidx] in self.lockedCells:
                                for k in range(3):
                                    for l in range(3):
                                        xidx2 = x * 3 + k
                                        yidx2 = y * 3 + l
                                        if self.grid[yidx2][xidx2] == self.grid[yidx][xidx] and [xidx2,
                                                                                                 yidx2] not in self.lockedCells:
                                            self.incorrectCells.append([xidx2, yidx2])

    ##### Helper functions
    def shadeincorrectCells(self, window, incorrectCells):
        for cell in incorrectCells:
            pygame.draw.rect(window, (247, 95, 84),
                             (cell[0] * cellSize + gridPos[0], cell[1] * cellSize + gridPos[1], cellSize, cellSize))

    def shadeLockedCells(self, window, lockedCells):
        for cell in lockedCells:
            pygame.draw.rect(window, (150, 150, 150),
                             (cell[0] * cellSize + gridPos[0], cell[1] * cellSize + gridPos[1], cellSize, cellSize))

    def drawNumbers(self, window):
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                if num != 0:
                    pos = [xidx * cellSize + gridPos[0], yidx * cellSize + gridPos[1]]
                    self.textToBoard(window, str(num), pos)

    def drawSelection(self, window, pos):
        pygame.draw.rect(window, lightBlue,
                         (pos[0] * cellSize + gridPos[0], pos[1] * cellSize + gridPos[1], cellSize, cellSize))

    def drawGrid(self, window):
        pygame.draw.rect(window, black, (gridPos[0], gridPos[1], wid - 50, ht - 150), 2)
        for i in range(9):
            if i % 3 != 0:
                pygame.draw.line(window, black, (gridPos[0], gridPos[1] + i * cellSize),
                                 (gridPos[0] + 450, gridPos[1] + (i * cellSize)))
                pygame.draw.line(window, black, (gridPos[0] + i * cellSize, gridPos[1]),
                                 (gridPos[0] + (i * cellSize), gridPos[1] + 450))
            else:
                pygame.draw.line(window, black, (gridPos[0] + i * cellSize, gridPos[1]),
                                 (gridPos[0] + (i * cellSize), gridPos[1] + 450), 2)
                pygame.draw.line(window, black, (gridPos[0], gridPos[1] + i * cellSize),
                                 (gridPos[0] + 450, gridPos[1] + (i * cellSize)), 2)

    def mouseOnGrid(self):
        if self.mousePos[0] < gridPos[0] or self.mousePos[1] < gridPos[1]:
            return False
        if self.mousePos[0] > gridPos[0] + gridSize or self.mousePos[1] > gridPos[1] + gridSize:
            return False
        return [(self.mousePos[0] - gridPos[0]) // cellSize, (self.mousePos[1] - gridPos[1]) // cellSize]

    def loadButtons(self):
        self.playButtons.append(Button(25, 40, wid // 6, 40, txt="check", function=self.checkallCells))
        self.playButtons.append(Button(120, 40, wid // 6, 40, txt="Easy", function=self.getPuzzle, params="1"))
        self.playButtons.append(Button(210, 40, wid // 6, 40, txt="Med", function=self.getPuzzle, params="2"))
        self.playButtons.append(Button(300, 40, wid // 6, 40, txt="Hard", function=self.getPuzzle, params="3"))
        self.playButtons.append(Button(390, 40, wid // 6, 40, txt="Evil", function=self.getPuzzle, params="4"))

    def textToBoard(self, window, text, pos):
        font = self.font.render(text, False, black)
        fontWidth = font.get_width()
        fontHeight = font.get_height()
        pos[0] += (cellSize - fontWidth) // 2
        pos[1] += (cellSize - fontHeight) // 2
        window.blit(font, pos)

    def load(self):
        self.playButtons = []
        self.loadButtons()
        self.lockedCells = []
        self.incorrectCells = []
        self.finished = False

        # setting locked cells
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                if num != 0:
                    self.lockedCells.append([xidx, yidx])
        # print(self.lockedCells)

    def isInt(self, string):
        try:
            int(string)
            return True
        except:
            return False

    def getPuzzle(self, difficulty):
        html_doc = requests.get("https://nine.websudoku.com/?level={}".format(difficulty)).content
        soup = BeautifulSoup(html_doc)
        ids = ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08',
               'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18',
               'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28',
               'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38',
               'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48',
               'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58',
               'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68',
               'f70', 'f71', 'f72', 'f73', 'f74', 'f75', 'f76', 'f77', 'f78',
               'f80', 'f81', 'f82', 'f83', 'f84', 'f85', 'f86', 'f87', 'f88']
        data = []
        for cid in ids:
            data.append(soup.find('input', id=cid))
        board = [[0 for x in range(9)] for y in range(9)]
        for index, cell in enumerate(data):
            try:
                board[index // 9][index % 9] = int(cell['value'])
            except:
                pass
        self.grid = board
        self.load()
    # def solvePuzzle(self,solved):
    #     solved=self.grid
    #     solved=solve(solved)
    #     print(solved)
