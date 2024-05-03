import sys

import pygame

class AlienInvasion:
    #Overall class to manage game assets and behavior

    def __init__(self):


        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Caleb's Alien Invasion")

    def run_game(self):
        #Main loop for game

        while True:
            for event in pygame.event.get():
                if event.type ==pygame.QUIT:
                    sys.exit()
            pygame.display.flip()

if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()

quit()

