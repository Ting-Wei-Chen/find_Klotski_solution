import sys
from queue import Queue
import copy
import time
import math
import pygame

class Solution:
    def __init__(self):
        self.visited = {}
        self.path = []

        self.current_game_state = [
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"]
        ]

        self.next_game_state = [
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"]
        ]

        ## store list of game_state, representing all paths going
        self.o_queue = Queue()

        self.WIDTH, self.HEIGHT = 800, 800
        self.CELL_SIZE = 100
        
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.BROWN = (162, 42, 42)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

        pygame.init()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        
        self.running = True
        self.restart = False

        while self.running:
            self.initialize()
            self.draw_grid_and_clear(self.current_game_state)

            self.finish_setting = False
            self.goal_set = False
            self.setting_problem()

            if not self.running or not self.goal_set:
                return

            self.visited[self.convert_to_string(self.current_game_state)] = True

            self.draw_grid_and_clear(self.current_game_state)

            self.find_solution()

            while self.running:
                if self.path != []:
                    for state in self.path:
                        self.draw_grid_and_clear(state)

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                self.running = False
                                break
                            #END
                        #END

                        if not self.running:
                            break

                        time.sleep(1)
                    #END
                    self.path = []
                else:
                    self.draw_grid_and_clear(self.current_game_state)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        break
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.restart = True
                        break
                #END

                if self.restart:
                    break
            #END
        #END
    #END

    def initialize(self):
        self.restart = False
        self.visited = {}
        self.path = []

        self.current_game_state = [
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"]
        ]

        self.next_game_state = [
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"]
        ]
    #END

    def draw_loading_icon(self, angle):
        """Draw a spinning arc to simulate a loading effect."""
        self.screen.fill(self.WHITE)  # Clear screen

        # Draw a spinning arc (like a clock hand)
        x, y, radius = self.WIDTH // 2, self.HEIGHT // 2, 50
        start_angle = math.radians(angle)
        end_angle = math.radians(angle + 270)  # Draw 3/4 of a circle
        pygame.draw.arc(self.screen, self.BLACK, (x - radius, y - radius, radius * 2, radius * 2), start_angle, end_angle, 5)

        pygame.display.flip()

    def draw_grid_and_clear(self, state):
        self.screen.fill(self.WHITE)  # Clear screen
        self.draw_grid(state)
        pygame.display.flip()

    def draw_grid(self, state):
        """Draw grid and placed blocks"""

        for row in range(5):
            for col in range(4):
                element = state[row][col]
                
                if self.is_empty(element):
                    rect = pygame.Rect(col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
                    pygame.draw.rect(self.screen, self.WHITE, rect) 
                    pygame.draw.rect(self.screen, self.BLACK, rect, 1)
                elif self.is_single_square(element):
                    rect = pygame.Rect(col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
                    pygame.draw.rect(self.screen, self.GRAY, rect) 
                    pygame.draw.rect(self.screen, self.BLACK, rect, 1)
                elif self.valid_rectangle_position(row, col, state):
                    rect = pygame.Rect(col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE*2)
                    pygame.draw.rect(self.screen, self.BROWN, rect)
                    pygame.draw.rect(self.screen, self.BLACK, rect, 1)
                elif self.valid_horizontal_position(row, col, state):
                    rect = pygame.Rect(col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE*2, self.CELL_SIZE)
                    pygame.draw.rect(self.screen, self.GREEN, rect)
                    pygame.draw.rect(self.screen, self.BLACK, rect, 1)
                elif self.valid_goal_position(row, col, state):
                    rect = pygame.Rect(col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE*2, self.CELL_SIZE*2)
                    pygame.draw.rect(self.screen, self.RED, rect)
                    pygame.draw.rect(self.screen, self.BLACK, rect, 1)
            #END
        #END
    #END
    
    def setting_problem(self):
        object_distance = 15

        self.finish_setting = False
        self.goal_set = False
        self.num_rect = 0
        self.num_hor_rect = 0
        self.setting_state = "selecting_adding_object"

        while not self.finish_setting:
            self.screen.fill(self.WHITE)  # Clear screen

            add_single_square_rect = pygame.Rect(object_distance, self.HEIGHT-object_distance-self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
            pygame.draw.rect(self.screen, self.GRAY, add_single_square_rect) 

            add_rectangle_rect = pygame.Rect(self.CELL_SIZE + object_distance * 2, self.HEIGHT-object_distance-self.CELL_SIZE*2, self.CELL_SIZE, self.CELL_SIZE*2)
            pygame.draw.rect(self.screen, self.BROWN, add_rectangle_rect) 

            add_horizontal_rectangle_rect = pygame.Rect(self.CELL_SIZE *2 + object_distance * 3, self.HEIGHT-object_distance-self.CELL_SIZE, self.CELL_SIZE * 2, self.CELL_SIZE)
            pygame.draw.rect(self.screen, self.GREEN, add_horizontal_rectangle_rect) 
            
            add_goal_rect = pygame.Rect(self.CELL_SIZE * 4 + object_distance * 4, self.HEIGHT - object_distance - self.CELL_SIZE*2, self.CELL_SIZE*2, self.CELL_SIZE*2)
            pygame.draw.rect(self.screen, self.RED, add_goal_rect) 

            self.draw_grid(self.current_game_state)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.finish_setting = True
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if add_single_square_rect.collidepoint(event.pos):
                        self.setting_state = "adding_single_square"
                    elif add_rectangle_rect.collidepoint(event.pos):
                        self.setting_state = "adding_rectangle"
                    elif add_horizontal_rectangle_rect.collidepoint(event.pos):
                        self.setting_state = "adding_horizontal_rectangle"
                    elif add_goal_rect.collidepoint(event.pos):
                        if not self.goal_set:
                            self.setting_state = "adding_goal"
                    else:
                        if self.setting_state == "selecting_adding_object":
                            if (not mouse_x >= 4 * self.CELL_SIZE) and (not mouse_y >= 5 * self.CELL_SIZE):
                                row = mouse_y // self.CELL_SIZE
                                col = mouse_x // self.CELL_SIZE

                                if self.is_single_square(self.current_game_state[row][col]):
                                    self.current_game_state[row][col] = "0"
                                elif self.valid_rectangle_position(row, col, self.current_game_state):
                                    self.current_game_state[row][col] = "0"
                                    self.current_game_state[row+1][col] = "0"
                                elif self.valid_goal_position(row, col, self.current_game_state):
                                    self.goal_set = False

                                    self.current_game_state[row][col] = "0"
                                    self.current_game_state[row+1][col] = "0"
                                    self.current_game_state[row][col+1] = "0"
                                    self.current_game_state[row+1][col+1] = "0"
                            elif self.goal_set:
                                self.finish_setting = True
                                break
                        else:
                            if mouse_x >= 4 * self.CELL_SIZE or mouse_y >= 5 * self.CELL_SIZE:
                                self.setting_state = "selecting_adding_object"
                                continue

                    if self.setting_state == "adding_single_square":
                        if mouse_x >= 4 * self.CELL_SIZE or mouse_y >= 5 * self.CELL_SIZE:
                            continue
                        row = mouse_y // self.CELL_SIZE
                        col = mouse_x // self.CELL_SIZE

                        if self.is_empty(self.current_game_state[row][col]):
                            self.current_game_state[row][col] = "a"
                        
                        continue
                    elif self.setting_state == "adding_rectangle":
                        if mouse_x >= 4 * self.CELL_SIZE or mouse_y >= 4 * self.CELL_SIZE:
                            continue
                        row = mouse_y // self.CELL_SIZE
                        col = mouse_x // self.CELL_SIZE
                        
                        if self.is_empty(self.current_game_state[row][col]) and self.is_empty(self.current_game_state[row+1][col]):
                            self.num_rect += 1
                            self.current_game_state[row][col]   = str(self.num_rect)
                            self.current_game_state[row+1][col] = str(self.num_rect)
                        continue
                    elif self.setting_state == "adding_horizontal_rectangle":
                        if mouse_x >= 3 * self.CELL_SIZE or mouse_y >= 5 * self.CELL_SIZE:
                            continue
                        row = mouse_y // self.CELL_SIZE
                        col = mouse_x // self.CELL_SIZE

                        if self.is_empty(self.current_game_state[row][col]) and self.is_empty(self.current_game_state[row][col+1]):
                            self.num_hor_rect += 1
                            self.current_game_state[row][col]   = str(-1 * self.num_hor_rect)
                            self.current_game_state[row][col+1] = str(-1 * self.num_hor_rect)
                        continue
                    elif self.setting_state == "adding_goal":
                        if mouse_x >= 3 * self.CELL_SIZE or mouse_y >= 4 * self.CELL_SIZE:
                            continue
                        row = mouse_y // self.CELL_SIZE
                        col = mouse_x // self.CELL_SIZE

                        if self.is_empty(self.current_game_state[row][col]) and self.is_empty(self.current_game_state[row+1][col]) \
                            and self.is_empty(self.current_game_state[row][col+1]) and self.is_empty(self.current_game_state[row+1][col+1]):
                            self.current_game_state[row][col]     = "A"
                            self.current_game_state[row+1][col]   = "A"
                            self.current_game_state[row][col+1]   = "A"
                            self.current_game_state[row+1][col+1] = "A"

                            self.goal_set = True
                        continue

            #END
        #END
    #END

    def is_single_square(self, s):
        return s.isalpha() and s.islower()
    def is_rectangle(self, s):
        return s.isdigit() and int(s) > 0
    def is_horizontal_rectangle(self, s):
        return s.startswith("-") and s[1:].isdigit() and int(s[1:]) > 0
    def is_empty(self, s):
        return s == "0"
    def is_goal(self, s):
        return s == "A"
    
    def error(self, error_msg):
        print("ERROR: {}".format(error_msg))
        sys.exit(-1)

    # Function to convert grid to a hashable state (tuple of tuples)
    def convert_to_string(self, game_state):
        res = ""
        for x_pos in range(5):
            for y_pos in range(4):
                if self.is_single_square(game_state[x_pos][y_pos]):
                    res += "a"
                elif self.is_empty(game_state[x_pos][y_pos]):
                    res += "0"
                elif self.is_rectangle(game_state[x_pos][y_pos]):
                    res += "1"
                elif self.is_horizontal_rectangle(game_state[x_pos][y_pos]):
                    res += "2"
                elif self.is_goal(game_state[x_pos][y_pos]):
                    res += "A"
        
        return res
    
    def print_game_state(self, state):
        for i in range(5):
            
            for j in range(4):
                print(state[i][j], end="")
                print(" ", end = "")
            #END
            print()
        #END
        print("-------------------")
    #END

    def valid_rectangle_position(self, x_pos, y_pos, state):
        if x_pos > 3:
            return False
        
        if not self.is_rectangle(state[x_pos][y_pos]):
            return False
        
        if state[x_pos+1][y_pos] != state[x_pos][y_pos]:
            return False
        
        return True
    #END

    def valid_horizontal_position(self, x_pos, y_pos, state):
        if y_pos > 2:
            return False
        
        if not self.is_horizontal_rectangle(state[x_pos][y_pos]):
            return False
        
        if state[x_pos][y_pos+1] != state[x_pos][y_pos]:
            return False
        
        return True

    def valid_goal_position(self, x_pos, y_pos, state):
        if x_pos > 3:
            return False
        
        if y_pos > 2:
            return False

        if not self.is_goal(state[x_pos][y_pos]):
            return False
        if not self.is_goal(state[x_pos+1][y_pos]):
            return False
        if not self.is_goal(state[x_pos][y_pos+1]):
            return False
        if not self.is_goal(state[x_pos+1][y_pos+1]):
            return False
        
        return True
    #END

    ## return True if movement is valid, else return False
    ## if valid, store new game state in self.next_game_state
    ## direction can be "up", "down", "left", "right"
    def move(self, x_pos, y_pos, direction, state):
        self.next_game_state = copy.deepcopy(state)

        s = state[x_pos][y_pos]

        if self.is_empty(s):
            return False
        elif self.is_single_square(s):
            if direction == "up":
                if x_pos == 0:
                    return False
                if not self.is_empty(state[x_pos-1][y_pos]):
                    return False

                self.next_game_state[x_pos-1][y_pos] = state[x_pos][y_pos]
                self.next_game_state[x_pos][y_pos]   = "0"

                return True
            elif direction == "down":
                if x_pos == 4:
                    return False
                if not self.is_empty(state[x_pos+1][y_pos]):
                    return False

                self.next_game_state[x_pos+1][y_pos] = state[x_pos][y_pos]
                self.next_game_state[x_pos][y_pos]   = "0"

                return True
            elif direction == "left":
                if y_pos == 0:
                    return False
                if not self.is_empty(state[x_pos][y_pos-1]):
                    return False

                self.next_game_state[x_pos][y_pos-1] = state[x_pos][y_pos]
                self.next_game_state[x_pos][y_pos]   = "0"

                return True
            elif direction == "right":
                if y_pos == 3:
                    return False
                if not self.is_empty(state[x_pos][y_pos+1]):
                    return False

                self.next_game_state[x_pos][y_pos+1] = state[x_pos][y_pos]
                self.next_game_state[x_pos][y_pos]   = "0"

                return True
            else:
                self.error(direction + " not a valid direction")
        elif self.is_rectangle(s):
            if not self.valid_rectangle_position(x_pos, y_pos, state):
                return False
            
            if direction == "up":
                if x_pos == 0:
                    return False
                if not self.is_empty(state[x_pos-1][y_pos]):
                    return False

                self.next_game_state[x_pos-1][y_pos] = state[x_pos][y_pos]
                self.next_game_state[x_pos+1][y_pos] = "0"

                return True
            elif direction == "down":
                if x_pos == 3:
                    return False
                if not self.is_empty(state[x_pos+2][y_pos]):
                    return False

                self.next_game_state[x_pos+2][y_pos] = state[x_pos][y_pos]
                self.next_game_state[x_pos][y_pos]   = "0"

                return True
            elif direction == "left":
                if y_pos == 0:
                    return False
                
                if not self.is_empty(state[x_pos][y_pos-1]):
                    return False
                if not self.is_empty(state[x_pos+1][y_pos-1]):
                    return False
                
                self.next_game_state[x_pos][y_pos-1]   = state[x_pos][y_pos]
                self.next_game_state[x_pos+1][y_pos-1] = state[x_pos][y_pos]
                self.next_game_state[x_pos][y_pos]   = "0"
                self.next_game_state[x_pos+1][y_pos]   = "0"

                return True
            elif direction == "right":
                if y_pos == 3:
                    return False
                
                if not self.is_empty(state[x_pos][y_pos+1]):
                    return False
                if not self.is_empty(state[x_pos+1][y_pos+1]):
                    return False
                
                self.next_game_state[x_pos][y_pos+1]   = state[x_pos][y_pos]
                self.next_game_state[x_pos+1][y_pos+1] = state[x_pos][y_pos]
                self.next_game_state[x_pos][y_pos]   = "0"
                self.next_game_state[x_pos+1][y_pos]   = "0"

                return True
            else:
                self.error(direction + " not a valid direction")
        elif self.is_horizontal_rectangle(s):
            if not self.valid_horizontal_position(x_pos, y_pos, state):
                return False
            
            if direction == "left":
                if y_pos == 0:
                    return False
                if not self.is_empty(state[x_pos][y_pos-1]):
                    return False

                self.next_game_state[x_pos][y_pos-1] = state[x_pos][y_pos]
                self.next_game_state[x_pos][y_pos+1] = "0"

                return True
            elif direction == "right":
                if y_pos == 2:
                    return False
                if not self.is_empty(state[x_pos][y_pos+2]):
                    return False

                self.next_game_state[x_pos][y_pos+2] = state[x_pos][y_pos]
                self.next_game_state[x_pos][y_pos]   = "0"

                return True
            elif direction == "up":
                if x_pos == 0:
                    return False
                
                if not self.is_empty(state[x_pos-1][y_pos]):
                    return False
                if not self.is_empty(state[x_pos-1][y_pos+1]):
                    return False
                
                self.next_game_state[x_pos-1][y_pos]  = state[x_pos][y_pos]
                self.next_game_state[x_pos-1][y_pos+1] = state[x_pos][y_pos]
                self.next_game_state[x_pos][y_pos]   = "0"
                self.next_game_state[x_pos][y_pos+1]   = "0"

                return True
            elif direction == "down":
                if x_pos == 4:
                    return False
                
                if not self.is_empty(state[x_pos+1][y_pos]):
                    return False
                if not self.is_empty(state[x_pos+1][y_pos+1]):
                    return False
                
                self.next_game_state[x_pos+1][y_pos]   = state[x_pos][y_pos]
                self.next_game_state[x_pos+1][y_pos+1] = state[x_pos][y_pos]
                self.next_game_state[x_pos][y_pos]   = "0"
                self.next_game_state[x_pos][y_pos+1]   = "0"

                return True
            else:
                self.error(direction + " not a valid direction")
        elif self.is_goal(s):
            if not self.valid_goal_position(x_pos, y_pos, state):
                return False
            
            if direction == "up":
                if x_pos == 0:
                    return False
                if not self.is_empty(state[x_pos-1][y_pos]):
                    return False
                
                if not self.is_empty(state[x_pos-1][y_pos+1]):
                    return False

                self.next_game_state[x_pos-1][y_pos]   = "A"
                self.next_game_state[x_pos-1][y_pos+1] = "A"
                self.next_game_state[x_pos+1][y_pos]   = "0"
                self.next_game_state[x_pos+1][y_pos+1] = "0"

                return True
            elif direction == "down":
                if x_pos == 3:
                    return False
                if not self.is_empty(state[x_pos+2][y_pos]):
                    return False
                
                if not self.is_empty(state[x_pos+2][y_pos+1]):
                    return False

                self.next_game_state[x_pos+2][y_pos]   = "A"
                self.next_game_state[x_pos+2][y_pos+1] = "A"
                self.next_game_state[x_pos][y_pos]     = "0"
                self.next_game_state[x_pos][y_pos+1]   = "0"

                return True
            elif direction == "left":
                if y_pos == 0:
                    return False
                if not self.is_empty(state[x_pos][y_pos-1]):
                    return False
                
                if not self.is_empty(state[x_pos+1][y_pos-1]):
                    return False

                self.next_game_state[x_pos][y_pos-1]   = "A"
                self.next_game_state[x_pos+1][y_pos-1] = "A"
                self.next_game_state[x_pos][y_pos+1]   = "0"
                self.next_game_state[x_pos+1][y_pos+1] = "0"

                return True
            elif direction == "right":
                if y_pos == 2:
                    return False
                if not self.is_empty(state[x_pos][y_pos+2]):
                    return False
                
                if not self.is_empty(state[x_pos+1][y_pos+2]):
                    return False

                self.next_game_state[x_pos][y_pos+2]   = "A"
                self.next_game_state[x_pos+1][y_pos+2] = "A"
                self.next_game_state[x_pos][y_pos]     = "0"
                self.next_game_state[x_pos+1][y_pos]   = "0"

                return True
            else:
                self.error(direction + " not a valid direction")
        elif self.is_empty(s):
            return False
        else:
            self.error("program has bug")

    def success(self, state):
        return self.valid_goal_position(3, 1, state)
    #END

    def print_path(self, path):
        for state in path:
            self.print_game_state(state)
            print("---------------")

    def find_solution(self):
        angle = 0

        while not self.o_queue.empty():
            path = self.o_queue.get()

        path = []
        path.append(copy.deepcopy(self.current_game_state))
        
        self.o_queue.put(path)

        self.draw_loading_icon(angle)
        angle = (angle + 10) % 360

        while not self.o_queue.empty():
            path = self.o_queue.get()

            #print("new Branch Found")
            #self.print_game_state(path[-1])

            self.current_game_state = copy.deepcopy(path[-1])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.path = []
                    return
            
            self.draw_loading_icon(angle)
            angle = (angle + 10) % 360

            for x_pos in range(5):
                for y_pos in range(4):
                    for direction in ["left", "right", "up", "down"]:
                        current_x_pos = x_pos
                        current_y_pos = y_pos

                        state = copy.deepcopy(self.current_game_state)

                        while self.move(current_x_pos, current_y_pos, direction, state):
                            if not self.running:
                                self.path = []
                                return
                            #print("Movement")
                            #print("{} {} {}".format(str(x_pos), str(y_pos), direction))
                            if self.success(self.next_game_state):
                                self.current_game_state = copy.deepcopy(self.next_game_state)
                                path.append(self.next_game_state)
                                self.path = copy.deepcopy(path)

                                return 
                            
                            if not self.convert_to_string(self.next_game_state) in self.visited:
                                self.visited[self.convert_to_string(self.next_game_state)] = True
                                path.append(self.next_game_state)
                                self.o_queue.put(copy.deepcopy(path))
                                path.pop()
                        
                            if direction == "left":
                                current_y_pos -= 1
                            elif direction == "right":
                                current_y_pos += 1
                            elif direction == "up":
                                current_x_pos -= 1
                            elif direction == "down":
                                current_x_pos += 1 
                            
                            state = copy.deepcopy(self.next_game_state)
                    #END
                #END
            #END
        #END

        return
#END


if __name__ == "__main__":
    o_solution = Solution()
