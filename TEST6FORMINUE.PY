import pygame
import math
from queue import PriorityQueue
import json
import os
import random

pygame.init()
WIDTH = 800
ROWS = 20
POPUP_FONT_SIZE = 50
POPUP_COLOR = (255, 255, 255)
POPUP_BG_COLOR = (0, 0, 0)
POPUP_DURATION = 2000
MARGIN_TOP = 50
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
YELLOW = [255, 255, 0]
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
PURPLE = [128, 0, 128]
ORANGE = [255, 165, 0]
GREY = [128, 128, 128]
TURQUOISE = [64, 224, 208]

class Spot:
    def __init__(self, row, col, width, total_rows, color):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = color
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def make_player1(self):
        self.color = BLUE
    
    def make_player2(self):
        self.color = YELLOW

    def draw(self, win, current=False):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        if current:
            pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.width), 3)  # Red border for current spot

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[(self.row + 1) * ROWS + self.col].is_barrier():
            self.neighbors.append(grid[(self.row + 1) * ROWS + self.col])

        if self.row > 0 and not grid[(self.row - 1) * ROWS + self.col].is_barrier():
            self.neighbors.append(grid[(self.row - 1) * ROWS + self.col])

        if self.col < self.total_rows - 1 and not grid[self.row * ROWS + (1 + self.col)].is_barrier():
            self.neighbors.append(grid[self.row * ROWS + (1 + self.col)])

        if self.col > 0 and not grid[self.row * ROWS + (self.col - 1)].is_barrier():
            self.neighbors.append(grid[self.row * ROWS + (self.col - 1)])

    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def display_popup_message(message):
    font = pygame.font.SysFont(None, POPUP_FONT_SIZE)
    text = font.render(message, True, POPUP_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, MARGIN_TOP // 2))
    pygame.draw.rect(WIN, POPUP_BG_COLOR, text_rect)
    WIN.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(POPUP_DURATION)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {row: float("inf") for row in grid}
    g_score[start] = 0
    f_score = {row: float("inf") for row in grid}
    f_score[start] = h(start.get_pos(), end.get_pos())
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def make_grid(rows, width, maze_data):
    grid = []
    gap = width // rows
    for row, col, color in maze_data:
        spot = Spot(row, col, gap, rows, color)
        grid.append(spot)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width, current_spot=None):
    if pygame.display.get_surface() is not None:  
        win.fill(WHITE)
        for spot in grid:
            spot.draw(win, current=spot == current_spot)

        draw_grid(win, rows, width)

        pygame.display.update()



def save_path(path, file_name):
    with open(file_name, 'w') as file:
        json.dump(path, file)


def load_maze(file_name):
    try:
        with open(file_name, 'r') as file:
            maze_data = json.load(file)
        return maze_data
    except FileNotFoundError:
        return None

def main(win, width):
    player1 = 0
    player2 = 0
    with open('player1_path.json', 'w') as file:
        pass 
    with open('player2_path.json', 'w') as file:
        pass
    maze_id = random.randint(1, 3)
    maze_data = load_maze(f"maze{maze_id}.json")
    grid = make_grid(ROWS, width, maze_data)
    display_popup_message("Player 1, it's your turn!")
    player_turn = 1
    player1_path = []
    player2_path = []
    game_over = False
    run = True

    start_spot = None
    end_spot = None

    for spot in grid:
        if spot.is_start():
            start_spot = spot
        elif spot.is_end():
            end_spot = spot

    current_spot = start_spot

    while run:
        draw(win, grid, ROWS, width, current_spot)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if current_spot.row > 0:
                            new_spot = grid[(current_spot.row - 1) * ROWS + current_spot.col]
                            if new_spot.color != BLACK:
                                current_spot = new_spot
                                if player_turn == 1:
                                        if current_spot.color != BLUE:
                                            current_spot.make_player1()
                                            player1_path.append(current_spot.get_pos())
                                else:
                                    if current_spot.color != YELLOW:
                                        current_spot.make_player2()
                                        player2_path.append(current_spot.get_pos())
                    elif event.key == pygame.K_RIGHT:
                        if current_spot.row < ROWS - 1:
                            new_spot = grid[(current_spot.row + 1) * ROWS + current_spot.col]
                            if new_spot.color != BLACK:
                                current_spot = new_spot
                                if player_turn == 1:
                                        if current_spot.color != BLUE:
                                            current_spot.make_player1()
                                            player1_path.append(current_spot.get_pos())
                                else:
                                    if current_spot.color != YELLOW:
                                        current_spot.make_player2()
                                        player2_path.append(current_spot.get_pos())
                    elif event.key == pygame.K_UP:
                        if current_spot.col > 0:
                            new_spot = grid[current_spot.row * ROWS + (current_spot.col - 1)]
                            if new_spot.color != BLACK:
                                current_spot = new_spot
                                if player_turn == 1:
                                        if current_spot.color != BLUE:
                                            current_spot.make_player1()
                                            player1_path.append(current_spot.get_pos())
                                else:
                                    if current_spot.color != YELLOW:
                                        current_spot.make_player2()
                                        player2_path.append(current_spot.get_pos())
                    elif event.key == pygame.K_DOWN:
                        if current_spot.col < ROWS - 1:
                            new_spot = grid[current_spot.row * ROWS + (current_spot.col + 1)]
                            if new_spot.color != BLACK:
                                current_spot = new_spot
                                if player_turn == 1:
                                        if current_spot.color != BLUE:
                                            current_spot.make_player1()
                                            player1_path.append(current_spot.get_pos())
                                else:
                                    if current_spot.color != YELLOW:
                                        current_spot.make_player2()
                                        player2_path.append(current_spot.get_pos())
                    elif event.key == pygame.K_x: 
                        current_spot.reset()
                        item_to_remove = current_spot.get_pos()
                        if player_turn == 1:
                            player1_path.remove(item_to_remove)
                        else:
                            player2_path.remove(item_to_remove)

                  
              
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if current_spot.x == end_spot.x and current_spot.y == end_spot.y:    
                        if player_turn == 1:
                            save_path((player1_path), "player1_path.json")
                            display_popup_message("Player 2, it's your turn!")
                            player_turn = 2
                            current_spot = start_spot 
                            game_over = False
                        else:

                            save_path(list(set(player2_path)), "player2_path.json")
                            display_popup_message("Game Over!")
                            game_over = True
                        player1_path = []
                        player2_path = []
                        for spot in grid:
                            spot.reset()
                        grid = make_grid(ROWS, width, maze_data)

                        # print("end spot  = " , end_spot.x, end_spot.y)
                    else:
                        # print("end spot  = " , end_spot.x, end_spot.y)
                        # print ("current spot = ", current_spot.x, current_spot.y)
                        display_popup_message("Invalid Moves!")        
                        
        if game_over:
            start = None
            end = None
            for spot in grid:
                if spot.is_start():
                    start = spot
                elif spot.is_end():
                    end = spot
            if start and end:
                for row in grid:
                    row.update_neighbors(grid)
                algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
        
                            
    if(game_over):                                  
        player1_path_data= load_maze("player1_path.json")
        player2_path_data = load_maze("player2_path.json")
    else:
        player1_path_data = []
        player2_path_data = []
    if player1_path_data:
            for row in player1_path_data:
                if (grid[row[0]*ROWS+row[1]]).color==PURPLE:
                        player1 += 1
                    
                    
    if player2_path_data:
            for row in player2_path_data:
                if (grid[row[0]*ROWS+row[1]]).color==PURPLE:
                            player2 += 1
  
    pl1=player1-len(player1_path_data)
    pl2=player2-len(player2_path_data)

    win.fill(WHITE)
    if pl1 > pl2:
        display_popup_message("Player 1 wins!")
    elif pl2 > pl1:
        display_popup_message("Player 2 wins!")
    else:
        display_popup_message("It's a tie!")

    pygame.quit()
 
if __name__ == "__main__":
    main(WIN, WIDTH)