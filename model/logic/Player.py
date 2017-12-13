import pygame

from utils.Constants import GRAVITY, SCREEN_WIDTH, SCREEN_HEIGHT
from utils.Utils import load_image


class Player:
    # border sprite
    __width = 30
    __height = 50
    # change in position
    __vel_x = 0
    __vel_y = 0
    # borders
    __max_falling_speed = 15
    __acceleration = 0.5
    __max_vel_x = 7

    def __init__(self):
        # initialization
        self.__x = 30
        self.__y = 500
        self.__score = -10
        self.__spritesheet_image = load_image('spritesheet.png')
        self.__spritesheet = []
        # idle
        self.__cropped1 = pygame.Surface((33, 57), pygame.SRCALPHA, 32)
        self.__cropped2 = pygame.Surface((33, 57), pygame.SRCALPHA, 32)
        self.__cropped3 = pygame.Surface((33, 57), pygame.SRCALPHA, 32)
        self.__cropped1.blit(self.__spritesheet_image, (0, 0), (0, 0, 33, 57))
        self.__cropped2.blit(self.__spritesheet_image, (0, 0), (37, 0, 33, 57))
        self.__cropped3.blit(self.__spritesheet_image, (0, 0), (75, 0, 33, 57))
        self.__spritesheet.append(self.__cropped1)
        self.__spritesheet.append(self.__cropped2)
        self.__spritesheet.append(self.__cropped3)
        # going right
        self.__cropped4 = pygame.Surface((33, 57), pygame.SRCALPHA, 32)
        self.__cropped5 = pygame.Surface((33, 57), pygame.SRCALPHA, 32)
        self.__cropped6 = pygame.Surface((33, 57), pygame.SRCALPHA, 32)
        self.__cropped4.blit(self.__spritesheet_image, (0, 0), (0, 56, 33, 57))
        self.__cropped5.blit(self.__spritesheet_image, (0, 0), (37, 56, 33, 57))
        self.__cropped6.blit(self.__spritesheet_image, (0, 0), (75, 56, 33, 57))
        self.__spritesheet.append(self.__cropped4)
        self.__spritesheet.append(self.__cropped5)
        self.__spritesheet.append(self.__cropped6)
        # going left
        self.__spritesheet.append(pygame.transform.flip(self.__cropped4, True, False))
        self.__spritesheet.append(pygame.transform.flip(self.__cropped5, True, False))
        self.__spritesheet.append(pygame.transform.flip(self.__cropped6, True, False))
        # jumping
        self.__cropped7 = pygame.Surface((33, 57), pygame.SRCALPHA, 32)
        self.__cropped7.blit(self.__spritesheet_image, (0, 0), (75, 112, 33, 57))
        self.__spritesheet.append(self.__cropped7)
        self.__spritesheet.append(self.__cropped7)
        self.__spritesheet.append(self.__cropped7)
        # to work with the display of the sprite
        self.__sprite_index_x = 0
        self.__sprite_index_y = 0
        self.__frame_counter = 0
        self.__frame_delay = 9

    def draw(self, game_display, camera):
        game_display.blit(self.__spritesheet[self.__sprite_index_y * 3 + self.__sprite_index_x],
                          (self.__x, self.__y - camera.y))
        self.__frame_counter += 1
        if self.__frame_counter >= self.__frame_delay:
            self.__sprite_index_x += 1
            if self.__sprite_index_x > 2:
                self.__sprite_index_x = 0
            self.__frame_counter = 0

    def update(self):
        self.__x += self.__vel_x
        self.__y += self.__vel_y
        self.__vel_y += GRAVITY
        if self.__vel_y > self.__max_falling_speed:
            self.__vel_y = self.__max_falling_speed
        if self.__x <= 0:
            self.__x = 0
        if self.__x + self.__width >= SCREEN_WIDTH:
            self.__x = SCREEN_WIDTH - self.__width

    def combo(self):
        if self.__x == 0:
            if self.__vel_y < 0 and self.__vel_x < 0:
                self.__vel_y -= 10
                self.__vel_x *= -1.5
        if self.__x + self.__width >= SCREEN_WIDTH:
            if self.__vel_y < 0 and self.__vel_x > 0:
                self.__vel_y -= 10
                self.__vel_x *= -1.5

    def __on_platform(self, platform):
        return platform.rect.collidepoint((self.__x, self.__y + self.__height)) or \
               platform.rect.collidepoint((self.__x + self.__width, self.__y + self.__height))

    def on_any_platform(self, platform_controller, floor):
        for p in platform_controller.platform_set:
            if self.__on_platform(p):
                return True
        if self.__on_platform(floor):
            return True
        return False

    def collide_platform(self, platform, index):
        for i in range(0, self.__vel_y):
            if pygame.Rect(self.__x, self.__y - i, self.__width, self.__height).colliderect(platform.rect):
                if platform.rect.collidepoint((self.__x, self.__y + self.__height - i)) or \
                        platform.rect.collidepoint(self.__x + self.__width, self.__y + self.__height - i):
                    self.__y = platform.y - self.__height
                    if not platform.collected_score:
                        self.__score += 10
                        if self.__score < index * 10:
                            self.__score = index * 10
                        platform.collected_score = True

    def get_rect(self):
        return pygame.Rect(self.__x, self.__y, self.__width, self.__height)

    def fallen_off_screen(self, camera):
        if self.__y - camera.y + self.__height >= SCREEN_HEIGHT:
            return True
        return False

    @property
    def y(self):
        return self.__y

    @property
    def score(self):
        return self.__score

    @property
    def vel_x(self):
        return self.__vel_x

    @property
    def vel_y(self):
        return self.__vel_y

    @property
    def sprite_index_x(self):
        return self.__sprite_index_x

    @property
    def sprite_index_y(self):
        return self.__sprite_index_y

    @property
    def acceleration(self):
        return self.__acceleration

    @property
    def max_vel_x(self):
        return self.__max_vel_x

    @vel_x.setter
    def vel_x(self, vel_x):
        self.__vel_x = vel_x

    @vel_y.setter
    def vel_y(self, vel_y):
        self.__vel_y = vel_y

    @sprite_index_x.setter
    def sprite_index_x(self, sprite_index_x):
        self.__sprite_index_x = sprite_index_x

    @sprite_index_y.setter
    def sprite_index_y(self, sprite_index_y):
        self.__sprite_index_y = sprite_index_y
