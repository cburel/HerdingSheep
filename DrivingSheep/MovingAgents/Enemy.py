from ast import Constant
from dis import dis
import pygame
from pygame.locals import *
import random
import math
import Constants
from Agent import Agent

class Sheep(Agent):

	def __init__(self, image, pos, size, spd, color, turnSpd):
		super().__init__(image, pos, size, spd, color, turnSpd)
		self.isFleeing = False
		self.targetPos = None
		self.ticks = pygame.time.get_ticks()
	
	def switchMode(self):
		if self.isFleeing:
			self.isFleeing = False
		else:
			self.isFleeing = True

	def isPlayerClose(self, player):
		distance = self.pos - player.pos
		if distance.length() < Constants.FLEE_RANGE:
			self.isFleeing = True
			return True
		else:
			self.isFleeing = False
			return False

	def calcTrackingVelocity(self, player):
		self.targetPos = player.center

	def updateDirectionTime(self):
		ticks = pygame.time.get_ticks() - self.ticks
		if ticks > 1000:
			self.ticks = pygame.time.get_ticks()
			return True
		else:
			return False

	def update(self, bounds, screen, player):

		## initialize velocity
		#if pygame.Vector2.length(self.vel) == 0:
		#	angle = math.acos(random.randrange(-1, 1))
		#	self.vel = pygame.Vector2(math.cos(angle), math.sin(angle)) * self.spd
		
		#check if player is close
		self.isFleeing = self.isPlayerClose(player)

		# get forces on the sheep
		boundsForce = self.computeBoundaryForces(bounds, screen)
		if boundsForce != pygame.Vector2(0,0):
			pygame.Vector2.normalize(boundsForce)

		totalForce = boundsForce

		## wander if player isn't close
		#if not self.isFleeing:

		#	if self.updateDirectionTime() == True:
		#		theta = math.radians(random.randrange(-100, 100) / 100)

		#		pickTurn = random.randint(0, 100)
		#		if pickTurn < 50:
		#			theta += 0
		#		else:
		#			theta += 180

		#		#apply wander force			
		#		wanderDir = pygame.Vector2.normalize(self.vel) + pygame.Vector2(math.cos(theta), math.sin(theta))
		#		wanderDirForce = wanderDir * Constants.ENEMY_WANDER_FORCE
		#		wanderDirForceNorm = pygame.Vector2.normalize(wanderDirForce)

		#		totalForce = wanderDirForceNorm + (boundsForce * int(Constants.ENABLE_BOUNDARIES))
		#	else:
		#		totalForce = boundsForce * int(Constants.ENABLE_BOUNDARIES)

		# otherwise, flee
		if self.isFleeing:
			#apply flee force
			#store the calculated, normalized direction to the dog
			dirToDog = pygame.Vector2.normalize(player.pos - self.pos)

			#scale direction by the weight of this force to get applied force
			dirToDogForce = -dirToDog * Constants.ENEMY_FLEE_FORCE
						
			totalForce = (dirToDogForce * int(Constants.ENABLE_DOG) + (boundsForce * int(Constants.ENABLE_BOUNDARIES)))

			self.calcTrackingVelocity(player)
			self.vel += totalForce
		else:
			self.vel = pygame.Vector2(0,0)
					
		# prevent sheep from turning on a dime
		self.clampTurn(Constants.ENEMY_TURN_SPEED, totalForce)

		# update the agent
		super().update(bounds, screen)

	def draw(self, screen):
		if Constants.DEBUG_DOG_INFLUENCE:
			if self.isFleeing == True:
				pygame.draw.line(screen, (0, 0, 255), self.center, self.targetPos, 3)

		super().draw(screen)
