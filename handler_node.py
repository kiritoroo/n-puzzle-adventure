import pygame
import node
import settings
import numpy

pygame.init()

class HandlerNode:
    def __init__(self, _screen, _frame, _ratio):
        self.screen = _screen
        self.frame = _frame
        self.ratio = _ratio
        self.goal_puzzle = ([1,2,3,4,5,6,7,8,0],
                            [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0],
                            [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,0])
        self.start_puzzle = ([1,2,3,4,5,6,7,8,0],
                            [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0],
                            [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,0])
        numpy.random.shuffle(self.start_puzzle[self.ratio-3])

        self.node_choose = None
        self.index_choose = None

        self.all_node = []
        self.all_node_level = []

        self.max_level = 0

        self.solution_puzzle_path = None
        self.solution_puzzle_node = None

        self.init()

    def init(self):
        node_size = 1000
        offset = pygame.math.Vector2(10,-50)
        spawn_point = (settings.SCREEN_WIDTH/2 - (node_size/6) + offset.x,
                    settings.SCREEN_HEIGHT/2 - (node_size/6) + offset.y)
        self.root = node.Node(self.screen, self.start_puzzle[self.ratio-3], 0, node_size, int(self.ratio), spawn_point, self)
        self.get_all_node(self.root)

    def draw(self):
        for i in range(len(self.all_node)):
            self.all_node[i].draw()

    def update(self):
        for i in range(len(self.all_node)):
            self.all_node[i].update()

    def set_image(self, _path, _ratio):
        self.root.set_image(_path, _ratio)

    def set_ratio(self, _ratio):
        self.ratio = _ratio
        for i in range(len(self.all_node)):
            self.all_node[i].set_ratio(_ratio)

    def get_all_node(self, _node):
        self.all_node.append(_node)
        for i in range(len(_node.children)):
            self.get_all_node(_node.children[i])
    
    def append_node(self, _node):
        self.all_node.append(_node)

    def shuffle_puzzle(self, _node):
        numpy.random.shuffle(_node.puzzle)
        _node.set_puzzle(_node.puzzle)
