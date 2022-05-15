from winreg import HKEY_CLASSES_ROOT
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
    def __init__(self, _screen, _puzzle, _level, _size, _pos, _handler):
        self.screen = _screen
        self.puzzle = _puzzle
        self.level = _level
        self.size = _size
        self.pos = pygame.math.Vector2(_pos)
        self.handler = _handler
        self.images = None
        self.init()

    def init(self):
        self.is_move = False
        self.is_choose = False

        self.is_move_up = False
        self.is_move_right = False
        self.is_move_down = False
        self.is_move_left = False

        self.blocks = []
        self.children = []
        self.parent = None

        self.h_cost_block = []
        self.h_cost = 0
        self.g_cost = 0
        self.f_cost = 0

        self.default_size = self.size

        self.surf = pygame.Surface((self.size/3 + 10, self.size/3 + 10))
        self.surf.fill(colors.BLUE_CLOUD)
        self.rect = self.surf.get_rect(topleft = (self.pos.x - 5, self.pos.y - 5))
        self.create_puzzle()
        
    def draw(self):
        ### Draw block
        for i in range(9):
            self.blocks[i].draw()
        
        ### Draw caro line
        for i in range(1,3):
            # Vertical
            pygame.draw.line(self.screen,
                            colors.BLACK,
                            (i*self.size/9 + self.pos.x, self.pos.y),
                            (i*self.size/9 + self.pos.x, self.pos.y + self.size/3 - 2))
            # Horizontal
            pygame.draw.line(self.screen,
                            colors.BLACK,
                            (self.pos.x, i*self.size/9 + self.pos.y),
                            (self.pos.x + self.size/3 - 2, i*self.size/9 + self.pos.y))

    def update(self):
        pass

    def set_cost(self, _cost):
        self.h_cost_block, self.h_cost = _cost
        self.g_cost = self.level
        self.f_cost = self.h_cost + self.g_cost

    def set_image(self, _path):
        self.images = image_service.split_image(_path)
        self.create_puzzle()

    def set_puzzle(self, _puzzle):
        self.puzzle = _puzzle
        self.create_puzzle()

    def create_puzzle(self):
        self.blocks = []

        if self.parent != None:
            offset_y = self.parent.surf.get_height() + 20
            offset_x = self.pos.x - self.parent.pos.x
            self.pos = pygame.math.Vector2(self.parent.pos.x + offset_x, self.parent.pos.y + offset_y)
        self.surf = pygame.Surface((self.size/3 + 10, self.size/3 + 10))
        self.rect = self.surf.get_rect(topleft = (self.pos.x - 5, self.pos.y - 5))

        for i in range(9):
            if self.images != None:
                self.blocks.append(block.Block(self.screen,
                                            self.size/9,
                                            (i%3*self.size/9 + self.pos.x,
                                             i//3*self.size/9 + self.pos.y),
                                            self.puzzle[i],
                                            colors.BLUE_CLOUD,
                                            self.images[self.puzzle[i]]))
            else:
                self.blocks.append(block.Block(self.screen,
                                            self.size/9,
                                            (i%3*self.size/9 + self.pos.x,
                                             i//3*self.size/9 + self.pos.y),
                                            self.puzzle[i],
                                            colors.BLUE_CLOUD,
                                            None))
            if self.puzzle[i] == 0:
                self.block_null_index = i
    
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

    def child_up(self):
        pass
    def child_right(self):
        pass
    def child_down(self):
        pass
    def child_left(self):
        pass

    def general_child(self):
        self.child_up()
        self.child_right
        self.child_down()
        self.child_left
    
    def move_up(self):
        # Animation
        if self.is_move_up or self.is_move_right or self.is_move_down or self.is_move_left:
            return

        n = self.block_null_index
        if n - 3 < 0:
            return

        self.is_move_up = True
        block_up = self.blocks[n-3]
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
        next_puzzle = numpy.zeros(9, dtype = int)
        self.copy_puzzle(next_puzzle, self.puzzle)
        temp = next_puzzle[n-3]
        next_puzzle[n-3] = next_puzzle[n]
        next_puzzle[n] = temp
        self.set_puzzle(next_puzzle)
        
    def move_right(self):
        # Animation
        if self.is_move_up or self.is_move_right or self.is_move_down or self.is_move_left:
            return

        n = self.block_null_index
        if n%3 >= 3-1:
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
        next_puzzle = numpy.zeros(9, dtype = int)
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
        if n + 3 >= 9:
            return

        self.is_move_down = True
        block_down = self.blocks[n+3]
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
        next_puzzle = numpy.zeros(9, dtype = int)
        self.copy_puzzle(next_puzzle, self.puzzle)
        temp = next_puzzle[n+3]
        next_puzzle[n+3] = next_puzzle[n]
        next_puzzle[n] = temp
        self.set_puzzle(next_puzzle)

    def move_left(self):
        # Animation
        if self.is_move_up or self.is_move_right or self.is_move_down or self.is_move_left:
            return
        
        n = self.block_null_index
        if n%3 <= 0:
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
        next_puzzle = numpy.zeros(9, dtype = int)
        self.copy_puzzle(next_puzzle, self.puzzle)
        temp = next_puzzle[n-1]
        next_puzzle[n-1] = next_puzzle[n]
        next_puzzle[n] = temp
        self.set_puzzle(next_puzzle)