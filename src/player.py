import pygame

import playerdata


class Player(playerdata.Playerdata):

    def __init__(self, uuid):
        super().__init__(uuid)
        self.rect = (self.x, self.y, self.width, self.height)

    def get_uuid(self): return self.uuid

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def ch_color(self):
        self.change_color()

    def change_color(self):
        print(self.color)
        if self.color == [0, 255, 0]:
            self.set_color([255, 0, 0])
        elif self.color == [255, 0, 0]:
            self.set_color([0, 0, 255])
        elif self.color == [0, 0, 255]:
            self.set_color([0, 255, 0])

    def move(self, keys):

        for direction in keys:
            if direction == "left":
                self.x -= self.speed
            if direction == "right":
                self.x += self.speed
            if direction == "up":
                self.y -= self.speed
            if direction == "down":
                self.y += self.speed

        self.set_pos()
