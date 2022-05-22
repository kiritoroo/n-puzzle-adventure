from operator import contains
import pygame
import pygame_gui
import settings
import colors

pygame.init()
class DEV:
    def __init__(self, _frame):
        self.frame = _frame
        self.screen = self.frame.screen
        self.ui_manager = pygame_gui.UIManager((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), 'theme.json')

        self.init()
        self.ui_elements()

    def init(self):
        pass
    
    def ui_elements(self):
        self.pos = pygame.math.Vector2(0,0) 
        self.panel_surf = pygame.Surface((850, 400))
        self.panel_surf.set_alpha(150)
        self.panel_surf.fill(colors.GRAY_LIGHT)
        self.panel_rect = self.panel_surf.get_rect(topleft = self.pos)

        #General
        rect_general_1 = pygame.Rect((350, 350), (500, 50))
        self.label_general_1 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                        text = 'Mouse Pos: ' + str(pygame.mouse.get_pos()),
                                                        relative_rect = rect_general_1,
                                                        object_id = "#label_dev_2")
        rect_general_1 = pygame.Rect((50, 350), (500, 50))
        self.label_general_2 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                        text = 'Mouse Rel: ' + str(pygame.mouse.get_rel()),
                                                        relative_rect = rect_general_1,
                                                        object_id = "#label_dev_2")

        # Short Label
        rect_short_1 = pygame.Rect((20, 30), (300, 50))
        self.label_short_1 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                        text = '1. __________________________',
                                                        relative_rect = rect_short_1,
                                                        object_id = "#label_dev_1")
        rect_short_2 = pygame.Rect((20, 60), (300, 50))
        self.label_short_2 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                        text = '2. __________________________',
                                                        relative_rect = rect_short_2,
                                                        object_id = "#label_dev_1")

        rect_short_3 = pygame.Rect((20, 90), (300, 50))
        self.label_short_3 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                        text = '3. __________________________',
                                                        relative_rect = rect_short_3,
                                                        object_id = "#label_dev_1")

        rect_short_4 = pygame.Rect((20, 120), (300, 50))
        self.label_short_4 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                        text = '4. __________________________',
                                                        relative_rect = rect_short_4,
                                                        object_id = "#label_dev_1")  

        rect_short_5 = pygame.Rect((20, 150), (300, 50))
        self.label_short_5 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                        text = '5. __________________________',
                                                        relative_rect = rect_short_5,
                                                        object_id = "#label_dev_1") 
        
        rect_short_6 = pygame.Rect((20, 180), (300, 50))
        self.label_short_6 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                        text = '6. __________________________',
                                                        relative_rect = rect_short_6,
                                                        object_id = "#label_dev_1")                              

        rect_short_7 = pygame.Rect((20, 210), (300, 50))
        self.label_short_7 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                        text = '7. __________________________',
                                                        relative_rect = rect_short_7,
                                                        object_id = "#label_dev_1")   
    
        rect_short_8 = pygame.Rect((20, 240), (300, 50))
        self.label_short_8 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                        text = '8. __________________________',
                                                        relative_rect = rect_short_8,
                                                        object_id = "#label_dev_1")   
    
        rect_short_9 = pygame.Rect((20, 270), (300, 50))
        self.label_short_9 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                        text = '9. __________________________',
                                                        relative_rect = rect_short_9,
                                                        object_id = "#label_dev_1") 

        rect_short_10 = pygame.Rect((20, 300), (300, 50))
        self.label_short_8 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                        text = '10. __________________________',
                                                        relative_rect = rect_short_10,
                                                        object_id = "#label_dev_1")  

        # Long Label
        rect_long_1 = pygame.Rect((350, 30), (500, 50))
        self.label_long_1 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                        text = '1. _______________________________________',
                                                        relative_rect = rect_long_1,
                                                        object_id = "#label_dev_2")
        rect_long_2 = pygame.Rect((350, 60), (500, 50))
        self.label_long_2 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                        text = '2. _______________________________________',
                                                        relative_rect = rect_long_2,
                                                        object_id = "#label_dev_2")

        rect_long_3 = pygame.Rect((350, 90), (500, 50))
        self.label_long_3 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                        text = '3. _______________________________________',
                                                        relative_rect = rect_long_3,
                                                        object_id = "#label_dev_2")

        rect_long_4 = pygame.Rect((350, 120), (500, 50))
        self.label_long_4 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                        text = '4. _______________________________________',
                                                        relative_rect = rect_long_4,
                                                        object_id = "#label_dev_2")

        rect_long_5 = pygame.Rect((350, 150), (500, 50))
        self.label_long_5 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                        text = '5. _______________________________________',
                                                        relative_rect = rect_long_5,
                                                        object_id = "#label_dev_2")

        rect_long_6 = pygame.Rect((350, 180), (500, 50))
        self.label_long_6 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                        text = '6. _______________________________________',
                                                        relative_rect = rect_long_6,
                                                        object_id = "#label_dev_2")

        rect_long_7 = pygame.Rect((350, 210), (500, 50))
        self.label_long_7 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                        text = '7. _______________________________________',
                                                        relative_rect = rect_long_7,
                                                        object_id = "#label_dev_2")

        rect_long_8 = pygame.Rect((350, 240), (500, 50))
        self.label_long_8 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                        text = '8. _______________________________________',
                                                        relative_rect = rect_long_8,
                                                        object_id = "#label_dev_2")

        rect_long_9 = pygame.Rect((350, 270), (500, 50))
        self.label_long_9 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                        text = '9. _______________________________________',
                                                        relative_rect = rect_long_9,
                                                        object_id = "#label_dev_2")

        rect_long_10 = pygame.Rect((350, 300), (500, 50))
        self.label_long_10 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                        text = '10. ______________________________________',
                                                        relative_rect = rect_long_10,
                                                        object_id = "#label_dev_2")
    def draw(self, _display_surface):
        self.screen.blit(self.panel_surf, self.panel_rect)
        self.ui_manager.draw_ui(_display_surface)

    def update(self, _delta_time):
        self.label_general_1.set_text('Mouse Pos: ' + str(pygame.mouse.get_pos()))
        self.label_general_2.set_text('Mouse Rel: ' + str(pygame.mouse.get_rel()))
        self.ui_manager.update(_delta_time)