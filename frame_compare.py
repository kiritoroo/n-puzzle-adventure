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

try:
    import numpy
except:
    os.system('pip install numpy')
    import numpy

from threading import Thread
import threading
import handler_node
import datetime
import settings
import time
import node
import dev_support
import getpass
import multiprocessing
import data

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
        self.final_puzzle = [1,2,3,0,5,6,7,8,4]
        self.ratio = (3,4,5)
        self.current_ratio = self.ratio[0]

        self.state1 = 'WAITTING'
        self.state2 = 'WAITTING'
        self.state3 = 'WAITTING'
        self.state4 = 'WAITTING'

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

        self.handlerNode1.root.set_draw_to_child(False)
        self.handlerNode2.root.set_draw_to_child(False)
        self.handlerNode3.root.set_draw_to_child(False)
        self.handlerNode4.root.set_draw_to_child(False)

        self.handlerNode1.set_algorithm('A* (Manhattan)')
        self.handlerNode2.set_algorithm('Hill Climb')
        self.handlerNode3.set_algorithm('A* (Euclidean)')
        self.handlerNode4.set_algorithm('BFS')

        self.dropdown_choose_1.disable()
        self.dropdown_choose_2.disable()
        self.dropdown_choose_3.disable()
        self.dropdown_choose_4.disable()

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
        self.label_timetext1 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "Time: 00:00",
                                                            relative_rect = pygame.Rect((650,30), (180, 30)),
                                                            object_id= "#label_text")
        self.label_timetext2 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "Time: 00:00",
                                                            relative_rect = pygame.Rect((1080,30), (180, 30)),
                                                            object_id= "#label_text")
        self.label_timetext3 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "Time: 00:00",
                                                            relative_rect = pygame.Rect((650,380), (180, 30)),
                                                            object_id= "#label_text")
        self.label_timetext4 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "Time: 00:00",
                                                            relative_rect = pygame.Rect((1080,380), (180, 30)),
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
        self.label_node_count4 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "visited node: ",
                                                            relative_rect = pygame.Rect((855,600), (200, 20)),
                                                            object_id= "#label_text_small")
        
        self.label_state_1 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "WAITING",
                                                            relative_rect = pygame.Rect((625,155), (200, 25)),
                                                            object_id= "#label_text_waitting")
        self.label_state_2 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "WAITING",
                                                            relative_rect = pygame.Rect((1055,155), (200, 25)),
                                                            object_id= "#label_text_waitting")
        self.label_state_3 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "WAITING",
                                                            relative_rect = pygame.Rect((625,500), (200, 25)),
                                                            object_id= "#label_text_waitting")
        self.label_state_4 = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "WAITING",
                                                            relative_rect = pygame.Rect((1055,500), (200, 25)),
                                                            object_id= "#label_text_waitting")

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
        
        #textbox
        self.input_start_state = pygame_gui.elements.UITextEntryLine(relative_rect = pygame.Rect((40,400), (230, 35)),
                                                                     manager = self.ui_manager,
                                                                     object_id = "#input_1")
        rect_choose_puzzle = pygame.Rect((40,450), (270, 35))
        self.puzzle_options = []
        for i in range(len(data.puzzle_random)):
            self.puzzle_options.append(str(i))
        self.dropdown_choose_puzzle = pygame_gui.elements.UIDropDownMenu(options_list = self.puzzle_options,
                                                                    starting_option = self.puzzle_options[0],
                                                                    relative_rect = rect_choose_puzzle,
                                                                    manager = self.ui_manager)

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
                                                                    starting_option = combobox_options_2[3],
                                                                    relative_rect = rect_choose_2,
                                                                    manager = self.ui_manager)
        rect_choose_3 = pygame.Rect((420,635), (270, 35)) #Node 3
        combobox_options_3 = ['BFS', 'A* (Manhattan)', 'A* (Euclidean)', 'Hill Climb']
        self.dropdown_choose_3 = pygame_gui.elements.UIDropDownMenu(options_list = combobox_options_3,
                                                                    starting_option = combobox_options_3[2],
                                                                    relative_rect = rect_choose_3,
                                                                    manager = self.ui_manager)
        rect_choose_4 = pygame.Rect((850,635), (270, 35)) #Node 4
        combobox_options_4 = ['BFS', 'A* (Manhattan)', 'A* (Euclidean)', 'Hill Climb']
        self.dropdown_choose_4 = pygame_gui.elements.UIDropDownMenu(options_list = combobox_options_4,
                                                                    starting_option = combobox_options_4[0],
                                                                    relative_rect = rect_choose_4,
                                                                    manager = self.ui_manager)
        
    def ui_event(self, _event):
        if _event.type == pygame_gui.UI_BUTTON_PRESSED:
            if _event.ui_element == self.button_back:
                self.handlerNode1.set_run(False)
                self.handlerNode2.set_run(False)
                self.handlerNode3.set_run(False)
                self.handlerNode4.set_run(False)
                self.frame_handler.set_current_frame('frame_menu')
            if _event.ui_element == self.button_Play:
                self.is_play = True

                self.label_timetext1.set_text('Time: 00:00s')
                self.label_timetext2.set_text('Time: 00:00s')
                self.label_timetext3.set_text('Time: 00:00s')
                self.label_timetext4.set_text('Time: 00:00s')

                self.state1 = 'FINDING'
                self.start_time1 = datetime.datetime.now()
                p1 = multiprocessing.Process(target = self.handlerNode1.find_solution())
                p1.start()
                self.state1 = 'FINAL'


                self.state2 = 'FINDING'
                self.start_time2 = datetime.datetime.now()
                p2 = multiprocessing.Process(target = self.handlerNode2.find_solution())
                p2.start()
                self.state2 = 'FINAL'

                self.state3 = 'FINDING'
                self.start_time3 = datetime.datetime.now()
                p3 = multiprocessing.Process(target = self.handlerNode3.find_solution())
                p3.start()
                self.state3 = 'FINAL'
                print(self.handlerNode1.node_count)
                print(str(self.handlerNode1.frame.execute_time1)[::-1].split(':', 1)[0][::-1])
                print(self.handlerNode2.node_count)
                print(str(self.handlerNode2.frame.execute_time2)[::-1].split(':', 1)[0][::-1])
                print(self.handlerNode3.node_count)
                print(str(self.handlerNode3.frame.execute_time3)[::-1].split(':', 1)[0][::-1])
                self.state4 = 'FINDING'
                self.start_time4 = datetime.datetime.now()
                p4 = multiprocessing.Process(target = self.handlerNode4.find_solution())
                p4.start()
                self.state4 = 'FINAL'
               
                print(self.handlerNode4.node_count)
                print(str(self.handlerNode4.frame.execute_time4)[::-1].split(':', 1)[0][::-1])




            if _event.ui_element == self.button_ok_start:
                self.handlerNode1.set_root(self.input_start_state.get_text())
                self.handlerNode2.set_root(self.input_start_state.get_text())
                self.handlerNode3.set_root(self.input_start_state.get_text())
                self.handlerNode4.set_root(self.input_start_state.get_text())

        if _event.type == pygame.KEYDOWN:
            if _event.key == pygame.K_F2:
                if self.is_show_dev:
                    self.is_show_dev = False
                else:
                    self.is_show_dev = True

        if _event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if _event.ui_element == self.dropdown_choose_puzzle:
                self.handlerNode1.root.set_puzzle(data.puzzle_random[int(_event.text)])
                self.handlerNode2.root.set_puzzle(data.puzzle_random[int(_event.text)])
                self.handlerNode3.root.set_puzzle(data.puzzle_random[int(_event.text)])
                self.handlerNode4.root.set_puzzle(data.puzzle_random[int(_event.text)])
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
        self.handlerNode1.draw_root()
        self.handlerNode2.draw_root()
        self.handlerNode3.draw_root()
        self.handlerNode4.draw_root()
        if self.is_show_dev:
            self.dev.draw(_display_surface)

    def update(self, _delta_time):
        self.handlerNode1.update_root()
        self.handlerNode2.update_root()
        self.handlerNode3.update_root()
        self.handlerNode4.update_root()
        self.ui_manager.update(_delta_time)
        self.development()
        self.dev.update(_delta_time)

        self.label_node_count1.set_text('visited node: ' + str(self.handlerNode1.node_count))
        self.label_node_count2.set_text('visited node: ' + str(self.handlerNode2.node_count))
        self.label_node_count3.set_text('visited node: ' + str(self.handlerNode3.node_count))
        self.label_node_count4.set_text('visited node: ' + str(self.handlerNode4.node_count))

        if self.handlerNode1.node_count > 4999:
            self.state1 = 'OVERTIME'
        if self.handlerNode2.node_count > 4999:
            self.state2 = 'OVERTIME'
        if self.handlerNode3.node_count > 4999:
            self.state3 = 'OVERTIME'
        if self.handlerNode4.node_count > 4999:
            self.state4 = 'OVERTIME'
    
        self.label_state_1.set_text(self.state1)
        self.label_state_2.set_text(self.state2)
        self.label_state_3.set_text(self.state3)
        self.label_state_4.set_text(self.state4)

    def development(self):
        pass
# Final Build

