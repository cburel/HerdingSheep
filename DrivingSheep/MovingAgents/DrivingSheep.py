import pygame
from pygame.locals import *
import Constants
import random
from Enemy import Sheep
from Player import Dog

#initialize pygame
pygame.init()

#setup
screen = pygame.display.set_mode((Constants.DISPLAY_WIDTH, Constants.DISPLAY_HEIGHT))
dogImage = pygame.image.load('dog.png')
sheepImage = pygame.image.load('sheep.png')

player = Dog(dogImage, pygame.Vector2(Constants.PLAYER_XPOS, Constants.PLAYER_YPOS), (Constants.PLAYER_SIZE), Constants.PLAYER_SPD, Constants.PLAYER_COLOR, Constants.PLAYER_TURN_SPEED)
bounds = pygame.Vector2(Constants.DISPLAY_WIDTH, Constants.DISPLAY_HEIGHT)

enemies = []
for i in range (1, Constants.MAX_ENEMIES + 1):
	enemies.append(Sheep(sheepImage, pygame.Vector2(random.randrange(0, bounds.x), random.randrange(0, bounds.y)), Constants.ENEMY_SIZE, Constants.ENEMY_SPD, Constants.ENEMY_COLOR, Constants.ENEMY_TURN_SPEED))

#main gameplay loop
hasQuit = False
while not hasQuit:

	# event handler
	for event in pygame.event.get():

		#quit the game
		if event.type == QUIT:
			hasQuit = True
				
	#make screen cornflower blue
	screen.fill(Constants.BACKGROUND_COLOR)
	
	#update the agents
	targetEnemy = player.update(bounds, screen, enemies)
	for enemy in enemies:
		enemy.update(bounds, screen, player)

	#draw the agents
	player.draw(screen)
	for enemy in enemies:
		enemy.draw(screen)

	#detect player-enemy tag
	if player.isInCollision(targetEnemy):
		player.swapTarget(enemies)
	
	#flip display buffer
	pygame.display.flip()

	#constrain to 60 fps
	Constants.CLOCK.tick(60)

#quit the game
pygame.quit()
quit()