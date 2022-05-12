from winreg import HKEY_CLASSES_ROOT
import pygame
import numpy as np
import settings
import colors
import image_service

import block

class Node:
    def __init__(self, _screen, _puzzle, _level, _size, _pos):
        self.screen = _screen
        self.puzzle = _puzzle
        self.level = _level
        self.size = _size
        self.pos = pygame.math.Vector2(_pos)
        self.images = None
        self.init()

    def init(self):
        self.is_move = False
        self.is_choose = False

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
        self.images = self.image_service.get_image(_path)
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
                                            self.images[i]))
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
            if np.array_equal(self.children[i].puzzle, _child_node.puzzle):
                return True
        return False

    def is_same_puzzle(self, _p):
        for i in range(len(self.puzzle)):
            if self.puzzle[i] != _p[i]:
                return False
        return True

    def child_up(self):
        i = self.block_null_index
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
        pass
    def move_right(self):
        pass
    def move_down(self):
        pass
    def move_left(self):
        pass

    


