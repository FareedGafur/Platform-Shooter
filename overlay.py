import pygame

class Overlay:

	def __init__(self, player):

		# Gets player data, specifically health
		self.player = player

		self.display_surface = pygame.display.get_surface()

		# Gets health image
		self.health_surf = pygame.image.load('../graphics/health.png').convert_alpha()

		

	def display(self):

		# For every hp the player has, blit that amount of health images
		for h in range(self.player.health):
			x = 10 + h * (self.health_surf.get_width() + 4)
			y = 10
			self.display_surface.blit(self.health_surf, (x, y))
