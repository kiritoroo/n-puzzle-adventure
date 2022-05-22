import pygame
import pygame_gui
import dev_support
import settings

class Frame:
    def __init__(self, _frame_handler, _screen):
        pygame.init()
        self.ui_manager = pygame_gui.UIManager((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), 'theme.json')
        self.frame_handler = _frame_handler
        self.screen = _screen
        self.init()
        self.ui_elements()

    def init(self):
        self.is_show_dev = False
        self.dev = dev_support.DEV(self)

    def ui_elements(self):
        
        #button
        rect_back = pygame.Rect((8, 650), (100, 50))
        self.button_back = pygame_gui.elements.UIButton(relative_rect = rect_back,
                                                        text = "Back",
                                                        manager = self.ui_manager,
                                                        object_id="#button_back")

        rect_up = pygame.Rect((25, 50), (125, 50))
        self.button_up = pygame_gui.elements.UIButton(relative_rect = rect_up,
                                                        text = "↑",
                                                        manager = self.ui_manager)

        rect_right = pygame.Rect((25, 105), (125, 50))
        self.button_right = pygame_gui.elements.UIButton(relative_rect = rect_right,
                                                        text = "→",
                                                        manager = self.ui_manager)

        rect_left = pygame.Rect((25, 160), (125, 50))
        self.button_left = pygame_gui.elements.UIButton(relative_rect = rect_left,
                                                        text = "←",
                                                        manager = self.ui_manager)

        rect_down = pygame.Rect((25, 215), (125, 50))
        self.button_down = pygame_gui.elements.UIButton(relative_rect = rect_down,
                                                        text = "↓",
                                                        manager = self.ui_manager)

        rect_general = pygame.Rect((25, 280), (125, 50))
        self.button_Play = pygame_gui.elements.UIButton(relative_rect = rect_general,
                                                        text = "Gerenal",
                                                        manager = self.ui_manager,
                                                        object_id = "#button_play" )

        rect_solve = pygame.Rect((25, 480), (125, 50))
        self.button_solve = pygame_gui.elements.UIButton(relative_rect = rect_solve,
                                                        text = "Slove",
                                                        manager = self.ui_manager,
                                                        object_id = "#button_play" )

        rect_ok1 = pygame.Rect((225, 540), (40, 35))
        self.button_ok_1 = pygame_gui.elements.UIButton(relative_rect = rect_ok1,
                                                        text = "OK",
                                                        manager = self.ui_manager,
                                                        object_id = "#button_ok")

        rect_ok2 = pygame.Rect((225, 580), (40, 35))
        self.button_ok_2 = pygame_gui.elements.UIButton(relative_rect = rect_ok2,
                                                        text = "OK",
                                                        manager = self.ui_manager,
                                                        object_id = "#button_ok")

        rect_play_solution = pygame.Rect((1123, 650), (125, 50))
        self.button_play_solution = pygame_gui.elements.UIButton(relative_rect = rect_play_solution,
                                                        text = "PLay Solution",
                                                        manager = self.ui_manager,
                                                        object_id = "#button_play_solution")

        # Panel
        rect_Pane1 = pygame.Rect((8,40), (120, 600))
        self.panel_1 = pygame_gui.elements.ui_panel.UIPanel(relative_rect = rect_Pane1,
                                                            starting_layer_height = 0,
                                                            manager = self.ui_manager)

        rect_Pane2 = pygame.Rect((1110,10), (150, 700))
        self.panel_2 = pygame_gui.elements.ui_panel.UIPanel(relative_rect = rect_Pane2,
                                                            starting_layer_height = 0,
                                                            manager= self.ui_manager,
                                                            object_id = "#panel_2")

        # Label
        rect_guide = pygame.Rect((2, 0), (250, 50))
        self.label_guide = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = 'F2 - Open/Close Development',
                                                            relative_rect = rect_guide,
                                                            object_id = "#label_dev_3")

        self.label_time = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "Time: ",
                                                            relative_rect = pygame.Rect((0, 355), (92, 50)),
                                                            object_id = "#label_guide")

        self.label_step = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "Steps: ",
                                                            relative_rect = pygame.Rect((0, 380 ), (100, 50)),
                                                            object_id = "#label_guide")

        # Drop down
        rect_choose_picture = pygame.Rect((15,440), (250, 35))
        picture_options = ['Algorithm 1', 'Algorithm 2', 'Algorithm 3']
        self.dropdown_choose_picture = pygame_gui.elements.UIDropDownMenu(options_list = picture_options,
                                                                    starting_option = picture_options[0],
                                                                    relative_rect = rect_choose_picture,
                                                                    manager = self.ui_manager)

        # Input
        self.input_start_state = pygame_gui.elements.UITextEntryLine(relative_rect = pygame.Rect((15, 540), (215, 35)),
                                                                     manager = self.ui_manager,
                                                                     object_id = "#input_1")

        self.input_goal_state = pygame_gui.elements.UITextEntryLine(relative_rect = pygame.Rect((15, 580), (215, 35)),
                                                                     manager = self.ui_manager,
                                                                     object_id = "#input_1")

    def render(self, _display_surface):
        self.ui_manager.draw_ui(_display_surface)
        if self.is_show_dev:
            self.dev.draw(_display_surface)

    def update(self, _delta_time):
        self.ui_manager.update(_delta_time)
        if self.is_show_dev:
            self.development()
            self.dev.update(_delta_time)
    
    def ui_event(self, _event):
        if _event.type == pygame.KEYDOWN:
            if _event.key == pygame.K_F2:
                if self.is_show_dev:
                    self.is_show_dev = False
                else:
                    self.is_show_dev = True

        if _event.type == pygame_gui.UI_BUTTON_PRESSED:
            if _event.ui_element == self.button_back:
                self.frame_handler.set_current_frame('frame_menu')
        
        self.ui_manager.process_events(_event)
    
    def get_input(self):
        pass

    def development(self):
        pass
        

