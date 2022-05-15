import pygame
import node
import settings
import numpy

pygame.init()

class HandlerNode:
    def __init__(self, _screen, _frame):
        self.screen = _screen
        self.frame = _frame
        self.start_puzzle = [1,2,3,0,5,6,4,7,8]
        self.goal_puzzle = [1,2,3,4,5,6,7,8,0] 

        self.node_choose = None
        self.index_choose = None

        self.all_node = []
        self.all_node_level = []

        self.max_level = 0

        self.solution_puzzle_path = None
        self.solution_puzzle_node = None

        self.init()

    def init(self):
        node_size = 900
        offset = pygame.math.Vector2(10,-50)
        spawn_point = (settings.SCREEN_WIDTH/2 - (node_size/6) + offset.x,
                    settings.SCREEN_HEIGHT/2 - (node_size/6) + offset.y)
        self.root = node.Node(self.screen, self.start_puzzle, 0, node_size, spawn_point, self)
        self.get_all_node(self.root)

    def draw(self):
        for i in range(len(self.all_node)):
            self.all_node[i].draw()

    def update(self):
        for i in range(len(self.all_node)):
            self.all_node[i].update()

    def set_image(self, _path):
        self.root.set_image(_path)

    def get_all_node(self, _node):
        self.all_node.append(_node)
        for i in range(len(_node.children)):
            self.get_all_node(_node.children[i])
    
    def append_node(self, _node):
        self.all_node.append(_node)

    def shuffle_puzzle(self, _node):
        numpy.random.shuffle(_node.puzzle)
        _node.set_puzzle(_node.puzzle)
