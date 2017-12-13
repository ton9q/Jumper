from pygame import *

from model.entity.Camera import Camera
from model.entity.Platform import Platform
from model.logic.PlatformController import PlatformController
from model.logic.Player import Player
from utils.Constants import *
from utils.Utils import *


def init_window():
    global game_display
    pygame.init()
    game_display = pygame.display.set_mode(RES)
    pygame.display.set_caption(GAME_CAPTION)


def reinit():
    global player
    global platform_controller
    global floor
    global camera
    player = Player()
    platform_controller = PlatformController()
    floor = Platform(0, SCREEN_HEIGHT - 36, SCREEN_WIDTH, 36)
    camera = Camera(player)


def main():
    game_loop = True
    game_state = 'Menu'
    selected_option = 0.30
    clock = pygame.time.Clock()
    fps = 60

    init_window()
    reinit()

    arrow_image = load_image('arrow.png')
    background = load_image('background.jpg')

    while game_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_loop = False
            if event.type == pygame.KEYDOWN:
                # Return to menu
                if event.key == pygame.K_ESCAPE:
                    if game_state == 'Game Over' or game_state == 'Playing' or game_state == 'About':
                        game_state = 'Menu'
                # Play again
                elif game_state == 'Game Over':
                    if event.key == pygame.K_SPACE:
                        reinit()
                        game_state = 'Playing'
                # Menu Events
                elif game_state == 'Menu':
                    if event.key == pygame.K_DOWN:
                        if selected_option <= 0.40:
                            selected_option += 0.10
                        else:
                            selected_option = 0.30
                    elif event.key == pygame.K_UP:
                        if selected_option >= 0.40:
                            selected_option -= 0.10
                        else:
                            selected_option = 0.50
                    elif event.key == pygame.K_RETURN:
                        if selected_option <= 0.31:
                            reinit()
                            game_state = 'Playing'
                        elif selected_option == 0.40:
                            game_state = 'About'
                        elif selected_option == 0.50:
                            game_loop = False

        if game_state == 'Menu':
            game_display.blit(background, (0, 0))
            game_display.blit(arrow_image,
                              (MENU_START_X + ARROW_HALF_WIDTH - 15,
                               MENU_START_Y + SCREEN_HEIGHT * selected_option - ARROW_HALF_HEIGHT))
            if pygame.font:
                # transparent black rectangle
                s = pygame.Surface((SCREEN_WIDTH / 2, round(SCREEN_HEIGHT / 1.45)), pygame.SRCALPHA)
                s.fill((0, 0, 0, 128))
                game_display.blit(s, (MENU_START_X, MENU_START_Y))
                # menu content
                message_display(game_display, 'Jumper', 0, MENU_START_Y + round(SCREEN_HEIGHT * 0.10), 60, WHITE, True)
                message_display(game_display, 'Play', 0, MENU_START_Y + round(SCREEN_HEIGHT * 0.30), 60, WHITE, True)
                message_display(game_display, 'About', 0, MENU_START_Y + round(SCREEN_HEIGHT * 0.40), 60, WHITE, True)
                message_display(game_display, 'Quit', 0, MENU_START_Y + round(SCREEN_HEIGHT * 0.50), 60, WHITE, True)

        elif game_state == 'Playing':
            keys_pressed = pygame.key.get_pressed()

            if keys_pressed[pygame.K_LEFT]:
                player.vel_x -= player.acceleration
                if player.vel_x < -player.max_vel_x:
                    player.vel_x = -player.max_vel_x
                player.sprite_index_y = 2
            elif keys_pressed[pygame.K_RIGHT]:
                player.vel_x += player.acceleration
                if player.vel_x > player.max_vel_x:
                    player.vel_x = player.max_vel_x
                player.sprite_index_y = 1
            # slip stop
            else:
                if player.vel_x < 0:
                    player.vel_x += player.acceleration
                    player.vel_x -= ICE_RESISTANCE
                    if player.vel_x > 0:
                        player.vel_x = 0
                else:
                    player.vel_x -= player.acceleration
                    player.vel_x += ICE_RESISTANCE
                    if player.vel_x < 0:
                        player.vel_x = 0
                        # zeroing the index for the sprite
                        if player.vel_y >= JUMP_VELOCITY / 2:
                            player.sprite_index_y = 0

            if keys_pressed[pygame.K_SPACE]:
                if player.on_any_platform(platform_controller, floor):
                    player.sprite_index_y = 3
                    if player.vel_y >= JUMP_VELOCITY / 2:
                        player.vel_y = -JUMP_VELOCITY

            player.update() # movement sprite
            player.combo() # acceleration from the wall
            player.collide_platform(floor, 0) # launch platform
            platform_controller.collide_set(player) # moving the platform
            platform_controller.score = player.score  # score for PlatformController
            camera.update(player.score) # camera update
            platform_controller.generate_new_platforms(camera) # platform generation
            # fallen
            if player.fallen_off_screen(camera):
                game_state = 'Game Over'
            # display
            game_display.blit(background, (0, 0))
            floor.draw(game_display, camera)
            platform_controller.draw(game_display, camera)
            player.draw(game_display, camera)
            message_display(game_display, str(player.score), 25, 30, 36, WHITE)

        elif game_state == 'Game Over':
            game_display.blit(background, (0, 0))
            if pygame.font:
                message_display(game_display, "GAME OVER", 0, 200, 70, WHITE, True)
                message_display(game_display, "Score: %d" % player.score, 0, 300, 50, WHITE, True)
                message_display(game_display, "Press SPACE to play again!", 0, 400, 50, WHITE, True)
                message_display(game_display, "Press ESC to return to menu!", 0, 500, 40, WHITE, True)

        elif game_state == 'About':
            game_display.blit(background, (0, 0))
            if pygame.font:
                for line in ABOUT_MESSAGE:
                    message_display(game_display, line, 0, MENU_START_Y + ABOUT_MESSAGE.index(line) * 35, 30, WHITE, True)
                message_display(game_display, "Press ESC to return to menu!", 0, 500, 40, WHITE, True)

        pygame.display.update()
        clock.tick(fps)


if __name__ == "__main__":
    main()
