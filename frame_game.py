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
    import numpy as np
except:
    os.system('pip install numpy')
    import numpy as np
    
import datetime
import settings
import time
import node
import handler_node
import dev_support
import getpass
import pathlib

pygame.init()
class Frame:
    def __init__(self, _frame_handler, _screen):
        self.ui_manager = pygame_gui.UIManager((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), 'theme.json')
        self.frame_handler = _frame_handler
        self.screen = _screen
        self.init()
        self.ui_elements()

    def init(self):
        self.step = 0
        self.is_play = False
        self.is_solve = False
        self.is_show_dev = False
        self.final_image = None
        self.current_image_path = None
        self.ratio = (3,4,5)
        self.current_ratio = self.ratio[0]

        self.run = True

        self.handlerNode = handler_node.HandlerNode(self.screen, self, self.current_ratio, 1000)
        self.dev = dev_support.DEV(self)
        self.final_image_puzzle = node.Node(self.screen, self.handlerNode.goal_puzzle[self.current_ratio-3], 0, 400, int(self.current_ratio), (settings.SCREEN_WIDTH-245, 190), self.handlerNode)
        self.handlerNode.append_node(self.final_image_puzzle)

    def ui_elements(self):
        #Button
        rect_Solve = pygame.Rect((100, 450), (150, 60))
        self.button_Solve = pygame_gui.elements.UIButton(relative_rect = rect_Solve,
                                                        text = "Solve",
                                                        manager = self.ui_manager)
        rect_Shuffle = pygame.Rect((600, 20), (100, 60))
        self.button_Shuffle = pygame_gui.elements.UIButton(relative_rect = rect_Shuffle,
                                                        text = "Shuffle",
                                                        manager = self.ui_manager)
        rect_Back = pygame.Rect((30, 650), (100, 50))
        self.button_Back = pygame_gui.elements.UIButton(relative_rect = rect_Back,
                                                        text = "Back",
                                                        manager = self.ui_manager,
                                                        object_id = "#button_back" ) 
        rect_Play = pygame.Rect((575, 500), (150, 70))
        self.button_Play = pygame_gui.elements.UIButton(relative_rect = rect_Play,
                                                        text = "Play",
                                                        manager = self.ui_manager,
                                                        object_id = "#button_play" ) 
        rect_add_picture = pygame.Rect((255, 100), (60, 60))
        self.button_add_picture = pygame_gui.elements.UIButton(relative_rect = rect_add_picture,
                                                        text = "+",
                                                        manager = self.ui_manager)

        # Panel
        rect_Pane1 = pygame.Rect((30,80), (300, 450))
        self.panel_1 = pygame_gui.elements.ui_panel.UIPanel(relative_rect = rect_Pane1,
                                                            starting_layer_height=0,
                                                            manager= self.ui_manager)
       
        # Label
        rect_guide = pygame.Rect((20, 0), (300, 50))
        self.label_guide = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = 'F2 - Open/Close Development',
                                                            relative_rect = rect_guide,
                                                            object_id = "#label_dev_1")

        self.label_up = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "Press ↑ to UP",
                                                            relative_rect = pygame.Rect((65,220), (200, 180)),
                                                            object_id = "#label_guide")
        self.label_down = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "Press ↓ to DOWN",
                                                            relative_rect = pygame.Rect((75,250), (200, 180)),
                                                            object_id = "#label_guide")
        self.label_right = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "Press → to RIGHT",
                                                            relative_rect = pygame.Rect((80,280), (200, 180)),
                                                            object_id = "#label_guide")
        self.label_left = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "Press ← to LEFT",
                                                            relative_rect = pygame.Rect((75,310), (200, 180)),
                                                            object_id = "#label_guide")
        self.label_time = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "00:00:00",
                                                            relative_rect = pygame.Rect((1000,270), (200, 180)),
                                                            object_id = "#label_time")
        self.label_step = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "Step: " + str(self.step),
                                                            relative_rect = pygame.Rect((1000,300), (200, 180)),
                                                            object_id = "#label_time")
        self.label_percent = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = str(round(self.handlerNode.root.percent_right))+' %',
                                                            relative_rect = pygame.Rect((1000,350), (200, 180)),
                                                            visible = False,
                                                            object_id = "#label_percent")

        # Picture
        self.picture_box1 = None

        # Drop down
        rect_choose_picture = pygame.Rect((100, 100), (150, 60))
        self.picture_options = ['Only Number', 'Picture 1', 'Picture 2']
        self.dropdown_choose_picture = pygame_gui.elements.UIDropDownMenu(options_list = self.picture_options,
                                                                    starting_option = self.picture_options[0],
                                                                    relative_rect = rect_choose_picture,
                                                                    manager = self.ui_manager)
        rect_choose_level = pygame.Rect((100, 180), (150, 60))
        self.level_options = ['Easy', 'Easy', 'Easy', 'Legend']
        self.dropdown_choose_level = pygame_gui.elements.UIDropDownMenu(options_list = self.level_options,
                                                                    starting_option = self.level_options[0],
                                                                    relative_rect = rect_choose_level,
                                                                    manager = self.ui_manager)
                                                                    
    def render(self, _display_surface):
        self.handlerNode.draw_root()
        self.ui_manager.draw_ui(_display_surface)
        if self.is_show_dev:
            self.dev.draw(_display_surface)

    def update(self, _delta_time):
        if self.current_ratio > 3:
            self.button_Solve.disable()
        else:
            self.button_Solve.enable()

        if self.is_solve:
            self.dropdown_choose_level.disable()
            self.dropdown_choose_picture.disable()
            self.button_Shuffle.visible = False
            self.button_Play.visible = False
            self.button_Solve.visible = False
        else:
            self.dropdown_choose_level.enable()
            self.dropdown_choose_picture.enable()
            self.button_Shuffle.visible = True
            if not self.is_play:
                self.button_Play.visible = True
            self.button_Solve.visible = True

            ''' Training Section
            self.handlerNode.shuffle_puzzle(self.handlerNode.root)
            f = open("data.txt", "a")
            self.is_solve = True
            self.handlerNode.set_algorithm('Hill Climb')
            f.write(str(self.handlerNode.root.puzzle))
            if self.handlerNode.find_solution() == True:
                f.write(', Visited Node: ' + str(self.handlerNode.node_count))
                f.write(', Total Step: ' + str(len(self.handlerNode.solution_path)))
                f.write(', Solution Path: ' + str(self.handlerNode.solution_path))
            else:
                f.write(' No Solution')
            f.write('\n')
            f.close()
            self.is_solve = False
            '''

        if self.is_play and self.is_solve == False:
            counter_time = int(round(datetime.datetime.now().timestamp())) - int(round(self.start_time.timestamp()))
            self.label_time.set_text(str(time.strftime('%H:%M:%S', time.gmtime(counter_time))))
            self.label_step.set_text('Step: '+str(self.step))
            self.label_percent.set_text(str(round(self.handlerNode.root.percent_right))+' %')
            if self.handlerNode.root.is_same_puzzle(self.handlerNode.goal_puzzle[self.current_ratio-3]):
                self.is_play = False
                # Dialog message
                if self.run is True:
                    return
                dialog_msg = '<b>You Win<br>Total time: '+str(self.label_time.text)+'</b><br>'
                rect_win = pygame.Rect((settings.SCREEN_WIDTH/2 - (300/2), settings.SCREEN_HEIGHT/2 - (150/2)), (300, 150))
                self.dialog_win_2 = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = rect_win,
                                                                                        action_long_desc = dialog_msg,
                                                                                        window_title ='Congratulations',
                                                                                        manager = self.ui_manager)
        self.get_input()
        self.handlerNode.update_root()
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
            if _event.key == pygame.K_UP or pygame.K_RIGHT or pygame.K_DOWN or pygame.K_LEFT:
                self.step += 1

        if _event.type == pygame_gui.UI_BUTTON_PRESSED:
            if _event.ui_element == self.button_Back:
                self.run = False
                self.handlerNode.set_run(False)
                self.frame_handler.set_current_frame('frame_menu')
            if _event.ui_element == self.button_Shuffle and not self.is_play:
                self.handlerNode.shuffle_puzzle(self.handlerNode.root)
            if _event.ui_element == self.button_Play and not self.is_play:
                self.is_play = True
                self.is_solve = False
                self.button_Play.visible = False
                self.button_Shuffle.visible = False
                self.dropdown_choose_picture.disable()
                self.dropdown_choose_level.disable()
                self.button_add_picture.disable()
                self.label_percent.visible = True
                self.start_time = datetime.datetime.now()
            if _event.ui_element == self.button_add_picture and not self.is_play:
                rect_dialog = pygame.Rect((settings.SCREEN_WIDTH/2 - (600/2), settings.SCREEN_HEIGHT/2 - (250/2)), (600, 250))
                init_path = 'C:/Users/{}/Downloads'
                self.file_dialog = pygame_gui.windows.ui_file_dialog.UIFileDialog(rect = rect_dialog,
                                                                                window_title = 'Choose you Picture',
                                                                                initial_file_path = init_path.format(getpass.getuser()),
                                                                                manager = self.ui_manager)

            if _event.ui_element == self.button_Solve:
                if self.level_options[self.current_ratio-3] == 'Hard' or self.level_options[self.current_ratio-3] == 'Medium':
                    # Dialog message
                    dialog_msg = 'No Support!, hihi'
                    rect_win = pygame.Rect((settings.SCREEN_WIDTH/2 - (300/2), settings.SCREEN_HEIGHT/2 - (150/2)), (300, 150))
                    self.dialog_win_4 = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = rect_win,
                                                                                            action_long_desc = dialog_msg,
                                                                                            window_title ='Solution info',
                                                                                            manager = self.ui_manager)
                    return
                f = open("data.txt", "a")
                self.is_solve = True
                self.handlerNode.set_algorithm('A* (Manhattan)')
                f.write(str(self.handlerNode.root.puzzle))
                start_time = datetime.datetime.now()
                if self.handlerNode.find_solution() == True and self.run:
                    end_time = datetime.datetime.now()
                    execute_time = int(round(end_time.timestamp())) - int(round(start_time.timestamp()))
                    f.write(' Visited Node: ' + str(self.handlerNode.node_count))
                    f.write(' Total Step: ' + str(len(self.handlerNode.solution_path)))
                    # Dialog message
                    dialog_msg = '<b>Final<br><br>Total time: '+str(time.strftime('%M:%S', time.gmtime(execute_time)))+' seconds'+'<br>Visited Node :'+str(self.handlerNode.node_count)+'<br>Steps: '+str(len(self.handlerNode.solution_path))+'</b><br>'
                    rect_win = pygame.Rect((settings.SCREEN_WIDTH/2 - (300/2), settings.SCREEN_HEIGHT/2 - (150/2)), (300, 300))
                    self.dialog_win = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = rect_win,
                                                                                            action_long_desc = dialog_msg,
                                                                                            window_title ='Solution info',
                                                                                            manager = self.ui_manager)
                else:
                    f.write(' No Solution')
                    # Dialog message
                    dialog_msg = 'No Solution'
                    rect_win = pygame.Rect((settings.SCREEN_WIDTH/2 - (300/2), settings.SCREEN_HEIGHT/2 - (150/2)), (300, 300))
                    self.dialog_win = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = rect_win,
                                                                                            action_long_desc = dialog_msg,
                                                                                            window_title ='Solution info',
                                                                                            manager = self.ui_manager)
                f.write('\n')
                f.close()
                self.is_solve = False


        if _event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED and not self.is_play:
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

        if _event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
            self.reset()
        
        if _event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
            if _event.ui_element == self.file_dialog:
                self.current_image_path = _event.text
                ext = pathlib.Path(_event.text).suffix
                if ext == '.png' or ext == '.jpg':
                    img = pygame.image.load(_event.text)
                    if img.get_width() == img.get_height():
                        self.set_final_image(self.current_image_path)
                    else:
                        print('Please pick image square size!')
                else:
                    print('Please pick Image!')
                    return

        self.ui_manager.process_events(_event)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if not self.is_play:
            return
        if keys[pygame.K_RIGHT]:
            self.handlerNode.root.move_right()
        if keys[pygame.K_UP]:
            self.handlerNode.root.move_up()
        if keys[pygame.K_DOWN]:
            self.handlerNode.root.move_down()
        if keys[pygame.K_LEFT]:
            self.handlerNode.root.move_left()

    def reset(self):
        self.handlerNode.shuffle_puzzle(self.handlerNode.root)
        self.handlerNode.reset_handler()
        self.label_time.set_text('00:00:00')    
        self.step = 0
        self.label_step.set_text('Step: '+str(0))
        self.label_percent.visible = False
        self.button_Play.visible = True
        self.button_Shuffle.visible = True
        self.dropdown_choose_picture.enable()
        self.dropdown_choose_level.enable()
        self.button_add_picture.enable()
    
    def reset_ratio(self, _ratio):
        self.current_ratio = _ratio
        self.handlerNode.set_ratio(_ratio)
        numpy.random.shuffle(self.handlerNode.start_puzzle[self.current_ratio-3])
        self.handlerNode.root.set_puzzle_2(self.handlerNode.start_puzzle[self.current_ratio-3])
        self.final_image_puzzle.set_puzzle_2(self.handlerNode.goal_puzzle[self.current_ratio-3])
        self.final_image_puzzle.create_puzzle()
        if self.final_image != None:
            self.set_final_image(self.current_image_path)
        self.handlerNode.root.create_puzzle()
    
    def set_final_image(self, _path):
        if self.picture_box1 != None:
            self.picture_box1.kill()
        if _path == None:
            self.final_image = None
            self.handlerNode.set_image(None, self.current_ratio)
        else:
            self.final_image = pygame.image.load(_path)
            rect_picture = pygame.Rect((settings.SCREEN_WIDTH-260, 180), (150, 150))
            self.picture_box1 = pygame_gui.elements.UIImage(relative_rect = rect_picture, 
                                                            image_surface = self.final_image,
                                                            manager = self.ui_manager)
            self.handlerNode.set_image(_path, self.current_ratio)

    def development(self):
        self.dev.label_short_1.set_text('Mode: '+self.level_options[self.current_ratio-3])
        self.dev.label_short_2.set_text('Node area: '+str(round(self.handlerNode.root.size)))
        self.dev.label_short_3.set_text('Puzzle size: '+str(round(self.handlerNode.root.blocks[0].size)))
        self.dev.label_short_4.set_text('Percent Complete: '+str(round(self.handlerNode.root.percent_right)))
        self.dev.label_long_1.set_text('Frame: '+str(self.handlerNode.frame.__module__))
        self.dev.label_long_2.set_text('Node count: ' + str(len(self.handlerNode.all_node)))
        self.dev.label_long_3.set_text('Level max: ' + str(self.handlerNode.max_level))
        self.dev.label_long_4.set_text('Node count 2: ' + str(self.handlerNode.node_count))
        if self.handlerNode.solution_path != None:
            self.dev.label_long_5.set_text('Solution length: ' + str(len(self.handlerNode.solution_path)))
        else:
            self.dev.label_long_5.set_text('Solution length: ' + 'None')
# Final Build
