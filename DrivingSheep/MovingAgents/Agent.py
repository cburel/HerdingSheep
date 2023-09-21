import pygame
from pygame.locals import *
import Constants
import math
import random

class Agent():
	def __init__(self, image, pos, size, spd, color, turnSpd):
		self.image = image
		self.pos = pos
		self.size = pygame.Vector2(size, size)
		self.spd = spd
		self.color = color
		self.angle = 0
		self.vel = pygame.Vector2(0,0)
		self.target = 0
		self.center = self.updateCenter()
		self.rect = self.updateRect()
		self.surf = self.updateSurf()
		self.upperLeft = self.updateUpperLeft()
		self.boundingRect = self.updateBoundingRect()

	#pretty print agent information
	def __str__(self):
		return ("Size: " +  str(self.size) + ", " + "Pos: " + str(self.pos) + ", " + "Vel: " + str(self.vel) + ", " + "Center: " + str(self.center))

	def updateVelocity(self, velocity):
		self.vel = pygame.Vector2.normalize(velocity)

	# calculate the center of the agent's rect
	def updateCenter(self):
		return pygame.Vector2(self.pos.x + self.size.x / 2, self.pos.y + self.size.y / 2)

	# calculate the collision rect
	def updateRect(self):
		return pygame.Rect(self.pos, self.size)

	def updateSurf(self):
		return pygame.transform.rotate(self.image, self.angle)

	def updateUpperLeft(self):
		return self.center - pygame.Vector2(self.surf.get_width() * 0.5, self.surf.get_height() * 0.5)

	def updateBoundingRect(self):
		return self.surf.get_bounding_rect().move(self.upperLeft.x, self.upperLeft.y)

	# check for collision with another agent
	def isInCollision(self, agent):
		if agent != None:
			if self.boundingRect.colliderect(agent.boundingRect):
				return True
			else:
				return False

	def clampTurn(self, turnSpd, totalForce):
		target = totalForce
		
		#get difference between normalized target direction and normalized current direction
		curr = self.vel

		if pygame.Vector2.length(target) == 0:
			return
		else:
			difference = pygame.Vector2.normalize(target) - pygame.Vector2.normalize(curr)

			# if the length of the difference vector is smaller than the turning speed, the agent can turn as fast
			length = pygame.Vector2.length(difference)
			if length < turnSpd:
				self.vel = target
			else:
				difference = pygame.Vector2.normalize(difference)
				pygame.Vector2.scale_to_length(difference, turnSpd)
				self.vel += difference
			self.vel = pygame.Vector2.normalize(self.vel) * self.spd

	# draw the agent
	def draw(self, screen):
		
		#draw the rectangle
		pygame.draw.rect(screen, self.color, self.rect)

		#calculate surface to draw
		self.surf = pygame.transform.rotate(self.image, self.angle)
		upperLeft = self.center - pygame.Vector2(self.surf.get_width() * 0.5, self.surf.get_height() * 0.5)
				
		#draw black debug collision rect border
		pygame.draw.rect(screen, (0,0,0), self.rect, 1)

		# draw debug line
		lineStart = self.updateCenter()
		scaledVel = pygame.Vector2(self.vel.x, self.vel.y)
		
		if self.vel == (0,0):
			scaledVel = self.vel
		else:
			pygame.Vector2.scale_to_length(scaledVel, Constants.VECTOR_LINE_LENGTH)
		
		lineEnd = pygame.Vector2(self.updateCenter().x + scaledVel.x, self.updateCenter().y + scaledVel.y)

		#draw velocity lines
		if Constants.DEBUG_VELOCITY:
			pygame.draw.line(screen, (0, 0, 255), lineStart, lineEnd, 3)
		
		#blit the dog/sheep image
		screen.blit(self.surf, [upperLeft.x, upperLeft.y])

		#change image angle
		self.angle = math.degrees(math.atan2(-self.vel.y, self.vel.x)) - 90

		# update and draw bounding rect
		self.surf = self.updateSurf()
		self.upperLeft = self.updateUpperLeft()
		self.boundingRect = self.updateBoundingRect()
		if Constants.DEBUG_BOUNDING_RECTS:
			pygame.draw.rect(screen, (0,0,0), self.boundingRect, 1)

	def computeBoundaryForces(self, bounds, screen):	
		boundsNearbyList = []
		boundsForce = pygame.Vector2(0,0)
		boundsSum = pygame.Vector2(0,0)

		#for each boundary agent is near, add boundary's normal force to list, compute force pushing away from boundary. add this force to a sum.
		if self.center.x < Constants.BORDER_RADIUS:
			boundsNearby = pygame.Vector2(0, self.center.y)
			boundsForce = pygame.Vector2(Constants.BORDER_RADIUS, 0) - (self.center - boundsNearby)
			boundsSum += boundsForce
			boundsNearbyList.append(boundsNearby)
		elif self.center.x > bounds.x - Constants.BORDER_RADIUS:
			boundsNearby = pygame.Vector2(bounds.x, self.center.y)
			boundsForce = (pygame.Vector2(Constants.BORDER_RADIUS, 0) + (self.center - boundsNearby)) * -1
			boundsSum += boundsForce
			boundsNearbyList.append(boundsNearby)

		if self.center.y < Constants.BORDER_RADIUS:
			boundsNearby = pygame.Vector2(self.center.x, 0)
			boundsForce = pygame.Vector2(0, Constants.BORDER_RADIUS) - (self.center - boundsNearby)
			boundsSum += boundsForce
			boundsNearbyList.append(boundsNearby)
		elif self.center.y > bounds.y - Constants.BORDER_RADIUS:
			boundsNearby = pygame.Vector2(self.center.x, bounds.y)
			boundsForce = (pygame.Vector2(0, Constants.BORDER_RADIUS) + (self.center - boundsNearby)) * -1
			boundsSum += boundsForce
			boundsNearbyList.append(boundsNearby)

		#draw a force line between boundary and agent
		if len(boundsNearbyList) > 0:
			for bound in boundsNearbyList:
				if Constants.DEBUG_BOUNDARIES:
					pygame.draw.line(screen, (255, 0, 0), self.center, bound, 1)

		return boundsSum
		
	#update the agent
	def update(self, bounds, screen):

		#move the agent
		self.pos += pygame.Vector2.normalize(self.vel) * self.spd

		# update agent's position
		self.boundingRect = self.updateBoundingRect()
		self.rect = self.updateRect()
		self.center = self.updateCenter()


			