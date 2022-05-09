# -*- coding: utf-8 -*-
import pygame
import pygame_gui
import sys, time

clock = pygame.time.Clock()

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('8 Puzzle Report')
        self.display_surface = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.ui_manager = pygame_gui.UIManager((800, 600), 'theme.json')
        self.gui_elements()
        
    def gui_elements(self):
        
        rect_push = pygame.Rect((100, 100), (100, 100))
        self.button_push = pygame_gui.elements.UIButton(relative_rect = rect_push,
                                                        text = "Push",
                                                        manager = self.ui_manager)

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
                self.ui_manager.process_events(event)
            self.ui_manager.update(dt)
    

            self.display_surface.fill('WHITE')
            self.ui_manager.draw_ui(self.display_surface)

            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()
