import pygame
import numpy
import sys, time
import settings
import colors
import datetime

pygame.init()
clock = pygame.time.Clock()
class UniformedSearch:
    def __init__(self):
        self.goal_found = False
        self.goal_node = None

    def init_all(self, screen, _root, _goal_puzzle, _handlerNode):
        self.root = _root
        self.goal_puzzle = _goal_puzzle
        self.handlerNode = _handlerNode
        self.screen = screen
    
    def bfs(self):
        visited_list = []
        queue_list = []
        
        queue_list.append(self.root)

        last_time = time.time()
        while(len(queue_list) > 0 and not self.goal_found):
            dt = time.time() - last_time  
            last_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handlerNode.frame.ui_event(event)
            if not self.handlerNode.is_run:
                return
            current_node = queue_list[0] 
            queue_list.pop(0)
            visited_list.append(current_node)
              
            current_node.general_child()
            
            self.handlerNode.all_node = []
            self.handlerNode.get_all_node(self.handlerNode.root)
            self.handlerNode.get_max_level()
            
            self.screen.fill(colors.WHITE)
            self.handlerNode.draw()             
            self.handlerNode.update()
            self.handlerNode.frame.update(dt)
            self.handlerNode.frame.render(self.screen)
    
            pygame.display.update()
            clock.tick(settings.FRAME_RATE)
                        
            for i in range(len(current_node.children)):
                current_child = current_node.children[i]
                if current_child.is_same_puzzle(self.goal_puzzle):
                    self.goal_found = True
                    self.goal_node = current_child
                    self.goal_node.set_color(colors.GREEN_LIME)
                
                if not self.contains_node(visited_list, current_child) and not self.contains_node(queue_list, current_child):
                    queue_list.append(current_child)   
                else:
                    current_child.set_color(colors.RED_DEFAULT)
    def bfs_quickly(self):
        visited_list = []
        queue_list = []

        queue_list.append(self.root)

        last_time = time.time()
        while(len(queue_list) > 0 and not self.goal_found):
            dt = time.time() - last_time  
            last_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handlerNode.frame.ui_event(event)
            if not self.handlerNode.is_run:
                return
                
            current_node = queue_list[0] 
            queue_list.pop(0)
            visited_list.append(current_node)
              
            current_node.general_child()
            
            self.screen.fill(colors.WHITE)
            if self.handlerNode.frame.__module__ == 'frame_compare':
                self.handlerNode.frame.execute_time4 = datetime.datetime.now() - self.handlerNode.frame.start_time4
                self.handlerNode.frame.label_timetext4.set_text('Time: ' + str(self.handlerNode.frame.execute_time4)[::-1].split(':', 1)[0][::-1] + 's')
            self.handlerNode.update()
            self.handlerNode.frame.update(dt)
            self.handlerNode.frame.render(self.screen)
    
            pygame.display.update()
            clock.tick(settings.FRAME_RATE)
                        
            for i in range(len(current_node.children)):
                current_child = current_node.children[i]
                if current_child.is_same_puzzle(self.goal_puzzle):
                    self.goal_found = True
                    self.goal_node = current_child
                    self.goal_node.set_color(colors.GREEN_LIME)
                    self.handlerNode.all_node = []
                    self.handlerNode.get_all_node(self.handlerNode.root)

                    return True
                if not self.contains_node(visited_list, current_child) and not self.contains_node(queue_list, current_child):
                    queue_list.append(current_child)   
                else:
                    current_child.set_color(colors.RED_DEFAULT)
            
            if (self.handlerNode.node_count) > 15000:
                return False

    def reset_goal_found(self):
        self.goal_found = False
        self.goal_node = None

    def contains_node(self, _list, _node):
        contain = False
        for i in range(len(_list)):
            if _list[i].is_same_puzzle(_node.puzzle):
                contain = True
        return contain

    def solution_path(self):
        if not self.goal_found:
            return
        
        n = self.goal_node
        solution = []
        solution.append(n.puzzle)
        while n.parent != None:
            n.set_line_color(colors.GREEN_LIME)
            n = n.parent
            solution.append(n.puzzle)
        solution.reverse()
        print(solution)
        return solution

class InformedSearch:
    def __init__(self):
        self.goal_found = False
        self.goal_node = None

    def init_all(self, screen, _root, _goal_puzzle, _handlerNode):
        self.root = _root
        self.goal_puzzle = _goal_puzzle
        self.handlerNode = _handlerNode
        self.screen = screen
        
    def a_star(self, _type):
        visited_list = []
        queue_list = []
        
        queue_list.append(self.root)
        
        last_time = time.time()
        while(len(queue_list) > 0 and not self.goal_found):  
            dt = time.time() - last_time
            last_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handlerNode.frame.ui_event(event)
            if not self.handlerNode.is_run:
                return

            h_cost_min = queue_list[0].h_cost
            h_cost_min_index = 0
            percent_right_max = queue_list[0].percent_right
            for i in range(len(queue_list)):
                if queue_list[i].h_cost < h_cost_min:
                    h_cost_min = queue_list[i].h_cost
                    percent_right_max = queue_list[i].percent_right
                    h_cost_min_index = i
            
            current_node = queue_list[h_cost_min_index] 
            queue_list.pop(h_cost_min_index)
            visited_list.append(current_node)
              
            current_node.general_child()
            #current_node.set_minimum(True)
            
            self.handlerNode.all_node = []
            self.handlerNode.get_all_node(self.handlerNode.root)
            self.handlerNode.get_max_level()
            
            self.screen.fill(colors.WHITE)
            self.handlerNode.draw()             
            self.handlerNode.update()
            self.handlerNode.frame.render(self.screen)
            self.handlerNode.frame.update(dt)
            pygame.display.update()
            clock.tick(settings.FRAME_RATE)
                        
            for i in range(len(current_node.children)):
                current_child = current_node.children[i]
                if current_child.is_same_puzzle(self.goal_puzzle):
                    self.goal_found = True
                    self.goal_node = current_child
                    self.goal_node.set_color(colors.GREEN_LIME)
                if _type == 0:
                    current_child.set_cost(self.manhattan_distance(current_child.puzzle))
                elif _type == 1:
                    current_child.set_cost(self.euclidean_distance(current_child.puzzle))
                if not self.contains_node(visited_list, current_child) and not self.contains_node(queue_list, current_child):
                    queue_list.append(current_child)   
                else:
                    current_child.set_color(colors.RED_DEFAULT)
            
    def a_star_quickly(self, _type):
        visited_list = []
        queue_list = []
        
        queue_list.append(self.root)
        
        last_time = time.time()
        while(len(queue_list) > 0 and not self.goal_found):  
            dt = time.time() - last_time
            last_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handlerNode.frame.ui_event(event)
            if not self.handlerNode.is_run:
                return

            h_cost_min = queue_list[0].h_cost
            h_cost_min_index = 0
            percent_right_max = queue_list[0].percent_right
            for i in range(len(queue_list)):
                if queue_list[i].h_cost < h_cost_min and queue_list[i].percent_right > percent_right_max:
                    h_cost_min = queue_list[i].h_cost
                    percent_right_max = queue_list[i].percent_right
                    h_cost_min_index = i
            
            current_node = queue_list[h_cost_min_index] 
            queue_list.pop(h_cost_min_index)
            visited_list.append(current_node)
              
            current_node.general_child()
            #current_node.set_minimum(True)

            self.screen.fill(colors.WHITE)
            if self.handlerNode.frame.__module__ == 'frame_compare':
                if _type == 0:
                    self.handlerNode.frame.execute_time1 = datetime.datetime.now() - self.handlerNode.frame.start_time1
                    self.handlerNode.frame.label_timetext1.set_text('Time: ' + str(self.handlerNode.frame.execute_time1)[::-1].split(':', 1)[0][::-1] + 's')
                elif _type == 1:
                    self.handlerNode.frame.execute_time3 = datetime.datetime.now() - self.handlerNode.frame.start_time3
                    self.handlerNode.frame.label_timetext3.set_text('Time: ' + str(self.handlerNode.frame.execute_time3)[::-1].split(':', 1)[0][::-1] + 's')
            self.handlerNode.update()
            self.handlerNode.frame.render(self.screen)
            self.handlerNode.frame.update(dt)
    
            pygame.display.update()
            clock.tick(settings.FRAME_RATE)
                        
            for i in range(len(current_node.children)):
                current_child = current_node.children[i]
                if current_child.is_same_puzzle(self.goal_puzzle):
                    self.goal_found = True
                    self.goal_node = current_child
                    self.goal_node.set_color(colors.GREEN_LIME)
                    self.handlerNode.all_node = []
                    self.handlerNode.get_all_node(self.handlerNode.root)

                    return True
                if _type == 0:
                    current_child.set_cost(self.manhattan_distance(current_child.puzzle))
                elif _type == 1:
                    current_child.set_cost(self.euclidean_distance(current_child.puzzle))
                if not self.contains_node(visited_list, current_child) and not self.contains_node(queue_list, current_child):
                    queue_list.append(current_child)   
                else:
                    current_child.set_color(colors.RED_DEFAULT)
            
            if (self.handlerNode.node_count) > 5000:
                return False
    # Distance    
    def manhattan_distance(self, _puzzle):
        _puzzle_2d = numpy.zeros((3,3), dtype = int)
        _goal_puzzle_2d = numpy.zeros((3,3), dtype = int)
        
        # convert array to 2D array
        k = 0
        for i in range(3):
            for j in range(3):
                _puzzle_2d[i][j] = _puzzle[k]
                _goal_puzzle_2d[i][j] = self.goal_puzzle[k]
                k += 1
    
        # cal h_cost all block
        # cal h_cost total
        h_block = numpy.zeros((3,3), dtype = int)
        h_node = 0
        for i in range(3):
            for j in range(3):
                if _puzzle_2d[i][j] != 0:
                    x1, y1 = self.get_goal_ij(_puzzle_2d[i][j], _goal_puzzle_2d)
                    x2, y2 = i, j
                    h_cost = abs(x1-x2) + abs(y1-y2)
                    h_block[i][j] = h_cost
                    h_node += h_block[i][j]
        
        return h_block, h_node
    
    def euclidean_distance(self, _puzzle):
        _puzzle_2d = numpy.zeros((3,3), dtype = int)
        _goal_puzzle_2d = numpy.zeros((3,3), dtype = int)
        
        # convert array to 2D array
        k = 0
        for i in range(3):
            for j in range(3):
                _puzzle_2d[i][j] = _puzzle[k]
                _goal_puzzle_2d[i][j] = self.goal_puzzle[k]
                k += 1
    
        # cal h_cost total
        h_block = numpy.zeros((3,3), dtype = int)
        h_node = 0
        for i in range(3):
            for j in range(3):
                if _puzzle_2d[i][j] != 0:
                    x1, y1 = self.get_goal_ij(_puzzle_2d[i][j], _goal_puzzle_2d)
                    x2, y2 = i, j
                    dx, dy = x2-x1, y2-y1
                    h_cost = numpy.hypot(dx, dy)
                    h_block[i][j] = h_cost
                    h_node += h_block[i][j]

        return h_block, h_node
    # End Distance

    def get_goal_ij(self, value, _goal_puzzle_2d):
        for i in range(3):
            for j in range(3):
                if value == _goal_puzzle_2d[i][j]:
                    return(i,j)
    def reset_goal_found(self):
        self.goal_found = False
        self.goal_node = None

    def contains_node(self, _list, _node):
        contain = False
        for i in range(len(_list)):
            if _list[i].is_same_puzzle(_node.puzzle):
                contain = True
        return contain

    def solution_path(self):
        if not self.goal_found:
            return
        
        n = self.goal_node
        solution = []
        solution.append(n.puzzle)
        while n.parent != None:
            n.set_line_color(colors.GREEN_LIME)
            n = n.parent
            solution.append(n.puzzle)
        solution.reverse()
        print(solution)
        return solution

class LocalSearch:
    def __init__(self):
        self.goal_found = False
        self.goal_node = None

    def init_all(self, screen, _root, _goal_puzzle, _handlerNode):
        self.root = _root
        self.goal_puzzle = _goal_puzzle
        self.handlerNode = _handlerNode
        self.screen = screen
        
    def hill_climb(self):
        visited_list = []
        queue_list = []
        
        queue_list.append(self.root)
        
        last_time = time.time()
        while(len(queue_list) > 0 and not self.goal_found):  
            dt = time.time() - last_time
            last_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handlerNode.frame.ui_event(event)
            if not self.handlerNode.is_run:
                return

            percent_right_max = queue_list[0].percent_right
            percent_false_min = queue_list[0].percent_false
            best_index = 0
            for i in range(len(queue_list)):
                if queue_list[i].percent_false < percent_false_min:
                    percent_right_max = queue_list[i].percent_right
                    percent_false_min = queue_list[i].percent_false
                    best_index = i

            current_node = queue_list[best_index] 
            queue_list.pop(best_index)
            visited_list.append(current_node)
              
            current_node.general_child()
            
            self.handlerNode.all_node = []
            self.handlerNode.get_all_node(self.handlerNode.root)
            self.handlerNode.get_max_level()
            
            self.screen.fill(colors.WHITE)
            self.handlerNode.draw()             
            self.handlerNode.update()
            self.handlerNode.frame.render(self.screen)
            self.handlerNode.frame.update(dt)
    
            pygame.display.update()
            clock.tick(settings.FRAME_RATE)
                        
            for i in range(len(current_node.children)):
                current_child = current_node.children[i]
                if current_child.is_same_puzzle(self.goal_puzzle):
                    self.goal_found = True
                    self.goal_node = current_child
                    self.goal_node.set_color(colors.GREEN_LIME)
                if not self.contains_node(visited_list, current_child) and not self.contains_node(queue_list, current_child):
                    queue_list.append(current_child)   
                else:
                    current_child.set_color(colors.RED_DEFAULT)

    def hill_climb_quickly(self):
        visited_list = []
        queue_list = []
        
        queue_list.append(self.root)
        
        last_time = time.time()
        while(len(queue_list) > 0 and not self.goal_found):  
            dt = time.time() - last_time
            last_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handlerNode.frame.ui_event(event)
            if not self.handlerNode.is_run:
                return

            percent_right_max = queue_list[0].percent_right
            percent_false_min = queue_list[0].percent_false
            best_index = 0
            for i in range(len(queue_list)):
                if queue_list[i].percent_false < percent_false_min:
                    percent_right_max = queue_list[i].percent_right
                    percent_false_min = queue_list[i].percent_false
                    best_index = i

            current_node = queue_list[best_index] 
            queue_list.pop(best_index)
            visited_list.append(current_node)
              
            current_node.general_child()

            self.screen.fill(colors.WHITE)
            if self.handlerNode.frame.__module__ == 'frame_compare':
                self.handlerNode.frame.execute_time2 = datetime.datetime.now() - self.handlerNode.frame.start_time2
                self.handlerNode.frame.label_timetext2.set_text('Time: ' + str(self.handlerNode.frame.execute_time2)[::-1].split(':', 1)[0][::-1] + 's')
            self.handlerNode.draw()             
            self.handlerNode.update()
            self.handlerNode.frame.render(self.screen)
            self.handlerNode.frame.update(dt)
    
            pygame.display.update()
            clock.tick(settings.FRAME_RATE)
                        
            for i in range(len(current_node.children)):
                current_child = current_node.children[i]
                if current_child.is_same_puzzle(self.goal_puzzle):
                    self.goal_found = True
                    self.goal_node = current_child
                    self.goal_node.set_color(colors.GREEN_LIME)            
                    self.handlerNode.all_node = []
                    self.handlerNode.get_all_node(self.handlerNode.root)
            
                    return True
                if not self.contains_node(visited_list, current_child) and not self.contains_node(queue_list, current_child):
                    queue_list.append(current_child)   
                else:
                    current_child.set_color(colors.RED_DEFAULT)

                if (self.handlerNode.node_count) > 5000:
                    return False

    def reset_goal_found(self):
        self.goal_found = False
        self.goal_node = None

    def contains_node(self, _list, _node):
        contain = False
        for i in range(len(_list)):
            if _list[i].is_same_puzzle(_node.puzzle):
                contain = True
        return contain

    def solution_path(self):
        if not self.goal_found:
            return
        
        n = self.goal_node
        solution = []
        solution.append(n.puzzle)
        while n.parent != None:
            n.set_line_color(colors.GREEN_LIME)
            n = n.parent
            solution.append(n.puzzle)
        solution.reverse()
        print(solution)
        return solution
