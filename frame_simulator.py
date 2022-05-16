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
        
        #button
        rect_back = pygame.Rect((8, 650), (100, 50))
        self.button_back = pygame_gui.elements.UIButton(relative_rect = rect_back,
                                                        text = "Back",
                                                        manager = self.ui_manager,
                                                        object_id="#button_back")
        
        rect_Solve = pygame.Rect((25, 50), (125, 50))
        self.button_Solve = pygame_gui.elements.UIButton(relative_rect = rect_Solve,
                                                        text = "↑",
                                                        manager = self.ui_manager)
        
        rect_Solve = pygame.Rect((25, 105), (125, 50))
        self.button_Solve = pygame_gui.elements.UIButton(relative_rect = rect_Solve,
                                                        text = "→",
                                                        manager = self.ui_manager)
        
        rect_Solve = pygame.Rect((25, 160), (125, 50))
        self.button_Solve = pygame_gui.elements.UIButton(relative_rect = rect_Solve,
                                                        text = "←",
                                                        manager = self.ui_manager)
        
        rect_Solve = pygame.Rect((25, 215), (125, 50))
        self.button_Solve = pygame_gui.elements.UIButton(relative_rect = rect_Solve,
                                                        text = "↓",
                                                        manager = self.ui_manager)
        
        rect_Play = pygame.Rect((25, 280), (125, 50))
        self.button_Play = pygame_gui.elements.UIButton(relative_rect = rect_Play,
                                                        text = "Gerenal",
                                                        manager = self.ui_manager,
                                                        object_id = "#button_play" )
        
        rect_Slove = pygame.Rect((25, 480), (125, 50))
        self.button_Play = pygame_gui.elements.UIButton(relative_rect = rect_Slove,
                                                        text = "Slove",
                                                        manager = self.ui_manager,
                                                        object_id = "#button_play" )
        
        rect_Solve = pygame.Rect((230, 540), (35, 35))
        self.button_Solve = pygame_gui.elements.UIButton(relative_rect = rect_Solve,
                                                        text = "OK",
                                                        manager = self.ui_manager)
        
        rect_Solve = pygame.Rect((230, 580), (35, 35))
        self.button_Solve = pygame_gui.elements.UIButton(relative_rect = rect_Solve,
                                                        text = "OK",
                                                        manager = self.ui_manager)
        
        # Panel
        rect_Pane1 = pygame.Rect((8,40), (100, 600))
        self.panel_1 = pygame_gui.elements.ui_panel.UIPanel(relative_rect = rect_Pane1,
                                                            starting_layer_height=0,
                                                            manager= self.ui_manager)
        
        rect_Pane1 = pygame.Rect((1110,10), (150, 700))
        self.panel_1 = pygame_gui.elements.ui_panel.UIPanel(relative_rect = rect_Pane1,
                                                            starting_layer_height=0,
                                                            manager= self.ui_manager)
        
        rect_Solve = pygame.Rect((1123, 650), (125, 50))
        self.button_Solve = pygame_gui.elements.UIButton(relative_rect = rect_Solve,
                                                        text = "PLay Solution",
                                                        manager = self.ui_manager)
        
        # Label
        rect_guide = pygame.Rect((2, 0), (250, 50))
        self.label_guide = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = 'F2 - Open/Close Development',
                                                            relative_rect = rect_guide,
                                                            object_id = "#label_dev_3")
        
        self.label_up = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "Time: ",
                                                            relative_rect = pygame.Rect((0, 355), (92, 50)),
                                                            object_id = "#label_guide")
        
        self.label_up = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "Steps: ",
                                                            relative_rect = pygame.Rect((0, 380 ), (100, 50)),
                                                            object_id = "#label_guide")
        
        # Drop down
        rect_choose_picture = pygame.Rect((15,440), (250, 35))
        picture_options = ['', '1', '2']
        self.dropdown_choose_picture = pygame_gui.elements.UIDropDownMenu(options_list = picture_options,
                                                                    starting_option = picture_options[0],
                                                                    relative_rect = rect_choose_picture,
                                                                    manager = self.ui_manager)
        
        ###Star STate Input
        self.input_start_state = pygame_gui.elements.UITextEntryLine(relative_rect = pygame.Rect((15, 540), (218, 35)),
                                                                     manager = self.ui_manager)
        
        self.input_start_state = pygame_gui.elements.UITextEntryLine(relative_rect = pygame.Rect((15, 580), (218, 35)),
                                                                     manager = self.ui_manager)
    
    def ui_event(self, _event):
        if _event.type == pygame_gui.UI_BUTTON_PRESSED:
            if _event.ui_element == self.button_back:
                self.frame_handler.set_current_frame('frame_menu')
                
        self.ui_manager.process_events(_event)

            
    def render(self, _display_surface):
        self.ui_manager.draw_ui(_display_surface)

    def update(self, _delta_time):
        self.ui_manager.update(_delta_time)

