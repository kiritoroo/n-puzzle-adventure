import pygame
import node
import settings
import numpy
import algorithm
import colors
import sys

pygame.init()
clock = pygame.time.Clock()
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
        self.node_count = 1

        self.solution_path = None
        self.solution_node = None

        self.str_algorithm = 'BFS'
        self.algorithm = algorithm.UniformedSearch()

        self.init()

    def init(self):
        node_size = self.size
        offset = pygame.math.Vector2(10,-50)
        spawn_point = (settings.SCREEN_WIDTH/2 - (node_size/6) + offset.x,
                    settings.SCREEN_HEIGHT/2 - (node_size/6) + offset.y)
        self.root = node.Node(self.screen, self.start_puzzle[self.ratio-3], 0, node_size, int(self.ratio), spawn_point, self)
        self.root.set_draw_to_child(False)
        self.root.set_draw_to_parent(False)
        self.get_all_node(self.root)

        if self.frame.__module__ == 'frame_simulator':
            self.proplem_node = node.Node(self.screen, self.root.puzzle, 0, 300, self.ratio, (1130,530), self)

    def draw_root(self):
        self.root.draw()

    def update_root(self):
        self.root.update()


    def draw(self):
        for i in range(len(self.all_node)):
            self.all_node[i].draw()

    def update(self):
        for i in range(len(self.all_node)):
            if self.algorithm.goal_found:
                if self.all_node[i].children == [] and self.all_node[i].level < self.algorithm.goal_node.level:
                    self.all_node[i].set_color(colors.RED_LIGHT)
                if self.all_node[i].is_same_puzzle(self.goal_puzzle[self.ratio-3]):
                    self.all_node[i].set_color(colors.GREEN_LIME)
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
        elif _str_algorithm == "A* (Euclidean)":
            self.algorithm = algorithm.InformedSearch()
            self.str_algorithm = "A* (Euclidean)"
        elif _str_algorithm == "Hill Climb":
            self.algorithm = algorithm.LocalSearch()
            self.str_algorithm = 'Hill Climb'
        print(self.str_algorithm)

    def solve_all(self):
        self.reset_handler()
        self.algorithm.init_all(self.screen, self.root, self.goal_puzzle[self.ratio-3], self)
        if self.str_algorithm == 'BFS':
            self.algorithm.bfs()
        elif self.str_algorithm == 'A* (Manhattan)':
            self.algorithm.a_star(0)
        elif self.str_algorithm == 'A* (Euclidean)':
            self.algorithm.a_star(1)
        elif self.str_algorithm == 'Hill Climb':
            self.algorithm.hill_climb()
        self.solution_path = self.algorithm.solution_path()
        self.create_solution_node()
    
    def find_solution(self):
        self.reset_handler()
        self.algorithm.init_all(self.screen, self.root, self.goal_puzzle[self.ratio-3], self)
        if self.str_algorithm == 'BFS':
            self.algorithm.bfs()
        elif self.str_algorithm == 'A* (Manhattan)':
            if self.algorithm.a_star_quickly(0) == False:
                return False
        self.solution_path = self.algorithm.solution_path()
        self.create_solution_node()
        self.play_solution_root()
        return True

    def create_solution_node(self):
        self.solution_node = []
        if self.solution_path != None:
            start_pos_x = 350
            for i in range(len(self.solution_path)):
                _node = node.Node(self.screen,
                                  self.solution_path[i],
                                  0,
                                  (200),
                                  self.ratio,
                                  (start_pos_x, 600),
                                  self)
                self.solution_node.append(_node)
                start_pos_x += 100

    def draw_solution(self):
        for i in range(len(self.solution_node)):
            self.solution_node[i].draw()
            if i+1 < len(self.solution_node):
                pygame.draw.line(self.screen, colors.GREEN_LIGHT, 
                                 (self.solution_node[i].pos[0] + self.solution_node[i].surf.get_width()/2, self.solution_node[i].pos[1] + self.solution_node[i].surf.get_height()/2),
                                 (self.solution_node[i+1].pos[0], self.solution_node[i+1].pos[1] + self.solution_node[i+1].surf.get_height()/2),
                                 5)          
            self.solution_node[i].update

    def play_solution(self):
        if self.solution_path == None:
            return
        for i in range(len(self.solution_path)):
            self.proplem_node.set_puzzle(self.solution_path[i])   
            
            self.proplem_node.set_color("ORANGE")
            self.proplem_node.draw()
            pygame.display.update()
            clock.tick(5)

    def play_solution_root(self):
        if self.solution_path == None:
            return
        for i in range(len(self.solution_path)):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.frame.ui_event(event)
            
            self.root.set_puzzle(self.solution_path[i])               
            self.root.draw()
            pygame.display.update()
            clock.tick(10)
    # End Algorithm

    # HARDCORE
    def reset_handler(self):
        self.all_node = []
        self.node_count = 1
        self.solution_path = None
        self.solution_node = None
        self.index_choose = None
        self.node_choose = None
        self.root.set_children([])
        self.get_all_node(self.root)
        self.get_max_level()
        self.algorithm.reset_goal_found()

    def valid_puzzle(self, _puzzle_string):
        valid = False
        print(len(_puzzle_string))
        if len(_puzzle_string) == 9 or len(_puzzle_string) == 16 or len(_puzzle_string) == 25:
            ref = list(range(int(numpy.math.pow(self.ratio,2))))
            valid = True
            for i in _puzzle_string:
                if int(i) not in ref:
                    valid = False
                else:
                    ref.remove(int(i))
        print(valid)
        return valid

    def set_goal(self, _string):
        puzzle_string = _string.split(" ")
        if self.valid_puzzle(puzzle_string):
            puzzle = []
            for i in range(9):
                puzzle.append(int(puzzle_string[i]))
            self.goal_puzzle = puzzle
            self.reset_handler()
            self.solution_node = []
            self.solution_path = None
            return True
        return False

    def set_root(self, string):
        puzzle_string = string.split(" ")
        if self.valid_puzzle(puzzle_string):
            puzzle = []
            for i in range(9):
                puzzle.append(int(puzzle_string[i]))
            self.root.set_puzzle(puzzle)
            self.reset_handler()
            self.proplem_node.set_puzzle(puzzle)
            self.proplem_node.set_puzzle(puzzle)
            self.solution_node = []
            self.solution_path = None
            return True
        return False

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
