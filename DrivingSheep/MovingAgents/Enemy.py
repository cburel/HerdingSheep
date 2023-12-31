from ast import Constant
from asyncio import constants
from dis import dis
import pygame
from pygame.locals import *
import random
import math
import Constants
from Agent import Agent
from Vector import Vector

class Sheep(Agent):

	def __init__(self, image, pos, size, spd, color, turnSpd):
		super().__init__(image, pos, size, spd, color, turnSpd)
		self.isFleeing = False
		self.targetPos = None
		self.ticks = pygame.time.get_ticks()
		self.neighbors = []
		self.neighborCount = 0
	
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

	def calcNeighbors(self, herd, screen):
		self.neighborCount = 0
		self.neighbors = []

		for sheep in herd:
			if sheep is not self:
				if (self.center - sheep.pos).length() < Constants.SHEEP_NEIGHBOR_RADIUS:
					self.neighborCount += 1
					self.neighbors += [sheep]
		if Constants.DEBUG_NEIGHBORS:
			for sheep in self.neighbors:
				pygame.draw.line(screen, (0, 0, 255), (self.center.x, self.center.y), (sheep.center.x, sheep.center.y), 1)

	def computeAlignment(self):
		alignment = Vector(0,0)

		if Constants.ENABLE_ALIGNMENT:
			for sheep in self.neighbors:
				alignment += sheep.vel

			if (self.neighborCount == 0):
				return alignment
			else:
				return alignment.scale(1 / self.neighborCount)

		return alignment
		

	def computeCohesion(self):
		cohesion = Vector(0,0)

		if Constants.ENABLE_COHESION:
			for sheep in self.neighbors:
				cohesion += sheep.pos

			if self.neighborCount > 0:
				Vector.scale(cohesion, 1 / self.neighborCount)
				cohesion -= self.center

		return cohesion
			

	def computeSeparation(self):
		separation = Vector(0,0)

		if Constants.ENABLE_SEPARATION:
			for sheep in self.neighbors:
				separation += self.center - sheep.pos

			if (self.neighborCount == 0):
				return separation
			else:
				Vector.scale(separation, 1 / self.neighborCount)
			return separation

		return separation

	def update(self, bounds, screen, player, herd):

		# initialize velocity
		if self.vel.length() == 0:
			angle = math.acos(random.randrange(-1, 1))
			self.vel = Vector(math.cos(angle), math.sin(angle)) * self.spd

		self.calcNeighbors(herd, screen)

		alignment = self.computeAlignment().normalize()
		cohesion = self.computeCohesion().normalize()
		separation = self.computeSeparation().normalize()
		
		#check if player is close
		self.isFleeing = self.isPlayerClose(player)

		# get forces on the sheep
		boundsForce = self.computeBoundaryForces(bounds, screen)
		if boundsForce != Vector(0,0):
			boundsForce.normalize()

		if self.isFleeing:
			#apply flee force
			#store the calculated, normalized direction to the dog
			dirToDog = (player.pos - self.pos).normalize()

			#scale direction by the weight of this force to get applied force
			dirToDogForce = dirToDog * Constants.ENEMY_FLEE_FORCE * -1

			self.calcTrackingVelocity(player)
		else:
			dirToDogForce = Vector(0,0)
					
		
		totalForce = alignment * Constants.ALIGNMENT_WEIGHT * Constants.ENABLE_ALIGNMENT + separation * Constants.SEPARATION_WEIGHT * Constants.ENABLE_SEPARATION + cohesion * Constants.COHESION_WEIGHT * Constants.ENABLE_COHESION + dirToDogForce * Constants.PLAYER_TO_SHEEP_FORCE * Constants.ENABLE_DOG + boundsForce * Constants.BOUNDARY_FORCE * Constants.ENABLE_BOUNDARIES

		# prevent sheep from turning on a dime
		self.clampTurn(Constants.ENEMY_TURN_SPEED, totalForce)
		
		self.vel += totalForce.normalize()


		# update the agent
		super().update(bounds, screen)

	def draw(self, screen):
		if Constants.DEBUG_DOG_INFLUENCE:
			if self.isFleeing == True:
				pygame.draw.line(screen, (0, 0, 255), (self.center.x, self.center.y), (self.targetPos.x, self.targetPos.y), 3)

		super().draw(screen)
