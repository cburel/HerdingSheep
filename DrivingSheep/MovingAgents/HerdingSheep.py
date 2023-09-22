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


def handleDebugging():        
	#Handle the Debugging for Forces
	events = pygame.event.get()
	for event in events:

		#if the player quits the game
		if event.type == QUIT:
			pygame.quit()
			quit()

		#if the player presses a debug key (1-0 on keyboard)
		if event.type == pygame.KEYUP:

			# Toggle Dog Influence
			if event.key == pygame.K_1:
				Constants.ENABLE_DOG = not Constants.ENABLE_DOG
				print("Toggle Dog Influence", Constants.ENABLE_DOG)

			# Toggle Alignment Influence
			if event.key == pygame.K_2: 
				Constants.ENABLE_ALIGNMENT = not Constants.ENABLE_ALIGNMENT
				print("Toggle Alignment Influence", Constants.ENABLE_ALIGNMENT)

			# Toggle Separation Influence
			if event.key == pygame.K_3: 
				Constants.ENABLE_SEPARATION = not Constants.ENABLE_SEPARATION
				print("Toggle Separation Influence", Constants.ENABLE_SEPARATION)

			# Toggle Cohesion Influence
			if event.key == pygame.K_4: 
				Constants.ENABLE_COHESION = not Constants.ENABLE_COHESION
				print("Toggle Cohesion Influence", Constants.ENABLE_COHESION)

			# Toggle Boundary Influence
			if event.key == pygame.K_5: 
				Constants.ENABLE_BOUNDARIES = not Constants.ENABLE_BOUNDARIES
				print("Toggle Boundary Influence", Constants.ENABLE_BOUNDARIES)

			# Toggle Dog Influence Lines
			if event.key == pygame.K_6: 
				Constants.DEBUG_DOG_INFLUENCE = not Constants.DEBUG_DOG_INFLUENCE
				print("Toggle Dog Influence Lines", Constants.DEBUG_DOG_INFLUENCE)
    
			# Toggle Velocity Lines
			if event.key == pygame.K_7: 
				Constants.DEBUG_VELOCITY = not Constants.DEBUG_VELOCITY
				print("Toggle Velocity Lines", Constants.DEBUG_VELOCITY)

			# Toggle Neighbor Lines
			if event.key == pygame.K_8: 
				Constants.DEBUG_NEIGHBORS = not Constants.DEBUG_NEIGHBORS
				print("Toggle Neighbor Lines", Constants.DEBUG_NEIGHBORS)

			# Toggle Boundary Force Lines
			if event.key == pygame.K_9: 
				Constants.DEBUG_BOUNDARIES = not Constants.DEBUG_BOUNDARIES
				print("Toggle Boundary Force Lines", Constants.DEBUG_BOUNDARIES)

			# Toggle Bounding Box Lines
			if event.key == pygame.K_0: 
				Constants.DEBUG_BOUNDING_RECTS = not Constants.DEBUG_BOUNDING_RECTS
				print("Toggle Bounding Box Lines", Constants.DEBUG_BOUNDING_RECTS)

#main gameplay loop
while True:
	
	#event handler
	handleDebugging()
				
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