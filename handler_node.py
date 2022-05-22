import pygame
import node
import settings
import numpy
import algorithm

pygame.init()

class HandlerNode:
    def __init__(self, _screen, _frame, _ratio, _size):
        self.screen = _screen
        self.frame = _frame
        self.ratio = _ratio
        self.size = _size
        self.zoom_rate = 1
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

        self.str_algorithm = 'BFS'
        self.algorithm = algorithm.UniformedSearch()

        self.init()

    def init(self):
        node_size = self.size
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
        for i in range(len(self.all_node)):
          self.all_node[i].set_image(_path, _ratio)

    def set_ratio(self, _ratio):
        self.ratio = _ratio
        for i in range(len(self.all_node)):
            self.all_node[i].set_ratio(_ratio)

    # Algorithm
    def set_algorithm(self, _str_algorithm):
        if _str_algorithm == 'BFS':
            self.algorithm = algorithm.UniformedSearch()
            self.str_algorithm = 'BFS'
        elif _str_algorithm == "A* (Manhattan)":
            self.algorithm = algorithm.InformedSearch()
            self.str_algorithm = "A* (Manhattan)"
        print(self.str_algorithm)

    def solve(self):
        self.reset_handler()
        self.algorithm.init_all(self.screen, self.root, self.goal_puzzle[self.ratio-3], self)
        if self.str_algorithm == 'BFS':
            self.algorithm.bfs()
        elif self.str_algorithm == "A* (Manhattan)":
            self.algorithm.a_star()
        self.solution_path = self.algorithm.solution_path()
        self.create_solution_node()
    # End Algorithm

    # HARDCORE
    def reset_handler(self):
        self.all_node = []
        self.index_choose = None
        self.node_choose = None
        self.root.set_children([])
        self.get_all_node(self.root)
        self.get_max_level()
        self.algorithm.reset_goal_found()

    def valid_puzzle(self, puzzle_string):
        valid = False
        print(len(puzzle_string))
        if len(puzzle_string) == 9:
            ref = list(range(9))
            valid = True
            for i in puzzle_string:
                if int(i) not in ref:
                    valid = False
                else:
                    ref.remove(int(i))
        print(valid)
        return valid
    def check_all_collider_mouse(self, _key):
        if _key == 3:
            for i in range(len(self.all_node)):
                self.all_node[i].set_is_choose(False)

        check = False
        for i in range(len(self.all_node)):
            if self.all_node[i].check_collider_mouse(_key):
                self.index_choose = i
                self.node_choose = self.all_node[i]
                check = True
                break
        if check == False:
            self.index_choose = None
            self.node_choose = None

        for i in range(len(self.all_node)):
            if i == self.index_choose and check == True:
                continue
            else:
                self.all_node[i].set_is_choose(False)

    def zoom(self, _zoom):
        self.zoom_rate = _zoom
        self.zoom_all(self.root, _zoom)
        self.reset_pos()
        
    def zoom_all(self, _node, _zoom):
        _node.set_zoom(_zoom)
        for i in range(len(_node.children)):
            self.zoom_all(_node.children[i], _zoom)

    def move(self, _node, _offset):
        new_pos = (_node.pos[0] + _offset[0],
                   _node.pos[1] + _offset[1])
        _node.set_pos(new_pos)   
        for i in range(len(_node.children)):
            self.move(_node.children[i], _offset)

    def get_max_level(self):
        self.max_level = 0
        for i in range(len(self.all_node)):
            if self.all_node[i].level > self.max_level:
                self.max_level = self.all_node[i].level
        self.get_all_node_level()
        self.reset_pos()    
   
    def get_all_node_level(self):    
        self.all_node_level = []
        for i in range(self.max_level + 1):
            self.all_node_level.append([])
        for i in range(len(self.all_node)):
            self.all_node_level[self.all_node[i].level].append(self.all_node[i])

    def reset_pos(self):
        offset = 40 * self.zoom_rate
        if self.max_level == 0:
            return
        for i in range(self.max_level + 1):
            total_width = 0
            for j in range(len(self.all_node_level[i])):
                total_width += self.all_node_level[i][j].surf.get_width() + offset
            start_pos_x = self.root.pos[0] - total_width/2 + self.all_node_level[i][j].surf.get_width()/2
            for j in range(len(self.all_node_level[i])):
                if  self.all_node_level[i][j].level > 0:
                    self.all_node_level[i][j].set_pos((start_pos_x, self.all_node_level[i][j].pos[1]))
                start_pos_x += self.all_node_level[i][j].surf.get_width() + offset
    # End HARDCORE

    def get_all_node(self, _node):
        self.all_node.append(_node)
        for i in range(len(_node.children)):
            self.get_all_node(_node.children[i])

    def append_node(self, _node):
        self.all_node.append(_node)

    def shuffle_puzzle(self, _node):
        numpy.random.shuffle(_node.puzzle)
        _node.set_puzzle(_node.puzzle)
