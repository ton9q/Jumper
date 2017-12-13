import pygame

from model.entity.IceSprite import IceSprite


class Platform:
    def __init__(self, x, y, width, height):
        self.__x = x
        self.__y = y
        self.__height = height
        self.__width = width
        self.__rect = pygame.Rect(x, y, width, height)
        self.__collected_score = False

    def draw(self, game_display, camera):
        for i in range(self.__x, self.__x + self.__width, 10):
            sprite = IceSprite([i, self.y - camera.y])
            game_display.blit(sprite.image, sprite.rect)

    @property
    def y(self):
        return self.__y

    @property
    def rect(self):
        return self.__rect

    @property
    def collected_score(self):
        return self.__collected_score

    @collected_score.setter
    def collected_score(self, collected_score):
        self.__collected_score = collected_score
