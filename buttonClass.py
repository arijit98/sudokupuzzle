import pygame


class Button:
    def __init__(self, x, y, w, h, txt=None, col=(73, 173, 73), highCol=(189, 189, 189), function=None, params=None):
        self.image = pygame.Surface((w, h))
        self.pos = (x, y)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.text = txt
        self.colour = col
        self.highlightedColour = highCol
        self.function = function
        self.params = params
        self.highlighted = False
        self.width=w
        self.height=h

    def update(self, mouse):
        if self.rect.collidepoint(mouse):
            self.highlighted = True
        else:
            self.highlighted = False

    def draw(self, window):
        if self.highlighted:
            self.image.fill(self.highlightedColour)
        else:
            self.image.fill(self.colour)
        if self.text:
            self.drawText(self.text)
        window.blit(self.image, self.pos)

    def click(self):
        if self.params:
            self.function(self.params)
        else:
            self.function()

    def drawText(self,text):
        font=pygame.font.SysFont("arial",20,bold=1)
        text=font.render(text,False,(0,0,0))
        width,height=text.get_size()
        x=(self.width-width)//2
        y=(self.height-height)//2
        self.image.blit(text,(x,y))