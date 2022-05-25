from threading import Thread
import threading
import pygame
import pygame_gui
import handler_node
import datetime
import settings
import numpy
import time
import node
import dev_support
import getpass
import multiprocessing

class Frame:
    def __init__(self, _frame_handler, _screen):
        pygame.init()
        self.ui_manager = pygame_gui.UIManager((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), 'theme.json')
        self.frame_handler = _frame_handler
        self.screen = _screen
        self.ui_elements()
        self.init()

    def init(self):
        self.is_play = False
        self.is_show_dev = False
        self.final_puzzle = [1,2,3,0,5,6,4
        
        ,7,8]

        self.ratio = (3,4,5)
        self.current_ratio = self.ratio[0]
        self.handlerNode1 = handler_node.HandlerNode(self.screen, self, self.current_ratio, 500)
        self.handlerNode2 = handler_node.HandlerNode(self.screen, self, self.current_ratio, 500)
        self.handlerNode3 = handler_node.HandlerNode(self.screen, self, self.current_ratio, 500)
        self.handlerNode4 = handler_node.HandlerNode(self.screen, self, self.current_ratio, 500)
        self.handlerNode1.root.set_pos((460,60))
        self.handlerNode2.root.set_pos((890,60))
        self.handlerNode3.root.set_pos((460,390))
        self.handlerNode4.root.set_pos((890,390))
        self.handlerNode1.root.set_puzzle(self.final_puzzle)
        self.handlerNode2.root.set_puzzle(self.final_puzzle)
        self.handlerNode3.root.set_puzzle(self.final_puzzle)
        self.handlerNode4.root.set_puzzle(self.final_puzzle)



        self.dev = dev_support.DEV(self)

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
        self.label_step = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "0",
                                                            relative_rect = pygame.Rect((40,50), (250, 600)),
                                                            object_id = "#label_time_1")

        self.label_timetext1 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "Time: 00:00",
                                                            relative_rect = pygame.Rect((680,30), (150, 30)),
                                                            object_id= "#label_text")
        self.label_timetext2 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "Time: 00:00",
                                                            relative_rect = pygame.Rect((680,380), (150, 30)),
                                                            object_id= "#label_text")
        self.label_timetext3 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "Time: 00:00",
                                                            relative_rect = pygame.Rect((1110,30), (150, 30)),
                                                            object_id= "#label_text")
        self.label_timetext4 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "Time: 00:00",
                                                            relative_rect = pygame.Rect((1110,380), (150, 30)),
                                                            object_id= "#label_text")


        self.label_node_count1 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "visited node: ",
                                                            relative_rect = pygame.Rect((425,255), (200, 20)),
                                                            object_id= "#label_text_small")
        self.label_node_count2 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "visited node: ",
                                                            relative_rect = pygame.Rect((855,255), (200, 20)),
                                                            object_id= "#label_text_small")
        self.label_node_count3 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "visited node: ",
                                                            relative_rect = pygame.Rect((425,600), (200, 20)),
                                                            object_id= "#label_text_small")
        self.label_nod_count4 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "visited node: ",
                                                            relative_rect = pygame.Rect((855,600), (200, 20)),
                                                            object_id= "#label_text_small")
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
        rect_choose_1 = pygame.Rect((420,295), (270, 35)) #Node 1
        combobox_options_1 = ['BFS', 'A* (Manhattan)', 'A* (Euclidean)', 'Hill Climb']
        self.dropdown_choose_1 = pygame_gui.elements.UIDropDownMenu(options_list = combobox_options_1,
                                                                    starting_option = combobox_options_1[1],
                                                                    relative_rect = rect_choose_1,
                                                                    manager = self.ui_manager)
        rect_choose_2 = pygame.Rect((850,295), (270, 35)) #Node 2
        combobox_options_2 = ['BFS', 'A* (Manhattan)', 'A* (Euclidean)', 'Hill Climb']
        self.dropdown_choose_2 = pygame_gui.elements.UIDropDownMenu(options_list = combobox_options_2,
                                                                    starting_option = combobox_options_2[1],
                                                                    relative_rect = rect_choose_2,
                                                                    manager = self.ui_manager)
        rect_choose_3 = pygame.Rect((420,635), (270, 35)) #Node 3
        combobox_options_3 = ['BFS', 'A* (Manhattan)', 'A* (Euclidean)', 'Hill Climb']
        self.dropdown_choose_3 = pygame_gui.elements.UIDropDownMenu(options_list = combobox_options_3,
                                                                    starting_option = combobox_options_3[1],
                                                                    relative_rect = rect_choose_3,
                                                                    manager = self.ui_manager)
        rect_choose_4 = pygame.Rect((850,635), (270, 35)) #Node 4
        combobox_options_4 = ['BFS', 'A* (Manhattan)', 'A* (Euclidean)', 'Hill Climb']
        self.dropdown_choose_4 = pygame_gui.elements.UIDropDownMenu(options_list = combobox_options_4,
                                                                    starting_option = combobox_options_4[1],
                                                                    relative_rect = rect_choose_4,
                                                                    manager = self.ui_manager)
        
    def ui_event(self, _event):
        if _event.type == pygame_gui.UI_BUTTON_PRESSED:
            if _event.ui_element == self.button_back:
                self.frame_handler.set_current_frame('frame_menu')
            if _event.ui_element == self.button_Play:
                self.is_play = True
                p1 = multiprocessing.Process(target = self.handlerNode1.find_solution())
                p2 = multiprocessing.Process(target = self.handlerNode2.find_solution())
                p3 = multiprocessing.Process(target = self.handlerNode3.find_solution())
                p4 = multiprocessing.Process(target = self.handlerNode4.find_solution())
                p1.start()
                p2.start()
                p3.start()
                p4.start()

        if _event.type == pygame.KEYDOWN:
            if _event.key == pygame.K_F2:
                if self.is_show_dev:
                    self.is_show_dev = False
                else:
                    self.is_show_dev = True

        if _event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if _event.ui_element == self.dropdown_choose_1:
                self.handlerNode1.set_algorithm(_event.text)
            if _event.ui_element == self.dropdown_choose_2:
                self.handlerNode2.set_algorithm(_event.text)
            if _event.ui_element == self.dropdown_choose_3:
                self.handlerNode3.set_algorithm(_event.text)
            if _event.ui_element == self.dropdown_choose_4:
                self.handlerNode4.set_algorithm(_event.text)

        self.ui_manager.process_events(_event)
            
    def render(self, _display_surface):
        self.ui_manager.draw_ui(_display_surface)
        self.handlerNode1.draw()
        self.handlerNode2.draw()
        self.handlerNode3.draw()
        self.handlerNode4.draw()
        if self.is_show_dev:
            self.dev.draw(_display_surface)

    def update(self, _delta_time):
        self.handlerNode1.update()
        self.handlerNode2.update()
        self.handlerNode3.update()
        self.handlerNode4.update()
        self.ui_manager.update(_delta_time)
        self.development()
        self.dev.update(_delta_time)

    def development(self):
        pass


