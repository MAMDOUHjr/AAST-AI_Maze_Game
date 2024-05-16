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
POPUP_COLOR = (255, 255, 255)  # White color for popup messages
POPUP_BG_COLOR = (0, 0, 0)      # Black color for background of popup messages
POPUP_DURATION = 2000 
MARGIN_TOP = 50
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")


RED = [55, 0, 0]
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

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[(self.row+1) * ROWS + self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[(self.row+1) * ROWS + self.col])

        if self.row > 0 and not grid[(self.row -1)* ROWS+ self.col].is_barrier():  # UP
            self.neighbors.append(grid[(self.row-1) * ROWS+ self.col])

        if self.col < self.total_rows - 1 and not grid[self.row * ROWS +(1 + self.col)].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row * ROWS +(1 + self.col)])

        if self.col > 0 and not grid[self.row *ROWS+(self.col-1)].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row*ROWS+(self.col-1)])

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
    pygame.draw.rect(WIN, POPUP_BG_COLOR, text_rect)  # Draw background rectangle for the message
    WIN.blit(text, text_rect)                         # Draw the message text
    pygame.display.update()                           # Update the display
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


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        row.draw(win)

    draw_grid(win, rows, width)

    pygame.display.update()


def save_path(path, file_name):
    with open(file_name, 'w') as file:
        json.dump(path, file)

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


def load_maze(file_name):
    try:
        with open(file_name, 'r') as file:
            maze_data = json.load(file)
        return maze_data
    except FileNotFoundError:
        return None


def save_maze(grid, file_name, run_id = 1):
    file_name = f'maze{run_id}.json'

    maze = load_maze(file_name)
    new_maze = []

    for row in grid:
        new_maze.append((row.row, row.col, row.color))

    if maze:
        maze.extend(new_maze)
    else:
        maze = new_maze

    with open(file_name, 'w') as file:
        json.dump(maze, file)


def main(win, width):
    maze_id = random.randint(1, 3)  # Assuming you have 5 maze files
    maze_data = load_maze(f"maze{maze_id}.json")
    grid = make_grid(ROWS, width, maze_data)
    display_popup_message("Player 1, it's your turn!") 
    player_turn = 1
    player1_path = []  # Define player1_path
    player2_path = []  # Define player2_path
    game_over = False
    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0] and not game_over:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row * ROWS + col]
                if player_turn == 1:
                    if spot.color == WHITE:
                        spot.make_player1()
                        player1_path.append((row, col))
                else:
                    if spot.color == WHITE:
                        spot.make_player2()
                        player2_path.append((row, col))

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row * ROWS + col]
                spot.reset()

            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_RETURN:
                    if player_turn == 1:
                        save_path(player1_path, "player1_path.json")
                        display_popup_message("Player 2, it's your turn!") 
                        player_turn = 2
                    else:
                        save_path(player2_path, "player2_path.json")
                        display_popup_message("Game Over!") 
                        game_over = True
                    player1_path = []   
                    player2_path = []
                    for row in grid:
                        row.reset() 
                    grid = make_grid(ROWS, width, maze_data)

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


    pygame.quit()

main(WIN, WIDTH)
