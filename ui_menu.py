import pygame
import pygame_gui

class UI:
    def __init__(self):
        pygame.init()
        self.ui_manager = pygame_gui.UIManager((1280, 800), 'theme.json')
        self.ui_elements()

    def ui_elements(self):
        
        rect_push = pygame.Rect((100, 100), (100, 100))
        self.button_push = pygame_gui.elements.UIButton(relative_rect = rect_push,
                                                        text = "Push",
                                                        manager = self.ui_manager,
                                                        object_id="#button_push")
    
    def ui_event(self, _event):
        if _event.type == pygame_gui.UI_BUTTON_PRESSED:
            if _event.ui_element == self.button_push:
                print('press push')

        self.ui_manager.process_events(_event)

            
    def render(self, _display_surface):
        self.ui_manager.draw_ui(_display_surface)

    def update(self, _delta_time):
        self.ui_manager.update(_delta_time)


