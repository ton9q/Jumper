import math
from random import getrandbits
from random import randrange

from model.entity.Platform import Platform
from utils.Constants import SCREEN_WIDTH, MAX_JUMP

class PlatformController:
    def __init__(self):
        self.__platform_set = []
        self.__number_platforms = 10
        self.__last_x = MAX_JUMP
        self.__score = 0
        for i in range(0, self.__number_platforms):
            self.__platform_set.append(self.__generate_platform(i, self.__score))

    def __generate_platform(self, index, score):
        if (score < MAX_JUMP * MAX_JUMP):
            change = int(math.sqrt(score))
        else:
            change = MAX_JUMP - 1
        width = 200 - randrange(change, change + 60)
        height = 20
        y = 600 - index * 100
        while True:
            side = bool(getrandbits(1))
            if side:
                x = randrange(self.__last_x - MAX_JUMP, self.__last_x - change)
            else:
                x = randrange(self.__last_x + width + change, self.__last_x + MAX_JUMP + width)
            if x >= 0 and x <= SCREEN_WIDTH - width:
                break
        self.__last_x = x
        return Platform(x, y, width, height)

    def generate_new_platforms(self, camera):
        if self.__platform_set[-1].y - camera.y > -50:
            for i in range(self.__number_platforms, self.__number_platforms + 10):
                self.__platform_set.append(self.__generate_platform(i, self.__score))
            self.__number_platforms += 10

    def draw(self, game_display, camera):
        for platform in self.__platform_set:
            platform.draw(game_display, camera)

    def collide_set(self, player):
        for index, platform in enumerate(self.__platform_set):
            player.collide_platform(platform, index)

    @property
    def score(self):
        return self.__score

    @property
    def platform_set(self):
        return self.__platform_set

    @score.setter
    def score(self, score):
        self.__score = score
