import pygame
import numpy
import sys, time
import settings
import colors

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

            current_node = queue_list[0] 
            queue_list.pop(0)
            visited_list.append(current_node)
              
            current_node.general_child()
            
            self.handlerNode.all_node = []
            self.handlerNode.get_all_node(self.handlerNode.root)
            self.handlerNode.get_max_level()
            
            self.screen.fill('WHITE')
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
            n.set_line_color('GREEN')
            n = n.parent
            solution.append(n.puzzle)
        solution.reverse()
        print(solution)
        return solution
    