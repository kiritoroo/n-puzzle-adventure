# -*- coding: utf-8 -*-
import pygame
import sys, time

import ui_handler

clock = pygame.time.Clock()

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('8 Puzzle Report')

        self.ui = ui_handler.UI()
        self.clock = pygame.time.Clock()
        self.display_surface = pygame.display.set_mode((1280, 800))

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
                self.ui.ui_event(event)

            # Update Display
            self.ui.update(dt)
            
            self.display_surface.fill('WHITE')

            # Render Display
            self.ui.render(self.display_surface)
            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()
