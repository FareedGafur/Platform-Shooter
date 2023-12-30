import pygame
from settings import *
from pygame.math import Vector2 as vector
from entities import Entity


class Enemy(Entity): # Inherits attributes from entitiy class
	def __init__(self, pos, path, groups, shoot, player, collision_sprites):

		super().__init__(pos, path, groups, shoot)
		self.player = player

		for sprite in collision_sprites.sprites(): # Ensures enemies stay on top of platforms by checking for collisions from the midbottom of the enemies
			if sprite.rect.collidepoint(self.rect.midbottom):
				self.rect.bottom = sprite.rect.top

		self.cooldown = 1200


	def get_status(self):

		if self.player.rect.centerx < self.rect.centerx: #Checks for where to player is, then makes enemies face towards player

			self.status = 'left'

		else:
			self.status = 'right'


	def check_fire(self):
		# Gets enemy and player positions
		enemy_pos = vector(self.rect.center)
		player_pos = vector(self.player.rect.center)

		# Gets distance from player
		distance = (player_pos - enemy_pos).magnitude()

		# Checks to see if player is within line of fire for enemies 
		same_y = True if self.rect.top - 20 < player_pos.y < self.rect.bottom + 20 else False

		if distance < 600 and same_y and self.can_shoot: #If conditions met, enemy will shoot at player
			bullet_direction = vector(1,0) if self.status == 'right' else vector(-1, 0) # Direction shot depends on enemy status
			y_offset = vector(0, -16) # y offset to make bullets appear in line with enemy gun
			pos = self.rect.center + bullet_direction * 80
			self.shoot(pos + y_offset, bullet_direction, self) # Shoots at player

			self.can_shoot = False #Shoot cooldown
			self.shoot_time = pygame.time.get_ticks() # Gets time the enemy shot



	def update(self, dt):
		self.get_status()
		self.animate(dt)
		self.blink()

		self.shoot_timer()
		self.vulnerability_timer()
		self.check_fire()

		#death
		self.check_death()
		
			