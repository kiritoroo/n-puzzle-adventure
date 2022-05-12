import pygame
import pygame_gui

import settings

class Frame:
    def __init__(self, _frame_handler, _screen):
        pygame.init()
        self.ui_manager = pygame_gui.UIManager((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), 'theme.json')
        self.frame_handler = _frame_handler
        self.screen = _screen
        self.ui_elements()

    def ui_elements(self):
        
        rect_push = pygame.Rect((100, 100), (100, 100))
        self.button_back = pygame_gui.elements.UIButton(relative_rect = rect_push,
                                                        text = "Back",
                                                        manager = self.ui_manager,
                                                        object_id="#button_back")
    
    def ui_event(self, _event):
        if _event.type == pygame_gui.UI_BUTTON_PRESSED:
            if _event.ui_element == self.button_back:
                self.frame_handler.set_current_frame('frame_menu')
                
        self.ui_manager.process_events(_event)

            
    def render(self, _display_surface):
        self.ui_manager.draw_ui(_display_surface)

    def update(self, _delta_time):
        self.ui_manager.update(_delta_time)


