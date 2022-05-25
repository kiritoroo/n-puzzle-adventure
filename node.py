import pygame
import sys, time
import numpy
import settings
import colors
import image_service
import block

pygame.init()
clock = pygame.time.Clock()
class Node:
    def __init__(self, _screen, _puzzle, _level, _size, _ratio, _pos, _handler):
        self.screen = _screen
        self.puzzle = _puzzle
        self.level = _level
        self.size = _size
        self.ratio = int(_ratio)
        self.pos = pygame.math.Vector2(_pos)
        self.handler = _handler
        self.images = None
        self.path = None
        self.zoom = 1
        self.init()

    def init(self):
        self.is_minimum = False
        self.is_move = False
        self.is_choose = False

        self.is_move_up = False
        self.is_move_right = False
        self.is_move_down = False
        self.is_move_left = False

        self.is_info1_open = False
        self.is_info2_open = False 

        self.is_draw_link_to_child = True
        self.is_draw_link_to_parent = True

        self.mouse_rel = (0,0)
        self.total_width_child = 0

        self.blocks = []
        self.children = []
        self.parent = None

        self.percent_right = round(self.check_percent_right())
        self.percent_false = 100 - self.percent_right
        self.h_cost_block = []
        self.h_cost = 0
        self.g_cost = 0
        self.f_cost = 0

        self.default_size = self.size
        self.line_color = colors.RED_LIGHT

        self.surf = pygame.Surface((self.size/self.ratio + 10, self.size/self.ratio + 10))
        self.surf.fill(colors.GRAY_LIGHT)
        self.rect = self.surf.get_rect(topleft = (self.pos.x - 5, self.pos.y - 5))
        self.create_puzzle()
        self.interactive_init()

    def draw(self):
        # if self.is_minimum:
        #     self.surf = pygame.Surface(((self.size/self.ratio + 10)/2, (self.size/self.ratio + 10)/2))
        #     self.rect = self.surf.get_rect(topleft = (self.pos.x - 5, self.pos.y - 5))
        #     self.surf.fill(colors.BLUE_CLOUD)
        #     self.screen.blit(self.surf, self.rect)
        #     # Draw link to children
        #     for i in range(len(self.children)):
        #         pygame.draw.line(self.screen,
        #                         colors.RED_LIGHT,
        #                         (self.pos[0] + self.size/6,self.pos[1] + self.size/6),
        #                         (self.children[i].pos[0] + self.children[i].size/6, self.children[i].pos[1] + self.children[i].size/6),
        #                         3)  

        #     # Draw link to parent
        #     if self.parent != None:
        #         if self.line_color == colors.GREEN_LIME:
        #             pygame.draw.line(self.screen,
        #                             self.line_color,
        #                             (self.pos[0] + self.size/6,self.pos[1] + self.size/6),
        #                             (self.parent.pos[0] + self.parent.size/6, self.parent.pos[1] + self.parent.size/6),
        #                             3)  
        #     return

        self.surf = pygame.Surface((self.size/self.ratio + 10, self.size/self.ratio + 10))
        ### Draw background
        if self.is_choose:
            self.surf.fill(colors.GREEN_LIME)
        else:
            self.surf.fill(colors.GRAY_LIGHT)
        self.screen.blit(self.surf, self.rect)

        ### Draw block
        for i in range(numpy.power(self.ratio, 2)):
            self.blocks[i].draw()
        
        ### Draw caro line
        for i in range(1, self.ratio):
            # Vertical
            pygame.draw.line(self.screen,
                            colors.GRAY_LIGHT,
                            (i*self.size/numpy.power(self.ratio, 2) + self.pos.x, self.pos.y),
                            (i*self.size/numpy.power(self.ratio, 2) + self.pos.x, self.pos.y + self.size/self.ratio - 2))
            # Horizontal
            pygame.draw.line(self.screen,
                            colors.GRAY_LIGHT,
                            (self.pos.x, i*self.size/numpy.power(self.ratio, 2) + self.pos.y),
                            (self.pos.x + self.size/self.ratio - 2, i*self.size/numpy.power(self.ratio, 2) + self.pos.y))
        if self.is_draw_link_to_child:
            # Draw link to children
            for i in range(len(self.children)):
                pygame.draw.line(self.screen,
                                colors.RED_LIGHT,
                                (self.pos[0] + self.size/6,self.pos[1] + self.size/6),
                                (self.children[i].pos[0] + self.children[i].size/6, self.children[i].pos[1] + self.children[i].size/6),
                                3)  

        if self.is_draw_link_to_parent:
            # Draw link to parent
            if self.parent != None:
                if self.line_color == colors.GREEN_LIME:
                    pygame.draw.line(self.screen,
                                    self.line_color,
                                    (self.pos[0] + self.size/6,self.pos[1] + self.size/6),
                                    (self.parent.pos[0] + self.parent.size/6, self.parent.pos[1] + self.parent.size/6),
                                    3)  
        self.interactive_draw()

    def update(self):
        self.move_node()
        self.interactive_update()

    def set_minimum(self, _value):
        self.is_minimum = _value

    def set_cost(self, _cost):
        self.h_cost_block, self.h_cost = _cost
        self.g_cost = self.level
        self.f_cost = self.h_cost + self.g_cost

    def set_size(self, _size):
        self.size = _size
        self.create_puzzle()

    def set_zoom(self, _zoom):
        self.zoom = _zoom
        self.create_puzzle()
        self.reset_pos_children()

    def set_image(self, _path, _ratio):
        self.images = image_service.split_image(_path, _ratio)
        self.path = _path
        self.create_puzzle()
        self.interactive_init()

    def set_color(self, _color):
        for i in range(len(self.blocks)):
            self.blocks[i].set_color(_color)

    def set_line_color(self, _color):
        self.line_color = _color

    def set_parent(self, _parent):
        self.parent = _parent

    def set_children(self, _children):
        self.children = _children

    def set_default_size(self, _size):
        self.default_size = _size
    
    def set_pos(self, _pos):
        self.pos = pygame.math.Vector2(_pos)
        self.create_puzzle()
        self.interactive_init()

    def set_puzzle(self, _puzzle):
        self.puzzle = _puzzle
        self.create_puzzle()
    
    def set_puzzle_2(self, _puzzle):
        self.puzzle = _puzzle
    
    def set_is_choose(self, _value):
        self.is_choose = _value

    def set_ratio(self, _ratio):
        self.ratio = _ratio

    def set_draw_to_child(self, _value):
        self.is_draw_link_to_child = _value
    
    def set_draw_to_parent(self, _value):
        self.is_draw_link_to_parent = _value

    # HARDCODE
    def check_collider_mouse(self, _key):
        if self.handler.frame.__module__ == 'frame_game':
            return

        mouse_pos = pygame.mouse.get_pos()
        if _key == 1:
            if self.rect.collidepoint(mouse_pos):
                if self.is_choose == False:
                    self.is_choose = True
                    return True
                elif self.is_choose == True:
                    return True

        elif _key == 2:
            if self.rect.collidepoint(mouse_pos):
                if self.is_move == True:
                    self.is_move = False
                    self.is_choose = True
                    return True
                elif self.is_move == False:
                    self.is_move = True
                    self.is_choose = True
                    return True
        elif _key == 3:
            self.is_move = False
            self.is_choose = False
            return False

        if self.info_button_rect.collidepoint(mouse_pos):
            if self.is_info1_open:
                self.is_info1_open = False
            else:
                self.is_info1_open = True
        if self.info2_button_rect.collidepoint(mouse_pos):
            if self.is_info2_open:
                self.is_info2_open = False
            else:
                self.is_info2_open = True

    def move_node(self):
        if self.is_choose and self.is_move:
            self.mouse_rel = pygame.mouse.get_rel()
            mouse_pos = pygame.mouse.get_pos()
            offset_x = self.surf.get_width()/2
            offset_y = self.surf.get_height()/2
            self.pos = pygame.math.Vector2(mouse_pos[0]-offset_x, mouse_pos[1]-offset_y)
            self.create_puzzle()
            self.interactive_init()
            for i in range(len(self.children)):
                self.move_all_child(self.children[i], pygame.math.Vector2(self.mouse_rel))

    def move_all_child(self, _node, _offset):
        new_pos = (_node.pos[0] + _offset[0],
                   _node.pos[1] + _offset[1])
        _node.set_pos(new_pos)
        for i in range(len(_node.children)):
            self.move_all_child(_node.children[i], _offset)
     
    def reset_pos_children(self):
        offset = 30 * self.zoom
        total_width = 0
        for i in range(len(self.children)):
            total_width += self.children[i].surf.get_width() + offset
        start_pos_x = round(self.pos[0] - total_width/2 + self.surf.get_width()/2 + 5)
        start_pos_y = self.pos.y + self.surf.get_width() + 40 * self.zoom
        for i in range(len(self.children)):
            self.children[i].set_pos((start_pos_x, start_pos_y))
            start_pos_x += round(self.children[i].surf.get_width() + offset)
    # End HARDCORE

    # INTERACTIVE
    def interactive_init(self):
        if self.is_minimum:
            return
        if self.handler.frame.__module__ == 'frame_game':
            return
        if self.handler.frame.__module__ == 'frame_compare':
            return

        # Button
        self.info_button_surf = pygame.Surface(((self.size/self.ratio + 10)/8, (self.size/self.ratio + 10)/8))
        self.info_button_rect = self.info_button_surf.get_rect(topleft = (self.pos.x + self.surf.get_width() + 2, self.pos.y + 10))
        self.info_button_surf.fill(colors.GREEN_LIGHT)
        self.info_button_surf.set_alpha(150)
        self.text1_pos = (self.info_button_rect.left + self.info_button_surf.get_width() / 2,
                        self.info_button_rect.top + self.info_button_surf.get_height() / 2)
        self.text1_surf = settings.font.render('+', True, colors.GREEN_DARK)
        self.text1_rect = self.text1_surf.get_rect(center = self.text1_pos)

        self.info2_button_surf = pygame.Surface(((self.size/self.ratio + 10)/8, (self.size/self.ratio + 10)/8))
        self.info2_button_rect = self.info2_button_surf.get_rect(topleft = (self.pos.x + self.surf.get_width() + 2, 
                                                            self.pos.y + self.info_button_surf.get_height() + 15))
        self.info2_button_surf.fill(colors.GREEN_LIGHT)
        self.info2_button_surf.set_alpha(150)
        self.text2_pos = (self.info2_button_rect.left + self.info2_button_surf.get_width() / 2,
                        self.info2_button_rect.top + self.info2_button_surf.get_height() / 2)
        self.text2_surf = settings.font.render('-', True, colors.GREEN_DARK)
        self.text2_rect = self.text1_surf.get_rect(center = self.text2_pos)

        # Panel
        self.panel_surf = pygame.Surface((self.size/4, self.size/4))
        self.panel_pos = pygame.math.Vector2(self.rect.left + self.surf.get_width() / 2,
                                        self.rect.top + self.surf.get_height() / 2)
        self.panel_surf.set_alpha(150)
        self.panel_surf.fill(colors.GREEN_LIGHT)
        self.panel_rect = self.panel_surf.get_rect(center = self.panel_pos)

    def interactive_draw(self):
        if self.handler.frame.__module__ == 'frame_game':
            return
        if self.handler.frame.__module__ == 'frame_compare':
            return
        if self.is_minimum:
            return

        self.screen.blit(self.info_button_surf, self.info_button_rect)
        self.screen.blit(self.text1_surf, self.text1_rect)
        self.screen.blit(self.info2_button_surf, self.info2_button_rect)
        self.screen.blit(self.text2_surf, self.text2_rect)

        if self.is_info1_open:
            self.screen.blit(self.panel_surf, self.panel_rect)

    def interactive_update(self):
        if self.handler.frame.__module__ == 'frame_game':
            return
        if self.handler.frame.__module__ == 'frame_compare':
            return
        if self.is_minimum:
            return
        pass

    # End INTERACTOVE

    def create_puzzle(self):
        if self.is_minimum:
            return

        self.blocks = []

        if self.ratio == 3:
            self.size = self.default_size
        elif self.ratio == 4:
            self.size = self.default_size + self.default_size/100*33
        elif self.ratio == 5:
            self.size = self.default_size + self.default_size/100*66

        self.size = self.size * self.zoom

        if self.parent != None:
            offset_y = self.parent.surf.get_height() + 20
            offset_x = self.pos.x - self.parent.pos.x
            self.pos = pygame.math.Vector2(self.parent.pos.x + offset_x, self.parent.pos.y + offset_y)
        self.surf = pygame.Surface((self.size/self.ratio + 10, self.size/self.ratio + 10))
        self.rect = self.surf.get_rect(topleft = (self.pos.x - 5, self.pos.y - 5))

        for i in range(numpy.power(self.ratio, 2)):
            if self.images != None:
                self.blocks.append(block.Block(self.screen,
                                            self.size/numpy.power(self.ratio, 2),
                                            (i%self.ratio*self.size/numpy.power(self.ratio, 2) + self.pos.x,
                                             i//self.ratio*self.size/numpy.power(self.ratio, 2) + self.pos.y),
                                            self.puzzle[i],
                                            colors.BLUE_CLOUD,
                                            self.images[self.puzzle[i]]))
            else:
                self.blocks.append(block.Block(self.screen,
                                            self.size/numpy.power(self.ratio, 2),
                                            (i%self.ratio*self.size/numpy.power(self.ratio, 2) + self.pos.x,
                                             i//self.ratio*self.size/numpy.power(self.ratio, 2) + self.pos.y),
                                            self.puzzle[i],
                                            colors.BLUE_CLOUD,
                                            None))
            if self.puzzle[i] == 0:
                self.block_null_index = i
        self.percent_right = round(self.check_percent_right())
        self.percent_false = 100 - (self.percent_right)
        self.interactive_init()
    
    def copy_puzzle(self, a, b):
        for i in range(len(b)):
            a[i] = b[i]
    
    def is_child_contain(self, _child_node):
        for i in range(len(self.children)):
            if numpy.array_equal(self.children[i].puzzle, _child_node.puzzle):
                return True
        return False

    def is_same_puzzle(self, _p):
        for i in range(len(self.puzzle)):
            if self.puzzle[i] != _p[i]:
                return False
        return True

    def check_percent_right(self):
        count = 0
        for i in range(len(self.puzzle)):
            if self.puzzle[i] == self.handler.goal_puzzle[self.ratio-3][i]:
                if self.puzzle[i] == 0:
                    continue
                else:
                    count += 1
        percent = (count*100)/ (numpy.power(self.ratio, 2)-1)
        return percent

    def child_up(self):
        n = self.block_null_index
        if n - self.ratio >= 0:
            child_puzzle = numpy.zeros(numpy.power(self.ratio, 2), dtype = int)
            self.copy_puzzle(child_puzzle, self.puzzle)
            temp = child_puzzle[n-self.ratio]
            child_puzzle[n-self.ratio] = child_puzzle[n]
            child_puzzle[n] = temp
            child_node = Node(self.screen, 
                        child_puzzle,
                        self.level+1,
                        self.size,
                        self.ratio,
                        (self.pos[0], self.pos[1]+self.surf.get_height()+40*self.zoom),
                        self.handler)
            child_node.set_default_size(self.default_size)
            if self.is_child_contain(child_node):
                return
            child_node.set_image(self.path, self.ratio)
            self.children.append(child_node)
            child_node.set_parent(self)
            child_node.set_zoom(self.handler.zoom_rate)
            self.reset_pos_children()
            self.handler.node_count +=1


    def child_right(self):
        n = self.block_null_index
        if n%self.ratio < self.ratio-1:
            child_puzzle = numpy.zeros(numpy.power(self.ratio, 2), dtype = int)
            self.copy_puzzle(child_puzzle, self.puzzle)
            temp = child_puzzle[n+1]
            child_puzzle[n+1] = child_puzzle[n]
            child_puzzle[n] = temp
            child_node = Node(self.screen, 
                        child_puzzle,
                        self.level+1,
                        self.size,
                        self.ratio,
                        (self.pos[0], self.pos[1]+self.surf.get_height()+40*self.zoom),
                        self.handler)
            child_node.set_default_size(self.default_size)
            if self.is_child_contain(child_node):
                return
            child_node.set_image(self.path, self.ratio)
            self.children.append(child_node)
            child_node.set_parent(self)
            child_node.set_zoom(self.handler.zoom_rate)
            self.reset_pos_children()
            self.handler.node_count +=1

    def child_down(self):
        n = self.block_null_index
        if n + self.ratio < numpy.power(self.ratio, 2):
            child_puzzle = numpy.zeros(numpy.power(self.ratio, 2), dtype = int)
            self.copy_puzzle(child_puzzle, self.puzzle)
            temp = child_puzzle[n+self.ratio]
            child_puzzle[n+self.ratio] = child_puzzle[n]
            child_puzzle[n] = temp
            child_node = Node(self.screen, 
                        child_puzzle,
                        self.level+1,
                        self.size,
                        self.ratio,
                        (self.pos[0], self.pos[1]+self.surf.get_height()+40*self.zoom),
                        self.handler)
            child_node.set_default_size(self.default_size)
            if self.is_child_contain(child_node):
                return
            child_node.set_image(self.path, self.ratio)
            self.children.append(child_node)
            child_node.set_parent(self)
            child_node.set_zoom(self.handler.zoom_rate)
            self.reset_pos_children()
            self.handler.node_count +=1

    def child_left(self):
        n = self.block_null_index
        if n%self.ratio > 0:
            child_puzzle = numpy.zeros(numpy.power(self.ratio, 2), dtype = int)
            self.copy_puzzle(child_puzzle, self.puzzle)
            temp = child_puzzle[n-1]
            child_puzzle[n-1] = child_puzzle[n]
            child_puzzle[n] = temp
            child_node = Node(self.screen, 
                        child_puzzle,
                        self.level+1,
                        self.size,
                        self.ratio,
                        (self.pos[0], self.pos[1]+self.surf.get_height()+40*self.zoom),
                        self.handler)
            child_node.set_default_size(self.default_size)
            if self.is_child_contain(child_node):
                return
            child_node.set_image(self.path, self.ratio)
            self.children.append(child_node)
            child_node.set_parent(self) 
            child_node.set_zoom(self.handler.zoom_rate)
            self.reset_pos_children()
            self.handler.node_count +=1

    def general_child(self):
        self.child_up()
        self.child_right()
        self.child_down()
        self.child_left()
    
    def move_up(self):
        # Animation
        if self.is_move_up or self.is_move_right or self.is_move_down or self.is_move_left:
            return

        n = self.block_null_index
        if n - self.ratio < 0:
            return

        self.is_move_up = True
        block_up = self.blocks[n-self.ratio]
        block_null = self.blocks[n]
        y_last_up = block_null.pos.y
        y_last_null = block_up.pos.y

        last_time = time.time()
        for i in range(15):
            dt = time.time() - last_time
            last_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handler.frame.ui_event(event)

            if block_up.pos.y < y_last_up:
                block_up.set_pos((block_up.pos.x, block_up.pos.y + i))
            if block_null.pos.y > y_last_null:
                block_null.set_pos((block_null.pos.x, block_null.pos.y - i))
            
            # Update & Draw
            self.screen.fill(colors.WHITE)
            self.draw()
            self.update()
            self.handler.frame.render(self.screen)
            self.handler.frame.update(dt)
            pygame.display.update()
            clock.tick(settings.FRAME_RATE_HALF)

        block_up.set_pos((block_up.pos.x, y_last_up))
        block_null.set_pos((block_null.pos.x, y_last_null))
        self.is_move_up = False
        
        # Logic
        next_puzzle = numpy.zeros(numpy.power(self.ratio, 2), dtype = int)
        self.copy_puzzle(next_puzzle, self.puzzle)
        temp = next_puzzle[n-self.ratio]
        next_puzzle[n-self.ratio] = next_puzzle[n]
        next_puzzle[n] = temp
        self.set_puzzle(next_puzzle)
        
    def move_right(self):
        # Animation
        if self.is_move_up or self.is_move_right or self.is_move_down or self.is_move_left:
            return

        n = self.block_null_index
        if n%self.ratio >= self.ratio-1:
            return

        self.is_move_right = True
        block_right = self.blocks[n+1]
        block_null = self.blocks[n]
        x_last_right = block_null.pos.x
        x_last_null = block_right.pos.x

        last_time = time.time()
        for i in range(15):
            dt = time.time() - last_time
            last_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handler.frame.ui_event(event)

            if block_right.pos.x > x_last_right:
                block_right.set_pos((block_right.pos.x - i, block_right.pos.y))
            if block_null.pos.x < x_last_null:
                block_null.set_pos((block_null.pos.x + i, block_null.pos.y))
            
            # Update & Draw
            self.screen.fill(colors.WHITE)
            self.draw()
            self.update()
            self.handler.frame.render(self.screen)
            self.handler.frame.update(dt)
            pygame.display.update()
            clock.tick(settings.FRAME_RATE_HALF)

        block_right.set_pos((x_last_right, block_right.pos.y))
        block_null.set_pos((x_last_null, block_null.pos.y))
        self.is_move_right = False
        
        # Logic
        next_puzzle = numpy.zeros(numpy.power(self.ratio, 2), dtype = int)
        self.copy_puzzle(next_puzzle, self.puzzle)
        temp = next_puzzle[n+1]
        next_puzzle[n+1] = next_puzzle[n]
        next_puzzle[n] = temp
        self.set_puzzle(next_puzzle)

    def move_down(self):
        # Animation
        if self.is_move_up or self.is_move_right or self.is_move_down or self.is_move_left:
            return
    
        n = self.block_null_index
        if n + self.ratio >= numpy.power(self.ratio, 2):
            return

        self.is_move_down = True
        block_down = self.blocks[n+self.ratio]
        block_null = self.blocks[n]
        y_last_down = block_null.pos.y
        y_last_null = block_down.pos.y

        last_time = time.time()
        for i in range(15):
            dt = time.time() - last_time
            last_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handler.frame.ui_event(event)
            
            if block_down.pos.y > y_last_down:
                block_down.set_pos((block_down.pos.x, block_down.pos.y - i))
            if block_null.pos.y < y_last_null:
                block_null.set_pos((block_null.pos.x, block_null.pos.y + i))
            
            # Update & Draw
            self.screen.fill(colors.WHITE)
            self.draw()
            self.update()
            self.handler.frame.render(self.screen)
            self.handler.frame.update(dt)
            pygame.display.update()
            clock.tick(settings.FRAME_RATE_HALF)
        
        block_down.set_pos((block_down.pos.x, y_last_down))
        block_null.set_pos((block_null.pos.x, y_last_null))
        self.is_move_down = False

        # Logic
        next_puzzle = numpy.zeros(numpy.power(self.ratio, 2), dtype = int)
        self.copy_puzzle(next_puzzle, self.puzzle)
        temp = next_puzzle[n+self.ratio]
        next_puzzle[n+self.ratio] = next_puzzle[n]
        next_puzzle[n] = temp
        self.set_puzzle(next_puzzle)

    def move_left(self):
        # Animation
        if self.is_move_up or self.is_move_right or self.is_move_down or self.is_move_left:
            return
        
        n = self.block_null_index
        if n%self.ratio <= 0:
            return

        self.is_move_left = True
        block_left = self.blocks[n-1]
        block_null = self.blocks[n]
        x_last_left = block_null.pos.x
        x_last_null = block_left.pos.x

        last_time = time.time()
        for i in range(15):
            dt = time.time() - last_time
            last_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handler.frame.ui_event(event)
            
            if block_left.pos.x < x_last_left:
                block_left.set_pos((block_left.pos.x + i, block_left.pos.y))
            if block_null.pos.x > x_last_null:
                block_null.set_pos((block_null.pos.x - i, block_null.pos.y))
            
            # Update & Draw
            self.screen.fill(colors.WHITE)
            self.draw()
            self.update()
            self.handler.frame.render(self.screen)
            self.handler.frame.update(dt)
            pygame.display.update()
            clock.tick(settings.FRAME_RATE_HALF)

        block_left.set_pos((x_last_left, block_left.pos.y))
        block_null.set_pos((x_last_null, block_null.pos.y))
        self.is_move_left = False

        # Logic 
        next_puzzle = numpy.zeros(numpy.power(self.ratio, 2), dtype = int)
        self.copy_puzzle(next_puzzle, self.puzzle)
        temp = next_puzzle[n-1]
        next_puzzle[n-1] = next_puzzle[n]
        next_puzzle[n] = temp
        self.set_puzzle(next_puzzle)