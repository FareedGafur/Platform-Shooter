import pygame, sys
from settings import *
from pygame.math import Vector2 as vector
from entities import Entity

class Player(Entity):


	def __init__(self, pos, groups, path, collision_sprites, shoot):

		super().__init__(pos, path, groups, shoot)

		# collision

		self.collision_sprites = collision_sprites

		# vertical movement

		self.gravity = 15
		self.jump_speed = 800 
		self.on_floor = False
		self.moving_floor = None

		# health

		self.health = 10


	def get_status(self):

		# idle status
		if self.direction.x == 0 and self.on_floor:

			self.status = self.status.split('_')[0] + '_idle'

		# jump status
		if self.direction.y != 0 and not self.on_floor:

			self.status = self.status.split('_')[0] + '_jump'

		# duck status
		if self.on_floor and self.duck:
			self.status = self.status.split('_')[0] + '_duck'


	def check_contact(self):

		# Creates a bottom rect that checks if player is on the floor
		bottom_rect = pygame.Rect(0,0,self.rect.width, 5)
		bottom_rect.midtop = self.rect.midbottom

		for sprite in self.collision_sprites.sprites(): #If player is on moving platform, but in contact with platform, set on_floor to true
			if sprite.rect.colliderect(bottom_rect):
				if self.direction.y > 0:
					self.on_floor = True

				if hasattr(sprite, 'direction'): ################
					self.moving_floor = sprite


	def input(self):

		keys = pygame.key.get_pressed()
		

		# Vertical Movement

		if keys[pygame.K_UP] and self.on_floor:
			
			self.direction.y = -self.jump_speed

		if keys[pygame.K_DOWN]:
			
			self.duck = True

		else:
			self.duck = False


		# Horizontal Movement

		if keys[pygame.K_RIGHT]:
			
			self.direction.x = 1
			self.status = 'right'

		elif keys[pygame.K_LEFT]:
			
			self.direction.x = -1
			self.status = 'left'

		else:
			self.direction.x = 0

		# if space is clicked and can_shoot is true, initiate attack

		if keys[pygame.K_SPACE] and self.can_shoot:

			# Gets direction for attack depending on where the player is facing
			direction = vector(1,0) if self.status.split('_')[0] == 'right' else vector(-1,0)

			# Gets position for where the bullet will spawn
			pos = self.rect.center + direction * 70

			# offset to make sure bullet aligns with player... also depends on if player is ducking
			y_offset = vector(0, -16) if not self.duck else vector(0,10)

			#Player shoots
			self.shoot(pos + y_offset, direction, self)

			self.can_shoot = False # Initiate cooldown
			self.shoot_time = pygame.time.get_ticks() # gets time player shoots


	def collision(self, direction):
		
		for sprite in self.collision_sprites.sprites():

			if sprite.rect.colliderect(self.rect):

				# left collision
				if direction == 'horizontal':
					
					if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
						self.rect.left = sprite.rect.right


				# right collision
					if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
						self.rect.right = sprite.rect.left

					self.pos.x = self.rect.x

				else:

				# top collision
					if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
						self.rect.top = sprite.rect.bottom


				# bottom collision
					if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
						self.rect.bottom = sprite.rect.top
						self.on_floor = True

					self.pos.y = self.rect.y
					self.direction.y = 0

		if self.on_floor and self.direction.y != 0:
			self.on_floor = False


	def move(self, dt):

		#Player can not move while ducking
		if self.duck and self.on_floor:
			self.direction.x = 0



		# Horizontal Movement + Collision
		self.pos.x += self.direction.x * self.speed * dt
		self.rect.x = round(self.pos.x)
		self.collision('horizontal')
		
		

		# Vertical Movement + Collision
		self.direction.y += self.gravity
		self.pos.y += self.direction.y * dt

		# glue the player to the platform

		if self.moving_floor and self.moving_floor.direction.y > 0 and self.direction.y > 0:

			self.direction.y = 0
			self.rect.bottom = self.moving_floor.rect.top
			self.pos.y = self.rect.y
			self.on_floor = True
			self.moving_floor = None


		self.rect.y = round(self.pos.y)
		self.collision('vertical') #Always check for contact with floor
		
		
	def check_death(self):
		if self.health <= 0: # if health is less than or equal to zero, kill player and close game
			self.kill()
			pygame.quit()
			sys.exit()

	def update(self, dt):
		self.old_rect = self.rect.copy()
		self.input()
		self.get_status()
		self.move(dt)
		self.check_contact()
		self.animate(dt)
		self.blink()

		# Timer
		self.shoot_timer()
		self.vulnerability_timer()

		#death
		self.check_death()

			

