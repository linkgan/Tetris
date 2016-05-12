#Import packages
import pygame

'''
User defined classes
'''
import block
import piece
from user_const import *


#The game grid where all the pieces will be aligned against
class Grid():
	def __init__(self, cols, rows, size, color, loc=[0,0],hs = 0):
		self.is_paused = False
		self.color = color
		self.loc = loc
		self.cols = cols
		self.rows = rows
		self.size = size
		#self.height = rows * size
		#self.width = cols * size
		self.list_of_blocks = []
		self.block_group = pygame.sprite.Group()
		self.high_score = hs

		self.large_text = pygame.font.SysFont("monospace",50)
		self.small_text = pygame.font.SysFont("monospace",25)

		#Initialize all empty blocks in their locations
		for j in range(rows):
			for i in range(cols):
				new_block = block.Block(self, [i, j])
				self.list_of_blocks.append(new_block)
				self.block_group.add(new_block)

	'''
	Set functions
	'''
	def reset_game(self):
		self.high_score = 0
		for i in self.list_of_blocks:
			i.reset()


	'''
	Get functions
	'''
	def get_image_coord(self, col_num, row_num):
		return [self.loc[0]+self.size * col_num, self.loc[1]+self.size*row_num]

	#Check if coord is within the valid range of coordinates. If not, return OUT_OF_BOUNDS
	def get_valid_coord(self,coord):
		if((0<= coord[0] < self.cols) and (0<= coord[1] < self.rows)):
			return coord
		return OUT_OF_BOUNDS

	#Returns the block based on its current location in grid
	#Or if block not found, return False
	def get_block(self, coord):
		#if(coord[0]>=self.rows or coord[1] >= self.cols or coord[0] <0 or coord[1] <0):
		#	return OUT_OF_BOUNDS
		for i in self.list_of_blocks:
			if(i.is_block(coord)): return i
		return False

	def get_dim(self):
		return [self.cols, self.rows]

	def get_cell_size(self):
		return self.size

	def get_highscore(self):
		return self.high_score


	'''
	Comparison functions
	'''

	#Check if the current block location is occupying an empty space on grid
	def is_empty(self, x, y):
		for i in self.list_of_blocks:
			if(i.get_x() == x and i.get_y()==y): 
				return False
			else: True


	def is_row_full(self, row):
		for i in range(self.cols):
			if(self.get_block((i,row)).is_fixed()==False): return False
		return True

	def is_game_over(self, screen):
		for i in range(self.cols):
			if(self.get_block((i,0)).is_fixed()):
				self.is_paused = True
				self.display_text(self.large_text, "Game Over SUCKER.", (SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2), screen)	
				self.display_text(self.large_text, "Press Y to continue", (SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2+50), screen)	
				pygame.display.flip()
				while(self.is_paused):
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							pygame.quit()
						elif event.type == pygame.KEYDOWN:
							if event.key == pygame.K_y:
								print "Game Continue"
								self.is_paused = False
				return True
		else: return False


	'''
	Utility functions
	'''

	#Make row above (row - 1) drop down
	def dropdown(self, row):
		#Reversing range so that it processes the bottom-est row first
		for j in reversed(range(row+1)):
			for i in range(self.cols):
				#Skip over the last row
				if(j>=1):
					block1 = self.get_block((i,j))
					block2 = self.get_block((i,j-1))
					block1.set_fixed(block2.get_fixed())
					block1.set_type(block2.get_type())
					block2.reset()

	def clear_rows(self):
		for i in range(self.rows):
			if(self.is_row_full(i)):
				self.high_score += 1
				print "High Score = "+str(self.high_score)	
				self.dropdown(i)
				i = 0 #Reset the iterator
		return DONE

	def pause(self, pygame, screen):
		self.is_paused = True
		self.display_text(self.large_text, "Game Paused", (SCREEN_WIDTH/2-50, SCREEN_HEIGHT/2), screen)
		pygame.display.flip()
		while(self.is_paused):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						print "Unpause"
						self.is_paused = False
		return True

	def display_text(self, pytext, text, location, screen):
		label = pytext.render(text, 1, WHITE)
		screen.blit(label,location)

	def draw_blocks(self, screen):
		for i in self.list_of_blocks:
			i.draw(screen)


