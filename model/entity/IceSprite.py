import pygame

from utils.Utils import load_image


class IceSprite(pygame.sprite.Sprite):
    __image = None

    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        if IceSprite.__image is None:
            IceSprite.__image = load_image("ice.png")
        self.__image = IceSprite.__image
        self.__rect = self.__image.get_rect()
        self.__rect.topleft = location

    @property
    def image(self):
        return self.__image

    @property
    def rect(self):
        return self.__rect
