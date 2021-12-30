import copy

import pygame.event
import Game

MAP_SIZE = (30, 25)
BLOCK_SIZE = 25

pygame.init()
pygame.font.init()
font = pygame.font.Font(pygame.font.get_default_font(), 36)
screen = pygame.display.set_mode((MAP_SIZE[0] * BLOCK_SIZE, MAP_SIZE[1] * BLOCK_SIZE))
GameManager = Game.GameManager(MAP_SIZE, BLOCK_SIZE)

DIR_ON_KEY = {
    pygame.K_UP: [0, -1],
    pygame.K_DOWN: [0, 1],
    pygame.K_LEFT: [-1, 0],
    pygame.K_RIGHT: [1, 0]
}

time = 1
while not GameManager.gameOver:
    time += GameManager.tick() / 1000
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key in DIR_ON_KEY:
                GameManager.turn_snake(copy.copy(DIR_ON_KEY[event.key]))

    if time > GameManager.gameSpeed:
        GameManager.update()
        time = 0
    GameManager.draw(screen)
    pygame.display.set_caption(f'Snake Game : {GameManager.score}')
    pygame.display.update()

screen.fill((0, 0, 0))
screen.blit(
    font.render("Game Over!!", True, (255, 0, 0)),
    (120, 120)
)
pygame.display.update()
pygame.time.delay(3000)

exit()
