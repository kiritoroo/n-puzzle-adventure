import os

try:
    import pygame
except:
    os.system('pip install pygame')
    import pygame

try:
    import pygame_gui
except:
    os.system('pip install pygame_gui')
    import pygame_gui

import sys

import settings

class Frame:
    def __init__(self, _frame_handler, _screen):
        pygame.init()
        self.ui_manager = pygame_gui.UIManager((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), 'theme.json')
        self.frame_handler = _frame_handler
        self.screen = _screen
        self.ui_elements()

    def ui_elements(self):
        
        rect_Npuzzlegame = pygame.Rect((540, 280), (200, 60))
        rect_Algorithm = pygame.Rect((540, 350), (200, 60))
        rect_Compare = pygame.Rect((540, 420), (200, 60))
        rect_Exit = pygame.Rect((590, 520), (100, 60))
        #Button
        self.button_Npuzzlegame = pygame_gui.elements.UIButton(relative_rect = rect_Npuzzlegame,
                                                               text = "N Puzzle Game",
                                                               manager = self.ui_manager)
        self.button_Algorithm = pygame_gui.elements.UIButton(relative_rect = rect_Algorithm,
                                                             text = "Algorithm Simulator",
                                                             manager = self.ui_manager)
        self.button_Compare = pygame_gui.elements.UIButton(relative_rect = rect_Compare,
                                                           text = "Compare Algorithm",
                                                           manager = self.ui_manager)
        self.button_Exit = pygame_gui.elements.UIButton(relative_rect = rect_Exit,
                                                        text = "Exit",
                                                        manager = self.ui_manager,
                                                        object_id = "#button_exit" ) 
 
        #Label
        self.label_title = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                                text = "AI FINAL PROJECT",
                                                                relative_rect = pygame.Rect((20,0), (settings.SCREEN_WIDTH, 300)),
                                                                object_id = '#label_title')
        self.label_mentor = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                                 text = "Mentor:",
                                                                 relative_rect = pygame.Rect((900,550), (400, 50)))
        self.label_mentor_name = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                                      text = "Mr.Hoang Van Dung",
                                                                      relative_rect = pygame.Rect((970,570), (400, 50)))
        self.label_author = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                                 text = "Author:",
                                                                 relative_rect = pygame.Rect((900,590), (400, 50)))
        self.label_author_name1 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                                       text = "Le Kien Trung",
                                                                       relative_rect = pygame.Rect((955,610), (400, 50)))
        self.label_author_name2 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                                       text = "Nguyen Huu Thang",
                                                                       relative_rect = pygame.Rect((968,630), (400, 50)))
        self.label_author_name3 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                                       text = "Nguyen Phuoc Toan",
                                                                       relative_rect = pygame.Rect((972,650), (400, 50)))
        self.label_subtitle = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                                   text = "Artificial Intelligence - 8 Puzzle Final Project",
                                                                   relative_rect = pygame.Rect((10,450), (500, 450)))

    def ui_event(self, _event):
        if _event.type == pygame_gui.UI_BUTTON_PRESSED:
            if _event.ui_element == self.button_Npuzzlegame:
                self.frame_handler.set_current_frame('frame_game')
            elif _event.ui_element == self.button_Algorithm:
                self.frame_handler.set_current_frame('frame_simulator')
            elif _event.ui_element == self.button_Compare:
                self.frame_handler.set_current_frame('frame_compare')
            elif _event.ui_element == self.button_Exit:
                pygame.quit()
                sys.exit()
            else:
                return

        self.ui_manager.process_events(_event)

            
    def render(self, _display_surface):
        self.ui_manager.draw_ui(_display_surface)

    def update(self, _delta_time):
        self.ui_manager.update(_delta_time)
# Final Build

