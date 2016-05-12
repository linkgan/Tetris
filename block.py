
#Included packages
import pygame

#User defined classes
import grid
from user_const import *

#Fundamental building block of Tetris. Each block is associated with its type
class Block(pygame.sprite.Sprite):
	def __init__(self, grid, loc=[0,0], block_type = DEFAULT):
		# Call the parent class (Sprite) constructor
		super(self.__class__, self).__init__()
		self.grid = grid
		self.loc = loc
		self.width = self.grid.get_cell_size()
		self.height = self.grid.get_cell_size()
		self.type = block_type
		self.fixed = False
		self.image_list = []
		
		#Sprite class
		#Initialize an array of images to use later
		for i in IMAGE_NAMES:
			temp_image = pygame.image.load(image_folder+i).convert()
			temp_image = pygame.transform.scale(temp_image, (int(self.width), int(self.height)))
			self.image_list.append(temp_image)

		self.image = self.image_list[DEFAULT]
		self.rect = self.image.get_rect()
        #Set location of block
		self.coord = self.grid.get_image_coord(self.loc[0], self.loc[1])
		self.rect.x = self.coord[0]
		self.rect.y = self.coord[1]

	'''
	Set functions
	'''

	def set_type(self, block_type):
		self.type = block_type
	def set_x_loc(self,x):
		self.loc[0] = x
	def set_y_loc(self,y):
		self.loc[1] = y
	def set_visible(self, vis):
		self.is_visible = vis
	def set_fixed(self, fixed):
		self.fixed = fixed

	#Resets the block back to default properties
	def reset(self):
		self.set_type(DEFAULT)
		self.set_fixed(False)
		self.is_visible = False

	'''
	Get functions
	'''
	def get_x(self):
		return self.loc[0]
	def get_y(self):
		return self.loc[1]
	def get_coord(self):
		return (self.loc)
	def get_type(self):
		return self.type
	def get_fixed(self):
		return self.fixed

	'''
	Comparison functions
	'''
	#Check if this is the block given the location
	def is_block(self,loc):
		if(self.loc[0] == loc[0] and self.loc[1] == loc[1]): 
			return True
		else: 
			return False

	def is_fixed(self):
		return self.fixed


	'''
	Utility functions
	'''

	def load_image(self):
		self.image = self.image_list[self.get_type()]
		self.image = pygame.transform.scale(self.image, (int(self.width)-2, int(self.height)-2))
		self.rect = self.image.get_rect()

	def draw(self, screen):
		self.load_image()
		self.coord = self.grid.get_image_coord(self.get_x(), self.get_y())
		self.rect.x = self.coord[0]
		self.rect.y = self.coord[1]
		screen.blit(self.image, (self.rect.x, self.rect.y))
