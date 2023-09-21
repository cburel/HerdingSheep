from asyncio.windows_events import NULL
from typing import List
import pygame
from pygame.locals import *
from Agent import Agent
import Constants
import math
import random


class Dog(Agent):

	def __init__(self, image, pos, size, spd, color, turnSpd):
		super().__init__(image, pos, size, spd, color, turnSpd)
		self.targetAgent = NULL
		self.hasTagged = False

	def swapTarget(self, enemies):
		if self.hasTagged == True:
			self.hasTagged = False
		else:
			self.hasTagged = True

			#select new sheep to move towards
			self.targetAgent = max([e for e in enemies], key=lambda e: self.pos.distance_to(pygame.math.Vector2(e.pos.x, e.pos.y)))

	def draw(self, screen):
		pygame.draw.line(screen, (255, 0, 0), self.center, self.targetAgent.center, 3)
		super().draw(screen)

	def update(self, bounds, screen, enemies: List):

		#get boundary forces
		boundsForce = self.computeBoundaryForces(bounds, screen)

		if pygame.Vector2.length(self.vel) == 0:
			angle = math.acos(random.randrange(-1, 1))
			self.vel = pygame.Vector2(math.cos(angle), math.sin(angle)) * self.spd

		# gets appropriate enemy and moves player towards it
		# shoutout to Rabbid76 on SO for the lambda fn
		if self.hasTagged == False:
			self.targetAgent = min([e for e in enemies], key=lambda e: self.pos.distance_to(pygame.math.Vector2(e.pos.x, e.pos.y)))

		#store the calculated, normalized direction to the sheep being tracked
		dirToSheep = pygame.Vector2.normalize(self.targetAgent.pos - self.pos)

		#scale direction by the weight of this force to get applied force and store it
		dirToSheepForce = dirToSheep * Constants.PLAYER_TO_SHEEP_FORCE

		#take applied force, normalize it, scale it by deltatime and speed to modify dog's velocity
		dirToSheepForceNorm = pygame.Vector2.normalize(dirToSheepForce)
		
		totalForce = dirToSheepForceNorm + boundsForce
		self.clampTurn(Constants.PLAYER_TURN_SPEED, totalForce)

		super().updateVelocity(self.vel)
		super().update(bounds, screen)

		return self.targetAgent