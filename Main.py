import pygame, random

rules = {
	"blank" : [[0, 4],    [0, 3],    [0, 1],    [0, 2]], 
	"down"  : [[0, 4],    [1, 2, 4], [2, 3, 4], [1, 3, 4]],
	"left"  : [[1, 2, 3], [0, 3],    [2, 3, 4], [1, 3, 4]], 
	"right" : [[1, 2, 3], [1, 2, 4], [2, 3, 4], [0, 2]], 
	"up"    : [[1, 2, 3], [1, 2, 4], [0, 1],    [1, 3, 4]]	
}

SIZE = 500
DIM = 20
CELL_SIZE = SIZE//DIM

# loading and resizing the images
images_name = ["blank", "down", "left", "right", "up"]
images = [pygame.image.load("Tiles/Demo/"+name+".png") for name in images_name]
images = [pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE)) for img in images]


screen = pygame.display.set_mode((SIZE, SIZE))

class Cell:

	def __init__(self, i):

		self.collapsed = False

		self._options = [0, 1, 2, 3, 4]

		self.pos = i%DIM, i//DIM

	def show(self):

		screen.blit(self.img, (self.pos[0] * CELL_SIZE, self.pos[1] * CELL_SIZE))

	@property
	def options(self):

		return self._options

	@options.setter
	def options(self, val):

		self._options = val

		# if the cell is collapsed load the image correspoding to it's entropy
		if len(self._options) == 1:

			self.collapsed = True

			self.img = images[self.options[0]]

			self.rules = rules[images_name[self.options[0]]]


def update_options(opt_1, opt_2):

	"""function that take out the option not appearing on both lists"""

	updated_options = []
	for elem in opt_1:
		if elem not in opt_2:
			continue

		updated_options.append(elem)

	return updated_options

grid = [Cell(i) for i in range(DIM*DIM)]

done = False
stop = False
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True 
	if not stop:
		screen.fill((120, 120, 120))
		for cell in grid:
			if cell.collapsed:
				cell.show()

		sorted_grid = sorted(grid, key = lambda x: len(x.options))

		#pick the cell with the least entropy and collapse it
		sorted_grid = [elem for elem in sorted_grid if not elem.collapsed]
		try:
			choosen_cell = random.choice([obj for obj in sorted_grid if len(obj.options) == len(sorted_grid[0].options)])

		except IndexError:
			print(sorted_grid)
			stop = True

		choosen_cell.options = [random.choice(choosen_cell.options)]

		# updating the entropy of the grid accordingly to the last collapsed cell
		for j in range(DIM):
			for i in range(DIM):
				index = i + j * DIM
				if not grid[index].collapsed: 
					
					# checking if the neighbors cell are collapsed if so updating the entropy accordingly
					# up
					if j > 0:
						if grid[i + (j - 1) * DIM].collapsed:
							grid[index].options = update_options(grid[index].options, grid[i + (j - 1) * DIM].rules[2])

					#right
					if i < DIM-1:
						if grid[i + 1 + j * DIM].collapsed:
							grid[index].options = update_options(grid[index].options, grid[i + j * DIM + 1].rules[3])

					#down
					if j < DIM-1:
						if grid[i + (j + 1) * DIM].collapsed:
							grid[index].options = update_options(grid[index].options, grid[i + (j + 1) * DIM].rules[0])

					#left
					if i > 0:
						if grid[i - 1 + j * DIM].collapsed:
							grid[index].options = update_options(grid[index].options, grid[i + j * DIM - 1].rules[1])

		# print(*[(obj.pos, obj.options, obj.collapsed) for obj in sorted_grid], sep = "\n")


	pygame.display.flip()
	# pygame.time.wait(100)