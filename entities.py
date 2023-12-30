import pygame
from pygame.math import Vector2 as vector
from settings import *
from os import walk
from math import sin



class Entity(pygame.sprite.Sprite):
	

	def __init__(self, pos, path, groups, shoot):

		super().__init__(groups)

		# graphics setup
		self.import_assets(path)
		self.frame_index = 0
		self.status = 'right'

		# Image setup
		self.image = self.animations[self.status][self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)
		self.old_rect = self.rect.copy()
		self.z = LAYERS['Level']
		self.mask = pygame.mask.from_surface(self.image)

		# float based movement

		self.direction = vector()
		self.pos = vector(self.rect.topleft)
		self.speed = 400


		# Shooting setup
		self.shoot = shoot
		self.can_shoot = True
		self.shoot_time = None
		self.cooldown = 200
		self.duck = False

		# health

		self.health = 3
		self.is_vulnerable = True
		self.hit_time = None

	def damage(self):

		if self.is_vulnerable: # If damaged, lose one hp, become invulnerable, get the time the entity was damaged
			self.health -= 1
			self.is_vulnerable = False
			self.hit_time = pygame.time.get_ticks()

	def check_death(self): 

		if self.health <= 0: # Kills entity if health is <= 0
			self.kill()

	def animate(self, dt):

		self.frame_index += 7 * dt

		if self.frame_index >= len(self.animations[self.status]): # Ensures the frame index doesnt exceed the amount of frames 
			self.frame_index = 0

		self.image = self.animations[self.status][int(self.frame_index)] #Update image and mask
		self.mask = pygame.mask.from_surface(self.image)

	def shoot_timer(self):
		if not self.can_shoot: # timer which checks when the entity is allowed to shoot again after shooting
			current_time = pygame.time.get_ticks()
			if current_time - self.shoot_time > self.cooldown:
				self.can_shoot = True

	def vulnerability_timer(self):

		if not self.is_vulnerable: # If invulnerable, constantly check for the elapsed time, and make entity vulnerable once it exceeds 500 ms
			current_time = pygame.time.get_ticks()
			if current_time - self.hit_time > 500:
				self.is_vulnerable = True

	def blink(self):
		
		if not self.is_vulnerable: # When damaged, entity will blink white to show it is invulnerable
			if self.wave_value(): # Using the sine function, entity will blink when sine value is greater than 0 (positive)
				mask = pygame.mask.from_surface(self.image) # Creates a mask over the entity
				white_surf = mask.to_surface()
				white_surf.set_colorkey((0,0,0)) # Mask is set to white to make it look like it is blinking
				self.image = white_surf

	def wave_value(self):

		value = sin(pygame.time.get_ticks())  # Used in the blink method, and causes the entity to blink when sine is positive

		if value >= 0: 

			return True
		else:
			return False

	def import_assets(self, path):

		self.animations = {}

		for index,folder in enumerate(walk(path)):  # Imports assets needed for the entities

			if index == 0:
				for name in folder[1]:
					self.animations[name] = []

			else:
				for file_name in sorted(folder[2], key = lambda string: int(string.split('.')[0])):
					path = folder[0].replace('\\', '/') + '/' + file_name
					surf = pygame.image.load(path).convert_alpha()
					key = folder[0].split('\\')[1]
					self.animations[key].append(surf)
