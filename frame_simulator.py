from logging import root
import pygame
import pygame_gui
import dev_support
import settings
import handler_node
import node
import time
import datetime
import numpy

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
        self.ratio = (3,4,5)
        self.current_ratio = self.ratio[0]
        self.rect_list = []
        self.mouse_rel = (0,0)
        self.zoom = 1
        self.final_image = None
        self.current_image_path = None
        self.stop = False

        self.dev = dev_support.DEV(self)
        self.handlerNode = handler_node.HandlerNode(self.screen, self, self.current_ratio, 300)

    def ui_elements(self):
        
        #button
        rect_back = pygame.Rect((8, 650), (100, 50))
        self.button_back = pygame_gui.elements.UIButton(relative_rect = rect_back,
                                                        text = "Back",
                                                        manager = self.ui_manager,
                                                        object_id="#button_back")

        rect_up = pygame.Rect((25, 135), (80, 30))
        self.rect_list.append(rect_up)
        self.button_up = pygame_gui.elements.UIButton(relative_rect = rect_up,
                                                        text = "↑",
                                                        manager = self.ui_manager)

        rect_right = pygame.Rect((25, 170), (80, 30))
        self.rect_list.append(rect_right)
        self.button_right = pygame_gui.elements.UIButton(relative_rect = rect_right,
                                                        text = "→",
                                                        manager = self.ui_manager)

        rect_down = pygame.Rect((25, 215), (80, 30))
        self.rect_list.append(rect_down)
        self.button_down = pygame_gui.elements.UIButton(relative_rect = rect_down,
                                                        text = "↓",
                                                        manager = self.ui_manager)

        rect_left = pygame.Rect((25, 250), (80, 30))
        self.rect_list.append(rect_left)
        self.button_left = pygame_gui.elements.UIButton(relative_rect = rect_left,
                                                        text = "←",
                                                        manager = self.ui_manager)

        rect_general = pygame.Rect((25, 280), (125, 50))
        self.rect_list.append(rect_general)
        self.button_general = pygame_gui.elements.UIButton(relative_rect = rect_general,
                                                        text = "Gerenal",
                                                        manager = self.ui_manager,
                                                        object_id = "#button_play" )

        rect_solve = pygame.Rect((25, 480), (125, 50))
        self.rect_list.append(rect_solve)
        self.button_solve = pygame_gui.elements.UIButton(relative_rect = rect_solve,
                                                        text = "Slove",
                                                        manager = self.ui_manager,
                                                        object_id = "#button_play" )

        rect_ok1 = pygame.Rect((225, 540), (40, 35))
        self.button_set_start = pygame_gui.elements.UIButton(relative_rect = rect_ok1,
                                                        text = "OK",
                                                        manager = self.ui_manager,
                                                        object_id = "#button_ok")

        rect_ok2 = pygame.Rect((225, 580), (40, 35))
        self.button_set_goal = pygame_gui.elements.UIButton(relative_rect = rect_ok2,
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
        rect_choose_algorithm = pygame.Rect((15,440), (250, 35))
        self.rect_list.append(rect_choose_algorithm)
        algorithm_options = ['BFS', 'A* (Manhattan)', 'A* (Euclidean)', 'Hill Climb']
        self.dropdown_choose_algorithm = pygame_gui.elements.UIDropDownMenu(options_list = algorithm_options,
                                                                    starting_option = algorithm_options[1],
                                                                    relative_rect = rect_choose_algorithm,
                                                                    manager = self.ui_manager)

        # Input
        self.input_start_state = pygame_gui.elements.UITextEntryLine(relative_rect = pygame.Rect((15, 540), (215, 35)),
                                                                     manager = self.ui_manager,
                                                                     object_id = "#input_1")

        self.input_goal_state = pygame_gui.elements.UITextEntryLine(relative_rect = pygame.Rect((15, 580), (215, 35)),
                                                                     manager = self.ui_manager,
                                                                     object_id = "#input_1")
       
        # Drop down
        rect_choose_picture = pygame.Rect((25, 50), (150, 40))
        self.rect_list.append(rect_choose_picture)
        self.picture_options = ['Only Number', 'Picture 1', 'Picture 2']
        self.dropdown_choose_picture = pygame_gui.elements.UIDropDownMenu(options_list = self.picture_options,
                                                                    starting_option = self.picture_options[0],
                                                                    relative_rect = rect_choose_picture,
                                                                    manager = self.ui_manager)
        rect_choose_level = pygame.Rect((25, 90), (150, 40))
        self.rect_list.append(rect_choose_level)
        self.level_options = ['Easy', 'Medium', 'Hard', 'Legend']
        self.dropdown_choose_level = pygame_gui.elements.UIDropDownMenu(options_list = self.level_options,
                                                                    starting_option = self.level_options[0],
                                                                    relative_rect = rect_choose_level,
                                                                    manager = self.ui_manager)
    
    def render(self, _display_surface):
        self.handlerNode.draw()
        self.ui_manager.draw_ui(_display_surface)
        if self.is_show_dev:
            self.dev.draw(_display_surface)
        # Top layer
    
        if self.handlerNode.proplem_node.is_same_puzzle(self.handlerNode.goal_puzzle[self.current_ratio-3]):
            self.handlerNode.proplem_node.set_color("GREEN")
        else:
            self.handlerNode.proplem_node.set_color("ORANGE")
        self.handlerNode.proplem_node.draw()

    def update(self, _delta_time):
        if len(self.handlerNode.root.children) > 0:
            self.dropdown_choose_level.disable()
            self.dropdown_choose_picture.disable()
        else:
            self.dropdown_choose_level.enable()
            self.dropdown_choose_picture.enable()

        self.get_input()
        self.handlerNode.update()
        self.ui_manager.update(_delta_time)

        self.development()
        self.dev.update(_delta_time)
        
    def ui_event(self, _event):
        if _event.type == pygame.MOUSEWHEEL:
            if _event.y == 1 and self.zoom < 2:
                self.zoom += 0.1
            if _event.y == -1 and self.zoom > 0.5:
                self.zoom -= 0.1
            self.handlerNode.zoom(self.zoom)

        if _event.type == pygame.KEYDOWN:
            if _event.key == pygame.K_F2:
                if self.is_show_dev:
                    self.is_show_dev = False
                else:
                    self.is_show_dev = True
            if self.handlerNode.node_choose != None:
                if _event.key == pygame.K_SPACE:
                    self.handlerNode.node_choose.general_child()
                if _event.key == pygame.K_UP:
                    self.handlerNode.node_choose.child_up()
                if _event.key == pygame.K_RIGHT:
                    self.handlerNode.node_choose.child_right()
                if _event.key == pygame.K_DOWN:
                    self.handlerNode.node_choose.child_down()
                if _event.key == pygame.K_LEFT:
                    self.handlerNode.node_choose.child_left()
            self.handlerNode.all_node = []
            self.handlerNode.get_all_node(self.handlerNode.root)
            self.handlerNode.get_max_level()
            self.handlerNode.zoom(self.zoom)

        if _event.type == pygame_gui.UI_BUTTON_PRESSED:
            if _event.ui_element == self.button_back:
                self.stop = True
                self.frame_handler.set_current_frame('frame_menu')
            if _event.ui_element == self.button_solve:
                self.handlerNode.solve_all ()
            if _event.ui_element == self.button_play_solution:
                self.handlerNode.play_solution()
            if _event.ui_element == self.button_set_start:
                self.handlerNode.set_root(self.input_start_state.get_text())
            if _event.ui_element == self.button_set_goal:
                self.handlerNode.set_goal(self.input_goal_state.get_text())
            if self.handlerNode.node_choose != None:
                if _event.ui_element == self.button_general:
                    self.handlerNode.node_choose.general_child()
                if _event.ui_element == self.button_up:
                    self.handlerNode.node_choose.child_up()
                if _event.ui_element == self.button_right:
                    self.handlerNode.node_choose.child_right()
                if _event.ui_element == self.button_down:
                    self.handlerNode.node_choose.child_down()
                if _event.ui_element == self.button_left:
                    self.handlerNode.node_choose.child_left()
            self.handlerNode.all_node = []
            self.handlerNode.get_all_node(self.handlerNode.root)
            self.handlerNode.get_max_level()
            self.handlerNode.zoom(self.zoom)

        if _event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if _event.ui_element == self.dropdown_choose_picture:
                if _event.text == 'Only Number':
                    self.current_image_path = None
                elif _event.text == 'Picture 1':
                    self.current_image_path = 'resources/img1.jpg'
                elif _event.text == 'Picture 2':
                    self.current_image_path = 'resources/img2.jpg'
                self.set_final_image(self.current_image_path)
            if _event.ui_element == self.dropdown_choose_level:
                if _event.text == 'Easy':
                    self.reset_ratio(self.ratio[0])
                elif _event.text == 'Medium':
                    self.reset_ratio(self.ratio[1])
                elif _event.text == 'Hard':
                    self.reset_ratio(self.ratio[2])
                else:
                    pass
            if _event.ui_element == self.dropdown_choose_algorithm:
                self.handlerNode.set_algorithm(_event.text)

        # MOUSEBUTTONDOWN MOUSEBUTTONUP MOUSEBUTTONMOTION MOUSEWHEEL
        # 1 - Left, 2 - Mid, 3 - Right, 4 - Up, 5 - Down
        if _event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            check = False
            for i in range(len(self.rect_list)):
                if self.rect_list[i].collidepoint(mouse_pos):
                    check = True
            if check == False:
                self.handlerNode.check_all_collider_mouse(_event.button)
            
        self.ui_manager.process_events(_event)
    
    def get_input(self):
        if pygame.mouse.get_pressed()[2]:
            self.mouse_rel = pygame.mouse.get_rel()
            self.handlerNode.move(self.handlerNode.root, pygame.math.Vector2(self.mouse_rel))
    
    # HARDCORE
    def set_final_image(self, _path):
        if _path == None:
            self.final_image = None
            self.handlerNode.set_image(None, self.current_ratio)
        else:
            self.final_image = pygame.image.load(_path)           
            self.handlerNode.set_image(_path, self.current_ratio)

    def reset_ratio(self, _ratio):
        self.current_ratio = _ratio
        self.handlerNode.set_ratio(_ratio)
        numpy.random.shuffle(self.handlerNode.start_puzzle[self.current_ratio-3])
        self.handlerNode.root.set_puzzle_2(self.handlerNode.start_puzzle[self.current_ratio-3]) 
        if self.final_image != None:
            self.set_final_image(self.current_image_path)
        self.handlerNode.root.create_puzzle()
    # End HARDCORE
    
    def development(self):
        self.dev.label_short_1.set_text('root is choose: ' + str(self.handlerNode.root.is_choose))
        self.dev.label_short_2.set_text('root pos: ' + str(self.handlerNode.root.pos))
        self.dev.label_short_4.set_text('zoom: ' + "{:.2f}".format(self.zoom))
        self.dev.label_long_1.set_text('Frame: ' + str(self.handlerNode.frame.__module__))
        self.dev.label_long_2.set_text('Node count: ' + str(len(self.handlerNode.all_node)))
        if self.handlerNode.node_choose is None:
            self.dev.label_long_3.set_text('Node choose: None')
            self.dev.label_long_4.set_text('Level choose: None')
            self.dev.label_short_3.set_text('Mouse rel: ' + str(self.mouse_rel))
            self.dev.label_long_7.set_text('h-block: ' + 'None')
            self.dev.label_long_8.set_text('h-cost: ' + 'None')
            self.dev.label_long_9.set_text('g-cost: ' + 'None')
            self.dev.label_long_10.set_text('% right: ' + 'None')
        else:
            self.dev.label_long_3.set_text('Node choose: ' + str(self.handlerNode.node_choose.puzzle))
            self.dev.label_long_4.set_text('Level choose: ' + str(self.handlerNode.node_choose.level))
            self.dev.label_short_3.set_text('Mouse rel: ' + str(self.handlerNode.node_choose.mouse_rel))
            self.dev.label_long_7.set_text('h-block: ' + str(self.handlerNode.node_choose.h_cost_block))
            self.dev.label_long_8.set_text('h-cost: ' + str(self.handlerNode.node_choose.h_cost))
            self.dev.label_long_9.set_text('g-cost: ' + str(self.handlerNode.node_choose.g_cost))
            self.dev.label_long_10.set_text('% right: ' + str(self.handlerNode.node_choose.percent_right) + ", % false: " + str(self.handlerNode.node_choose.percent_false))
        self.dev.label_long_5.set_text('Max level: ' + str(self.handlerNode.max_level))
        self.dev.label_long_6.set_text('Node-level-arr-count: ' + str(len(self.handlerNode.all_node_level)))


