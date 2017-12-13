import math

from utils.Constants import SCREEN_HEIGHT


class Camera:
    def __init__(self, player):
        self.__y = 0
        self.__player = player

    def update(self, score):
        if self.__player.y - self.__y <= SCREEN_HEIGHT / 2:
            self.__y = self.__player.y - SCREEN_HEIGHT / 2
        if self.__player.y < SCREEN_HEIGHT / 2:
            change = int(math.sqrt(score)) / 10
            if not change:
                self.__y -= 1
            if (change < 4):
                self.__y -= change
            else:
                self.__y -= 4

    @property
    def y(self):
        return self.__y
