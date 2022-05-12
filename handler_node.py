import pygame
import node
import settings

class HandlerNode:
    def __init__(self, _screen):
        self.screen = _screen

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
        self.root = node.Node(self.screen, self.start_puzzle, 0, node_size, spawn_point)
        self.get_all_node(self.root)

    def update(self):
        for i in range(len(self.all_node)):
            self.all_node[i].update()
    
    def draw(self):
        for i in range(len(self.all_node)):
            self.all_node[i].draw()

    def get_all_node(self, node):
        self.all_node.append(node)
        for i in range(len(node.children)):
            self.get_all_node(node.children[i])
