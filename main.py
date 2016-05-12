'''
May 11, 2016

This is my attempt to recreate the game of tetri using python and pygame

'''

#Included packages
import pygame

#User defined classes
import grid
import piece
import block
from user_const import *


def main():
	done = False
	pygame.init()
	# Used to manage how fast the screen updates
	clock = pygame.time.Clock()
	# Set the height and width of the screen
	screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
	logo = pygame.image.load(image_folder+LOGO_IMAGE).convert()
	#logo = pygame.transform.scale(logo, (int(self.width), int(self.height)))

	#Initialize Main Game Grid
	game_grid = grid.Grid(GRID_COLS, GRID_ROWS, int((SCREEN_HEIGHT-GRID_BORDER)/GRID_ROWS), BLACK, [GRID_START_X, GRID_BORDER/2])

	#Initialize Preview Game Grid
	preview_grid = grid.Grid(4, 4, int((SCREEN_HEIGHT-GRID_BORDER)/GRID_ROWS), BLACK, [GRID_START_X_SMALL, GRID_BORDER/2])
	#Initialize Starting Piece
	game_piece = piece.Piece(game_grid)
	preview_piece = piece.Piece(preview_grid, loc=[1,0])

	while not done:

		#Check if game is over
		# Clear the screen
		screen.fill(BLACK)
		screen.blit(logo, LOGO_POS)

		game_grid.display_text(game_grid.small_text, "High score: {}".format(game_grid.get_highscore()), (50,150), screen)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					game_piece.move(DIR_LEFT)
				elif event.key == pygame.K_RIGHT:
					game_piece.move(DIR_RIGHT)
				elif event.key == pygame.K_DOWN:
					game_piece.move(DIR_DOWN)
				elif event.key == pygame.K_a:
					game_piece.rotate(COUNTER)
				elif event.key == pygame.K_d:
					game_piece.rotate(CLOCKWISE)
				elif event.key == pygame.K_n:
					game_piece.reset_blocks()
					game_piece = piece.Piece(game_grid)
				elif event.key == pygame.K_SPACE:
					print "Pause"
					game_grid.pause(pygame, screen)
					
		drop_loop = game_piece.dropdown()

		if(drop_loop == DONE):
			if(game_grid.is_game_over(screen)): 
				game_grid.reset_game()

				print ("Game over")
			#If game over, reset the game grid, using next piece.Piece as preview piece
			game_piece = piece.Piece(game_grid, preview_piece.get_type())
			preview_piece.reset_blocks()
			preview_piece = piece.Piece(preview_grid, loc=[1,0])

		preview_grid.draw_blocks(screen)
		game_grid.draw_blocks(screen)

		# Go ahead and update the screen with what we've drawn.
		pygame.display.flip()

		# Set frames per second
		clock.tick(3+game_grid.get_highscore())
		
	pygame.quit()

if __name__ == "__main__":
	main()
