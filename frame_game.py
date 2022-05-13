import pygame
import pygame_gui
import datetime
import settings
import time
import node
import handler_node
import dev_support

pygame.init()
class Frame:
    def __init__(self, _frame_handler, _screen):
        self.ui_manager = pygame_gui.UIManager((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), 'theme.json')
        self.frame_handler = _frame_handler
        self.screen = _screen
        self.init()
        self.ui_elements()

    def init(self):
        self.is_play = False
        self.is_show_dev = False

        self.final_image = None
        self.handlerNode = handler_node.HandlerNode(self.screen, self)
        self.dev_tools = dev_support.DEV(self)

    def ui_elements(self):
        #Button
        rect_Solve = pygame.Rect((100, 200), (150, 60))
        self.button_Solve = pygame_gui.elements.UIButton(relative_rect = rect_Solve,
                                                        text = "Solve",
                                                        manager = self.ui_manager)
        rect_Shuffle = pygame.Rect((600, 20), (100, 60))
        self.button_Shuffle = pygame_gui.elements.UIButton(relative_rect = rect_Shuffle,
                                                        text = "Shuffle",
                                                        manager = self.ui_manager)
        rect_Back = pygame.Rect((30, 650), (80, 30))
        self.button_Back = pygame_gui.elements.UIButton(relative_rect = rect_Back,
                                                        text = "Back",
                                                        manager = self.ui_manager,
                                                        object_id = "#button_back" ) 
        rect_Play = pygame.Rect((580, 500), (150, 70))
        self.button_Play = pygame_gui.elements.UIButton(relative_rect = rect_Play,
                                                        text = "Play",
                                                        manager = self.ui_manager,
                                                        object_id = "#button_play" ) 
       
        #Panel
        rect_Pane1 = pygame.Rect((30,80), (300, 450))
        self.panel_1 = pygame_gui.elements.ui_panel.UIPanel(relative_rect = rect_Pane1,
                                                            starting_layer_height=0,
                                                            manager= self.ui_manager)
       
        #Label
        rect_guide = pygame.Rect((20, 0), (300, 50))
        self.label_guide = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = 'F2 - Close/Open Development Tools',
                                                            relative_rect = rect_guide,
                                                            object_id = "#label_dev_1")

        self.label_up = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "Press ↑ to UP",
                                                            relative_rect = pygame.Rect((80,270), (200, 180)),
                                                            object_id = "#label_guide")
        self.label_down = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "Press ↓ to DOWN",
                                                            relative_rect = pygame.Rect((90,300), (200, 180)),
                                                            object_id = "#label_guide")
        self.label_right = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "Press → to RIGHT",
                                                            relative_rect = pygame.Rect((95,330), (200, 180)),
                                                            object_id = "#label_guide")
        self.label_left = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "Press ← to LEFT",
                                                            relative_rect = pygame.Rect((90,360), (200, 180)),
                                                            object_id = "#label_guide")
        self.label_time = pygame_gui.elements.ui_label.UILabel(manager = self.ui_manager,
                                                            text = "00:00:00",
                                                            relative_rect = pygame.Rect((1000,270), (200, 180)),
                                                            object_id = "#label_time")
                                   
        #Picture
        self.picture_box1 = None

        #Drop down
        rect_choose_picture = pygame.Rect((100,100), (150, 60))
        picture_options = ['Only Number', 'Picture 1', 'Picture 2']
        self.dropdown_choose_picture = pygame_gui.elements.UIDropDownMenu(options_list = picture_options,
                                                                    starting_option = picture_options[0],
                                                                    relative_rect = rect_choose_picture,
                                                                    manager = self.ui_manager)
    def render(self, _display_surface):
        self.handlerNode.draw()
        self.ui_manager.draw_ui(_display_surface)
        if self.is_show_dev:
            self.dev_tools.draw(_display_surface)

    def update(self, _delta_time):
        if self.is_play:
            counter_time = int(round(datetime.datetime.now().timestamp())) - int(round(self.start_time.timestamp()))
            self.label_time.set_text(str(time.strftime('%H:%M:%S', time.gmtime(counter_time))))
        
        self.get_input()
        self.handlerNode.update()
        self.ui_manager.update(_delta_time)
        if self.is_show_dev:
            self.dev_tools.update(_delta_time)

    def ui_event(self, _event):
        if _event.type == pygame.KEYDOWN:
            if _event.key == pygame.K_F2:
                if self.is_show_dev:
                    self.is_show_dev = False
                else:
                    self.is_show_dev = True

        if _event.type == pygame_gui.UI_BUTTON_PRESSED:
            if _event.ui_element == self.button_Back:
                self.frame_handler.set_current_frame('frame_menu')
            if _event.ui_element == self.button_Shuffle and not self.is_play:
                self.handlerNode.shuffle_puzzle(self.handlerNode.root)
            if _event.ui_element == self.button_Play and not self.is_play:
                self.is_play = True
                self.button_Play.visible = False
                self.button_Shuffle.disable()
                self.dropdown_choose_picture.disable()
                self.start_time = datetime.datetime.now()

        if _event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED and not self.is_play:
            if _event.ui_element == self.dropdown_choose_picture:
                if _event.text == 'Only Number':
                    self.set_final_image(None)
                elif _event.text == 'Picture 1':
                    self.set_final_image('resources/img1.jpg')

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

    def set_final_image(self, _path):
        if _path == None:
            self.final_image = None
            if self.picture_box1 != None:
                self.picture_box1.kill()
            self.handlerNode.set_image(None)
        else:
            self.final_image = pygame.image.load(_path)
            rect_picture = pygame.Rect((settings.SCREEN_WIDTH-260, 180), (150, 150))
            self.picture_box1 = pygame_gui.elements.UIImage(relative_rect = rect_picture, 
                                                            image_surface = self.final_image,
                                                            manager = self.ui_manager)
            self.handlerNode.set_image(_path)


