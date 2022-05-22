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
        #panel
        rect_Pane1 = pygame.Rect((30,20), (300, 650))
        self.panel_1 = pygame_gui.elements.ui_panel.UIPanel(relative_rect = rect_Pane1,
                                                            starting_layer_height=0,
                                                            manager= self.ui_manager)
        rect_Pane_algorithm1 = pygame.Rect((420,20), (410, 310))
        self.panel_algorithm1 = pygame_gui.elements.ui_panel.UIPanel(relative_rect = rect_Pane_algorithm1,
                                                            starting_layer_height=0,
                                                            manager= self.ui_manager,
                                                            object_id= "panel1")
        rect_Pane_algorithm2 = pygame.Rect((850,20), (410, 310))
        self.panel_algorithm2 = pygame_gui.elements.ui_panel.UIPanel(relative_rect = rect_Pane_algorithm2,
                                                            starting_layer_height=0,
                                                            manager= self.ui_manager,
                                                            object_id= "panel1")
        rect_Pane_algorithm3 = pygame.Rect((420,360), (410, 310))
        self.panel_algorithm3 = pygame_gui.elements.ui_panel.UIPanel(relative_rect = rect_Pane_algorithm3,
                                                            starting_layer_height=0,
                                                            manager= self.ui_manager,
                                                            object_id= "panel1")
        rect_Pane_algorithm4 = pygame.Rect((850,360), (410, 310))
        self.panel_algorithm4 = pygame_gui.elements.ui_panel.UIPanel(relative_rect = rect_Pane_algorithm4,
                                                            starting_layer_height=0,
                                                            manager= self.ui_manager,
                                                            object_id= "panel1")
        
        #label
        self.label_F2 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                                      text = "F2 - Open/Close Development",
                                                                      relative_rect = pygame.Rect((10,0), (290, 20)),
                                                                      object_id = "#label_dev_1")
        self.label_timeAVG = pygame_gui.elements.ui_label.UILabel(manager= self.ui_manager,
                                                                  text = "Time AVG:",
                                                                  relative_rect = pygame.Rect((35,50),(130,500)),
                                                                  object_id= "#label_guide_1")
        self.label_stepAVG = pygame_gui.elements.ui_label.UILabel(manager= self.ui_manager,
                                                                  text = "Step AVG:",
                                                                  relative_rect = pygame.Rect((35,50),(130,600)),
                                                                  object_id= "#label_guide_1")
        self.label_time = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "00:00:00",
                                                            relative_rect = pygame.Rect((40,50), (350, 500)),
                                                            object_id = "#label_time_1")
        self.label_time = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "0",
                                                            relative_rect = pygame.Rect((40,50), (250, 600)),
                                                            object_id = "#label_time_1")
        self.label_timetext1 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "Time:",
                                                            relative_rect = pygame.Rect((690,30), (50, 30)),
                                                            object_id= "#label_text")
        self.label_timetext2 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "Time:",
                                                            relative_rect = pygame.Rect((690,380), (50, 30)),
                                                            object_id= "#label_text")
        self.label_timetext3 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "Time:",
                                                            relative_rect = pygame.Rect((1120,30), (50, 30)),
                                                            object_id= "#label_text")
        self.label_timetext4 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "Time:",
                                                            relative_rect = pygame.Rect((1120,380), (50, 30)),
                                                            object_id= "#label_text")
        self.label_timepanel1 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "00:00",
                                                            relative_rect = pygame.Rect((745,31), (60, 30)),
                                                            object_id= "#label_text")
        self.label_timepanel2 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "00:00",
                                                            relative_rect = pygame.Rect((1175,31), (60, 30)),
                                                            object_id= "#label_text")
        self.label_timepanel3 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "00:00",
                                                            relative_rect = pygame.Rect((745,381), (60, 30)),
                                                            object_id= "#label_text")
        self.label_timepanel4 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "00:00",
                                                            relative_rect = pygame.Rect((1175,381), (60, 30)),
                                                            object_id= "#label_text")
        #button
        rect_push = pygame.Rect((30, 670), (100, 50))
        self.button_back = pygame_gui.elements.UIButton(relative_rect = rect_push,
                                                        text = "Back",
                                                        manager = self.ui_manager,
                                                        object_id="#button_back")
        rect_play = pygame.Rect((130, 540), (100,50))
        self.button_Play = pygame_gui.elements.UIButton(relative_rect = rect_play,
                                                        text = "Play",
                                                        manager = self.ui_manager,
                                                        object_id = "#button_play")
        rect_ok_start = pygame.Rect((270, 400), (40, 35))
        self.button_ok_start = pygame_gui.elements.UIButton(relative_rect = rect_ok_start,
                                                        text = "OK",
                                                        manager = self.ui_manager,
                                                        object_id = "#button_ok")
        rect_ok_goal = pygame.Rect((270, 450), (40, 35))
        self.button_ok_goal = pygame_gui.elements.UIButton(relative_rect = rect_ok_goal,
                                                        text = "OK",
                                                        manager = self.ui_manager,
                                                        object_id = "#button_ok")
        
        #textbox
        self.input_start_state = pygame_gui.elements.UITextEntryLine(relative_rect = pygame.Rect((40,400), (230, 35)),
                                                                     manager = self.ui_manager,
                                                                     object_id = "#input_1")
        self.input_goal_state = pygame_gui.elements.UITextEntryLine(relative_rect = pygame.Rect((40,450), (230, 35)),
                                                                     manager = self.ui_manager,
                                                                     object_id = "#input_1")
        
        #dropdown
        rect_choose_1 = pygame.Rect((420,295), (270, 35))
        combobox_options_1 = ['Algorithm 1', 'Algorithm 2', 'Algorithm 3']
        self.dropdown_choose_1 = pygame_gui.elements.UIDropDownMenu(options_list = combobox_options_1,
                                                                    starting_option = combobox_options_1[0],
                                                                    relative_rect = rect_choose_1,
                                                                    manager = self.ui_manager)
        rect_choose_2 = pygame.Rect((850,295), (270, 35))
        combobox_options_2 = ['Algorithm 1', 'Algorithm 2', 'Algorithm 3']
        self.dropdown_choose_2 = pygame_gui.elements.UIDropDownMenu(options_list = combobox_options_2,
                                                                    starting_option = combobox_options_2[0],
                                                                    relative_rect = rect_choose_2,
                                                                    manager = self.ui_manager)
        rect_choose_3 = pygame.Rect((420,635), (270, 35))
        combobox_options_3 = ['Algorithm 1', 'Algorithm 2', 'Algorithm 3']
        self.dropdown_choose_3 = pygame_gui.elements.UIDropDownMenu(options_list = combobox_options_3,
                                                                    starting_option = combobox_options_3[0],
                                                                    relative_rect = rect_choose_3,
                                                                    manager = self.ui_manager)
        rect_choose_4 = pygame.Rect((850,635), (270, 35))
        combobox_options_4 = ['Algorithm 1', 'Algorithm 2', 'Algorithm 3']
        self.dropdown_choose_4 = pygame_gui.elements.UIDropDownMenu(options_list = combobox_options_4,
                                                                    starting_option = combobox_options_4[0],
                                                                    relative_rect = rect_choose_4,
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


