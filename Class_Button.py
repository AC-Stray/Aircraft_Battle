import pygame
from pygame.locals import *
update_log = '''
Button2.0 by AbsoCube Studio
Button2.0 Update Log:
Update Time : 2019/11/22 Friday
Update Contents :
    Text display position :
        Before : Align with the top left corner of the button.
        New : Button's center.
    Change button properties :
        Before : Create the button with new property and override the old button.
        New : Call function "set_x", "set_y", "set_color".
'''
print(update_log)


class button():
    def __init__(self, posx, posy, length, width, text, bfont, color, textcolor=(0, 0, 0)):
        self.posx = posx
        self.posy = posy
        self.color = color
        self.length = length
        self.width = width
        self.tcolor = textcolor
        self.font = bfont
        self.text = text
        if self.tcolor == "opposite":
            tcl = []
            for c in color:
                tcl.append(255-c)
            self.textcolor = (tcl[0], tcl[1], tcl[2])
        else:
            self.textcolor = textcolor
        self.rect = pygame.Rect(self.posx, self.posy, length, width)

    def show(self, scr):
        if self.color:
            scr.fill(self.color, self.rect)
        text = self.font.render(self.text, True, self.textcolor)
        text_rect = text.get_rect()
        text_rect.centerx = self.posx+self.length//2
        text_rect.centery = self.posy+self.width//2
        scr.blit(text, text_rect)

    def pressed(self, event):
        if event.type == MOUSEBUTTONDOWN:
            mousedownx, mousedowny = event.pos
            if self.posx <= mousedownx <= self.posx+self.length and self.posy <= mousedowny <= self.posy+self.width:
                return True
            else:
                return False

    def set_x(self, posx):
        self.posx = posx

    def set_y(self, posy):
        self.posy = posy

    def set_color(self, color):
        self.color = color
        if self.tcolor == "opposite":
            tcl = []
            for c in color:
                tcl.append(255-c)
            self.textcolor = (tcl[0], tcl[1], tcl[2])