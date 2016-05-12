#Import packages
import pygame
from random import randint
import numpy  as np

import block
import grid
from user_const import *



#A Piece is a list of coordinates of blocks arranged in its proper location to form a Tetromino
#It's type determine's the arrangement of blocks

class Piece():
	def __init__(self, grid, piece_type = RANDOM, loc=(5,0), orient = 0):
		#self.side_length = side_length #Sets the block's side length
		self.loc = loc

		if(piece_type == RANDOM):
			self.type = randint(1,7) 
		else: self.type = piece_type #Sets the piece type
		self.grid = grid 
		self.list_of_blocks = []
		self.list_of_coords = []

		#Keep track of neighboring blocks
		self.neighbor_down = []
		self.neighbor_right = []
		self.neighbor_left = [] 

		self.fixed = False
		self.arrange_blocks()
	
	'''
	Set functions
	'''
	def set_fixed(self, fixed):
		self.fixed = fixed
		for i in self.list_of_coords:
			block = self.grid.get_block(i)
			block.set_fixed(fixed)

	def set_type(self, piece_type):
		self.type = piece_type
		for i in self.list_of_coords:
			self.grid.get_block(i).set_type(piece_type)

	def set_loc(self):
		self.loc = self.list_of_coords[0]

	#For each piece, get the list of neighbor blocks to check whether or not the piece has hit another fixed block
	def set_neighbor_coords(self):
		self.reset_neighbors()
		for i in self.list_of_coords:
			right_coord = (i[0]+1, i[1])
			down_coord = (i[0],i[1]+1)
			left_coord = (i[0]-1,i[1])
			self.get_neighbors(DIR_RIGHT).append(self.grid.get_valid_coord(right_coord))
			self.get_neighbors(DIR_DOWN).append(self.grid.get_valid_coord(down_coord))
			self.get_neighbors(DIR_LEFT).append(self.grid.get_valid_coord(left_coord))
		return True

	def reset_blocks(self):
		self.fixed = False
		for i in self.list_of_coords:
			self.grid.get_block(i).reset()
		self.list_of_coords = []

	def reset_neighbors(self):
		self.neighbor_down = []
		self.neighbor_left = []
		self.neighbor_right = []

	'''
	Get functions
	'''
	def get_coords(self):
		return self.list_of_coords

	def get_center(self):
		#Changes the center block based on the shape of the piece. So ensures that the pieces are rotating in a 3X3 box
		if (self.type == T or self.type == L2 or self.type == L1): return self.list_of_coords[1]
		elif(self.type == S1): return self.list_of_coords[0]
		return (self.list_of_coords[2])

	def get_type(self):
		return self.type

	def get_x(self):
		return self.list_of_blocks[0].get_x()
	def get_y(self):
		return self.list_of_blocks[0].get_y()

	def get_neighbors(self, direction):
		if(direction == DIR_DOWN): return self.neighbor_down
		if(direction == DIR_LEFT): return self.neighbor_left
		if(direction == DIR_RIGHT): return self.neighbor_right


	'''
	Comparison functions
	'''

	def is_fixed(self):
		return self.fixed

	def is_valid_neighbors(self, coords):
		for i in coords:
			if i == OUT_OF_BOUNDS: return False
		for i in coords:
			if(self.grid.get_block(i).is_fixed()): return False
		return True

	'''
	Utility functions
	'''

	#Arranges the blocks within each piece so it looks like the intended piece on the grid
	def arrange_blocks(self, list_of_coords=DEFAULT):
		self.reset_blocks()
		#Appends the correct blocks for initializing piece

		#Arranges blocks from scratch is the list of blocks is empty
		if(list_of_coords==DEFAULT):

		#DEFAULT PIECE ARRANGEMENT
			if(self.type == STICK):
				self.list_of_coords.append((self.loc[0], self.loc[1]))
				self.list_of_coords.append((self.loc[0], self.loc[1]+1))
				self.list_of_coords.append((self.loc[0], self.loc[1]+2))
				self.list_of_coords.append((self.loc[0], self.loc[1]+3))

			elif(self.type == SQUARE):
				self.list_of_coords.append((self.loc[0], self.loc[1]))
				self.list_of_coords.append((self.loc[0], self.loc[1]+1))
				self.list_of_coords.append((self.loc[0]+1, self.loc[1]))
				self.list_of_coords.append((self.loc[0]+1, self.loc[1]+1))

			elif(self.type == S1):
				self.list_of_coords.append((self.loc[0], self.loc[1]))
				self.list_of_coords.append((self.loc[0]+1, self.loc[1]))
				self.list_of_coords.append((self.loc[0]-1, self.loc[1]+1))
				self.list_of_coords.append((self.loc[0], self.loc[1]+1))
				

			elif(self.type == S2):
				self.list_of_coords.append((self.loc[0], self.loc[1]))
				self.list_of_coords.append((self.loc[0]+1, self.loc[1]))
				self.list_of_coords.append((self.loc[0]+1, self.loc[1]+1))
				self.list_of_coords.append((self.loc[0]+1, self.loc[1]+2))

			elif(self.type == T):
				self.list_of_coords.append((self.loc[0], self.loc[1]))
				self.list_of_coords.append((self.loc[0], self.loc[1]+1))
				self.list_of_coords.append((self.loc[0]+1, self.loc[1]+1))
				self.list_of_coords.append((self.loc[0]-1, self.loc[1]+1))

			elif(self.type == L1):
				self.list_of_coords.append((self.loc[0], self.loc[1]))
				self.list_of_coords.append((self.loc[0], self.loc[1]+1))
				self.list_of_coords.append((self.loc[0], self.loc[1]+2))
				self.list_of_coords.append((self.loc[0]+1, self.loc[1]+2))
			
			elif(self.type == L2):
				self.list_of_coords.append((self.loc[0], self.loc[1]))
				self.list_of_coords.append((self.loc[0], self.loc[1]+1))
				self.list_of_coords.append((self.loc[0], self.loc[1]+2))
				self.list_of_coords.append((self.loc[0]-1, self.loc[1]+2))

		#If the piece is supplied with the list of blocks, set the new list of coords with the input
		elif(list_of_coords!= DEFAULT):
			self.list_of_coords = list_of_coords
			
		#Set the type for the individual blocks in this piece
		for i in self.list_of_coords:
			self.grid.get_block(i).set_type(self.type)
		
		self.set_loc()
		self.set_neighbor_coords()

	#Rotates the piece in the direction specified, and rearranges the block
	def rotate(self, direction):
		if(self.type == SQUARE): return True
		center = self.get_center()
		rotated_coord = []
		for i in self.list_of_coords:
			centered_i = np.subtract(i, center)
			if(direction == CLOCKWISE):
				temp_coord = (centered_i[1]*-1,centered_i[0])
			elif(direction == COUNTER):
				temp_coord = (centered_i[1],centered_i[0]*-1)
			rotated_coord.append((temp_coord[0]+center[0],temp_coord[1]+center[1]))
		
		#Check whether the rotated the block is out of bounds of is overlapping with a fixed block
		for i in rotated_coord:
			temp_coord = self.grid.get_valid_coord(i)
			if(temp_coord == OUT_OF_BOUNDS): return False
			if(self.grid.get_block(temp_coord).is_fixed()): return False

		#If it passes the test then rearrange this block
		self.arrange_blocks(rotated_coord)
		return True
	
	#Moves the piece in the given direction. 
	#A move is DONE when it moves down and hits the bottom row or it collides with an existing fixed block
	#A move is VALID when it does not collide with anything

	def move(self, direction, spaces=1):
		move_list_of_coords = []

		#Move in chosen direction
		#Check for fixed blocks in that direction
		if(direction == DIR_DOWN):
			if(self.is_valid_neighbors(self.get_neighbors(direction))==False):
				self.set_fixed(True)
				return DONE

		elif(direction == DIR_LEFT or direction == DIR_RIGHT):
			if(self.is_valid_neighbors(self.get_neighbors(direction))==False):
				return INVALID

		#Set move direction to the neighbor direction
		move_list_of_coords = self.get_neighbors(direction)
		self.arrange_blocks(move_list_of_coords)
		return VALID

	#Moving the piece down, until it hits something. Then checks whether a row needs to be cleared
	def dropdown(self):
		#Check if a row needs to be cleared
		if(self.move(DIR_DOWN)==DONE): 
			return (self.grid.clear_rows())

	def __str__(self):
		ret_str = "Piece type: " + str(self.type) + "\n"
		ret_str += str(self.list_of_coords)
		return ret_str