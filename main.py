# -*- coding: utf-8 -*-
import pygame
import sys, time

clock = pygame.time.Clock()

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('8 Puzzle Report')
        self.display_surface = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

    def run(self):
        last_time = time.time()
        while True:  
            dt = time.time() - last_time
            last_time = time.time()
                    
            # Handler Event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.display_surface.fill('GREEN')

            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()
