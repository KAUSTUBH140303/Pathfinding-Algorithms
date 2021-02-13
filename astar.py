import pygame, math, time
from queue import PriorityQueue

pygame.init()

## Global Variables
WIDTH = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
GREY = (100, 100, 100)


## Creating Window
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* ALGORITHM")


## CLASS PROPERTIES
class Node:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_visited(self):
		return self.color == YELLOW

	def is_open(self):
		return self.color == PURPLE

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == GREEN

	def is_end(self):
		return self.color == RED

	def reset(self):
		self.color = WHITE

	def make_closed(self):
		self.color = YELLOW

	def make_open(self):
		self.color = PURPLE

	def make_barrier(self):
		self.color = BLACK

	def make_start(self):
		self.color = GREEN

	def make_end(self):
		self.color = RED

	def make_path(self):
		self.color = BLUE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): ## DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): ## UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): ## RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): ## LEFT
			self.neighbors.append(grid[self.row][self.col - 1])
			

	def __lt__(self, other):
		return False


## Utility Functions
def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i, j, gap, rows)
			grid[i].append(node)
	return grid

def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
	for i in range(rows):
		pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, width))

def draw(win, grid, rows, width):
	win.fill(WHITE)
	for row in grid:
		for node in row:
			node.draw(win)
	draw_grid(win, rows, width)
	pygame.display.update()

def get_clicked_pos(pos, rows, width):
	gap = width // rows
	x, y = pos
	row = x // gap
	col = y // gap
	return row, col

def reconstructPath(prev, c, draw):
	while c in prev:
		c = prev[c]
		c.make_path()
		draw()

## ALGORITHM
def algorithm(draw, grid, start, end):
	count = 0
	opens = PriorityQueue()
	opens.put((0, count, start))
	prev = {}
	g = {node: float("inf") for row in grid for node in row}
	g[start] = 0
	f = {node: float("inf") for row in grid for node in row}
	f[start] = h(start.get_pos(), end.get_pos())
	opensHash = {start}
	while not opens.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		c = opens.get()[2]
		opensHash.remove(c)
		if c == end:
			reconstructPath(prev, end, draw)
			return True
		for neighbor in c.neighbors:
			temp = g[c] + 1
			if temp < g[neighbor]:
				prev[neighbor] = c
				g[neighbor] = temp
				f[neighbor] = temp + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in opensHash:
					count += 1
					opens.put((f[neighbor], count, neighbor))
					opensHash.add(neighbor)
					neighbor.make_open()
		draw()
		if c != start:
			c.make_closed()
		time.sleep(0.05)
	return False

## MAIN Function
def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)
	start = None
	end = None
	run = True
	started = False
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
			if started:
				continue
			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				node = grid[row][col]
				if not start and node != end:
					start = node
					start.make_start()
				elif not end and node != start:
					end = node
					end.make_end()
				elif node != end and node != start:
					node.make_barrier()
			elif pygame.mouse.get_pressed()[2]:
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				node = grid[row][col]
				node.reset()
				if node == start:
					start = None
				elif node == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and not started:
					for row in grid:
						for node in row:
							node.update_neighbors(grid)
					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
				



main(WIN, WIDTH)
