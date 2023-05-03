import pygame
import sys
from settings import *
from debug import debug
from level import Level


class Game:
    def __init__(self):

        # General setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Zelda")
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)

        self.level = Level()

        # sound
        main_sound = pygame.mixer.Sound('../audio/main.ogg')
        main_sound.set_volume(0.2)
        main_sound.play(loops=-1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_u:
                        self.level.toggle_upgrade()
                    elif event.key == pygame.K_ESCAPE:
                        self.level.toggle_menu()
            self.screen.fill(WATER_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
